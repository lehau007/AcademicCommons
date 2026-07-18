"""OpenRouter (openrouter.ai) vision provider. OpenAI-compatible, mirrors ``groq.py``.

Gateway aggregating hundreds of models. Default model ``openai/gpt-5.4-mini`` was
picked from a mid-priced candidate comparison (see tests/openrouter_api_doc.md) for
its speed and OCR/vision transcription accuracy on lecture-slide images.
"""

from __future__ import annotations

import base64
import time
from typing import Any

from app.services.document_processing.config import DocumentProcessingConfig
from app.services.document_processing.metrics import LlmCallRecorder
from app.services.document_processing.progress import ProgressEmitter
from app.services.document_processing.providers.base import ProviderResponse, VisionLanguageProvider

try:
    from openai import OpenAI

    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


class OpenRouterVisionProvider(VisionLanguageProvider):
    provider_name = "openrouter"
    supports_vision = True

    def __init__(
        self,
        config: DocumentProcessingConfig,
        *,
        recorder: LlmCallRecorder,
        emitter: ProgressEmitter,
    ) -> None:
        self._config = config
        self._recorder = recorder
        self._emitter = emitter

    def complete(
        self,
        prompt: str,
        *,
        images: list[bytes] | None = None,
        operation: str = "text",
    ) -> ProviderResponse:
        model = self._config.openrouter_model
        if not HAS_OPENAI:
            msg = "openai_client_not_installed"
            self._recorder.record(operation, "openrouter", model, "error", 0, error=msg)
            return ProviderResponse(
                text="",
                provider="openrouter",
                model=model,
                status="error",
                latency_ms=0,
                error=msg,
            )
        api_key = self._config.openrouter_api_key
        if not api_key:
            msg = "OPENROUTER_API_KEY_missing"
            self._recorder.record(operation, "openrouter", model, "error", 0, error=msg)
            return ProviderResponse(
                text="",
                provider="openrouter",
                model=model,
                status="error",
                latency_ms=0,
                error=msg,
            )

        t0 = time.time()
        self._emitter.emit(
            "llm_call_start",
            operation=operation,
            provider="openrouter",
            model=model,
            has_image=bool(images),
        )
        try:
            client = OpenAI(
                api_key=api_key,
                base_url=self._config.openrouter_base_url,
                timeout=self._config.request_timeout_seconds,
            )
            if images:
                content_parts: list[Any] = [{"type": "text", "text": prompt}]
                for img in images:
                    b64 = base64.b64encode(img).decode("utf-8")
                    content_parts.append({
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{b64}"},
                    })
                messages: list[Any] = [{"role": "user", "content": content_parts}]
            else:
                messages = [{"role": "user", "content": prompt}]
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.3,
                max_tokens=4096,
            )
            latency_ms = int((time.time() - t0) * 1000)
            usage = response.usage
            prompt_tokens = usage.prompt_tokens if usage else 0
            completion_tokens = usage.completion_tokens if usage else 0
            self._recorder.record(
                operation, "openrouter", model, "success", latency_ms,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
            )
            self._emitter.emit(
                "llm_call_success",
                operation=operation,
                provider="openrouter",
                model=model,
                latency_ms=latency_ms,
            )
            return ProviderResponse(
                text=response.choices[0].message.content or "",
                provider="openrouter",
                model=model,
                status="success",
                latency_ms=latency_ms,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
            )
        except Exception as e:
            latency_ms = int((time.time() - t0) * 1000)
            status_code = getattr(e, "status_code", None)
            err_detail = (
                f"{type(e).__name__}(HTTP_{status_code}): {e}"
                if status_code
                else f"{type(e).__name__}: {e}"
            )
            self._recorder.record(operation, "openrouter", model, "error", latency_ms, error=err_detail)
            self._emitter.emit(
                "llm_call_error",
                operation=operation,
                provider="openrouter",
                model=model,
                latency_ms=latency_ms,
                error=err_detail,
            )
            return ProviderResponse(
                text="",
                provider="openrouter",
                model=model,
                status="error",
                latency_ms=latency_ms,
                error=err_detail,
            )
