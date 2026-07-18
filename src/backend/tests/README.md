# Backend Tests

Unit, integration, and E2E tests for the Academic Knowledge backend.
All commands assume you are in `src/backend/`.

---

## Running Tests

### Unit tests (no external services)

```bash
uv run pytest tests/unit
```

### Integration tests (requires local Docker services)

Start services first:

```bash
docker compose up -d postgres redis minio
uv run alembic upgrade head
uv run python -m app.cli seed
```

Then run:

```bash
RUN_STORAGE_INTEGRATION=1 uv run pytest tests/integration
```

### E2E tests (requires full stack)

```bash
RUN_E2E=1 uv run pytest tests/e2e
```

### Coverage report

```bash
uv run pytest --cov=app tests/unit
```

### Run a subset by keyword

```bash
uv run pytest -k "test_state_machine"
uv run pytest -k "test_auth or test_rbac"
uv run pytest -k "ocr"
```

### Run a specific test file

```bash
uv run pytest tests/unit/test_state_machine.py
uv run pytest tests/integration/test_storage_minio.py
```

---

## Must-Pass Test List

The following tests must pass before any deployment or PR merge. FR-IDs reference the SRS (`docs/SRS.md`).

### Phase A — Foundation

| Area | Test | Notes |
|---|---|---|
| Auth/RBAC | `test_401_without_token` | All protected endpoints |
| Auth/RBAC | `test_401_invalid_token` | |
| Auth/RBAC | `test_403_wrong_role` | Student accessing admin endpoint |
| Auth/RBAC | `test_200_with_valid_token` | |
| State machine | `test_allowed_transition_truth_table` | All valid transitions |
| State machine | `test_invalid_transition_no_mutation` | Rejected transitions must not change state |
| State machine | `test_actor_policy` | Each transition requires the correct actor role |
| State machine | `test_state_audit_log_written` | Transition writes to `document_state_logs` |
| ORM metadata | `test_17_tables_present` | Schema has exactly 17 tables |
| ORM metadata | `test_vector_columns_use_embedding_dimension` | pgvector column is vector(1024) |
| ORM metadata | `test_partial_latest_indexes` | Partial indexes on `is_latest=true` exist |
| Seed loader | `test_seed_27_courses` | 27 courses loaded |
| Seed loader | `test_seed_6_users` | 6 users loaded |
| Seed loader | `test_seed_3_assignments` | 3 active reviewer assignments loaded |
| Seed loader | `test_seed_deterministic_uuids` | Re-run produces same UUIDs (idempotent) |
| Storage | `test_key_layout` | Storage key format matches spec |
| Storage | `test_s3_bucket_bootstrap` | Bucket created if not exists |
| Storage | `test_put_get_roundtrip` | Upload + download produces same bytes |
| LLM router | `test_provider_request_shapes` | Azure/Gemini/Groq request formats |
| LLM router | `test_router_fallback_on_failure` | Falls back to Gemini when Azure fails |
| LLM router | `test_router_all_fail` | Raises after all providers fail |
| Embedding | `test_deterministic_embedding_returns_1024_dimensional_vectors` | Embedding vector has 1024 dimensions |
| Health | `test_health_ok_without_services` | `/api/v1/health` returns 200 even when DB/Redis/MinIO are down |

### Phase B — Domain APIs

| FR | Test |
|---|---|
| FR-UP-02 | `test_official_uniqueness_archives_previous` — uploading a new official doc marks the previous revision `is_latest=false` |
| FR-UP-07 | `test_reject_encrypted_pdf` — upload returns 422 for password-protected PDFs |
| FR-UP-07 | `test_reject_video` — upload returns 422 for video file MIME types |

### Phase C — Worker Pipeline

| FR | Test |
|---|---|
| FR-PP-06 | `test_ocr_idempotency` — re-queuing a completed OCR job does not create a duplicate job |
| FR-PP-07 | `test_ocr_retry_3_times_then_fail` — OCR worker retries 3 times then marks document `FAILED` |
| FR-EP-05 | `test_build_agent1_output_detects_duplicate_and_cold_start_reason` — Legacy Agent 1 embedding comparison flags documents with cosine similarity >= 0.92 as duplicates |
| FR-EP-05 | `test_build_agent1_output_with_precalculated_duplicate` — Agent 1 supports precalculated duplicate flag and similarity from Chunk-Level Set Matching |
| FR-EP-14 | `test_agent3_priority_rules_table_driven` — Agent 3 applies all priority rules from the spec; parameterized with table-driven cases |
| FR-CM-04 Level 1 | `test_upload_community_blocked_when_no_seed` — community upload blocked if the course has no approved seed document |
| FR-CM-04 Level 2 | `test_agent1_cold_start_under_3_approved` — Agent 1 skips similarity check and recommends APPROVE when fewer than 3 approved docs exist for the course |

### Phase D — HITL and AI Features

| FR | Test |
|---|---|
| FR-HR-02 | `test_review_queue_routing_with_no_reviewer` — document routed to admin queue when no reviewer is assigned to the course |
| FR-HR-06 | `test_mandatory_note_on_override` — reviewer override (approve after reject or reject after approve) returns 422 if `note` field is empty |
| FR-CI-02 | `test_namespace_routing_by_final_contribution_type` — chunks indexed into `official` or `community` namespace based on final contribution type |
| FR-CI-05 | `test_chunking_idempotency` — re-indexing an already-indexed document does not create duplicate chunks in pgvector |
| FR-VT-04 | `test_official_tier_boost_in_retrieval` — official-namespace chunks receive the `TUTOR_TIER_BOOST` score multiplier vs community chunks |
| FR-VT-06 | `test_tutor_citation_chunk_id_valid` — every chunk_id in the tutor response exists in the `chunks` table |
| FR-CV-04 | `test_ai_scores_not_in_public_ranking` — AI evaluation scores (Agent 1–3) are excluded from the public document ranking endpoint |
| FR-AD-03 | `test_admin_reprocess_failed_doc` — admin can trigger reprocessing of a `FAILED` document; state transitions to `PROCESSING` and a new job is queued |

### Phase E — Hardening

| NFR | Test |
|---|---|
| NFR-SEC-03 | `test_signed_url_ttl_15min` — signed URLs expire after 15 minutes; a request after 15 min returns 403 |
| NFR-REL-04 | `test_concurrency_guard_one_job_per_doc` — submitting a second OCR job for a document that already has an active job returns a conflict error (no duplicate job created) |

---

## Integration Test Details

The storage integration test uploads a 5 MB PDF-like payload to MinIO, fetches it through a signed URL, and verifies the SHA256 hash end-to-end.

The database integration tests run full Alembic migrations against a real Postgres container and verify the ORM metadata expectations (17 tables, vector(1024) column, partial indexes).

---

## E2E Test

The E2E happy-path test covers the full document lifecycle:

1. Admin creates a course and assigns a reviewer.
2. Student uploads a PDF (`summary_note` type).
3. OCR + eval pipeline runs and document reaches `PENDING_REVIEW`.
4. Reviewer approves; document transitions to `INDEXED`.
5. `/api/v1/tutor/query` returns an answer with a `chunk_id` that exists in the `chunks` table and whose `excerpt` matches content from the original file.

Run it with:

```bash
RUN_E2E=1 uv run pytest tests/e2e -v
```

The E2E test requires the full stack (`docker compose up -d --build`) with migrations and seed already applied.
