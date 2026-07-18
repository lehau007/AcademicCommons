"""Azure AI Foundry provider (primary). Ports experiment ``_call_azure_openai``."""

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


class AzureOpenAIVisionProvider(VisionLanguageProvider):
    provider_name = "azure_openai"
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
        deployment = self._config.azure_deployment or ""
        if not HAS_OPENAI:
            msg = "openai_client_not_installed"
            self._recorder.record(operation, "azure_openai", deployment, "error", 0, error=msg)
            return ProviderResponse(
                text="",
                provider="azure_openai",
                model=deployment,
                status="error",
                latency_ms=0,
                error=msg,
            )

        endpoint = self._config.azure_endpoint
        api_key = self._config.azure_api_key
        if not api_key:
            msg = "AZURE_AI_API_KEY_missing"
            self._recorder.record(operation, "azure_openai", deployment, "error", 0, error=msg)
            return ProviderResponse(
                text="",
                provider="azure_openai",
                model=deployment,
                status="error",
                latency_ms=0,
                error=msg,
            )

        last_error: str | None = None
        for attempt in range(2):
            t0 = time.time()
            self._emitter.emit(
                "llm_call_start",
                operation=operation,
                provider="azure_openai",
                model=deployment,
                attempt=attempt + 1,
                has_image=bool(images),
            )
            try:
                client = OpenAI(
                    base_url=endpoint,
                    api_key=api_key,
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
                    model=deployment,
                    messages=messages,
                    temperature=0.3,
                    max_tokens=4096,
                )

                latency_ms = int((time.time() - t0) * 1000)
                usage = response.usage
                prompt_tokens = usage.prompt_tokens if usage else 0
                completion_tokens = usage.completion_tokens if usage else 0
                self._recorder.record(
                    operation, "azure_openai", deployment, "success", latency_ms,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                )
                self._emitter.emit(
                    "llm_call_success",
                    operation=operation,
                    provider="azure_openai",
                    model=deployment,
                    attempt=attempt + 1,
                    latency_ms=latency_ms,
                )
                return ProviderResponse(
                    text=response.choices[0].message.content or "",
                    provider="azure_openai",
                    model=deployment,
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
                self._recorder.record(operation, "azure_openai", deployment, "error", latency_ms, error=err_detail)
                self._emitter.emit(
                    "llm_call_error",
                    operation=operation,
                    provider="azure_openai",
                    model=deployment,
                    attempt=attempt + 1,
                    latency_ms=latency_ms,
                    error=err_detail,
                )
                if attempt == 0:
                    time.sleep(2.0)

        return ProviderResponse(
            text="",
            provider="azure_openai",
            model=deployment,
            status="error",
            latency_ms=0,
            error=last_error,
        )
