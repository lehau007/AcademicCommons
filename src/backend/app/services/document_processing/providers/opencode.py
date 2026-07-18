"""OpenCode (opencode.ai) vision provider. OpenAI-compatible, mirrors ``groq.py``.

Go-plan gateway with a restricted model catalog (no Claude/GPT/Gemini). Default model
``minimax-m3`` is vision-capable but emits a leading ``<think>...</think>`` reasoning
trace ahead of the answer, which is stripped before returning.
"""

from __future__ import annotations

import base64
import re
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

_THINK_BLOCK_RE = re.compile(r"<think>.*?</think>\s*", re.DOTALL)


def _strip_think(content: str) -> str:
    """Remove minimax-m3's leading ``<think>...</think>`` reasoning trace.

    minimax emits the reasoning block *before* the OCR transcription. Closed
    blocks are removed outright. If the response was truncated at the token
    limit mid-thought (an unclosed ``<think>`` with no ``</think>``), there is
    no transcription after it to keep, so we drop everything from ``<think>``
    onward rather than leak raw reasoning as if it were document text.
    """
    if "<think>" not in content:
        return content.strip()
    stripped = _THINK_BLOCK_RE.sub("", content).strip()
    if "<think>" not in stripped:
        return stripped
    return stripped[: stripped.find("<think>")].strip()


class OpenCodeVisionProvider(VisionLanguageProvider):
    provider_name = "opencode"
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
        model = self._config.opencode_model
        if not HAS_OPENAI:
            msg = "openai_client_not_installed"
            self._recorder.record(operation, "opencode", model, "error", 0, error=msg)
            return ProviderResponse(
                text="",
                provider="opencode",
                model=model,
                status="error",
                latency_ms=0,
                error=msg,
            )
        api_key = self._config.opencode_api_key
        if not api_key:
            msg = "OPENCODE_API_KEY_missing"
            self._recorder.record(operation, "opencode", model, "error", 0, error=msg)
            return ProviderResponse(
                text="",
                provider="opencode",
                model=model,
                status="error",
                latency_ms=0,
                error=msg,
            )

        t0 = time.time()
        self._emitter.emit(
            "llm_call_start",
            operation=operation,
            provider="opencode",
            model=model,
            has_image=bool(images),
        )
        try:
            client = OpenAI(
                api_key=api_key,
                base_url=self._config.opencode_base_url,
                timeout=90.0,
                max_retries=1,
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
                # minimax-m3 spends part of its budget on a <think> reasoning
                # trace before the transcription; 4096 truncated text-dense
                # pages mid-thought, so give the answer room after reasoning.
                max_tokens=8192,
            )
            latency_ms = int((time.time() - t0) * 1000)
            usage = response.usage
            prompt_tokens = usage.prompt_tokens if usage else 0
            completion_tokens = usage.completion_tokens if usage else 0
            text = _strip_think(response.choices[0].message.content or "")
            self._recorder.record(
                operation, "opencode", model, "success", latency_ms,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
            )
            self._emitter.emit(
                "llm_call_success",
                operation=operation,
                provider="opencode",
                model=model,
                latency_ms=latency_ms,
            )
            return ProviderResponse(
                text=text,
                provider="opencode",
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
            self._recorder.record(operation, "opencode", model, "error", latency_ms, error=err_detail)
            self._emitter.emit(
                "llm_call_error",
                operation=operation,
                provider="opencode",
                model=model,
                latency_ms=latency_ms,
                error=err_detail,
            )
            return ProviderResponse(
                text="",
                provider="opencode",
                model=model,
                status="error",
                latency_ms=latency_ms,
                error=err_detail,
            )
