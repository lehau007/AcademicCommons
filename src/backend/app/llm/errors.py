from __future__ import annotations


class ProviderError(RuntimeError):
    """Remote AI-provider failure whose message is safe to show to end users.

    ``str(exc)`` is forwarded verbatim to the UI (SSE error events and HTTP 503
    ``detail``), so messages here are user-facing Vietnamese; technical detail
    belongs on the ``__cause__`` chain and in server logs.
    """

    code: str = "provider_failed"
    default_message: str = "Dịch vụ AI đang gặp sự cố. Vui lòng thử lại sau."

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or self.default_message)


class EmbeddingProviderError(ProviderError):
    code = "embedding_failed"
    default_message = "Dịch vụ embedding đang gặp sự cố. Vui lòng thử lại sau."


class RerankProviderError(ProviderError):
    code = "rerank_failed"
    default_message = "Dịch vụ xếp hạng kết quả (rerank) đang gặp sự cố. Vui lòng thử lại sau."


__all__ = ["EmbeddingProviderError", "ProviderError", "RerankProviderError"]
