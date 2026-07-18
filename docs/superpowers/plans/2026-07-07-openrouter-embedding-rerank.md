# OpenRouter Top-Tier Embedding & Rerank Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make OpenRouter the top-tier provider for embeddings (`openai/text-embedding-3-small`, 1536 dims) and reranking (`cohere/rerank-v3.5`), selected at startup by key presence, with runtime failures surfaced to the frontend as explicit 503/SSE errors instead of silent fallback.

**Architecture:** New `OpenRouterEmbedding` / `OpenRouterRerank` clients in `app/llm/`, wired into the existing construction-time tier factories in `retrieval_service.py`. New `ProviderError` exception family carries user-facing Vietnamese messages, mapped to HTTP 503 by a FastAPI exception handler (the tutor SSE stream already forwards `str(exc)` to the UI, and the frontend already displays `detail`/`message` strings — so no frontend code changes are needed). A destructive alembic migration widens pgvector columns 1024 → 1536, and a new `reindex-embeddings` CLI re-encodes existing content.

**Tech Stack:** FastAPI, SQLAlchemy (async), pgvector, alembic, openai python client (sync), httpx, typer, pytest (`uv run pytest`).

**Spec:** `docs/superpowers/specs/2026-07-07-openrouter-embedding-rerank-design.md`

## Global Constraints

- All backend code under `src/backend/`; run commands from `/Users/admin/Desktop/graduation-thesis/GraduationThesis/src/backend` unless stated otherwise.
- Tests: `uv run pytest tests/unit/<file> -v`; full suite `uv run pytest tests/unit`; lint `uv run ruff check app tests alembic`.
- OpenRouter models (exact strings): embedding `openai/text-embedding-3-small`, rerank `cohere/rerank-v3.5`. Reuse existing `openrouter_api_key` / `openrouter_base_url` settings.
- Embedding dimension: 1536 everywhere the DB is touched (`embedding_dim` setting, migration, factory).
- Rerank API: `POST {base}/rerank` with `{"model", "query", "documents": [str]}` → `{"results": [{"index": int, "relevance_score": float}]}`.
- **No silent runtime fallback** when OpenRouter is the active tier: errors must raise `EmbeddingProviderError` / `RerankProviderError`.
- User-facing error messages are Vietnamese (they are shown verbatim in the UI).
- Do not touch unrelated working-tree changes (`evaluation_report_service.py`, `mock_test_service.py`, `eval_worker.py` have uncommitted edits — leave them alone; commit only files this plan names).
- api/worker/frontend docker images are baked — changes require `docker compose build` (service names: `api`, `worker-eval`, `worker-index`, `worker-ocr`).

---

### Task 1: Provider error types

**Files:**
- Create: `src/backend/app/llm/errors.py`
- Test: `src/backend/tests/unit/test_llm_errors.py`

**Interfaces:**
- Produces: `ProviderError(RuntimeError)` with class attrs `code: str`, `default_message: str`, `__init__(self, message: str | None = None)`; subclasses `EmbeddingProviderError` (`code="embedding_failed"`) and `RerankProviderError` (`code="rerank_failed"`). Later tasks import these from `app.llm.errors`.

- [ ] **Step 1: Write the failing test**

```python
# src/backend/tests/unit/test_llm_errors.py
from __future__ import annotations

import pytest

from app.llm.errors import EmbeddingProviderError, ProviderError, RerankProviderError


def test_embedding_error_defaults() -> None:
    exc = EmbeddingProviderError()
    assert exc.code == "embedding_failed"
    assert "embedding" in str(exc).lower()
    assert isinstance(exc, ProviderError)


def test_rerank_error_defaults() -> None:
    exc = RerankProviderError()
    assert exc.code == "rerank_failed"
    assert isinstance(exc, ProviderError)


def test_custom_message_overrides_default() -> None:
    exc = EmbeddingProviderError("boom")
    assert str(exc) == "boom"


def test_provider_error_is_runtime_error() -> None:
    with pytest.raises(RuntimeError):
        raise RerankProviderError()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/unit/test_llm_errors.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'app.llm.errors'`

- [ ] **Step 3: Write minimal implementation**

