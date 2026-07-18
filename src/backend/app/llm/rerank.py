from __future__ import annotations

from typing import Any

import httpx

from app.llm.errors import RerankProviderError


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


__all__ = ["OpenRouterRerank", "RerankService"]
