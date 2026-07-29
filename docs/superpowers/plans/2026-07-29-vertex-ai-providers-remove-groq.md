# Google Vertex AI Providers Integration & Groq Removal Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the Groq provider across the backend due to output token limits, and integrate Google Vertex AI providers for LLM, VLM, Embedding, and Reranking using the `google.genai` SDK (`vertexai=True`) and Google Cloud CLI / ADC authentication (`google.auth.default()`). Additionally, increase and make configurable the output token budget (`normalization_max_output_tokens=16384`) for document normalization to prevent truncation on large inputs.

**Architecture:** 
1. **Groq Deletion:** Cleanly strip `GroqProvider`, `GroqVisionProvider`, and associated configuration from `app/llm/` and `app/services/document_processing/`.
2. **Document Normalization Token Expansion:** Increase the default output token limit for document processing and normalization from `4096` to `16384` (configurable via `DocumentProcessingConfig.normalization_max_output_tokens`), enabling full-page/multi-slide markdown normalization without truncation.
3. **Vertex AI Authentication:** Centralize ADC / `gcloud auth` resolution using `google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])` so credentials and default Google Cloud project IDs are automatically resolved from the local environment (`gcloud auth application-default login` or `gcloud auth login`).
4. **Vertex AI LLM & VLM:** Build `VertexGeminiProvider` (in `app/llm/providers.py`) and `VertexVisionProvider` (in `app/services/document_processing/providers/vertex.py`) leveraging `genai.Client(vertexai=True, project=..., location=..., credentials=...)`.
5. **Vertex AI Embedding & Reranking:** Build `VertexEmbedding` (in `app/llm/embeddings.py`) via `client.models.embed_content` and `VertexRerank` (in `app/llm/rerank.py`) via Vertex AI Discovery Engine Ranking API REST client powered by gcloud ADC bearer tokens.

**Tech Stack:** Python 3.11, FastAPI, `google-genai>=0.1.0`, `google-auth`, `httpx`, `pytest`.

---

## Global Constraints

- Preserve all existing public signatures and contracts except removing `groq` references.
- All Vertex AI calls MUST support `vertexai=True` and fallback to `google.auth.default()` for gcloud CLI authentication.
- Document processing VLM calls MUST respect configurable `normalization_max_output_tokens` (default `16384`).
- Code edits MUST maintain strict typing (mypy clean) and pass ruff formatting.
- Unit tests must mock external Google Vertex API calls so tests can execute without requiring live GCP credentials.

---

### Task 1: Remove Groq Provider & Expand Document Normalization Output Tokens

**Files:**
- Delete: `src/backend/app/services/document_processing/providers/groq.py`
- Modify: `src/backend/app/config.py`
- Modify: `src/backend/app/llm/providers.py`
- Modify: `src/backend/app/llm/__init__.py`
- Modify: `src/backend/app/llm/router.py`
- Modify: `src/backend/app/llm/optimizer_adapter.py`
- Modify: `src/backend/app/services/document_processing/config.py`
- Modify: `src/backend/app/services/document_processing/providers/__init__.py`
- Modify: `src/backend/app/services/document_processing/pipeline.py`
- Modify: `src/backend/app/services/document_processing/providers/gemini.py`
- Modify: `src/backend/.env.example`
- Test: `src/backend/tests/unit/test_groq_removal.py`

**Interfaces:**
- Consumes: Existing config and LLM router structures.
- Produces: Clean codebase without any `groq` dependencies or settings, with `normalization_max_output_tokens` set to `16384`.

- [ ] **Step 1: Write failing test verifying Groq removal & normalization token limit setting**

```python
# In tests/unit/test_groq_removal.py
import pytest
from app.config import settings
from app.services.document_processing.config import get_doc_processing_config

def test_groq_config_removed_and_token_limit_increased():
    assert not hasattr(settings, "groq_api_key")
    assert "groq" not in settings.llm_provider_order
    doc_cfg = get_doc_processing_config()
    assert doc_cfg.normalization_max_output_tokens == 16384
```

- [ ] **Step 2: Delete `groq.py` provider file and remove imports**

Delete `src/backend/app/services/document_processing/providers/groq.py`.

Modify `src/backend/app/llm/providers.py`: Remove `GroqProvider` class.
Modify `src/backend/app/llm/__init__.py`: Remove `GroqProvider` from exports.
Modify `src/backend/app/llm/router.py`: Remove `GroqProvider` import, `available["groq"]`, and `optimizer_bindings["groq"]`.
Modify `src/backend/app/llm/optimizer_adapter.py`: Remove `GroqClient` imports and bindings.