```python
# src/backend/app/llm/errors.py
from __future__ import annotations


class ProviderError(RuntimeError):
    """Remote AI-provider failure whose message is safe to show to end users.

    ``str(exc)`` is forwarded verbatim to the UI (SSE error events and HTTP 503
    ``detail``), so messages here are user-facing Vietnamese; technical detail
    belongs on the ``__cause__`` chain and in server logs.
    """

    code: str = "provider_failed"
    default_message: str = "Dịch vụ AI đang gặp sự cố. Vui lòng thử lại sau."

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or self.default_message)


class EmbeddingProviderError(ProviderError):
    code = "embedding_failed"
    default_message = "Dịch vụ embedding đang gặp sự cố. Vui lòng thử lại sau."


class RerankProviderError(ProviderError):
    code = "rerank_failed"
    default_message = "Dịch vụ xếp hạng kết quả (rerank) đang gặp sự cố. Vui lòng thử lại sau."


__all__ = ["EmbeddingProviderError", "ProviderError", "RerankProviderError"]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/unit/test_llm_errors.py -v`
Expected: 4 PASS

- [ ] **Step 5: Commit**

```bash
git add app/llm/errors.py tests/unit/test_llm_errors.py
git commit -m "feat: add user-facing provider error types for embedding/rerank"
```

---

### Task 2: OpenRouterEmbedding client

**Files:**
- Modify: `src/backend/app/llm/embeddings.py` (append class after `NvidiaEmbedding`)
- Modify: `src/backend/app/llm/__init__.py` (export)
- Test: `src/backend/tests/unit/test_openrouter_embedding.py`

**Interfaces:**
- Consumes: `EmbeddingProviderError` from Task 1; existing `EmbeddingService` ABC.
- Produces: `OpenRouterEmbedding(EmbeddingService)` with keyword-only ctor `(api_key, base_url="https://openrouter.ai/api/v1", model="openai/text-embedding-3-small", dimension=1536, batch_size=50, timeout=30.0, client=None)` and `encode(texts, input_type="passage") -> list[list[float]]`. Task 4's factory constructs it.

- [ ] **Step 1: Write the failing test**

```python
# src/backend/tests/unit/test_openrouter_embedding.py
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/unit/test_openrouter_embedding.py -v`
Expected: FAIL — `ImportError: cannot import name 'OpenRouterEmbedding'`

- [ ] **Step 3: Implement**

Append to `src/backend/app/llm/embeddings.py` (after `NvidiaEmbedding`, before `_hash_embedding`), and add the import at the top of the file:

```python
from app.llm.errors import EmbeddingProviderError
```

```python
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
```

In `src/backend/app/llm/__init__.py`: add `OpenRouterEmbedding` to the `from app.llm.embeddings import (...)` block and to `__all__` (keep alphabetical order).

- [ ] **Step 4: Run tests**

Run: `uv run pytest tests/unit/test_openrouter_embedding.py tests/unit/test_llm.py -v`
Expected: all PASS

- [ ] **Step 5: Commit**

```bash
git add app/llm/embeddings.py app/llm/__init__.py tests/unit/test_openrouter_embedding.py
git commit -m "feat: add OpenRouterEmbedding client (text-embedding-3-small, 1536 dims)"
```

---

### Task 3: OpenRouterRerank client

**Files:**
- Modify: `src/backend/app/llm/rerank.py` (append class, extend `__all__`)
- Test: `src/backend/tests/unit/test_openrouter_rerank.py`

**Interfaces:**
- Consumes: `RerankProviderError` from Task 1.
- Produces: `OpenRouterRerank` with keyword-only ctor `(api_key, base_url="https://openrouter.ai/api/v1", model="cohere/rerank-v3.5", timeout=30.0, client=None)` and `rank(query: str, passages: list[str]) -> list[int]` (indices sorted by descending relevance). Task 5 constructs it inside `_rerank`.

- [ ] **Step 1: Write the failing test**

```python
# src/backend/tests/unit/test_openrouter_rerank.py
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/unit/test_openrouter_rerank.py -v`
Expected: FAIL — `ImportError: cannot import name 'OpenRouterRerank'`

- [ ] **Step 3: Implement**

Append to `src/backend/app/llm/rerank.py` (import `RerankProviderError` at top):

```python
from app.llm.errors import RerankProviderError
```

```python
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

    def rank(self, query: str, passages: list[str]) -> list[int]:
        """Return indices of ``passages`` ordered by descending relevance."""
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
            return [int(item["index"]) for item in ordered]
        except Exception as exc:
            raise RerankProviderError() from exc
```

