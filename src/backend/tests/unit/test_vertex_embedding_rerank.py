from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from app.llm.embeddings import VertexEmbedding
from app.llm.errors import EmbeddingProviderError, RerankProviderError
from app.llm.rerank import VertexRerank


class _FakeEmbeddingItem:
    def __init__(self, values: list[float]) -> None:
        self.values = values


class _FakeEmbedResponse:
    def __init__(self, embeddings: list[_FakeEmbeddingItem]) -> None:
        self.embeddings = embeddings


class _FakeModelsAPI:
    def __init__(self, calls: list, fail: bool = False) -> None:
        self._calls = calls
        self._fail = fail

    def embed_content(self, *, model: str, contents: list[str]) -> _FakeEmbedResponse:
        if self._fail:
            raise RuntimeError("Vertex API error")
        self._calls.append({"model": model, "contents": list(contents)})
        embeddings = [_FakeEmbeddingItem([0.1, 0.2, 0.3]) for _ in contents]
        return _FakeEmbedResponse(embeddings)


class _FakeGenAIClient:
    def __init__(self, fail: bool = False) -> None:
        self.calls: list = []
        self.models = _FakeModelsAPI(self.calls, fail=fail)


class _FakeHttpResponse:
    def __init__(self, payload: dict, status: int = 200) -> None:
        self._payload = payload
        self._status = status

    def raise_for_status(self) -> None:
        if self._status >= 400:
            raise RuntimeError(f"HTTP {self._status}")

    def json(self) -> dict:
        return self._payload


class _FakeHttpClient:
    def __init__(self, payload: dict, status: int = 200) -> None:
        self.calls: list = []
        self._payload = payload
        self._status = status

    def post(self, url: str, json: dict | None = None, headers: dict | None = None) -> _FakeHttpResponse:
        self.calls.append({"url": url, "json": json, "headers": headers})
        return _FakeHttpResponse(self._payload, self._status)


# --- VertexEmbedding Tests ---

def test_vertex_embedding_encode_success() -> None:
    client = _FakeGenAIClient()
    service = VertexEmbedding(project_id="test-proj", client=client)
    vectors = service.encode(["hello", "world"])
    assert len(vectors) == 2
    assert vectors[0] == [0.1, 0.2, 0.3]
    assert client.calls[0]["model"] == "text-embedding-004"
    assert client.calls[0]["contents"] == ["hello", "world"]


def test_vertex_embedding_encode_batching() -> None:
    client = _FakeGenAIClient()
    service = VertexEmbedding(project_id="test-proj", batch_size=2, client=client)
    vectors = service.encode(["a", "b", "c", "d", "e"])
    assert len(vectors) == 5
    assert [len(c["contents"]) for c in client.calls] == [2, 2, 1]


def test_vertex_embedding_encode_empty() -> None:
    client = _FakeGenAIClient()
    service = VertexEmbedding(project_id="test-proj", client=client)
    assert service.encode([]) == []
    assert client.calls == []


def test_vertex_embedding_encode_error_propagation() -> None:
    client = _FakeGenAIClient(fail=True)
    service = VertexEmbedding(project_id="test-proj", client=client)
    with pytest.raises(EmbeddingProviderError) as excinfo:
        service.encode(["hello"])
    assert "Vertex AI embedding failed" in str(excinfo.value)


# --- VertexRerank Tests ---

@patch("app.llm.rerank.get_vertex_credentials_and_project")
def test_vertex_rerank_rank_scored_success(mock_auth: MagicMock) -> None:
    mock_creds = SimpleNamespace(token="fake-token")
    mock_auth.return_value = (mock_creds, "default-project")

    payload = {
        "records": [
            {"id": "0", "score": 0.3},
            {"id": "1", "score": 0.95},
            {"id": "2", "score": 0.6},
        ]
    }
    http_client = _FakeHttpClient(payload)
    reranker = VertexRerank(project_id="my-proj", location="global", client=http_client)

    passages = ["doc0", "doc1", "doc2"]
    scored = reranker.rank_scored("query string", passages)

    # Descending sort by score
    assert scored == [(1, 0.95), (2, 0.6), (0, 0.3)]

    # Check request call details
    assert len(http_client.calls) == 1
    call = http_client.calls[0]
    expected_url = (
        "https://discoveryengine.googleapis.com/v1alpha/projects/my-proj/"
        "locations/global/rankingConfigurations/default_ranking_config:rank"
    )
    assert call["url"] == expected_url
    assert call["headers"]["Authorization"] == "Bearer fake-token"
    assert call["headers"]["Content-Type"] == "application/json"
    assert call["json"] == {
        "model": "semantic-ranker-512@latest",
        "query": "query string",
        "records": [
            {"id": "0", "content": "doc0"},
            {"id": "1", "content": "doc1"},
            {"id": "2", "content": "doc2"},
        ],
        "topN": 3,
    }


@patch("app.llm.rerank.get_vertex_credentials_and_project")
def test_vertex_rerank_rank_indices_order(mock_auth: MagicMock) -> None:
    mock_creds = SimpleNamespace(token="fake-token")
    mock_auth.return_value = (mock_creds, "default-project")

    payload = {
        "records": [
            {"id": "0", "score": 0.3},
            {"id": "1", "score": 0.95},
            {"id": "2", "score": 0.6},
        ]
    }
    http_client = _FakeHttpClient(payload)
    reranker = VertexRerank(project_id="my-proj", client=http_client)

    indices = reranker.rank("query string", ["doc0", "doc1", "doc2"])
    assert indices == [1, 2, 0]


@patch("app.llm.rerank.get_vertex_credentials_and_project")
def test_vertex_rerank_empty_passages(mock_auth: MagicMock) -> None:
    http_client = _FakeHttpClient({"records": []})
    reranker = VertexRerank(client=http_client)
    assert reranker.rank_scored("query", []) == []
    assert reranker.rank("query", []) == []
    assert http_client.calls == []


@patch("app.llm.rerank.get_vertex_credentials_and_project")
def test_vertex_rerank_error_propagation(mock_auth: MagicMock) -> None:
    mock_creds = SimpleNamespace(token="fake-token")
    mock_auth.return_value = (mock_creds, "default-project")

    http_client = _FakeHttpClient({}, status=500)
    reranker = VertexRerank(client=http_client)

    with pytest.raises(RerankProviderError) as excinfo:
        reranker.rank_scored("query", ["doc0"])
    assert "Vertex AI ranking failed" in str(excinfo.value)