Modify `src/backend/app/services/document_processing/config.py`:
- Remove `groq_api_key`, `groq_model`, `groq_base_url`.
- Add `normalization_max_output_tokens: int = 16384`.

Modify `src/backend/app/services/document_processing/providers/gemini.py`:
- Update `max_output_tokens` in `GenerateContentConfig` from `4096` to `self._config.normalization_max_output_tokens`.

Modify `src/backend/app/services/document_processing/providers/__init__.py`: Remove `GroqVisionProvider`.
Modify `src/backend/app/services/document_processing/pipeline.py`: Remove `GroqVisionProvider` and `_groq` fallback branch.

- [ ] **Step 3: Clean up settings in `app/config.py` and `.env.example`**

In `src/backend/app/config.py`:
- Remove `groq_api_key` and `groq_model` fields.
- Remove `"groq_api_key"` from `_blank_string_to_none`.
- Update `llm_provider_order` default to `"vertex,bedrock,gemini"`.

In `src/backend/.env.example`:
- Remove `GROQ_API_KEY` and `GROQ_MODEL`.
- Update `LLM_PROVIDER_ORDER=vertex,bedrock,gemini`.
- Add `NORMALIZATION_MAX_OUTPUT_TOKENS=16384`.

- [ ] **Step 4: Run pytest to verify Groq cleanup and token limit setting**

Run: `pytest tests/unit/test_groq_removal.py`
Expected: PASS.

- [ ] **Step 5: Commit Task 1**

```bash
git add src/backend/
git commit -m "refactor: remove Groq provider and expand normalization max output tokens to 16384"
```

---

### Task 2: Vertex AI Authentication & Configuration Helper

**Files:**
- Create: `src/backend/app/llm/vertex_auth.py`
- Modify: `src/backend/app/config.py`
- Modify: `src/backend/.env.example`
- Test: `src/backend/tests/unit/test_vertex_auth.py`

**Interfaces:**
- Consumes: `google.auth.default()`, `settings.vertex_project_id`, `settings.vertex_location`.
- Produces: `get_vertex_credentials_and_project() -> tuple[google.auth.credentials.Credentials | None, str | None]`

- [ ] **Step 1: Write failing test for Vertex AI authentication helper**

```python
# In tests/unit/test_vertex_auth.py
from unittest.mock import patch, MagicMock
from app.llm.vertex_auth import get_vertex_credentials_and_project

def test_get_vertex_credentials_and_project_fallback():
    with patch("google.auth.default") as mock_auth_default:
        mock_creds = MagicMock()
        mock_auth_default.return_value = (mock_creds, "gcloud-project-123")
        creds, project_id = get_vertex_credentials_and_project()
        assert creds == mock_creds
        assert project_id == "gcloud-project-123"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/unit/test_vertex_auth.py`
Expected: FAIL with `ModuleNotFoundError: No module named 'app.llm.vertex_auth'`.

- [ ] **Step 3: Implement `vertex_auth.py` and settings**

Add settings in `src/backend/app/config.py`:
```python
vertex_project_id: str | None = None
vertex_location: str = "us-central1"
vertex_llm_model: str = "gemini-1.5-flash"
vertex_embedding_model: str = "text-embedding-004"
vertex_rerank_model: str = "semantic-ranker-512@latest"
```

Create `src/backend/app/llm/vertex_auth.py`:
```python
from __future__ import annotations
import logging
from typing import Any
import google.auth
from app.config import settings

logger = logging.getLogger(__name__)

def get_vertex_credentials_and_project() -> tuple[Any | None, str | None]:
    """Retrieve Google Cloud credentials and project ID using gcloud CLI / ADC."""
    project_id = settings.vertex_project_id
    credentials = None
    try:
        credentials, default_project = google.auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        if not project_id:
            project_id = default_project
    except Exception as exc:
        logger.warning(f"Could not load Google Cloud ADC credentials: {exc}")
    return credentials, project_id
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/unit/test_vertex_auth.py`
Expected: PASS.

- [ ] **Step 5: Commit Task 2**

```bash
git add src/backend/app/llm/vertex_auth.py src/backend/app/config.py src/backend/tests/unit/test_vertex_auth.py
git commit -m "feat(vertex): add Vertex AI authentication helper with gcloud ADC resolution"
```