Update the module export list: `__all__ = ["OpenRouterRerank", "RerankService"]`.

- [ ] **Step 4: Run tests**

Run: `uv run pytest tests/unit/test_openrouter_rerank.py -v`
Expected: 4 PASS

- [ ] **Step 5: Commit**

```bash
git add app/llm/rerank.py tests/unit/test_openrouter_rerank.py
git commit -m "feat: add OpenRouterRerank client (cohere/rerank-v3.5)"
```

---

### Task 4: Config fields + embedding tier factory

**Files:**
- Modify: `src/backend/app/config.py` (OpenRouter block ~line 48-51; `embedding_dim` ~line 92)
- Modify: `src/backend/app/services/retrieval_service.py:247-256` (`build_embedding_service`)
- Test: `src/backend/tests/unit/test_retrieval_service.py` (append)

**Interfaces:**
- Consumes: `OpenRouterEmbedding` from Task 2.
- Produces: settings fields `openrouter_embedding_model: str = "openai/text-embedding-3-small"`, `openrouter_rerank_model: str = "cohere/rerank-v3.5"`, `embedding_dim: int = 1536`; `build_embedding_service(settings)` returning OpenRouter → NVIDIA → Deterministic by key presence. Tasks 5/7/9 rely on these names.

- [ ] **Step 1: Write the failing tests** (append to `tests/unit/test_retrieval_service.py`; add imports at top of the file: `from types import SimpleNamespace`, and extend the existing imports with `NvidiaEmbedding, OpenRouterEmbedding` from `app.llm.embeddings` and `build_embedding_service` from `app.services.retrieval_service`)

```python
def _settings(**overrides) -> SimpleNamespace:
    base = dict(
        openrouter_api_key=None,
        openrouter_base_url="https://openrouter.ai/api/v1",
        openrouter_embedding_model="openai/text-embedding-3-small",
        openrouter_rerank_model="cohere/rerank-v3.5",
        nvidia_api_key=None,
        nvidia_base_url="https://integrate.api.nvidia.com/v1",
        nvidia_rerank_base="https://ai.api.nvidia.com/v1/retrieval",
        embedding_model="nvidia/nv-embedqa-e5-v5",
        embedding_dim=1536,
        rerank_model="nvidia/llama-nemotron-rerank-vl-1b-v2",
        rerank_enabled=True,
        tutor_mmr_lambda=0.7,
    )
    base.update(overrides)
    return SimpleNamespace(**base)


def test_build_embedding_service_prefers_openrouter() -> None:
    svc = build_embedding_service(_settings(openrouter_api_key="or-key", nvidia_api_key="nv-key"))
    assert isinstance(svc, OpenRouterEmbedding)
    assert svc.model == "openai/text-embedding-3-small"
    assert svc.dimension == 1536


def test_build_embedding_service_nvidia_when_no_openrouter_key() -> None:
    svc = build_embedding_service(_settings(nvidia_api_key="nv-key"))
    assert isinstance(svc, NvidiaEmbedding)


def test_build_embedding_service_offline_stub_without_keys() -> None:
    svc = build_embedding_service(_settings())
    assert isinstance(svc, DeterministicEmbeddingService)
    assert svc.dimension == 1536
```

- [ ] **Step 2: Run to verify failure**

Run: `uv run pytest tests/unit/test_retrieval_service.py -v`
Expected: new tests FAIL (`ImportError` / `AttributeError: openrouter_embedding_model`); existing tests PASS.

- [ ] **Step 3: Implement**

`src/backend/app/config.py` — extend the OpenRouter block:

```python
    # OpenRouter (openrouter.ai) gateway, OpenAI-compatible
    openrouter_api_key: str | None = None
    openrouter_model: str = "openai/gpt-5.4-mini"
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_embedding_model: str = "openai/text-embedding-3-small"
    openrouter_rerank_model: str = "cohere/rerank-v3.5"
```

and change `embedding_dim: int = 1024` → `embedding_dim: int = 1536` (leave the NVIDIA `embedding_model` line untouched; the NVIDIA tier is only usable after the downgrade migration, as recorded in the spec).

`src/backend/app/services/retrieval_service.py` — update import (line 12) to include `OpenRouterEmbedding`, and replace `build_embedding_service`:

