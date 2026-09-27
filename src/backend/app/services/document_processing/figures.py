"""Figure description: one VLM JSON call per figure crop, rendered as image line + description."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any

from app.services.document_processing.providers.chain import ProviderChain

FIGURE_LABELS = ("diagram", "chart", "table", "formula", "photo", "screenshot", "decorative", "other")

FIGURE_SCHEMA: dict[str, Any] = {
    "type": "OBJECT",
    "properties": {
        "label": {"type": "STRING", "enum": list(FIGURE_LABELS)},
        "caption": {"type": "STRING"},
        "description": {"type": "STRING"},
        "content_markdown": {"type": "STRING"},
    },
    "required": ["label", "caption", "description", "content_markdown"],
}

FIGURE_PROMPT = """You are indexing a figure cropped from a lecture document so students can search it.
Text found inside the figure region (may be garbled or empty): <<<{figure_text}>>>
Nearby page text: <<<{page_text}>>>
Return JSON:
- label: "decorative" for logos, branding, ornaments or icons with no learning value.
- caption: short title (at most 12 words) in the same language as the document.
- description: 2-4 sentences explaining what the figure shows and which concept it illustrates. Describe only what is visible; never invent values.
- content_markdown: if the figure is a table or matrix, the exact Markdown table; if it is a formula, LaTeX inside $$...$$; otherwise an empty string.
Do not answer or solve any question shown in the figure."""  # noqa: E501


@dataclass(frozen=True)
class FigureDescription:
    label: str
    caption: str
    description: str
    content_markdown: str
    failed: bool = False

    @property
    def is_decorative(self) -> bool:
        return self.label == "decorative"

    @classmethod
    def empty(cls) -> FigureDescription:
        return cls("other", "", "", "")


def _one_line(value: str) -> str:
    return " ".join(value.split())


def parse_figure_json(raw: str) -> FigureDescription:
    """Parse the VLM reply; degrade to a description-only result instead of raising."""
    text = raw.strip()
    if not text or text.startswith("[VISION_ERROR]"):
        return FigureDescription("other", "", "", "", failed=True)
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group(0))
        except json.JSONDecodeError:
            data = None
        if isinstance(data, dict):
            label = str(data.get("label", "other")).strip().lower()
            return FigureDescription(
                label=label if label in FIGURE_LABELS else "other",
                caption=_one_line(str(data.get("caption", ""))),
                description=_one_line(str(data.get("description", ""))),
                content_markdown=str(data.get("content_markdown") or "").strip(),
            )
    label_match = re.search(r'"label"\s*:\s*"(\w+)"', text)
    label = label_match.group(1).lower() if label_match else "other"
    return FigureDescription(label if label in FIGURE_LABELS else "other", "", "", "")


def render_figure_block(
    asset_ref: str,
    desc: FigureDescription,
    *,
    fallback_caption: str,
    fallback_text: str = "",
) -> str:
    caption = (desc.caption or fallback_caption).replace("[", "(").replace("]", ")")
    lines = [f"![{caption}]({asset_ref})"]
    if desc.description:
        lines.append(f"[Figure: {desc.description}]")
    block = "\n".join(lines)
    body = desc.content_markdown or ("" if desc.description else fallback_text.strip())
    return f"{block}\n\n{body}" if body else block


class FigureDescriber:
    def __init__(self, chain: ProviderChain) -> None:
        self._chain = chain

    def describe(self, image_png: bytes, *, figure_text: str, page_text: str) -> FigureDescription:
        if not self._chain.enabled:
            return FigureDescription.empty()
        prompt = FIGURE_PROMPT.format(figure_text=figure_text[:1500], page_text=page_text[:1500])
        raw = self._chain.vision(
            prompt, image_png, response_schema=FIGURE_SCHEMA, max_output_tokens=2048, operation="figure"
        )
        return parse_figure_json(raw)