---

### Task 3: Implement Google Vertex AI LLM & VLM Providers (`google.genai` client with `vertexai=True`)

**Files:**
- Modify: `src/backend/app/llm/providers.py`
- Modify: `src/backend/app/llm/router.py`
- Modify: `src/backend/app/llm/__init__.py`
- Create: `src/backend/app/services/document_processing/providers/vertex.py`
- Modify: `src/backend/app/services/document_processing/pipeline.py`
- Modify: `src/backend/app/services/document_processing/providers/__init__.py`
- Test: `src/backend/tests/unit/test_vertex_llm_vlm.py`

**Interfaces:**
- Consumes: `google.genai.Client(vertexai=True, project=..., location=..., credentials=...)`.
- Produces: `VertexGeminiProvider` (LLM) and `VertexVisionProvider` (VLM with `normalization_max_output_tokens=16384`).

- [ ] **Step 1: Write unit test for `VertexGeminiProvider` and `VertexVisionProvider`**

```python
# In tests/unit/test_vertex_llm_vlm.py
import pytest
from unittest.mock import MagicMock
from app.llm.providers import VertexGeminiProvider
from app.llm.providers import ChatMessage

@pytest.mark.asyncio
async def test_vertex_gemini_provider_chat():
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "Hello from Vertex Gemini"
    mock_response.usage_metadata = MagicMock(prompt_token_count=10, candidates_token_count=5)
    mock_client.models.generate_content.return_value = mock_response

    provider = VertexGeminiProvider(
        project_id="test-proj",
        location="us-central1",
        model="gemini-1.5-flash",
        client=mock_client,
    )
    result = await provider.chat([ChatMessage(role="user", content="Hi")])
    assert result.content == "Hello from Vertex Gemini"
    assert result.provider == "vertex"
```

- [ ] **Step 2: Implement `VertexGeminiProvider` in `app/llm/providers.py`**

```python
class VertexGeminiProvider(LLMProvider):
    provider_name = "vertex"

    def __init__(
        self,
        *,
        project_id: str | None = None,
        location: str = "us-central1",
        model: str = "gemini-1.5-flash",
        timeout: float = 30.0,
        credentials: Any | None = None,
        client: Any | None = None,
    ) -> None:
        self.model = model
        self.timeout = timeout
        if client is not None:
            self.client = client
        else:
            creds, resolved_project = get_vertex_credentials_and_project()
            self.client = genai.Client(
                vertexai=True,
                project=project_id or resolved_project,
                location=location,
                credentials=credentials or creds,
                http_options=genai_types.HttpOptions(timeout=int(timeout * 1000)),
            )

    async def chat(
        self,
        messages: list[ChatMessage],
        *,
        schema: dict[str, Any] | None = None,
        max_tokens: int | None = None,
    ) -> ProviderResult:
        started = time.perf_counter()
        config: dict[str, Any] = {}
        # Support generous default max output tokens for large LLM turns
        config["max_output_tokens"] = max_tokens if max_tokens is not None else 16384
        if schema is not None:
            config["response_mime_type"] = "application/json"
            config["response_schema"] = schema

        try:
            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model=self.model,
                contents=_messages_to_text(messages),
                config=genai_types.GenerateContentConfig(**config),
            )
        except Exception as exc:
            raise RuntimeError(f"Vertex Gemini client failed: {exc}") from exc

        usage = getattr(response, "usage_metadata", None)
        return ProviderResult(
            content=str(getattr(response, "text", "") or ""),
            tokens_in=int(getattr(usage, "prompt_token_count", 0) or 0),
            tokens_out=int(getattr(usage, "candidates_token_count", 0) or 0),
            latency_ms=_elapsed_ms(started),
            cost_usd=0.0,
            provider="vertex",
            model=self.model,
        )
```

- [ ] **Step 3: Implement `VertexVisionProvider` in `app/services/document_processing/providers/vertex.py`**

Implement VLM document processing provider using `genai.Client(vertexai=True)` with `max_output_tokens=self._config.normalization_max_output_tokens` (16384 tokens) to prevent truncation when generating normalized document markdown.

- [ ] **Step 4: Wire `vertex` into `LLMRouter` and `VisionLanguagePipeline`**

In `app/llm/router.py`:
Add `VertexGeminiProvider` to `available["vertex"]`.