```python
def build_embedding_service(settings: Any) -> EmbeddingService:
    """Return the highest-tier embedder with credentials: OpenRouter → NVIDIA → offline stub."""
    if getattr(settings, "openrouter_api_key", None):
        return OpenRouterEmbedding(
            api_key=settings.openrouter_api_key,
            base_url=settings.openrouter_base_url,
            model=settings.openrouter_embedding_model,
            dimension=settings.embedding_dim,
        )
    if settings.nvidia_api_key:
        return NvidiaEmbedding(
            api_key=settings.nvidia_api_key,
            base_url=settings.nvidia_base_url,
            model=settings.embedding_model,
            dimension=settings.embedding_dim,
        )
    return DeterministicEmbeddingService(settings.embedding_dim)
```

- [ ] **Step 4: Run tests**

Run: `uv run pytest tests/unit/test_retrieval_service.py -v`
Expected: all PASS

- [ ] **Step 5: Commit**

```bash
git add app/config.py app/services/retrieval_service.py tests/unit/test_retrieval_service.py
git commit -m "feat: OpenRouter as top embedding tier; embedding_dim 1536"
```

---

### Task 5: OpenRouter rerank wiring in `_rerank` (no silent fallback)

**Files:**
- Modify: `src/backend/app/services/retrieval_service.py:95-129` (`_rerank`)
- Test: `src/backend/tests/unit/test_retrieval_service.py` (append; import `_rerank` and `RerankProviderError`)

**Interfaces:**
- Consumes: `OpenRouterRerank` (Task 3), `_settings` helper (Task 4).
- Produces: `_rerank(query, candidates, query_vec, settings, k)` behavior: OpenRouter branch raises on failure; NVIDIA/MMR branches unchanged.

- [ ] **Step 1: Write the failing tests** (append to `tests/unit/test_retrieval_service.py`; add `import pytest` usage is already present; add imports `from app.llm.errors import RerankProviderError` and extend the `app.services.retrieval_service` import with `_rerank`)

```python
def test_rerank_uses_openrouter_order(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict = {}

    class FakeRerank:
        def __init__(self, **kwargs) -> None:
            captured["kwargs"] = kwargs

        def rank(self, query: str, passages: list[str]) -> list[int]:
            captured["query"] = query
            return [2, 0, 1]

    monkeypatch.setattr("app.llm.rerank.OpenRouterRerank", FakeRerank)
    candidates = [_make_chunk(0.9), _make_chunk(0.8), _make_chunk(0.7)]

    result = _rerank("q", candidates, [1.0, 0.0], _settings(openrouter_api_key="or-key"), k=2)

    assert [c.id for c in result] == [candidates[2].id, candidates[0].id]
    assert captured["kwargs"]["model"] == "cohere/rerank-v3.5"


def test_rerank_openrouter_error_propagates(monkeypatch: pytest.MonkeyPatch) -> None:
    class FailingRerank:
        def __init__(self, **kwargs) -> None:
            pass

        def rank(self, query: str, passages: list[str]) -> list[int]:
            raise RerankProviderError()

    monkeypatch.setattr("app.llm.rerank.OpenRouterRerank", FailingRerank)

    with pytest.raises(RerankProviderError):
        _rerank("q", [_make_chunk(0.9)], [1.0, 0.0], _settings(openrouter_api_key="or-key"), k=1)


def test_rerank_without_keys_uses_mmr() -> None:
    chunk = _make_chunk(0.9, embedding=[1.0, 0.0])
    result = _rerank("q", [chunk], [1.0, 0.0], _settings(), k=1)
    assert result == [chunk]


def test_rerank_openrouter_disabled_uses_mmr() -> None:
    chunk = _make_chunk(0.9, embedding=[1.0, 0.0])
    result = _rerank("q", [chunk], [1.0, 0.0], _settings(openrouter_api_key="or-key", rerank_enabled=False), k=1)
    assert result == [chunk]
```

- [ ] **Step 2: Run to verify failure**

Run: `uv run pytest tests/unit/test_retrieval_service.py -v`
Expected: `test_rerank_uses_openrouter_order` and `test_rerank_openrouter_error_propagates` FAIL (OpenRouter branch missing → MMR used / no exception raised); others PASS.

- [ ] **Step 3: Implement** — in `_rerank`, insert the OpenRouter branch before the NVIDIA branch and update the docstring:

