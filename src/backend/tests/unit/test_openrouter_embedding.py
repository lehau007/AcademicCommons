from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from app.llm.embeddings import NvidiaEmbedding, OpenRouterEmbedding
from app.llm.errors import EmbeddingProviderError


class _FakeEmbeddingsAPI:
    def __init__(self, dimension: int, calls: list, fail: bool = False) -> None:
        self._dimension = dimension
        self._calls = calls
        self._fail = fail

    def create(
        self,
        *,
        model: str,
        input: list[str],  # noqa: A002 - OpenAI SDK arg name
        extra_body: dict | None = None,
    ):
        if self._fail:
            raise ConnectionError("network down")
        self._calls.append({"model": model, "input": list(input), "extra_body": extra_body})
        data = [SimpleNamespace(embedding=[0.1] * self._dimension) for _ in input]
        return SimpleNamespace(data=data)


class _FakeClient:
    def __init__(self, dimension: int = 1536, fail: bool = False) -> None:
        self.calls: list = []
        self.embeddings = _FakeEmbeddingsAPI(dimension, self.calls, fail=fail)


def _service(client: _FakeClient, **kwargs) -> OpenRouterEmbedding:
    return OpenRouterEmbedding(api_key="test-key", client=client, **kwargs)


def _nvidia_service(client: _FakeClient, **kwargs) -> NvidiaEmbedding:
    return NvidiaEmbedding(api_key="test-key", client=client, **kwargs)


def test_encode_returns_expected_dimension() -> None:
    client = _FakeClient()
    vectors = _service(client).encode(["hello", "world"])
    assert len(vectors) == 2
    assert all(len(v) == 1536 for v in vectors)
    assert client.calls[0]["model"] == "openai/text-embedding-3-small"


def test_encode_batches_requests_and_logs_metadata_only(caplog) -> None:
    client = _FakeClient()
    with caplog.at_level("INFO", logger="app.llm.embeddings"):
        _service(client, batch_size=2).encode(
            ["DO_NOT_LOG_A", "DO_NOT_LOG_B", "DO_NOT_LOG_C", "DO_NOT_LOG_D", "DO_NOT_LOG_E"]
        )

    assert [len(c["input"]) for c in client.calls] == [2, 2, 1]
    combined = "\n".join(caplog.messages)
    assert combined.count("event=embedding_call_start") == 3
    assert combined.count("event=embedding_call_success") == 3
    assert "provider=openrouter" in combined
    assert "model=openai/text-embedding-3-small" in combined
    assert "input_type=passage" in combined
    assert "item_count=2" in combined
    assert "item_count=1" in combined
    assert "DO_NOT_LOG_A" not in combined
    assert "DO_NOT_LOG_E" not in combined


def test_encode_empty_returns_empty() -> None:
    client = _FakeClient()
    assert _service(client).encode([]) == []
    assert client.calls == []


def test_encode_wrong_dimension_raises() -> None:
    client = _FakeClient(dimension=1024)
    with pytest.raises(EmbeddingProviderError):
        _service(client).encode(["hello"])


def test_encode_api_error_wrapped() -> None:
    client = _FakeClient(fail=True)
    with pytest.raises(EmbeddingProviderError) as excinfo:
        _service(client).encode(["hello"])
    assert isinstance(excinfo.value.__cause__, ConnectionError)


def test_encode_api_error_logs_metadata_only(caplog) -> None:
    client = _FakeClient(fail=True)

    with pytest.raises(EmbeddingProviderError):
        with caplog.at_level("INFO", logger="app.llm.embeddings"):
            _service(client).encode(["DO_NOT_LOG_OPENROUTER_TEXT"])

    combined = "\n".join(caplog.messages)
    assert "event=embedding_call_start" in combined
    assert "event=embedding_call_error" in combined
    assert "provider=openrouter" in combined
    assert "exception_type=ConnectionError" in combined
    assert "DO_NOT_LOG_OPENROUTER_TEXT" not in combined


def test_nvidia_encode_batches_requests_and_logs_metadata_only(caplog) -> None:
    client = _FakeClient(dimension=1024)

    with caplog.at_level("INFO", logger="app.llm.embeddings"):
        vectors = _nvidia_service(client, batch_size=2, dimension=1024).encode(
            ["DO_NOT_LOG_N1", "DO_NOT_LOG_N2", "DO_NOT_LOG_N3", "DO_NOT_LOG_N4", "DO_NOT_LOG_N5"],
            input_type="query",
        )

    assert len(vectors) == 5
    assert [len(c["input"]) for c in client.calls] == [2, 2, 1]
    assert all(c["extra_body"] == {"input_type": "query", "truncate": "END"} for c in client.calls)
    combined = "\n".join(caplog.messages)
    assert combined.count("event=embedding_call_start") == 3
    assert combined.count("event=embedding_call_success") == 3
    assert "provider=nvidia" in combined
    assert "model=nvidia/nv-embedqa-e5-v5" in combined
    assert "dimension=1024" in combined
    assert "input_type=query" in combined
    assert "DO_NOT_LOG_N1" not in combined
    assert "DO_NOT_LOG_N5" not in combined


def test_nvidia_encode_error_logs_and_preserves_exception(caplog) -> None:
    client = _FakeClient(dimension=1024, fail=True)

    with pytest.raises(ConnectionError):
        with caplog.at_level("INFO", logger="app.llm.embeddings"):
            _nvidia_service(client, dimension=1024).encode(["DO_NOT_LOG_NVIDIA_TEXT"])

    combined = "\n".join(caplog.messages)
    assert "event=embedding_call_start" in combined
    assert "event=embedding_call_error" in combined
    assert "provider=nvidia" in combined
    assert "exception_type=ConnectionError" in combined
    assert "DO_NOT_LOG_NVIDIA_TEXT" not in combined


@pytest.mark.parametrize(
    ("service", "provider", "dimension", "input_type"),
    [
        (OpenRouterEmbedding(api_key="test-key"), "openrouter", 1536, "passage"),
        (NvidiaEmbedding(api_key="test-key"), "nvidia", 1024, "query"),
    ],
)
def test_hosted_embedding_client_bootstrap_error_logs_metadata_only(
    caplog,
    monkeypatch: pytest.MonkeyPatch,
    service,
    provider: str,
    dimension: int,
    input_type: str,
) -> None:
    monkeypatch.setattr(
        service,
        "_load_client",
        MagicMock(side_effect=ConnectionError("SECRET_BOOTSTRAP_FAILURE")),
    )

    with pytest.raises(ConnectionError, match="SECRET_BOOTSTRAP_FAILURE"):
        with caplog.at_level("INFO", logger="app.llm.embeddings"):
            service.encode(["SECRET_BOOTSTRAP_INPUT"], input_type=input_type)

    combined = "\n".join(caplog.messages)
    assert "event=embedding_call_start" in combined
    assert "event=embedding_call_error" in combined
    assert f"provider={provider}" in combined
    assert f"dimension={dimension}" in combined
    assert f"input_type={input_type}" in combined
    assert "item_count=1" in combined
    assert "latency_ms=" in combined
    assert "exception_type=ConnectionError" in combined
    assert "SECRET_BOOTSTRAP_FAILURE" not in combined
    assert "SECRET_BOOTSTRAP_INPUT" not in combined
