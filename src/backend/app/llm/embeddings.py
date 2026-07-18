from __future__ import annotations

import hashlib
import importlib
import math
from abc import ABC, abstractmethod
from typing import Any

from app.llm.errors import EmbeddingProviderError


class EmbeddingService(ABC):
    dimension: int

    @abstractmethod
    def encode(self, texts: list[str], input_type: str = "passage") -> list[list[float]]:
        raise NotImplementedError


class DeterministicEmbeddingService(EmbeddingService):
    def __init__(self, dimension: int = 1024) -> None:
        self.dimension = dimension

    def encode(self, texts: list[str], input_type: str = "passage") -> list[list[float]]:
        del input_type
        return [_hash_embedding(text, self.dimension) for text in texts]


class SentenceTransformerEmbedding(EmbeddingService):
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2", dimension: int = 384) -> None:
        self.model_name = model_name
        self.dimension = dimension
        self._model: Any | None = None

    def encode(self, texts: list[str], input_type: str = "passage") -> list[list[float]]:
        del input_type
        model = self._load_model()
        vectors = model.encode(texts, normalize_embeddings=True)
        return [list(map(float, vector)) for vector in vectors]

    def _load_model(self) -> Any:
        if self._model is None:
            try:
                sentence_transformers = importlib.import_module("sentence_transformers")
            except ImportError as exc:
                raise RuntimeError(
                    "sentence-transformers is required for SentenceTransformerEmbedding; "
                    "use DeterministicEmbeddingService in tests."
                ) from exc
            sentence_transformer = sentence_transformers.SentenceTransformer
            self._model = sentence_transformer(self.model_name)
        return self._model


class NvidiaEmbedding(EmbeddingService):
    """NVIDIA NIM hosted embeddings (asymmetric QA model).

    Uses the synchronous OpenAI client so it satisfies the sync ``encode``
    interface. ``input_type`` must be ``"query"`` for search queries and
    ``"passage"`` for documents/chunks being indexed.
    """

    def __init__(
        self,
        *,
        api_key: str,
        base_url: str = "https://integrate.api.nvidia.com/v1",
        model: str = "nvidia/nv-embedqa-e5-v5",
        dimension: int = 1024,
        batch_size: int = 50,
        timeout: float = 30.0,
        client: Any | None = None,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.dimension = dimension
        self.batch_size = batch_size
        self.timeout = timeout
        self._client = client

    def _load_client(self) -> Any:
        if self._client is None:
            from openai import OpenAI

            self._client = OpenAI(api_key=self.api_key, base_url=self.base_url, timeout=self.timeout)
        return self._client

    def encode(self, texts: list[str], input_type: str = "passage") -> list[list[float]]:
        if not texts:
            return []
        client = self._load_client()
        vectors: list[list[float]] = []
        for start in range(0, len(texts), self.batch_size):
            batch = texts[start : start + self.batch_size]
            response = client.embeddings.create(
                model=self.model,
                input=batch,
                extra_body={"input_type": input_type, "truncate": "END"},
            )
            vectors.extend([list(map(float, item.embedding)) for item in response.data])
        return vectors


class OpenRouterEmbedding(EmbeddingService):
    """OpenRouter-hosted embeddings via the OpenAI-compatible /embeddings endpoint.

    text-embedding-3 models are symmetric, so ``input_type`` is accepted for
    interface compatibility and ignored. Failures raise ``EmbeddingProviderError``
    so callers surface them to the UI instead of silently falling back.
    """

    def __init__(
        self,
        *,
        api_key: str,
        base_url: str = "https://openrouter.ai/api/v1",
        model: str = "openai/text-embedding-3-small",
        dimension: int = 1536,
        batch_size: int = 50,
        timeout: float = 30.0,
        client: Any | None = None,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.dimension = dimension
        self.batch_size = batch_size
        self.timeout = timeout
        self._client = client

    def _load_client(self) -> Any:
        if self._client is None:
            from openai import OpenAI

            self._client = OpenAI(api_key=self.api_key, base_url=self.base_url, timeout=self.timeout)
        return self._client

    def encode(self, texts: list[str], input_type: str = "passage") -> list[list[float]]:
        del input_type
        if not texts:
            return []
        client = self._load_client()
        vectors: list[list[float]] = []
        for start in range(0, len(texts), self.batch_size):
            batch = texts[start : start + self.batch_size]
            try:
                response = client.embeddings.create(model=self.model, input=batch)
            except Exception as exc:
                raise EmbeddingProviderError() from exc
            for item in response.data:
                vector = [float(v) for v in item.embedding]
                if len(vector) != self.dimension:
                    raise EmbeddingProviderError(
                        f"Embedding trả về {len(vector)} chiều, cần {self.dimension} chiều."
                    )
                vectors.append(vector)
        return vectors


def _hash_embedding(text: str, dimension: int) -> list[float]:
    values: list[float] = []
    counter = 0
    while len(values) < dimension:
        digest = hashlib.sha256(f"{counter}:{text}".encode()).digest()
        values.extend((byte / 127.5) - 1.0 for byte in digest)
        counter += 1
    vector = values[:dimension]
    norm = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [value / norm for value in vector]