```python
def _rerank(
    query: str,
    candidates: list[RetrievedChunk],
    query_vec: list[float],
    settings: Any,
    k: int,
) -> list[RetrievedChunk]:
    """Reorder candidates via the top-tier reranker.

    With an OpenRouter key the OpenRouter reranker is authoritative: failures
    raise ``RerankProviderError`` (surfaced to the UI) instead of silently
    falling back, because a silent quality drop is worse than a visible error.
    Without an OpenRouter key the legacy chain applies: NVIDIA reranker when
    configured (errors fall back to local MMR), else local MMR, so offline
    tests and degraded deployments keep working.
    """
    if not candidates:
        return []

    if getattr(settings, "openrouter_api_key", None) and getattr(settings, "rerank_enabled", False):
        import app.llm.rerank as rerank_module

        service = rerank_module.OpenRouterRerank(
            api_key=settings.openrouter_api_key,
            base_url=settings.openrouter_base_url,
            model=settings.openrouter_rerank_model,
        )
        order = service.rank(query, [c.content for c in candidates])
        reranked = [candidates[i] for i in order if 0 <= i < len(candidates)]
        return reranked[:k]

    api_key = getattr(settings, "nvidia_api_key", None)
    if api_key and getattr(settings, "rerank_enabled", False):
        # ... existing NVIDIA branch unchanged ...
```

(The `import app.llm.rerank as rerank_module` + attribute access keeps `monkeypatch.setattr("app.llm.rerank.OpenRouterRerank", ...)` effective.)

- [ ] **Step 4: Run tests**

Run: `uv run pytest tests/unit/test_retrieval_service.py -v`
Expected: all PASS

- [ ] **Step 5: Commit**

```bash
git add app/services/retrieval_service.py tests/unit/test_retrieval_service.py
git commit -m "feat: OpenRouter rerank as top tier with explicit error propagation"
```

---

### Task 6: HTTP 503 exception handlers

**Files:**
- Modify: `src/backend/app/main.py` (inside `create_app`)
- Test: `src/backend/tests/unit/test_provider_error_handler.py`

**Interfaces:**
- Consumes: `ProviderError` family (Task 1).
- Produces: any `ProviderError` raised in a JSON route → `503 {"detail": <user message>, "code": <error code>}` with CORS headers intact. (The tutor SSE stream needs no change — its generator already catches exceptions and emits `{"type": "error", "message": str(exc)}`, which the frontend displays.)

- [ ] **Step 1: Write the failing test**

```python
# src/backend/tests/unit/test_provider_error_handler.py
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
```

- [ ] **Step 2: Run to verify failure**

Run: `uv run pytest tests/unit/test_provider_error_handler.py -v`
Expected: FAIL — status 500, not 503.

- [ ] **Step 3: Implement** — in `src/backend/app/main.py` add imports and register the handler inside `create_app()` after the middleware setup:

```python
from starlette.responses import JSONResponse, Response

from app.llm.errors import ProviderError
```

```python
    @app.exception_handler(ProviderError)
    async def provider_error_handler(request: Request, exc: ProviderError) -> JSONResponse:
        # 503 with a handled body (instead of an unhandled 500) keeps CORS headers,
        # so the browser sees the real message rather than "Failed to fetch".
        _log.error("provider failure %s: %s", exc.code, exc, exc_info=exc)
        return JSONResponse(status_code=503, content={"detail": str(exc), "code": exc.code})
```

- [ ] **Step 4: Run tests**

Run: `uv run pytest tests/unit/test_provider_error_handler.py tests/unit/test_health.py -v`
Expected: all PASS

- [ ] **Step 5: Commit**

```bash
git add app/main.py tests/unit/test_provider_error_handler.py
git commit -m "feat: map provider errors to HTTP 503 with CORS-safe body"
```

---

### Task 7: Document summary embeddings follow the active tier

**Files:**
- Modify: `src/backend/app/services/document_summary_service.py:79-82,129-133`
- Test: `src/backend/tests/unit/test_document_summary_service.py` (append)

**Interfaces:**
- Consumes: retrieval `build_embedding_service` (Task 4).
- Produces: `document_summary_service.build_embedding_service()` default path returns the shared tier factory result; `upsert_document_summary`'s `RuntimeError` fallback sizes vectors from `settings.embedding_dim`. Existing tests keep passing an explicit 1024-dim service and stay valid (no DB involved).