In `app/services/document_processing/pipeline.py`:
Add `VertexVisionProvider` to `_vertex` fallback in `VisionLanguagePipeline`.

- [ ] **Step 5: Run tests for Task 3**

Run: `pytest tests/unit/test_vertex_llm_vlm.py`
Expected: PASS.

- [ ] **Step 6: Commit Task 3**

```bash
git add src/backend/
git commit -m "feat(vertex): implement Vertex AI Gemini LLM and VLM providers using google.genai with 16384 token output limit"
```

---

### Task 4: Implement Google Vertex AI Embedding & Reranking Providers

**Files:**
- Modify: `src/backend/app/llm/embeddings.py`
- Modify: `src/backend/app/llm/rerank.py`
- Modify: `src/backend/app/llm/__init__.py`
- Test: `src/backend/tests/unit/test_vertex_embedding_rerank.py`

**Interfaces:**
- Consumes: `VertexEmbedding(EmbeddingService)`, `VertexRerank`.
- Produces: Vertex AI Embedding & Reranking services.

- [ ] **Step 1: Write test for `VertexEmbedding` and `VertexRerank`**

```python
# In tests/unit/test_vertex_embedding_rerank.py
import pytest
from unittest.mock import MagicMock
from app.llm.embeddings import VertexEmbedding
from app.llm.rerank import VertexRerank

def test_vertex_embedding_encode():
    mock_client = MagicMock()
    mock_emb = MagicMock()
    mock_emb.values = [0.1, 0.2, 0.3]
    mock_res = MagicMock()
    mock_res.embeddings = [mock_emb]
    mock_client.models.embed_content.return_value = mock_res

    service = VertexEmbedding(
        project_id="test-proj",
        location="us-central1",
        model="text-embedding-004",
        dimension=3,
        client=mock_client,
    )
    vecs = service.encode(["hello world"])
    assert vecs == [[0.1, 0.2, 0.3]]
```

- [ ] **Step 2: Implement `VertexEmbedding` in `app/llm/embeddings.py`**

```python
class VertexEmbedding(EmbeddingService):
    """Google Vertex AI Text Embedding provider via google.genai with vertexai=True."""

    def __init__(
        self,
        *,
        project_id: str | None = None,
        location: str = "us-central1",
        model: str = "text-embedding-004",
        dimension: int = 768,
        batch_size: int = 50,
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
        client = self._load_client()
        vectors: list[list[float]] = []
        for start in range(0, len(texts), self.batch_size):
            batch = texts[start : start + self.batch_size]
            try:
                response = client.models.embed_content(
                    model=self.model,
                    contents=batch,
                )
                for item in response.embeddings:
                    vectors.append([float(v) for v in item.values])
            except Exception as exc:
                raise EmbeddingProviderError(f"Vertex AI embedding failed: {exc}") from exc
        return vectors
```

- [ ] **Step 3: Implement `VertexRerank` in `app/llm/rerank.py`**

```python
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
        
        # Ensure fresh OAuth2 access token from gcloud CLI / ADC
        if creds and hasattr(creds, "token") and not creds.token:
            import google.auth.transport.requests
            creds.refresh(google.auth.transport.requests.Request())

        token = getattr(creds, "token", "")
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
```

- [ ] **Step 4: Run tests for Task 4**

Run: `pytest tests/unit/test_vertex_embedding_rerank.py`
Expected: PASS.

- [ ] **Step 5: Commit Task 4**

```bash
git add src/backend/app/llm/embeddings.py src/backend/app/llm/rerank.py src/backend/app/llm/__init__.py src/backend/tests/unit/test_vertex_embedding_rerank.py
git commit -m "feat(vertex): implement Google Vertex AI Embedding and Reranking providers"
```

---

### Task 5: Integration Verification & Documentation Update

**Files:**
- Modify: `.agents/context/REGISTRY.md`
- Modify: `src/backend/README.md`
- Test: `src/backend/tests/unit/`

- [ ] **Step 1: Run full unit test suite**

Run: `pytest tests/unit`
Expected: All unit tests pass.

- [ ] **Step 2: Update REGISTRY.md & README.md**

Update `.agents/context/REGISTRY.md` with the new Google Vertex AI integration details, 16384 normalization output token limit, and removal of Groq provider.

- [ ] **Step 3: Commit Final Task**

```bash
git add .agents/context/REGISTRY.md src/backend/README.md
git commit -m "docs: update registry and documentation for Google Vertex AI providers and Groq removal"
```
