"""Verbatim page OCR for pages without a usable text layer (and standalone images)."""

from __future__ import annotations

import re
from dataclasses import dataclass

from app.services.document_processing.markdown_utils import strip_outer_fence
from app.services.document_processing.providers.chain import ProviderChain

OCR_PROMPT = """Transcribe this document page VERBATIM into clean Markdown in reading order.
- Headings -> #/##, lists -> -, tables and matrices -> Markdown tables, formulas -> LaTeX ($...$), code -> fenced code blocks.
- Keep the original language and wording. Do NOT answer, solve, summarize, translate or add anything not printed on the page.
- For a drawn diagram/chart/photo, transcribe any readable text/values in it, then add one line: [Figure: <2-4 sentence description of what it shows and which concept it illustrates; only what is visible>].
- Skip logos, page numbers and repeated university banners.
Output only the Markdown."""  # noqa: E501

_FIGURE_LINE_RE = re.compile(r"^\[Figure:", re.MULTILINE)


@dataclass(frozen=True)
class OcrResult:
    markdown: str
    has_figures: bool
    failed: bool


class PageOcr:
    def __init__(self, chain: ProviderChain) -> None:
        self._chain = chain

    def transcribe(self, image_bytes: bytes) -> OcrResult:
        raw = self._chain.vision(OCR_PROMPT, image_bytes, max_output_tokens=8192, operation="ocr")
        if raw.startswith("[VISION_PLACEHOLDER]"):
            return OcrResult(markdown="[VISION_PLACEHOLDER] OCR disabled.", has_figures=False, failed=False)
        if raw.startswith("[VISION_ERROR]") or not raw.strip():
            return OcrResult(markdown="", has_figures=False, failed=True)
        markdown = strip_outer_fence(raw).strip()
        return OcrResult(markdown=markdown, has_figures=bool(_FIGURE_LINE_RE.search(markdown)), failed=False)


def insert_page_image(markdown: str, asset_ref: str, page: int) -> str:
    """Put ``![Page N](ref)`` directly above the first ``[Figure: …]`` line."""
    match = _FIGURE_LINE_RE.search(markdown)
    image_line = f"![Page {page}]({asset_ref})\n"
    if match is None:
        return f"{markdown}\n\n{image_line.strip()}"
    return markdown[: match.start()] + image_line + markdown[match.start():]