- [ ] **Step 1: Write the failing test** (append; add `from types import SimpleNamespace` and `import app.services.document_summary_service as summary_module` to the test file imports)

```python
def test_default_embedding_service_follows_retrieval_tier(monkeypatch) -> None:
    fake_settings = SimpleNamespace(
        openrouter_api_key=None,
        nvidia_api_key=None,
        embedding_dim=1536,
    )
    monkeypatch.setattr("app.config.get_settings", lambda: fake_settings)

    service = summary_module.build_embedding_service()

    assert isinstance(service, DeterministicEmbeddingService)
    assert service.dimension == 1536
```

- [ ] **Step 2: Run to verify failure**

Run: `uv run pytest tests/unit/test_document_summary_service.py -v`
Expected: new test FAILS — `service.dimension == 1024`.

- [ ] **Step 3: Implement** — in `document_summary_service.py` replace the factory and the fallback:

```python
def build_embedding_service(*, prefer_sentence_transformer: bool = False) -> EmbeddingService:
    if prefer_sentence_transformer:
        return SentenceTransformerEmbedding()
    from app.config import get_settings
    from app.services.retrieval_service import build_embedding_service as build_tiered_embedding_service

    return build_tiered_embedding_service(get_settings())
```

and in `upsert_document_summary` (the `except RuntimeError` fallback, currently line 132-133):

```python
    except RuntimeError:
        from app.config import get_settings

        vector = DeterministicEmbeddingService(get_settings().embedding_dim).encode(
            [payload.overall_summary], input_type="passage"
        )[0]
```

- [ ] **Step 4: Run tests**

Run: `uv run pytest tests/unit/test_document_summary_service.py -v`
Expected: all PASS

- [ ] **Step 5: Commit**

```bash
git add app/services/document_summary_service.py tests/unit/test_document_summary_service.py
git commit -m "fix: size summary embeddings from the active tier (1536-safe)"
```

---

### Task 8: Alembic migration — vector(1024) → vector(1536)

**Files:**
- Create: `src/backend/alembic/versions/20260707_0001_embedding_dim_1536.py`

**Interfaces:**
- Consumes: current head revision `20260702_0001`.
- Produces: schema where `document_chunks.embedding` and `document_summaries.summary_embedding` are `vector(1536)`; embeddings nulled (Task 10 reindexes).

- [ ] **Step 1: Write the migration** (mirror of `20260621_0001_embedding_dim_1024.py`)

```python
"""migrate pgvector embedding columns from 1024 to 1536 dims (openai/text-embedding-3-small)

Revision ID: 20260707_0001
Revises: 20260702_0001
Create Date: 2026-07-07

Destructive: embeddings are nulled (vectors from the old model are unusable in
the new space anyway). Run `python -m app.cli reindex-embeddings` afterwards.
"""

from __future__ import annotations

from alembic import op

revision = "20260707_0001"
down_revision = "20260702_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("DROP INDEX IF EXISTS idx_chunk_embedding_hnsw;")
    op.execute("DROP INDEX IF EXISTS idx_summary_embedding_hnsw;")

    op.execute("ALTER TABLE document_chunks ALTER COLUMN embedding TYPE vector(1536) USING NULL;")
    op.execute("ALTER TABLE document_summaries ALTER COLUMN summary_embedding TYPE vector(1536) USING NULL;")

    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_chunk_embedding_hnsw
            ON document_chunks USING hnsw (embedding vector_cosine_ops)
            WITH (m = 16, ef_construction = 64);
        """
    )
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_summary_embedding_hnsw
            ON document_summaries USING hnsw (summary_embedding vector_cosine_ops)
            WITH (m = 16, ef_construction = 64);
        """
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS idx_chunk_embedding_hnsw;")
    op.execute("DROP INDEX IF EXISTS idx_summary_embedding_hnsw;")

    op.execute("ALTER TABLE document_chunks ALTER COLUMN embedding TYPE vector(1024) USING NULL;")
    op.execute("ALTER TABLE document_summaries ALTER COLUMN summary_embedding TYPE vector(1024) USING NULL;")

    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_chunk_embedding_hnsw
            ON document_chunks USING hnsw (embedding vector_cosine_ops)
            WITH (m = 16, ef_construction = 64);
        """
    )
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_summary_embedding_hnsw
            ON document_summaries USING hnsw (summary_embedding vector_cosine_ops)
            WITH (m = 16, ef_construction = 64);
        """
    )
```

