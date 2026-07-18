"""Visual classification of embedded images via the VLM.

Ports experiment ``classify_visual`` / ``_make_classification`` / ``get_specialized_prompt`` /
``_image_position_hint`` and the ``VISUAL_CATEGORIES`` / ``_LEARNING_VALUE_BY_LABEL`` tables
(lines ~663-793).
"""

from __future__ import annotations

import json
import re

from app.services.document_processing.config import DocumentProcessingConfig
from app.services.document_processing.models import VisualClassification
from app.services.document_processing.providers.chain import ProviderChain

VISUAL_CATEGORIES = [
    "table_or_matrix",
    "graph_diagram",
    "chart_plot",
    "formula",
    "general_visual",
    "decorative",
]

_LEARNING_VALUE_BY_LABEL = {
    "table_or_matrix": "high",
    "graph_diagram": "high",
    "chart_plot": "high",
    "formula": "high",
    "general_visual": "medium",
    "decorative": "none",
}


class VisualClassifier:
    def __init__(self, config: DocumentProcessingConfig, *, provider_chain: ProviderChain) -> None:
        self._config = config
        self._chain = provider_chain

    def make_classification(
        self,
        label: str,
        learning_value: str,
        confidence: float,
        reason: str,
        position_hint: str = "inline",
    ) -> VisualClassification:
        """Build classification dict + derive action. Mirrors ``_make_classification``.

        Action rules:
        - decorative + (header/footer position OR confidence >= 0.75) -> skip
        - decorative + inline + confidence < 0.75 -> minimal_tag
          (uncertain decorative inline might be a meaningful figure; tag rather than drop)
        - all other labels -> extract
        """
        if label == "decorative":
            if confidence >= 0.75 or position_hint in ("header", "footer"):
                action = "skip"
            else:
                action = "minimal_tag"
        else:
            action = "extract"

        return {
            "label": label,
            "learning_value": learning_value,
            "action": action,
            "confidence": round(float(confidence), 3),
            "reason": reason,
        }

    def classify(
        self,
        image_bytes: bytes,
        surrounding_text: str = "",
        position_hint: str = "inline",
    ) -> VisualClassification:
        """Mirrors experiment ``classify_visual``."""
        if not self._config.enable_real_vision:
            return self.make_classification(
                "general_visual", "medium", 0.5, "vision_disabled", position_hint
            )

        context_snippet = (surrounding_text or "").strip()[:1500]
        prompt = (
            "Classify this image and return a JSON object with exactly these four fields:\n"
            '  "label": one of [table_or_matrix, graph_diagram, chart_plot, formula, general_visual, decorative]\n'  # noqa: E501
            '  "learning_value": one of [none, low, medium, high]\n'
            '  "confidence": float 0.0-1.0\n'
            '  "reason": one short sentence\n\n'
            "Category guide:\n"
            "- table_or_matrix: data grids, matrices, structured tables\n"
            "- graph_diagram: nodes/edges, flowcharts, system architecture, conceptual diagrams (high learning value)\n"
            "- chart_plot: data charts — bar/line/scatter/pie plots with axes and data series (high learning value)\n"  # noqa: E501
            "- formula: equations, symbolic math, LaTeX-style notation\n"
            "- general_visual: figures with academic content — illustrations, screenshots that teach something\n"
            "- decorative: logos, course/school branding, page borders, repeated banners, dividers,\n"
            "  background flourishes, page-number ornaments, watermarks. NO learning value.\n\n"
            f"Position on page: {position_hint}\n"
            f"Surrounding text:\n---\n{context_snippet}\n---\n\n"
            'Return ONLY valid JSON, e.g. {"label":"decorative","learning_value":"none","confidence":0.9,"reason":"logo with no academic content"}'  # noqa: E501
        )
        raw = self._chain.vision(prompt, image_bytes).strip()

        # Try JSON parse first.
        try:
            match = re.search(r"\{[^{}]+\}", raw, re.DOTALL)
            if match:
                parsed = json.loads(match.group(0))
                label = parsed.get("label", "general_visual")
                if label not in VISUAL_CATEGORIES:
                    label = "general_visual"
                learning_value = parsed.get(
                    "learning_value", _LEARNING_VALUE_BY_LABEL.get(label, "medium")
                )
                confidence = float(parsed.get("confidence", 0.5))
                reason = str(parsed.get("reason", "vlm_classified"))
                return self.make_classification(
                    label, learning_value, confidence, reason, position_hint
                )
        except Exception:
            pass

        # Fallback: scan raw text for a category name.
        lower = raw.lower()
        for cat in VISUAL_CATEGORIES:
            if cat in lower:
                lv = _LEARNING_VALUE_BY_LABEL.get(cat, "medium")
                return self.make_classification(cat, lv, 0.5, "fallback_text_parse", position_hint)

        return self.make_classification(
            "general_visual", "medium", 0.5, "fallback_default", position_hint
        )

    @staticmethod
    def position_hint(rect_y0: float | None, rect_y1: float | None, page_height: float | None) -> str:
        """Mirrors experiment ``_image_position_hint``."""
        if rect_y0 is None or rect_y1 is None or not page_height:
            return "inline"
        top_band = page_height * 0.15
        bottom_band = page_height * 0.85
        if rect_y1 <= top_band:
            return "header"
        if rect_y0 >= bottom_band:
            return "footer"
        return "inline"

    @staticmethod
    def specialized_prompt(category: str, context: str = "") -> str:
        """Mirrors experiment ``get_specialized_prompt``.

        ``context`` is surrounding document text; when given it is appended so the
        VLM interprets the figure in the context of the lesson instead of captioning it.
        """
        if category == "table_or_matrix":
            prompt = "Extract the table as a Markdown table, preserving row labels, column labels, and exact numeric values. Keep the original language of the content; do not translate. Output the Markdown table, and ABOVE it a REQUIRED one-line summary in the document's language that identifies it as a table and states in one sentence what it shows, formatted exactly as: [Table: ...]."  # noqa: E501
        elif category == "graph_diagram":
            prompt = "Extract node labels, edges and directionality. Represent the diagram as a text-based ASCII diagram (using boxes [+---+] and arrows [-->] inside a preformatted ``` block), with a REQUIRED [Diagram: ...] line underneath that first names the diagram type (flowchart, tree, state machine, network, block diagram, ...) and then explains in 1-2 sentences the concept/process it illustrates and why it matters — not a restatement of which boxes connect to which. Write the summary in the document's language; keep the original language of the labels; do not translate."  # noqa: E501
        elif category == "chart_plot":
            prompt = (
                "This is a data chart. Extract its content so a reader who cannot see it loses nothing:\n"  # noqa: E501
                "1. Begin your output with a REQUIRED one-line summary in the document's language, formatted exactly as: [Chart: <chart type: bar/line/scatter/pie/...> — <one sentence on what it shows>].\n"  # noqa: E501
                "2. Chart title, axis labels and units (or slice labels for pie charts).\n"
                "3. Every data series: its name/legend entry and approximate values at notable points (peaks, crossings, endpoints). If values are readable, tabulate them as a Markdown table.\n"  # noqa: E501
                "4. The main trend or comparison the chart shows, in one or two sentences.\n"
                "Keep the original language of all labels; do not translate."
            )
        elif category == "formula":
            prompt = "Extract surrounding explanatory text separately from formula text. Return formulas in LaTeX. Keep the original language of the explanatory text; do not translate."  # noqa: E501
        elif category == "decorative":
            prompt = "This is a decorative image. Describe it minimally."
        else:
            prompt = (
                "Extract the full content of this visual element for a study document. Do NOT give a one-line caption; produce a structured extraction:\n"  # noqa: E501
                "1. Transcribe ALL text visible in the image verbatim (labels, annotations, callouts, captions), keeping the original language; do not translate.\n"  # noqa: E501
                "2. Describe the layout and the relationships between components — what points to what, what contains what, what is compared with what.\n"  # noqa: E501
                "3. If it is a diagram, flowchart, or memory layout, draw/represent it visually using a Markdown table or a text-based ASCII diagram (using boxes [+---+] and arrows [-->] inside a preformatted ``` block).\n"  # noqa: E501
                "4. State in one or two sentences what concept the figure illustrates or teaches.\n"  # noqa: E501
                "Focus only on content with learning value; avoid filler commentary about style."
            )

        context_snippet = (context or "").strip()[:1500]
        if context_snippet:
            prompt += (
                "\n\nSurrounding text from the document (use it to interpret the figure and its terminology; describe the figure itself, do not repeat this text):\n"  # noqa: E501
                f"---\n{context_snippet}\n---"
            )
        return prompt
