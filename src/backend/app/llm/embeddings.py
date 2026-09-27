from __future__ import annotations

import hashlib
import importlib
import logging
import math
import time
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

from google import genai

from app.llm.errors import EmbeddingProviderError
from app.llm.observability import log_event
from app.llm.vertex_auth import get_vertex_credentials_and_project

logger = logging.getLogger(__name__)


def _safe_log_event(event: str, **fields: object) -> None:
    try:
        log_event(logger, event, **fields)
    except Exception:
        pass


def _load_client_with_observability(
    load_client: Callable[[], Any],
    *,
    provider: str,
    model: str,
    item_count: int,
    dimension: int,
    input_type: str,
) -> Any:
    started = time.perf_counter()
    try:
        return load_client()
    except Exception as exc:
        fields = {
            "provider": provider,
            "model": model,
            "item_count": item_count,
            "dimension": dimension,
            "input_type": input_type,
        }
        _safe_log_event("embedding_call_start", **fields)
        _safe_log_event(
            "embedding_call_error",
            **fields,
            latency_ms=round((time.perf_counter() - started) * 1000),
            exception_type=type(exc).__name__,
        )
        raise


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
        client = _load_client_with_observability(
            self._load_client,
            provider="nvidia",
            model=self.model,
            item_count=len(texts),
            dimension=self.dimension,
            input_type=input_type,
        )
        vectors: list[list[float]] = []
        for start in range(0, len(texts), self.batch_size):
            batch = texts[start : start + self.batch_size]
            started = time.perf_counter()
            _safe_log_event(
                "embedding_call_start",
                provider="nvidia",
                model=self.model,
                item_count=len(batch),
                dimension=self.dimension,
                input_type=input_type,
            )
            try:
                response = client.embeddings.create(
                    model=self.model,
                    input=batch,
                    extra_body={"input_type": input_type, "truncate": "END"},
                )
                batch_vectors = [list(map(float, item.embedding)) for item in response.data]
            except Exception as exc:
                _safe_log_event(
                    "embedding_call_error",
                    provider="nvidia",
                    model=self.model,
                    item_count=len(batch),
                    dimension=self.dimension,
                    input_type=input_type,
                    latency_ms=round((time.perf_counter() - started) * 1000),
                    exception_type=type(exc).__name__,
                )
                raise
            _safe_log_event(
                "embedding_call_success",
                provider="nvidia",
                model=self.model,
                item_count=len(batch),
                dimension=self.dimension,
                input_type=input_type,
                latency_ms=round((time.perf_counter() - started) * 1000),
            )
            vectors.extend(batch_vectors)
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
        if not texts:
            return []
        client = _load_client_with_observability(
            self._load_client,
            provider="openrouter",
            model=self.model,
            item_count=len(texts),
            dimension=self.dimension,
            input_type=input_type,
        )
        vectors: list[list[float]] = []
        for start in range(0, len(texts), self.batch_size):
            batch = texts[start : start + self.batch_size]
            started = time.perf_counter()
            _safe_log_event(
                "embedding_call_start",
                provider="openrouter",
                model=self.model,
                item_count=len(batch),
                dimension=self.dimension,
                input_type=input_type,
            )
            try:
                response = client.embeddings.create(model=self.model, input=batch)
                batch_vectors: list[list[float]] = []
                for item in response.data:
                    vector = [float(v) for v in item.embedding]
                    if len(vector) != self.dimension:
                        raise EmbeddingProviderError(
                            f"Embedding trả về {len(vector)} chiều, cần {self.dimension} chiều."
                        )
                    batch_vectors.append(vector)
            except EmbeddingProviderError as exc:
                _safe_log_event(
                    "embedding_call_error",
                    provider="openrouter",
                    model=self.model,
                    item_count=len(batch),
                    dimension=self.dimension,
                    input_type=input_type,
                    latency_ms=round((time.perf_counter() - started) * 1000),
                    exception_type=type(exc).__name__,
                )
                raise
            except Exception as exc:
                _safe_log_event(
                    "embedding_call_error",
                    provider="openrouter",
                    model=self.model,
                    item_count=len(batch),
                    dimension=self.dimension,
                    input_type=input_type,
                    latency_ms=round((time.perf_counter() - started) * 1000),
                    exception_type=type(exc).__name__,
                )
                raise EmbeddingProviderError() from exc
            _safe_log_event(
                "embedding_call_success",
                provider="openrouter",
                model=self.model,
                item_count=len(batch),
                dimension=self.dimension,
                input_type=input_type,
                latency_ms=round((time.perf_counter() - started) * 1000),
            )
            vectors.extend(batch_vectors)
        return vectors


class VertexEmbedding(EmbeddingService):
    """Google Vertex AI Text Embedding provider via google.genai with vertexai=True."""

    def __init__(
        self,
        *,
        project_id: str | None = None,
        location: str = "us-central1",
        model: str = "text-embedding-004",
        dimension: int = 768,
        batch_size: int = 10,
        client: Any | None = None,
    ) -> None:
        self.project_id = project_id
        self.location = location
        self.model = model
        self.dimension = dimension
        self.batch_size = batch_size
        self._client = client

    def _load_client(self) -> Any:
        if self._client is None:
            creds, resolved_project = get_vertex_credentials_and_project()
            self._client = genai.Client(
                vertexai=True,
                project=self.project_id or resolved_project,
                location=self.location,
                credentials=creds,
            )
        return self._client

    def encode(self, texts: list[str], input_type: str = "passage") -> list[list[float]]:
        if not texts:
            return []
        client = _load_client_with_observability(
            self._load_client,
            provider="vertex",
            model=self.model,
            item_count=len(texts),
            dimension=self.dimension,
            input_type=input_type,
        )
        vectors: list[list[float]] = []
        for start in range(0, len(texts), self.batch_size):
            batch = texts[start : start + self.batch_size]
            started = time.perf_counter()
            _safe_log_event(
                "embedding_call_start",
                provider="vertex",
                model=self.model,
                item_count=len(batch),
                dimension=self.dimension,
                input_type=input_type,
            )
            try:
                response = client.models.embed_content(
                    model=self.model,
                    contents=batch,
                )
                batch_vectors = [[float(v) for v in item.values] for item in response.embeddings]
            except Exception as exc:
                _safe_log_event(
                    "embedding_call_error",
                    provider="vertex",
                    model=self.model,
                    item_count=len(batch),
                    dimension=self.dimension,
                    input_type=input_type,
                    latency_ms=round((time.perf_counter() - started) * 1000),
                    exception_type=type(exc).__name__,
                )
                raise EmbeddingProviderError(f"Vertex AI embedding failed: {exc}") from exc
            _safe_log_event(
                "embedding_call_success",
                provider="vertex",
                model=self.model,
                item_count=len(batch),
                dimension=self.dimension,
                input_type=input_type,
                latency_ms=round((time.perf_counter() - started) * 1000),
            )
            vectors.extend(batch_vectors)
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