- [ ] **Step 2: Verify the revision graph resolves**

Run: `uv run alembic heads`
Expected: single head `20260707_0001`.

- [ ] **Step 3: Commit**

```bash
git add alembic/versions/20260707_0001_embedding_dim_1536.py
git commit -m "feat: migrate pgvector columns to 1536 dims for text-embedding-3-small"
```

(The migration is *applied* to the live DB in Task 10, inside docker.)

---

### Task 9: `reindex-embeddings` CLI

**Files:**
- Create: `src/backend/app/services/reindex_service.py`
- Modify: `src/backend/app/cli.py`
- Test: `src/backend/tests/unit/test_reindex_service.py`

**Interfaces:**
- Consumes: `build_embedding_service` (Task 4), ORM models `DocumentChunk`, `DocumentSummary`.
- Produces: `async def reindex_embeddings(session, embedding_service, *, batch_size: int = 50) -> tuple[int, int]` (chunks updated, summaries updated); CLI command `python -m app.cli reindex-embeddings`.

- [ ] **Step 1: Write the failing test**

```python
# src/backend/tests/unit/test_reindex_service.py
from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

from sqlalchemy.sql.dml import Update

from app.llm.embeddings import DeterministicEmbeddingService
from app.services.reindex_service import reindex_embeddings


class _FakeResult:
    def __init__(self, rows: list) -> None:
        self._rows = rows

    def all(self) -> list:
        return self._rows


class _FakeSession:
    def __init__(self, chunk_rows: list, summary_rows: list) -> None:
        self._selects = [_FakeResult(chunk_rows), _FakeResult(summary_rows)]
        self.update_count = 0

    async def execute(self, stmt, *args, **kwargs):
        if isinstance(stmt, Update):
            self.update_count += 1
            return _FakeResult([])
        return self._selects.pop(0)


async def test_reindex_updates_all_chunks_and_summaries() -> None:
    chunk_rows = [SimpleNamespace(id=uuid4(), content=f"chunk {i}") for i in range(3)]
    summary_rows = [SimpleNamespace(id=uuid4(), overall_summary="summary text")]
    session = _FakeSession(chunk_rows, summary_rows)

    chunks, summaries = await reindex_embeddings(
        session, DeterministicEmbeddingService(1536), batch_size=2
    )

    assert (chunks, summaries) == (3, 1)
    assert session.update_count == 4


async def test_reindex_empty_database_is_noop() -> None:
    session = _FakeSession([], [])
    assert await reindex_embeddings(session, DeterministicEmbeddingService(1536)) == (0, 0)
    assert session.update_count == 0
```

- [ ] **Step 2: Run to verify failure**

Run: `uv run pytest tests/unit/test_reindex_service.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'app.services.reindex_service'`

- [ ] **Step 3: Implement**

```python
# src/backend/app/services/reindex_service.py
from __future__ import annotations

import asyncio

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.llm.embeddings import EmbeddingService
from app.models import DocumentSummary
from app.models.tables import DocumentChunk


async def reindex_embeddings(
    session: AsyncSession,
    embedding_service: EmbeddingService,
    *,
    batch_size: int = 50,
) -> tuple[int, int]:
    """Re-encode all chunk contents and summary texts with the active embedder.

    Required after switching embedding tiers or migrating the vector column
    dimension — stored vectors from another model are unusable. Returns
    (chunks_updated, summaries_updated). Caller commits.
    """
    chunk_rows = (await session.execute(select(DocumentChunk.id, DocumentChunk.content))).all()
    chunks_updated = 0
    for start in range(0, len(chunk_rows), batch_size):
        batch = chunk_rows[start : start + batch_size]
        vectors = await asyncio.to_thread(
            embedding_service.encode, [row.content for row in batch], "passage"
        )
        for row, vector in zip(batch, vectors, strict=True):
            await session.execute(
                update(DocumentChunk).where(DocumentChunk.id == row.id).values(embedding=vector)
            )
        chunks_updated += len(batch)

    summary_rows = (
        await session.execute(select(DocumentSummary.id, DocumentSummary.overall_summary))
    ).all()
    summaries_updated = 0
    for start in range(0, len(summary_rows), batch_size):
        batch = summary_rows[start : start + batch_size]
        vectors = await asyncio.to_thread(
            embedding_service.encode, [row.overall_summary for row in batch], "passage"
        )
        for row, vector in zip(batch, vectors, strict=True):
            await session.execute(
                update(DocumentSummary)
                .where(DocumentSummary.id == row.id)
                .values(summary_embedding=vector)
            )
        summaries_updated += len(batch)

    return chunks_updated, summaries_updated


__all__ = ["reindex_embeddings"]
```

