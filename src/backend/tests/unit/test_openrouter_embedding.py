from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.llm.embeddings import OpenRouterEmbedding
from app.llm.errors import EmbeddingProviderError


class _FakeEmbeddingsAPI:
    def __init__(self, dimension: int, calls: list, fail: bool = False) -> None:
        self._dimension = dimension
        self._calls = calls
        self._fail = fail

    def create(self, *, model: str, input: list[str]):  # noqa: A002 - OpenAI SDK arg name
        if self._fail:
            raise ConnectionError("network down")
        self._calls.append({"model": model, "input": list(input)})
        data = [SimpleNamespace(embedding=[0.1] * self._dimension) for _ in input]
        return SimpleNamespace(data=data)


class _FakeClient:
    def __init__(self, dimension: int = 1536, fail: bool = False) -> None:
        self.calls: list = []
        self.embeddings = _FakeEmbeddingsAPI(dimension, self.calls, fail=fail)


def _service(client: _FakeClient, **kwargs) -> OpenRouterEmbedding:
    return OpenRouterEmbedding(api_key="test-key", client=client, **kwargs)


def test_encode_returns_expected_dimension() -> None:
    client = _FakeClient()
    vectors = _service(client).encode(["hello", "world"])
    assert len(vectors) == 2
    assert all(len(v) == 1536 for v in vectors)
    assert client.calls[0]["model"] == "openai/text-embedding-3-small"


def test_encode_batches_requests() -> None:
    client = _FakeClient()
    _service(client, batch_size=2).encode(["a", "b", "c", "d", "e"])
    assert [len(c["input"]) for c in client.calls] == [2, 2, 1]


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
