# OpenRouter Embedding & Rerank — Top-Tier Provider Design

**Date:** 2026-07-07
**Status:** Approved (design discussion in session)

## Goal

Make OpenRouter the top-tier provider for both **embeddings** and **reranking** in the backend RAG stack, reusing the existing `openrouter_api_key` / `openrouter_base_url` already used by the LLM service. NVIDIA and local remain available as lower-tier options selected at construction time. When the active OpenRouter provider fails at runtime, the error is surfaced to the frontend as an explicit embed/rerank error — **no silent fallback**.

## Provider tiers (selected at startup, by key presence)

| Tier | Embedding | Rerank |
|---|---|---|
| 1 (top) | OpenRouter `openai/text-embedding-3-small` (1536 dims) | OpenRouter `cohere/rerank-v3.5` |
| 2 | NVIDIA `nv-embedqa-e5-v5` (1024 dims) | NVIDIA `llama-nemotron-rerank-vl-1b-v2` → MMR on error (unchanged) |
| 3 | Deterministic stub (offline/tests) | Local MMR |

Selection is **construction-time only** (in `build_embedding_service` / `_rerank`): embedding vectors from different models live in different spaces, so per-call runtime fallback would silently corrupt retrieval. Switching tiers requires re-indexing the corpus.

## API contracts (verified 2026-07-07)

- **Embeddings:** `POST {openrouter_base_url}/embeddings` — OpenAI-compatible (`model`, `input`); response `data[].embedding`.
- **Rerank:** `POST {openrouter_base_url}/rerank` — Cohere-style: request `{model, query, documents: [str]}`, response `{results: [{index, relevance_score}]}` sorted by descending relevance.

## Changes

### 1. Config (`src/backend/app/config.py`)
- `openrouter_embedding_model: str = "openai/text-embedding-3-small"`
- `openrouter_rerank_model: str = "cohere/rerank-v3.5"`
- `embedding_dim: int` default `1024` → `1536`

### 2. DB migration (`src/backend/alembic/versions/`)
New revision following the `20260621_0001` pattern: drop HNSW indexes, alter `document_chunks.embedding` and `document_summaries.summary_embedding` to `vector(1536) USING NULL`, recreate HNSW indexes. Downgrade restores `vector(1024)`. Destructive: existing embeddings are nulled; re-index required. Note: while the column is 1536, the NVIDIA tier (1024) cannot write to it — reverting to NVIDIA requires the downgrade migration + re-index.

### 3. Embedding client (`src/backend/app/llm/embeddings.py`)
`OpenRouterEmbedding(EmbeddingService)` — mirrors `NvidiaEmbedding` (sync OpenAI client, batching), but: no `input_type` extra body (text-embedding-3 is symmetric; parameter accepted and ignored), `dimension=1536`. Validates each returned vector length equals `dimension`; wraps API/validation failures in `EmbeddingProviderError`.

### 4. Rerank client (`src/backend/app/llm/rerank.py`)
`OpenRouterRerank` — `POST {base}/rerank` via httpx (same injection-friendly `client` pattern as `RerankService`), parses `results[].index`. Wraps failures in `RerankProviderError`.

### 5. Errors (`src/backend/app/llm/errors.py`, new)
`EmbeddingProviderError` and `RerankProviderError` (both subclass a common `ProviderError`).

### 6. Wiring (`src/backend/app/services/retrieval_service.py`)
- `build_embedding_service`: `openrouter_api_key` → `OpenRouterEmbedding`; elif `nvidia_api_key` → `NvidiaEmbedding`; else `DeterministicEmbeddingService`. (Index/eval workers and retrieval all share this factory, so index and query stay consistent.)
- `_rerank`: if `openrouter_api_key` and `rerank_enabled` → `OpenRouterRerank`; **errors propagate** (no MMR fallback). Elif `nvidia_api_key` → existing NVIDIA-then-MMR behavior, unchanged. Else MMR.

### 7. HTTP error surfacing (`src/backend/app/main.py` + tutor/retrieval call sites)
FastAPI exception handlers map `EmbeddingProviderError` → `503 {"detail": "embedding_failed"}` and `RerankProviderError` → `503 {"detail": "rerank_failed"}`. A handled response (not an unhandled 500) keeps CORS headers so the browser sees the real error instead of "Failed to fetch".

### 8. Frontend (`src/frontend`)
Tutor chat (and any surface calling retrieval-backed endpoints, e.g. mock test generation) detects 503 with `embedding_failed` / `rerank_failed` and shows a user-facing message (e.g. "Dịch vụ embedding/rerank đang lỗi, vui lòng thử lại sau") instead of a generic failure.

### 9. Document summary embeddings (`src/backend/app/services/document_summary_service.py`)
`upsert_document_summary` currently instantiates `DeterministicEmbeddingService()` with the default 1024 dims, which would fail against the 1536 column. It (and its `RuntimeError` fallback path) must size vectors from `settings.embedding_dim` — preferably by reusing the shared retrieval `build_embedding_service(settings)` so summary embeddings live in the same space as chunk embeddings.

### 10. Re-index command (`src/backend/app/cli.py`)
`reindex-embeddings`: for all existing `document_chunks` (and `document_summaries.summary_embedding` where applicable), re-encode stored `content` with the active embedding service and update the vector in place. Needed once after migrating, and any time the embedding tier changes. Batch to respect provider limits.

## Out of scope
- LLM-based reranking.
- Runtime cross-model fallback.
- Changes to `document_summary_service`'s summarization logic (only its embedding dimension handling changes, per §9).

## Testing
- Unit: `OpenRouterEmbedding` (batching, dimension validation, error wrapping) and `OpenRouterRerank` (payload shape, result parsing, error wrapping) with injected fake clients; `build_embedding_service` tier selection; `_rerank` provider selection and error propagation; exception-handler status codes.
- Live verification (docker stack with real key): embeddings return 1536-dim vectors; rerank returns a valid ordering; tutor query end-to-end; forced failure (bad model name) shows the error in the UI.