(If `DocumentSummary` is not exported from `app.models`, import it from its table module the same way `document_summary_service.py` does.)

Add the CLI command to `src/backend/app/cli.py`:

```python
@cli.command()
def reindex_embeddings(
    batch_size: Annotated[int, typer.Option("--batch-size", "-b")] = 50,
) -> None:
    """Re-encode all chunk/summary embeddings with the active embedding tier."""
    chunks, summaries = run(_reindex(batch_size))
    typer.echo(f"Reindexed {chunks} chunks and {summaries} summaries.")


async def _reindex(batch_size: int) -> tuple[int, int]:
    from app.services.reindex_service import reindex_embeddings as run_reindex
    from app.services.retrieval_service import build_embedding_service

    async with AsyncSessionLocal() as session:
        result = await run_reindex(
            session, build_embedding_service(get_settings()), batch_size=batch_size
        )
        await session.commit()
        return result
```

- [ ] **Step 4: Run tests**

Run: `uv run pytest tests/unit/test_reindex_service.py -v && uv run python -m app.cli --help`
Expected: tests PASS; `reindex-embeddings` listed in CLI help.

- [ ] **Step 5: Commit**

```bash
git add app/services/reindex_service.py app/cli.py tests/unit/test_reindex_service.py
git commit -m "feat: add reindex-embeddings CLI for embedding tier switches"
```

---

### Task 10: Full test suite, lint, live verification, docs

**Files:**
- Modify: `.agents/context/REGISTRY.md` (note OpenRouter embedding/rerank tier + reindex CLI)

- [ ] **Step 1: Full unit suite + lint**

Run (from `src/backend`): `uv run pytest tests/unit && uv run ruff check app tests alembic`
Expected: all tests PASS, no lint errors.

- [ ] **Step 2: Confirm the OpenRouter key is configured** (do not print secrets)

Run: `grep -c "^OPENROUTER_API_KEY=." src/backend/.env` (from repo root)
Expected: `1`. If `0`, stop and ask the user for the key.

- [ ] **Step 3: Rebuild baked images and restart**

Run (repo root): `docker compose build api worker-eval worker-index worker-ocr && docker compose up -d api worker-eval worker-index worker-ocr`

- [ ] **Step 4: Apply migration + reindex inside the api container**

```bash
docker compose exec api alembic upgrade head
docker compose exec api python -m app.cli reindex-embeddings
```

Expected: migration applies cleanly; reindex reports N chunks / M summaries (matches row counts).

- [ ] **Step 5: Verify schema and data**

```bash
docker compose exec postgres psql -U postgres -d academic_kb -c "\d document_chunks" | grep embedding
docker compose exec postgres psql -U postgres -d academic_kb -c "SELECT count(*) FILTER (WHERE embedding IS NULL) AS null_vecs, count(*) AS total FROM document_chunks;"
```

Expected: column type `vector(1536)`; `null_vecs = 0` (when the corpus has chunks).

- [ ] **Step 6: End-to-end tutor query**

Ask a course question through the frontend at :3000 (or `POST /api/v1/tutor/query` with a seeded user token) and confirm a cited answer returns; check `docker compose logs api --since 5m` for OpenRouter embedding/rerank calls without errors.

- [ ] **Step 7: Error-path check**

Temporarily set `OPENROUTER_RERANK_MODEL=invalid/model` for the api service (`docker compose up -d api` after env change), send a tutor query, confirm the UI shows the Vietnamese rerank error message (SSE error event / 503 detail), then restore the env and `docker compose up -d api`.

- [ ] **Step 8: Update REGISTRY.md and commit**

```bash
git add .agents/context/REGISTRY.md
git commit -m "docs: registry update for OpenRouter embedding/rerank tier"
```
