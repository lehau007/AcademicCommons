"""Provider fallback chain: Azure (primary) -> Gemini -> Groq (last resort).

Ports the experiment's ``call_vlm`` (vision dispatch) and the provider sequence inside
``_call_normalization_llm`` (text dispatch). The ``OCR_ENABLE_REAL_VISION`` short-circuit
lives here so callers (classifier/extractors/normalizer) stay simple.
"""

from __future__ import annotations

from app.services.document_processing.metrics import LlmCallRecorder
from app.services.document_processing.progress import ProgressEmitter
from app.services.document_processing.providers.base import VisionLanguageProvider


class ProviderChain:
    def __init__(
        self,
        providers: list[VisionLanguageProvider],
        *,
        recorder: LlmCallRecorder,
        emitter: ProgressEmitter,
        enable_real_vision: bool,
    ) -> None:
        self._providers = providers
        self._recorder = recorder
        self._emitter = emitter
        self._enable_real_vision = enable_real_vision

    def vision(self, prompt: str, images: bytes | list[bytes] | None = None) -> str:
        """Vision call with fallback. Mirrors experiment ``call_vlm``.

        Returns ``"[VISION_PLACEHOLDER] ..."`` when real vision is disabled.
        """
        if not self._enable_real_vision:
            return "[VISION_PLACEHOLDER] Real vision disabled."

        imgs: list[bytes] | None
        if images is None:
            imgs = None
        elif isinstance(images, bytes):
            imgs = [images]
        else:
            imgs = images

        last_error: str | None = None
        for provider in self._providers:
            response = provider.complete(prompt, images=imgs, operation="vision")
            if response.ok:
                return response.text
            last_error = response.error

        return f"[VISION_ERROR] All vision providers failed ({last_error})."

    def text(self, prompt: str, *, operation: str = "normalization") -> tuple[str, str | None]:
        """Text call with fallback. Mirrors experiment ``_call_normalization_llm`` sequence.

        Returns ``(output_text, error_or_None)``. On total failure returns the error string.
        """
        last_error: str | None = None
        for provider in self._providers:
            response = provider.complete(prompt, images=None, operation=operation)
            if response.ok:
                return response.text, None
            last_error = response.error

        return prompt, last_error
