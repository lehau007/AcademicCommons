"""Vision-capable LLM provider abstraction for document processing.

NOTE: the backend's existing ``app.llm`` providers are text-only; document processing
needs image input (VLM page classification + scanned-page OCR), so these providers are
self-contained but mirror the ``app.llm`` design idioms (ABC + result dataclass + chain).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderResponse:
    text: str
    provider: str
    model: str
    status: str  # "success" | "error"
    latency_ms: int
    prompt_tokens: int = 0
    completion_tokens: int = 0
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.status == "success"


class VisionLanguageProvider(ABC):
    """A single provider (Azure / Gemini / Groq). Synchronous, like the experiment.

    Implementations MUST record each call on the injected
    :class:`~app.services.document_processing.metrics.LlmCallRecorder` and emit
    ``llm_call_start`` / ``llm_call_success`` / ``llm_call_error`` progress events.
    """

    provider_name: str
    supports_vision: bool = True

    @abstractmethod
    def complete(
        self,
        prompt: str,
        *,
        images: list[bytes] | None = None,
        operation: str = "text",
    ) -> ProviderResponse:
        """Run a single completion. Returns a response; ``status == 'error'`` on failure.

        Implementations should NOT raise for ordinary provider/HTTP failures — return an
        error response so the chain can fall back. (Gemini may raise; the chain handles it.)
        """
        raise NotImplementedError
