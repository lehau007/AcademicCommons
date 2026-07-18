from __future__ import annotations

from app.services.document_processing.classification import (
    VISUAL_CATEGORIES,
    VisualClassifier,
)
from app.services.document_processing.config import DocumentProcessingConfig
from app.services.document_processing.providers.base import (
    ProviderResponse,
    VisionLanguageProvider,
)

from .conftest import make_chain


class _StubProvider(VisionLanguageProvider):
    provider_name = "stub"

    def __init__(self, text: str) -> None:
        self._text = text
        self.prompts: list[str] = []

    def complete(
        self,
        prompt: str,
        *,
        images: list[bytes] | None = None,
        operation: str = "text",
    ) -> ProviderResponse:
        self.prompts.append(prompt)
        return ProviderResponse(
            text=self._text, provider="stub", model="stub", status="success", latency_ms=0
        )


def _classifier() -> VisualClassifier:
    config = DocumentProcessingConfig(enable_real_vision=False)
    return VisualClassifier(config, provider_chain=make_chain())


def test_classify_vision_disabled_returns_placeholder_classification() -> None:
    result = _classifier().classify(b"x")
    assert set(result) >= {"label", "action", "confidence", "reason"}
    assert result["reason"] == "vision_disabled"
    assert result["label"] == "general_visual"


def test_make_classification_decorative_high_confidence_skips() -> None:
    result = _classifier().make_classification("decorative", "none", 0.9, "logo")
    assert result["action"] == "skip"


def test_make_classification_decorative_inline_low_confidence_minimal_tag() -> None:
    result = _classifier().make_classification(
        "decorative", "none", 0.5, "uncertain", position_hint="inline"
    )
    assert result["action"] == "minimal_tag"


def test_make_classification_decorative_header_skips_even_low_confidence() -> None:
    result = _classifier().make_classification(
        "decorative", "none", 0.5, "banner", position_hint="header"
    )
    assert result["action"] == "skip"


def test_make_classification_non_decorative_extracts() -> None:
    result = _classifier().make_classification("table_or_matrix", "high", 0.4, "table")
    assert result["action"] == "extract"


def test_position_hint_bands() -> None:
    page_height = 100.0
    # y1 within top 15% -> header
    assert VisualClassifier.position_hint(0.0, 10.0, page_height) == "header"
    # y0 within bottom 15% -> footer
    assert VisualClassifier.position_hint(90.0, 100.0, page_height) == "footer"
    # middle -> inline
    assert VisualClassifier.position_hint(40.0, 60.0, page_height) == "inline"
    # missing data -> inline
    assert VisualClassifier.position_hint(None, None, page_height) == "inline"
    assert VisualClassifier.position_hint(40.0, 60.0, None) == "inline"


def test_specialized_prompt_formula_non_empty() -> None:
    prompt = VisualClassifier.specialized_prompt("formula")
    assert isinstance(prompt, str)
    assert prompt.strip()


def test_visual_categories_include_chart_plot() -> None:
    assert "chart_plot" in VISUAL_CATEGORIES


def test_classify_accepts_chart_plot_label() -> None:
    stub = _StubProvider(
        '{"label":"chart_plot","learning_value":"high","confidence":0.9,"reason":"bar chart"}'
    )
    config = DocumentProcessingConfig(enable_real_vision=True)
    classifier = VisualClassifier(
        config, provider_chain=make_chain([stub], enable_real_vision=True)
    )
    result = classifier.classify(b"img")
    assert result["label"] == "chart_plot"
    assert result["action"] == "extract"


def test_classification_prompt_lists_chart_plot() -> None:
    stub = _StubProvider(
        '{"label":"general_visual","learning_value":"medium","confidence":0.5,"reason":"x"}'
    )
    config = DocumentProcessingConfig(enable_real_vision=True)
    classifier = VisualClassifier(
        config, provider_chain=make_chain([stub], enable_real_vision=True)
    )
    classifier.classify(b"img")
    assert len(stub.prompts) == 1
    assert "chart_plot" in stub.prompts[0]


def test_specialized_prompt_chart_plot_mentions_axes_and_series() -> None:
    prompt = VisualClassifier.specialized_prompt("chart_plot").lower()
    assert "axis" in prompt or "axes" in prompt
    assert "series" in prompt


def test_specialized_prompt_general_visual_requires_structured_extraction() -> None:
    prompt = VisualClassifier.specialized_prompt("general_visual").lower()
    # Must ask for verbatim text transcription, component relationships,
    # and the concept the figure illustrates — not just a caption.
    assert "verbatim" in prompt
    assert "relationship" in prompt
    assert "concept" in prompt


def test_specialized_prompt_includes_surrounding_context_when_given() -> None:
    prompt = VisualClassifier.specialized_prompt(
        "general_visual", context="Con trỏ trong C và cấp phát bộ nhớ động"
    )
    assert "Con trỏ trong C và cấp phát bộ nhớ động" in prompt


def test_specialized_prompt_without_context_unchanged() -> None:
    prompt = VisualClassifier.specialized_prompt("general_visual", context="")
    assert "Surrounding text" not in prompt
