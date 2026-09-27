"""Vertex AI vision provider. Ports Gemini vision VLM calls to Vertex AI via ADC."""

from __future__ import annotations

import threading
import time
from typing import Any

from app.llm.vertex_auth import get_vertex_credentials_and_project
from app.services.document_processing.config import DocumentProcessingConfig
from app.services.document_processing.metrics import LlmCallRecorder
from app.services.document_processing.progress import ProgressEmitter
from app.services.document_processing.providers.base import (
    ProviderResponse,
    VisionLanguageProvider,
    sniff_image_mime,
)

try:
    from google import genai
    from google.genai import types

    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False


class VertexVisionProvider(VisionLanguageProvider):
    provider_name = "vertex"
    supports_vision = True

    def __init__(
        self,
        config: DocumentProcessingConfig,
        *,
        recorder: LlmCallRecorder,
        emitter: ProgressEmitter,
        model: str | None = None,
        thinking_level: str | None = None,
    ) -> None:
        self._config = config
        self._recorder = recorder
        self._emitter = emitter
        self._model = model or config.ocr_vision_model
        self._thinking_level = thinking_level
        self._client: Any | None = None
        self._client_lock = threading.Lock()

    @property
    def model(self) -> str:
        return self._model

    def _get_client(self) -> Any:
        if self._client is None:
            with self._client_lock:  # the first burst of worker threads must build one client, not N
                if self._client is None:
                    creds, resolved_project = get_vertex_credentials_and_project()
                    self._client = genai.Client(
                        vertexai=True,
                        project=self._config.vertex_project_id or resolved_project,
                        location=self._config.vertex_genai_location,
                        credentials=creds,
                        http_options=types.HttpOptions(timeout=int(self._config.request_timeout_seconds * 1000)),
                    )
        return self._client

    def _error(self, operation: str, latency_ms: int, message: str) -> ProviderResponse:
        self._recorder.record(operation, "vertex", self._model, "error", latency_ms, error=message)
        self._emitter.emit(
            "llm_call_error", operation=operation, provider="vertex", model=self._model,
            latency_ms=latency_ms, error=message,
        )
        return ProviderResponse(
            text="", provider="vertex", model=self._model, status="error", latency_ms=latency_ms, error=message
        )

    def complete(
        self,
        prompt: str,
        *,
        images: list[bytes] | None = None,
        operation: str = "text",
        response_schema: dict[str, Any] | None = None,
        max_output_tokens: int | None = None,
    ) -> ProviderResponse:
        if not HAS_GENAI:
            return self._error(operation, 0, "google-genai not installed")

        t0 = time.time()
        self._emitter.emit(
            "llm_call_start", operation=operation, provider="vertex", model=self._model, has_image=bool(images)
        )
        try:
            client = self._get_client()
            contents: list[Any] = [
                types.Part.from_bytes(data=img, mime_type=sniff_image_mime(img)) for img in images or []
            ]
            contents.append(prompt)
            config_kwargs: dict[str, Any] = {
                "max_output_tokens": max_output_tokens or self._config.max_output_tokens,
                "temperature": 0.2,
                "automatic_function_calling": types.AutomaticFunctionCallingConfig(disable=True),
            }
            if self._thinking_level:
                config_kwargs["thinking_config"] = types.ThinkingConfig(thinking_level=self._thinking_level)
            if response_schema is not None:
                config_kwargs["response_mime_type"] = "application/json"
                config_kwargs["response_schema"] = response_schema
            response = client.models.generate_content(
                model=self._model, contents=contents, config=types.GenerateContentConfig(**config_kwargs)
            )
            latency_ms = int((time.time() - t0) * 1000)
            text = response.text or ""
            if not text.strip():
                return self._error(operation, latency_ms, "empty response text")
            usage = response.usage_metadata
            prompt_tokens = int(getattr(usage, "prompt_token_count", 0) or 0)
            completion_tokens = int(getattr(usage, "candidates_token_count", 0) or 0) + int(
                getattr(usage, "thoughts_token_count", 0) or 0
            )
            self._recorder.record(
                operation, "vertex", self._model, "success", latency_ms,
                prompt_tokens=prompt_tokens, completion_tokens=completion_tokens,
            )
            self._emitter.emit(
                "llm_call_success", operation=operation, provider="vertex", model=self._model, latency_ms=latency_ms
            )
            return ProviderResponse(
                text=text, provider="vertex", model=self._model, status="success", latency_ms=latency_ms,
                prompt_tokens=prompt_tokens, completion_tokens=completion_tokens,
            )
        except Exception as exc:  # noqa: BLE001 - any SDK/HTTP failure falls through the chain
            latency_ms = int((time.time() - t0) * 1000)
            status_code = getattr(exc, "status_code", None) or getattr(exc, "code", None)
            detail = (
                f"{type(exc).__name__}(HTTP_{status_code}): {exc}"
                if status_code
                else f"{type(exc).__name__}: {exc}"
            )
            return self._error(operation, latency_ms, detail[:500])
