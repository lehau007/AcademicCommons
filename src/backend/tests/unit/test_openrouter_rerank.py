from __future__ import annotations

import pytest

from app.llm.errors import RerankProviderError
from app.llm.rerank import OpenRouterRerank, RerankService


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


def test_rank_scored_logs_metadata_only(caplog) -> None:
    payload = {"results": [{"index": 1, "relevance_score": 0.8}, {"index": 0, "relevance_score": 0.3}]}
    service = OpenRouterRerank(api_key="test-key", client=_FakeHttpClient(payload))

    with caplog.at_level("INFO", logger="app.llm.rerank"):
        scored = service.rank_scored("DO_NOT_LOG_QUERY", ["DO_NOT_LOG_P0", "DO_NOT_LOG_P1"])

    assert scored == [(1, 0.8), (0, 0.3)]
    combined = "\n".join(caplog.messages)
    assert "event=rerank_call_start" in combined
    assert "event=rerank_call_success" in combined
    assert "provider=openrouter" in combined
    assert "model=cohere/rerank-v3.5" in combined
    assert "item_count=2" in combined
    assert "latency_ms=" in combined
    assert "DO_NOT_LOG_QUERY" not in combined
    assert "DO_NOT_LOG_P0" not in combined


def test_rank_http_error_logs_metadata_only(caplog) -> None:
    client = _FakeHttpClient({}, status=500)

    with pytest.raises(RerankProviderError):
        with caplog.at_level("INFO", logger="app.llm.rerank"):
            OpenRouterRerank(api_key="k", client=client).rank("DO_NOT_LOG_QUERY", ["DO_NOT_LOG_P0"])

    combined = "\n".join(caplog.messages)
    assert "event=rerank_call_start" in combined
    assert "event=rerank_call_error" in combined
    assert "provider=openrouter" in combined
    assert "exception_type=RuntimeError" in combined
    assert "latency_ms=" in combined
    assert "DO_NOT_LOG_QUERY" not in combined
    assert "DO_NOT_LOG_P0" not in combined


def test_nvidia_rank_logs_metadata_only(caplog) -> None:
    payload = {"rankings": [{"index": 2}, {"index": 0}, {"index": 1}]}
    client = _FakeHttpClient(payload)
    service = RerankService(api_key="test-key", client=client)

    with caplog.at_level("INFO", logger="app.llm.rerank"):
        order = service.rank("DO_NOT_LOG_QUERY", ["DO_NOT_LOG_P0", "DO_NOT_LOG_P1", "DO_NOT_LOG_P2"])

    assert order == [2, 0, 1]
    combined = "\n".join(caplog.messages)
    assert "event=rerank_call_start" in combined
    assert "event=rerank_call_success" in combined
    assert "provider=nvidia" in combined
    assert "model=nvidia/llama-nemotron-rerank-vl-1b-v2" in combined
    assert "item_count=3" in combined
    assert "latency_ms=" in combined
    assert "DO_NOT_LOG_QUERY" not in combined
    assert "DO_NOT_LOG_P0" not in combined


def test_nvidia_rank_http_error_logs_and_preserves_exception(caplog) -> None:
    client = _FakeHttpClient({}, status=500)
    service = RerankService(api_key="test-key", client=client)

    with pytest.raises(RuntimeError, match="HTTP 500"):
        with caplog.at_level("INFO", logger="app.llm.rerank"):
            service.rank("DO_NOT_LOG_QUERY", ["DO_NOT_LOG_PASSAGE"])

    combined = "\n".join(caplog.messages)
    assert "event=rerank_call_start" in combined
    assert "event=rerank_call_error" in combined
    assert "provider=nvidia" in combined
    assert "exception_type=RuntimeError" in combined
    assert "latency_ms=" in combined
    assert "DO_NOT_LOG_QUERY" not in combined
    assert "DO_NOT_LOG_PASSAGE" not in combined
