from __future__ import annotations

from fastapi.testclient import TestClient

from app.llm.errors import EmbeddingProviderError, RerankProviderError
from app.main import create_app


def _client_with_failing_routes() -> TestClient:
    app = create_app()

    @app.get("/boom-embedding")
    async def boom_embedding() -> None:
        raise EmbeddingProviderError()

    @app.get("/boom-rerank")
    async def boom_rerank() -> None:
        raise RerankProviderError()

    return TestClient(app, raise_server_exceptions=False)


def test_embedding_error_maps_to_503_with_cors() -> None:
    client = _client_with_failing_routes()
    res = client.get("/boom-embedding", headers={"Origin": "http://localhost:3000"})
    assert res.status_code == 503
    body = res.json()
    assert body["code"] == "embedding_failed"
    assert "embedding" in body["detail"].lower()
    assert res.headers.get("access-control-allow-origin") == "http://localhost:3000"


def test_rerank_error_maps_to_503() -> None:
    client = _client_with_failing_routes()
    res = client.get("/boom-rerank")
    assert res.status_code == 503
    assert res.json()["code"] == "rerank_failed"
