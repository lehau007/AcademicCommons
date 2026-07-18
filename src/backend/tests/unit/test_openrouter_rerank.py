from __future__ import annotations

import pytest

from app.llm.errors import RerankProviderError
from app.llm.rerank import OpenRouterRerank


class _FakeResponse:
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

    def post(self, url: str, json: dict | None = None, headers: dict | None = None) -> _FakeResponse:
        self.calls.append({"url": url, "json": json, "headers": headers})
        return _FakeResponse(self._payload, self._status)


def test_rank_returns_indices_sorted_by_relevance() -> None:
    payload = {
        "results": [
            {"index": 1, "relevance_score": 0.2},
            {"index": 2, "relevance_score": 0.9},
            {"index": 0, "relevance_score": 0.5},
        ]
    }
    client = _FakeHttpClient(payload)
    service = OpenRouterRerank(api_key="test-key", client=client)

    order = service.rank("question", ["p0", "p1", "p2"])

    assert order == [2, 0, 1]
    call = client.calls[0]
    assert call["url"] == "https://openrouter.ai/api/v1/rerank"
    assert call["json"] == {"model": "cohere/rerank-v3.5", "query": "question", "documents": ["p0", "p1", "p2"]}
    assert call["headers"]["Authorization"] == "Bearer test-key"


def test_rank_scored_returns_index_score_pairs_sorted() -> None:
    payload = {
        "results": [
            {"index": 1, "relevance_score": 0.2},
            {"index": 2, "relevance_score": 0.9},
            {"index": 0, "relevance_score": 0.5},
        ]
    }
    service = OpenRouterRerank(api_key="test-key", client=_FakeHttpClient(payload))

    scored = service.rank_scored("question", ["p0", "p1", "p2"])

    assert scored == [(2, 0.9), (0, 0.5), (1, 0.2)]


def test_rank_empty_passages_short_circuits() -> None:
    client = _FakeHttpClient({"results": []})
    assert OpenRouterRerank(api_key="k", client=client).rank("q", []) == []
    assert client.calls == []


def test_rank_http_error_wrapped() -> None:
    client = _FakeHttpClient({}, status=500)
    with pytest.raises(RerankProviderError):
        OpenRouterRerank(api_key="k", client=client).rank("q", ["p0"])


def test_rank_malformed_response_wrapped() -> None:
    client = _FakeHttpClient({"unexpected": True})
    with pytest.raises(RerankProviderError):
        OpenRouterRerank(api_key="k", client=client).rank("q", ["p0"])
