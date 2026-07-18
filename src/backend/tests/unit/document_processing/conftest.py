from __future__ import annotations

from app.services.document_processing.metrics import LlmCallRecorder
from app.services.document_processing.progress import ProgressEmitter
from app.services.document_processing.providers.base import (
    VisionLanguageProvider,
)
from app.services.document_processing.providers.chain import ProviderChain


def make_chain(
    providers: list[VisionLanguageProvider] | None = None,
    *,
    enable_real_vision: bool = False,
) -> ProviderChain:
    """Build a ProviderChain with throwaway recorder/emitter for unit tests."""
    return ProviderChain(
        providers or [],
        recorder=LlmCallRecorder(),
        emitter=ProgressEmitter(),
        enable_real_vision=enable_real_vision,
    )
