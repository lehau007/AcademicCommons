"""Bedrock vision provider. OpenAI-compatible, mirrors ``azure.py``.

Reaches Bedrock via the OpenAI-compatible chat.completions endpoint (api_key +
base_url), like the text-only :class:`app.llm.providers.BedrockProvider`, but stays
self-contained (sync, no optimizer SDK) so it can send image content parts.
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


class BedrockVisionProvider(VisionLanguageProvider):
    provider_name = "bedrock"
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
        model = self._config.bedrock_model_id or ""
        if not HAS_OPENAI:
            msg = "openai_client_not_installed"
            self._recorder.record(operation, "bedrock", model, "error", 0, error=msg)
            return ProviderResponse(
                text="",
                provider="bedrock",
                model=model,
                status="error",
                latency_ms=0,
                error=msg,
            )

        api_key = self._config.bedrock_api_key
        if not api_key:
            msg = "BEDROCK_API_KEY_missing"
            self._recorder.record(operation, "bedrock", model, "error", 0, error=msg)
            return ProviderResponse(
                text="",
                provider="bedrock",
                model=model,
                status="error",
                latency_ms=0,
                error=msg,
            )

        base_url = (
            self._config.bedrock_base_url
            or f"https://bedrock-mantle.{self._config.aws_region}.api.aws/v1"
        )

        last_error: str | None = None
        for attempt in range(2):
            t0 = time.time()
            self._emitter.emit(
                "llm_call_start",
                operation=operation,
                provider="bedrock",
                model=model,
                attempt=attempt + 1,
                has_image=bool(images),
            )
            try:
                client = OpenAI(
                    base_url=base_url,
                    api_key=api_key,
                    timeout=self._config.request_timeout_seconds,
                    # This provider already runs its own retry loop below; leaving
                    # the SDK default (2) stacks multiplicatively (up to 6 calls
                    # ~= 6 x timeout per batch), which is what let a stalled
                    # normalization batch run far past the OCR job timeout.
                    max_retries=0,
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
                    operation, "bedrock", model, "success", latency_ms,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                )
                self._emitter.emit(
                    "llm_call_success",
                    operation=operation,
                    provider="bedrock",
                    model=model,
                    attempt=attempt + 1,
                    latency_ms=latency_ms,
                )
                return ProviderResponse(
                    text=response.choices[0].message.content or "",
                    provider="bedrock",
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
                last_error = err_detail
                self._recorder.record(operation, "bedrock", model, "error", latency_ms, error=err_detail)
                self._emitter.emit(
                    "llm_call_error",
                    operation=operation,
                    provider="bedrock",
                    model=model,
                    attempt=attempt + 1,
                    latency_ms=latency_ms,
                    error=err_detail,
                )
                if attempt == 0:
                    time.sleep(2.0)

        return ProviderResponse(
            text="",
            provider="bedrock",
            model=model,
            status="error",
            latency_ms=0,
            error=last_error,
        )
