# Academic Knowledge Backend

FastAPI backend for the community academic knowledge management system.
Covers the full document lifecycle: upload → OCR → evaluate → HITL review → chunk/embed → AI features (Tutor, Mindmap, Mock Test).

---

## Quick Start (Docker)

From the repo root:

```bash
docker compose -f src/backend/docker-compose.yml up -d --build
```

Run migrations and seed data after the database is healthy:

```bash
docker compose -f src/backend/docker-compose.yml exec api uv run alembic upgrade head
docker compose -f src/backend/docker-compose.yml exec api uv run python -m app.cli seed
```

Health check:

```bash
curl http://localhost:8000/api/v1/health
```

---

## Development Setup (without Docker)

**Prerequisites**: Python 3.11+, `uv`, a running Postgres + Redis + MinIO (use `docker compose up -d postgres redis minio`).

```bash
cd src/backend
uv sync
```

Copy and edit the root-level env file:

```bash
cp ../../.env.example ../../.env
# edit .env — fill in AZURE_AI_API_KEY and other secrets
```

Run migrations and seed:

```bash
uv run alembic upgrade head
uv run python -m app.cli seed
```

Start the API server:

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Start the worker (separate terminal):

```bash
uv run python -m app.workers.main
```

---

## Project Structure

```
src/backend/
├── app/
│   ├── api/          # FastAPI routers (v1: auth, courses, documents, review, tutor, admin)
│   ├── core/         # State machine, RBAC, audit helpers
│   ├── db/           # SQLAlchemy async engine, session factory
│   ├── llm/          # LLM router (Vertex AI → Bedrock → Gemini), embedding & reranking services
│   ├── models/       # SQLAlchemy ORM models (17 tables)
│   ├── schemas/      # Pydantic v2 request/response contracts
│   ├── services/     # Business logic (document, review, tutor, mindmap, mock test)
│   ├── storage/      # MinIO/R2 S3-compatible adapter, signed URLs
│   ├── workers/      # ARQ async workers (OCR, eval, index)
│   ├── cli.py        # CLI commands: seed, export-openapi
│   ├── config.py     # Settings from env vars via pydantic-settings
│   └── main.py       # FastAPI app factory
├── alembic/          # Database migration scripts
├── tests/
│   ├── unit/         # Fast tests, no external services
│   ├── integration/  # Requires local Docker services (opt-in)
│   └── e2e/          # Full stack happy-path tests (opt-in)
└── docker/
    ├── Dockerfile.api
    └── Dockerfile.worker
```

---

## Running Tests

Unit tests (no external services required):

```bash
cd src/backend
uv run pytest tests/unit
```

Integration tests (requires `docker compose up -d postgres redis minio` first):

```bash
RUN_STORAGE_INTEGRATION=1 uv run pytest tests/integration
```

E2E tests (requires the full stack running):

```bash
RUN_E2E=1 uv run pytest tests/e2e
```

Coverage report:

```bash
uv run pytest --cov=app tests/unit
```

Lint and type checks:

```bash
uv run ruff check app tests alembic
uv run mypy app
```

See `tests/README.md` for the full must-pass test list and FR-ID mapping.

---

## Key Make Targets

The root `Makefile` provides convenience targets (run from the repo root):

```bash
make up          # docker compose up -d --build (full stack)
make down        # docker compose down
make migrate     # alembic upgrade head inside running api container
make seed        # app.cli seed inside running api container
make test        # uv run pytest tests/unit
make lint        # ruff check + mypy
make openapi     # export openapi.yaml to docs/api/openapi.yaml
```

---

## Environment Variables

All configuration is driven by environment variables. Copy `.env.example` at the repo root to `.env` and fill in secrets.

Key variables:

