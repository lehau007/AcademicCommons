from __future__ import annotations

import pytest

from app.llm.errors import EmbeddingProviderError, ProviderError, RerankProviderError


def test_embedding_error_defaults() -> None:
    exc = EmbeddingProviderError()
    assert exc.code == "embedding_failed"
    assert "embedding" in str(exc).lower()
    assert isinstance(exc, ProviderError)


def test_rerank_error_defaults() -> None:
    exc = RerankProviderError()
    assert exc.code == "rerank_failed"
    assert isinstance(exc, ProviderError)


def test_custom_message_overrides_default() -> None:
    exc = EmbeddingProviderError("boom")
    assert str(exc) == "boom"


def test_provider_error_is_runtime_error() -> None:
    with pytest.raises(RuntimeError):
        raise RerankProviderError()
