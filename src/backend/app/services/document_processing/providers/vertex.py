"""Vertex AI vision provider. Ports Gemini vision VLM calls to Vertex AI via ADC."""

from __future__ import annotations

import io
import time
from typing import Any

import PIL.Image

from app.llm.vertex_auth import get_vertex_credentials_and_project
from app.services.document_processing.config import DocumentProcessingConfig
from app.services.document_processing.metrics import LlmCallRecorder
from app.services.document_processing.progress import ProgressEmitter
from app.services.document_processing.providers.base import ProviderResponse, VisionLanguageProvider

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
    ) -> None:
        self._config = config
        self._recorder = recorder
        self._emitter = emitter
        self._client: Any | None = None

    def _get_client(self) -> Any:
        if self._client is None:
            creds, resolved_project = get_vertex_credentials_and_project()
            project_id = self._config.vertex_project_id or resolved_project
            location = self._config.vertex_location
            timeout_ms = int(getattr(self._config, "request_timeout_seconds", 120) * 1000)
            self._client = genai.Client(
                vertexai=True,
                project=project_id,
                location=location,
                credentials=creds,
                http_options=types.HttpOptions(timeout=timeout_ms),
            )
        return self._client

    def complete(
        self,
        prompt: str,
        *,
        images: list[bytes] | None = None,
        operation: str = "text",
    ) -> ProviderResponse:
        model_id = self._config.vertex_llm_model
        if not HAS_GENAI:
            msg = "google-genai not installed"
            self._recorder.record(operation, "vertex", model_id, "error", 0, error=msg)
            return ProviderResponse(
                text="",
                provider="vertex",
                model=model_id,
                status="error",
                latency_ms=0,
                error=msg,
            )

        client = self._get_client()
        t0 = time.time()
        self._emitter.emit(
            "llm_call_start",
            operation=operation,
            provider="vertex",
            model=model_id,
            has_image=bool(images),
        )
        try:
            contents: list[Any] = []
            if images:
                for img in images:
                    contents.append(PIL.Image.open(io.BytesIO(img)))
            contents.append(prompt)
            response = client.models.generate_content(
                model=model_id,
                contents=contents,
                config=types.GenerateContentConfig(
                    max_output_tokens=self._config.normalization_max_output_tokens,
                    temperature=0.3,
                ),
            )
            latency_ms = int((time.time() - t0) * 1000)
            usage = response.usage_metadata
            prompt_tokens = getattr(usage, "prompt_token_count", 0) or 0
            completion_tokens = getattr(usage, "candidates_token_count", 0) or 0
            self._recorder.record(
                operation, "vertex", model_id, "success", latency_ms,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
            )
            self._emitter.emit(
                "llm_call_success",
                operation=operation,
                provider="vertex",
                model=model_id,
                latency_ms=latency_ms,
            )
            return ProviderResponse(
                text=response.text or "",
                provider="vertex",
                model=model_id,
                status="success",
                latency_ms=latency_ms,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
            )
        except Exception as e:
            latency_ms = int((time.time() - t0) * 1000)
            status_code = getattr(e, "status_code", None) or getattr(e, "code", None)
            err_detail = (
                f"{type(e).__name__}(HTTP_{status_code}): {e}"
                if status_code
                else f"{type(e).__name__}: {e}"
            )
            self._recorder.record(operation, "vertex", model_id, "error", latency_ms, error=err_detail)
            self._emitter.emit(
                "llm_call_error",
                operation=operation,
                provider="vertex",
                model=model_id,
                latency_ms=latency_ms,
                error=err_detail,
            )
            return ProviderResponse(
                text="",
                provider="vertex",
                model=model_id,
                status="error",
                latency_ms=latency_ms,
                error=err_detail,
            )
