from __future__ import annotations

from typing import Any

import httpx

from app.llm.errors import RerankProviderError
from app.llm.vertex_auth import get_vertex_credentials_and_project


class RerankService:
    """NVIDIA NIM ranking endpoint client.

    Calls the hosted reranker for a (query, passages) pair and returns the
    relevance-sorted indices into the original passage list. Errors propagate
    to the caller, which is expected to fall back to a local ordering.
    """

    def __init__(
        self,
        *,
        api_key: str,
        url: str = "https://ai.api.nvidia.com/v1/retrieval/nvidia/llama-nemotron-rerank-vl-1b-v2/reranking",
        model: str = "nvidia/llama-nemotron-rerank-vl-1b-v2",
        timeout: float = 30.0,
        client: Any | None = None,
    ) -> None:
        self.api_key = api_key
        self.url = url
        self.model = model
        self.timeout = timeout
        self._client = client

    def rank(self, query: str, passages: list[str]) -> list[int]:
        """Return indices of ``passages`` ordered by descending relevance."""
        if not passages:
            return []

        payload = {
            "model": self.model,
            "query": {"text": query},
            "passages": [{"text": passage} for passage in passages],
            "truncate": "END",
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }

        if self._client is not None:
            response = self._client.post(self.url, json=payload, headers=headers)
        else:
            response = httpx.post(
                self.url,
                json=payload,
                headers=headers,
                timeout=self.timeout,
            )
        response.raise_for_status()
        rankings = response.json()["rankings"]
        return [int(item["index"]) for item in rankings]


class OpenRouterRerank:
    """OpenRouter rerank endpoint client (Cohere-style API).

    ``POST {base_url}/rerank`` with ``{model, query, documents}``; the response
    carries ``results: [{index, relevance_score}]``. Any failure raises
    ``RerankProviderError`` — callers must NOT silently fall back while
    OpenRouter is the active tier.
    """

    def __init__(
        self,
        *,
        api_key: str,
        base_url: str = "https://openrouter.ai/api/v1",
        model: str = "cohere/rerank-v3.5",
        timeout: float = 30.0,
        client: Any | None = None,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.timeout = timeout
        self._client = client

    def rank_scored(self, query: str, passages: list[str]) -> list[tuple[int, float]]:
        """Return ``(index, relevance_score)`` pairs ordered by descending relevance.

        The cross-encoder relevance score is the reranker's authoritative signal; callers
        should rank and threshold on it rather than falling back to bi-encoder cosine.
        """
        if not passages:
            return []

        url = f"{self.base_url.rstrip('/')}/rerank"
        payload = {"model": self.model, "query": query, "documents": passages}
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            if self._client is not None:
                response = self._client.post(url, json=payload, headers=headers)
            else:
                response = httpx.post(url, json=payload, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            results = response.json()["results"]
            ordered = sorted(results, key=lambda item: float(item["relevance_score"]), reverse=True)
            return [(int(item["index"]), float(item["relevance_score"])) for item in ordered]
        except Exception as exc:
            raise RerankProviderError() from exc

    def rank(self, query: str, passages: list[str]) -> list[int]:
        """Return indices of ``passages`` ordered by descending relevance."""
        return [idx for idx, _ in self.rank_scored(query, passages)]


class VertexRerank:
    """Google Vertex AI Discovery Engine Ranking API client with gcloud ADC auth."""

    def __init__(
        self,
        *,
        project_id: str | None = None,
        location: str = "global",
        model: str = "semantic-ranker-512@latest",
        timeout: float = 30.0,
        client: Any | None = None,
    ) -> None:
        self.project_id = project_id
        self.location = location
        self.model = model
        self.timeout = timeout
        self._client = client

    def rank_scored(self, query: str, passages: list[str]) -> list[tuple[int, float]]:
        if not passages:
            return []
        creds, resolved_project = get_vertex_credentials_and_project()
        project = self.project_id or resolved_project or "default"

        if creds and hasattr(creds, "token") and not creds.token:
            try:
                import google.auth.transport.requests

                creds.refresh(google.auth.transport.requests.Request())
            except Exception:
                pass

        token = getattr(creds, "token", "") or ""
        url = f"https://discoveryengine.googleapis.com/v1alpha/projects/{project}/locations/{self.location}/rankingConfigurations/default_ranking_config:rank"

        records = [{"id": str(i), "content": p} for i, p in enumerate(passages)]
        payload = {"model": self.model, "query": query, "records": records, "topN": len(passages)}
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        try:
            if self._client is not None:
                resp = self._client.post(url, json=payload, headers=headers)
            else:
                resp = httpx.post(url, json=payload, headers=headers, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            records_resp = data.get("records", [])
            results = []
            for item in records_resp:
                idx = int(item["id"])
                score = float(item.get("score", 0.0))
                results.append((idx, score))
            return sorted(results, key=lambda x: x[1], reverse=True)
        except Exception as exc:
            raise RerankProviderError(f"Vertex AI ranking failed: {exc}") from exc

    def rank(self, query: str, passages: list[str]) -> list[int]:
        return [idx for idx, _ in self.rank_scored(query, passages)]


__all__ = ["OpenRouterRerank", "RerankService", "VertexRerank"]
