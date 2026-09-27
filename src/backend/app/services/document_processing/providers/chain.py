"""Provider fallback chain with a process-wide concurrency cap."""

from __future__ import annotations

import threading
from typing import Any

from app.services.document_processing.metrics import LlmCallRecorder
from app.services.document_processing.progress import ProgressEmitter
from app.services.document_processing.providers.base import VisionLanguageProvider

_LIMITERS: dict[int, threading.BoundedSemaphore] = {}
_LIMITERS_LOCK = threading.Lock()


def _global_limiter(size: int) -> threading.BoundedSemaphore:
    """One semaphore per configured size, shared by every chain in this process."""
    with _LIMITERS_LOCK:
        limiter = _LIMITERS.get(size)
        if limiter is None:
            limiter = threading.BoundedSemaphore(max(1, size))
            _LIMITERS[size] = limiter
        return limiter


class ProviderChain:
    def __init__(
        self,
        providers: list[VisionLanguageProvider],
        *,
        recorder: LlmCallRecorder,
        emitter: ProgressEmitter,
        enable_real_vision: bool,
        global_concurrency: int = 32,
    ) -> None:
        self._providers = providers
        self._recorder = recorder
        self._emitter = emitter
        self._enable_real_vision = enable_real_vision
        self._limiter = _global_limiter(global_concurrency)

    @property
    def enabled(self) -> bool:
        return self._enable_real_vision

    def vision(
        self,
        prompt: str,
        images: bytes | list[bytes] | None = None,
        *,
        response_schema: dict[str, Any] | None = None,
        max_output_tokens: int | None = None,
        operation: str = "vision",
    ) -> str:
        """Try providers in order; returns text, a placeholder when disabled, or an error marker."""
        if not self._enable_real_vision:
            return "[VISION_PLACEHOLDER] Real vision disabled."

        imgs = [images] if isinstance(images, bytes) else images
        extra: dict[str, Any] = {}
        if response_schema is not None:
            extra["response_schema"] = response_schema
        if max_output_tokens is not None:
            extra["max_output_tokens"] = max_output_tokens

        last_error: str | None = None
        with self._limiter:
            for provider in self._providers:
                try:
                    response = provider.complete(prompt, images=imgs, operation=operation, **extra)
                except Exception as exc:  # noqa: BLE001 - a raising provider is just a failed attempt
                    last_error = f"{type(exc).__name__}: {exc}"
                    continue
                if response.ok:
                    return response.text
                last_error = response.error
        return f"[VISION_ERROR] All vision providers failed ({last_error})."