| Variable | Purpose |
|---|---|
| `POSTGRES_HOST` / `POSTGRES_DB` / ... | Database connection |
| `REDIS_URL` | ARQ job queue |
| `STORAGE_ENDPOINT` / `STORAGE_ACCESS_KEY` / ... | MinIO (local) or Cloudflare R2 (cloud) |
| `JWT_SECRET` | Token signing secret |
| `AZURE_AI_API_KEY` | Azure AI Foundry (primary LLM) |
| `AZURE_OPENAI_ENDPOINT` | Azure endpoint URL |
| `AZURE_OPENAI_DEPLOYMENT` | Model deployment name |
| `GEMINI_API_KEY` | Fallback LLM |
| `VERTEX_PROJECT_ID` | Optional Google Cloud project ID for Vertex AI (falls back to gcloud ADC) |
| `VERTEX_LOCATION` | Vertex AI location for embeddings/rerank (default `us-central1`) |
| `VERTEX_GENAI_LOCATION` | Vertex AI location for all generative Gemini calls (default `global`; the Gemini 3 models are served only there) |
| `VERTEX_CHAT_MODEL` / `VERTEX_CHAT_THINKING_LEVEL` | Tutor/chat model (default `gemini-3.8-flash` / `low`) |
| `OCR_VISION_MODEL` / `OCR_VISION_THINKING_LEVEL` | Primary model for scanned-page OCR and figure descriptions (default `gemini-3.5-flash-lite` / `minimal`) |
| `OCR_VISION_FALLBACK_MODEL` / `OCR_VISION_FALLBACK_THINKING_LEVEL` | Fallback vision model, also the first model of the tutor's figure viewer (default `gemini-3.8-flash` / `low`) |
| `DOCUMENT_PROCESSING_MAX_CONCURRENCY` | Concurrent VLM calls per document (default `16`) |
| `DOCUMENT_PROCESSING_GLOBAL_CONCURRENCY` | Process-wide cap on concurrent VLM calls across OCR jobs (default `32`) |
| `DOCUMENT_PROCESSING_REQUEST_TIMEOUT_SECONDS` | Per-call Vertex timeout before falling back to the next provider (default `60`) |
| `VERTEX_EMBEDDING_MODEL` | Vertex AI Text Embedding model (default `text-embedding-004`) |
| `VERTEX_RERANK_MODEL` | Vertex AI Discovery Engine Rerank model (default `semantic-ranker-512@latest`) |
| `EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` |
| `EMBEDDING_DIM` | `384` |

`*_THINKING_LEVEL` applies to Gemini 3 models only: set it to an empty value when the matching model
setting points at a non-Gemini-3 model (Gemini 2.5 models reject `thinking_level`).

See `.env.example` at the repo root for the full list and local-dev defaults.

---

## Architecture Notes

The backend was built incrementally across five phases:

- **Phase A** — Foundation: FastAPI scaffold, Docker local stack (Postgres + Redis + MinIO), SQLAlchemy ORM (17 tables, pgvector), S3-compatible storage adapter, JWT/RBAC auth, document state machine, audit logging, Pydantic contracts from JSON schemas, seed loader, OpenAPI export, LLM/embedding router.

- **Phase B** — Domain APIs: upload endpoint (file validation, state transition to `UPLOADED`), course management, user/reviewer management, document listing with filters, admin audit log endpoint.

- **Phase C** — Worker Pipeline: OCR worker wrapping the document-processing experiment, Agent 1–3 evaluation pipeline (summary → duplicate detection → priority rules), ARQ queue with OCR/eval/index queue names and duplicate-job rejection.

- **Phase D** — HITL and AI Features: review queue routing, reviewer assignment, mandatory notes on overrides, chunking/embedding on approval → `INDEXED`, Tutor RAG endpoint (MMR retrieval + tier boost + citation), Mindmap and Mock Test generation endpoints.

- **Phase E** — Hardening: signed URL TTL enforcement, concurrency guard (one active job per document), integration and E2E tests, Azure deployment configuration.

---

## API Documentation

Interactive OpenAPI docs are available at `/docs` (Swagger UI) and `/redoc` when the server is running:

```
http://localhost:8000/docs
http://localhost:8000/redoc
```

Export the OpenAPI spec to a static file:

```bash
cd src/backend
uv run python -m app.cli export-openapi --output ../../docs/api/openapi.yaml
```

The exported file at `docs/api/openapi.yaml` is the canonical contract for frontend integration.
