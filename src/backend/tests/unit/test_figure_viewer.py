from __future__ import annotations

from typing import Any

import pytest

from app.config import get_settings
from app.services import figure_viewer
from app.services.document_processing.metrics import LlmCallRecorder
from app.services.document_processing.progress import ProgressEmitter
from app.services.document_processing.providers.base import ProviderResponse, VisionLanguageProvider


class _RecordingProvider(VisionLanguageProvider):
    """Records every call on the injected recorder/emitter, like the real providers do."""

    provider_name = "fake"

    def __init__(self, recorder: LlmCallRecorder, emitter: ProgressEmitter) -> None:
        self._recorder, self._emitter = recorder, emitter

    def complete(self, prompt: str, *, images: list[bytes] | None = None, operation: str = "text",
                 **kwargs: Any) -> ProviderResponse:
        self._emitter.emit("llm_call_start", operation=operation)
        self._recorder.record(operation, "fake", "m", "success", 1, prompt_tokens=10, completion_tokens=5)
        self._emitter.emit("llm_call_success", operation=operation)
        return ProviderResponse("The figure shows a matrix.", "fake", "m", "success", 1)


@pytest.mark.asyncio
async def test_cached_viewer_retains_no_per_call_records(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        figure_viewer, "build_vision_providers",
        lambda config, *, recorder, emitter, purpose: [_RecordingProvider(recorder, emitter)],
    )
    viewer = figure_viewer.FigureViewer(get_settings())

    for _ in range(25):
        assert await viewer.ask(b"png", "What is shown?") == "The figure shows a matrix."

    assert viewer._chain._recorder.summary()["total_calls"] == 0
    assert viewer._chain._emitter.records == []
