from __future__ import annotations

from app.services.document_processing.config import DocumentProcessingConfig
from app.services.document_processing.metrics import LlmCallRecorder
from app.services.document_processing.progress import ProgressEmitter
from app.services.document_processing.providers.factory import build_vision_providers


def _names(providers: list) -> list[tuple[str, str | None]]:  # type: ignore[type-arg]
    return [(p.provider_name, getattr(p, "model", None)) for p in providers]


def test_vertex_expands_to_lite_then_flash_for_ocr() -> None:
    config = DocumentProcessingConfig(provider_order=("vertex", "gemini"), gemini_api_key="k")

    providers = build_vision_providers(config, recorder=LlmCallRecorder(), emitter=ProgressEmitter())

    assert _names(providers)[:2] == [("vertex", "gemini-3.5-flash-lite"), ("vertex", "gemini-3.8-flash")]
    assert providers[2].provider_name == "gemini"


def test_viewer_purpose_puts_flash_first() -> None:
    config = DocumentProcessingConfig(provider_order=("vertex",))

    providers = build_vision_providers(config, recorder=LlmCallRecorder(), emitter=ProgressEmitter(), purpose="viewer")

    assert _names(providers) == [("vertex", "gemini-3.8-flash"), ("vertex", "gemini-3.5-flash-lite")]


def test_unconfigured_and_unknown_providers_are_skipped() -> None:
    config = DocumentProcessingConfig(provider_order=("bedrock", "azure", "opencode", "openrouter", "gemini", "nope"))

    assert build_vision_providers(config, recorder=LlmCallRecorder(), emitter=ProgressEmitter()) == []
