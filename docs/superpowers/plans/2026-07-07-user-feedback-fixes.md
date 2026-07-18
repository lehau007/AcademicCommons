# User Feedback Fixes (2026-07-07 report) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix the confirmed P0/P1 bugs from `user_feedbacks.md` (2026-07-07 testing pass): tutor answers leaking raw JSON, community-upload consent not enforced server-side, `/documents/manage` filters being silently ignored, the permanently-failed admin action being a no-op, the global search page running on mock data, and two hardcoded placeholder values in the UI.

**Architecture:** Each backend fix is a small, targeted change to an existing service/endpoint — no new modules, no schema migrations. The recovery worker gets one additional `WHERE` guard. Frontend fixes replace mock/fake data sources with the already-existing real endpoints, following the exact `code` → `course_code` mapping pattern already used in `dashboard/page.tsx`.

**Tech Stack:** FastAPI + SQLAlchemy async (backend), Next.js 16 App Router + React 19 (frontend), pytest + httpx `ASGITransport` (backend tests).

## Global Constraints

- Backend API service runs as a **baked Docker image** — code edits are invisible until `docker compose build api worker-ocr worker-eval worker-index && docker compose up -d api worker-ocr worker-eval worker-index`. (See project memory `project-backend-docker-baked-image`.)
- Frontend runs as a **baked Docker image** at `:3000` — same rebuild requirement. CORS only allows origin `:3000`. (See project memory `project-frontend-docker-prod-build`.)
- Existing conventions: unit tests use a hand-rolled `FakeSession`/`FakeDBSession` (no real DB in tests); DB-dependent behavior across real Postgres is only verified via `RUN_E2E=1` tests in `tests/e2e/test_acceptance_flow.py` against the live docker stack.
- Follow existing code style exactly — do not refactor adjacent code.

---

### Task 1: Fix tutor answer leaking raw `{"used_doc_ids": [...]}` JSON (P0-2)

**Files:**
- Modify: `src/backend/app/services/tutor_service.py:583-587` (the `_postprocess_answer` function, defined at line 558)
- Test: `src/backend/tests/unit/test_tutor_service.py`

**Root cause:** `idx = answer_clean.rfind(json_marker); if idx > 0:` — when the model's entire answer is *just* the trailing id JSON (nothing before it), `rfind` returns `0`, and `idx > 0` is `False`, so the JSON is never stripped. The raw JSON string is then persisted as the assistant's chat message.

- [ ] **Step 1: Write the failing test**

Add to `src/backend/tests/unit/test_tutor_service.py` (near the existing `test_postprocess_answer_without_ids_returns_no_citations` test, using the same imports already present in that test — `CitationResponse`, `_postprocess_answer`, `DocumentTier`, `uuid4`):

```python
def test_postprocess_answer_json_only_answer_falls_back_to_friendly_message() -> None:
    from app.schemas.tutor import CitationResponse
    from app.services.tutor_service import _postprocess_answer

    doc_id = uuid4()
    chunk_id = uuid4()
    citation = CitationResponse(
        chunk_id=chunk_id,
        document_title="doc.pdf",
        document_tier=DocumentTier.COMMUNITY.value,
        document_subtype=None,
        section_title=None,
        page_number=None,
        chunk_order=1,
        excerpt="excerpt",
    )
    # The model answered with ONLY the trailing id-JSON — nothing before it.
    answer = f'{{"used_doc_ids": ["{doc_id}"]}}'

    answer_clean, filtered = _postprocess_answer(answer, [citation], {chunk_id: doc_id})

    assert answer_clean == "Xin lỗi, mình chưa rõ câu trả lời — bạn hỏi lại giúp mình nhé?"
    assert filtered == [citation]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd src/backend && python -m pytest tests/unit/test_tutor_service.py::test_postprocess_answer_json_only_answer_falls_back_to_friendly_message -v`
Expected: FAIL — `answer_clean` will equal the raw JSON string instead of the friendly fallback.

- [ ] **Step 3: Fix `_postprocess_answer`**

In `src/backend/app/services/tutor_service.py`, change the strip loop (currently at lines 583-587):

```python
    answer_clean = answer
    for json_marker in ['{"used_doc_ids"', '{"used_chunk_ids"', '{\n  "used_doc_ids"', '{\n  "used_chunk_ids"']:
        idx = answer_clean.rfind(json_marker)
        if idx > 0:
            answer_clean = answer_clean[:idx].rstrip()
```

to:

```python
    answer_clean = answer
    for json_marker in ['{"used_doc_ids"', '{"used_chunk_ids"', '{\n  "used_doc_ids"', '{\n  "used_chunk_ids"']:
        idx = answer_clean.rfind(json_marker)
        if idx >= 0:
            answer_clean = answer_clean[:idx].rstrip()

    if not answer_clean:
        answer_clean = "Xin lỗi, mình chưa rõ câu trả lời — bạn hỏi lại giúp mình nhé?"
```

(The safety strip for tool-call JSON leftovers a few lines below is unaffected — leave it as-is.)

- [ ] **Step 4: Run test to verify it passes**

Run: `cd src/backend && python -m pytest tests/unit/test_tutor_service.py -v -k postprocess_answer`
Expected: both `test_postprocess_answer_without_ids_returns_no_citations` and the new test PASS.

- [ ] **Step 5: Commit**

```bash
cd src/backend
git add app/services/tutor_service.py tests/unit/test_tutor_service.py
git commit -m "fix: tutor answer no longer leaks raw used_doc_ids JSON when it's the entire response"
```

---

### Task 2: Enforce `shared_rights_confirmed` server-side on community upload (P0-1)

**Files:**
- Modify: `src/backend/app/api/v1/documents.py:188-233` (the `upload_community` endpoint)
- Modify: `src/frontend/src/app/courses/[courseId]/page.tsx:533-546` (the `formData` built in `handleUploadSubmit`)
- Test: `src/backend/tests/unit/test_new_endpoints.py`

**Root cause:** The community upload handler never reads or validates a consent field; the frontend's `uploadConsent` checkbox is client-only decoration.

- [ ] **Step 1: Write the failing test**

Add to `src/backend/tests/unit/test_new_endpoints.py` (it already imports `ASGITransport`, `AsyncClient`, `create_access_token`, `get_session`, `app`, and has `FakeDBSession`/`make_user`/`override_session_helper` helpers defined at the top — reuse them):

```python
@pytest.mark.asyncio
async def test_upload_community_document_rejects_missing_consent() -> None:
    student = make_user("student")
    fake_db = FakeDBSession(user=student)
    app.dependency_overrides[get_session] = override_session_helper(fake_db)
    token = create_access_token(student)

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/documents/community",
                headers={"Authorization": f"Bearer {token}"},
                data={
                    "course_code": "IT3160E",
                    "contribution_type": "summary_note",
                    "topic_tags": "[]",
                    # shared_rights_confirmed intentionally omitted
                },
                files={"file": ("note.pdf", b"%PDF-1.4 test", "application/pdf")},
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_upload_community_document_rejects_false_consent() -> None:
    student = make_user("student")
    fake_db = FakeDBSession(user=student)
    app.dependency_overrides[get_session] = override_session_helper(fake_db)
    token = create_access_token(student)

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/documents/community",
                headers={"Authorization": f"Bearer {token}"},
                data={
                    "course_code": "IT3160E",
                    "contribution_type": "summary_note",
                    "topic_tags": "[]",
                    "shared_rights_confirmed": "false",
                },
                files={"file": ("note.pdf", b"%PDF-1.4 test", "application/pdf")},
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 422
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd src/backend && python -m pytest tests/unit/test_new_endpoints.py -v -k consent`
Expected: FAIL — both requests currently proceed past validation (they'll fail later or return 201/other, not 422), since there is no `shared_rights_confirmed` field at all yet.

- [ ] **Step 3: Add the required field and validation**

In `src/backend/app/api/v1/documents.py`, change the `upload_community` signature (currently lines 188-198):

```python
@router.post("/community", status_code=status.HTTP_201_CREATED, response_model=DocumentUploadResponse)
async def upload_community(
    session: SessionDep,
    storage: StorageDep,
    user: CurrentUserDep,
    course_code: str = Form(...),
    contribution_type: ContributionType = Form(...),
    file: UploadFile = File(...),
    topic_tags: str = Form(default="[]"),
    display_name: str | None = Form(default=None),
) -> DocumentUploadResponse:
```

to:

```python
@router.post("/community", status_code=status.HTTP_201_CREATED, response_model=DocumentUploadResponse)
async def upload_community(
    session: SessionDep,
    storage: StorageDep,
    user: CurrentUserDep,
    course_code: str = Form(...),
    contribution_type: ContributionType = Form(...),
    file: UploadFile = File(...),
    shared_rights_confirmed: bool = Form(...),
    topic_tags: str = Form(default="[]"),
    display_name: str | None = Form(default=None),
) -> DocumentUploadResponse:
    if not shared_rights_confirmed:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="You must confirm you have the rights to share this material before uploading.",
        )
```

(Leave the rest of the function body — the `try/except` for `topic_tags`, the size checks, the call to `upload_community_document` — untouched; just insert the new parameter and the check above the existing `try:` block.)

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd src/backend && python -m pytest tests/unit/test_new_endpoints.py -v -k consent`
Expected: both PASS with `422`.

- [ ] **Step 5: Wire the frontend to send the field**

In `src/frontend/src/app/courses/[courseId]/page.tsx`, in `handleUploadSubmit` (currently lines 533-546), add one line after `formData.append("display_name", uploadTitle);`:

```tsx
    const formData = new FormData();
    formData.append("course_code", courseId);
    formData.append("file", uploadFile!); // validated non-null above
    formData.append("display_name", uploadTitle);
    formData.append("shared_rights_confirmed", String(uploadConsent));
```

(`uploadConsent` is already validated to be `true` earlier in the same function at line 524-526, so this always sends `"true"` in practice — but the field must exist for the server-side check to see it.)

- [ ] **Step 6: Commit**

```bash
cd src/backend
git add app/api/v1/documents.py tests/unit/test_new_endpoints.py
git commit -m "fix: enforce shared_rights_confirmed server-side on community document upload"
cd ../frontend
git add src/app/courses/\[courseId\]/page.tsx
git commit -m "fix: send shared_rights_confirmed on community document upload"
```

---

### Task 3: Add `status`/`course_code`/`limit`/`offset` filters to `/documents/manage` (P1-2, resolves the P0-3 and P1-11 count-mismatch artifacts)

**Files:**
- Modify: `src/backend/app/services/document_service.py:402-438` (`list_documents_for_management`)
- Modify: `src/backend/app/api/v1/documents.py:110-146` (`list_managed_documents`)
- Test: `src/backend/tests/e2e/test_acceptance_flow.py` (DB-dependent filtering can only be verified against the real Postgres stack — this repo has no SQLite/in-memory DB test fixture, so this is an e2e test gated by `RUN_E2E=1`, matching existing convention)

**Root cause:** `list_documents_for_management` only accepts `uploaded_from`/`uploaded_to`; the endpoint doesn't even declare `status`, `course_code`, `limit`, `offset` as `Query` params, so FastAPI silently drops them and the frontend's server call returns every document regardless of the `?status=...` in the URL.

- [ ] **Step 1: Extend the service function**

In `src/backend/app/services/document_service.py`, change `list_documents_for_management` (currently lines 402-438):

```python
async def list_documents_for_management(
    session: AsyncSession,
    user: User,
    uploaded_from: datetime | None = None,
    uploaded_to: datetime | None = None,
) -> list[Document]:
    """List documents an admin/reviewer oversees, across all pipeline statuses.

    Admins see every document; reviewers see documents in courses they have an
    active assignment for. Used by the admin/reviewer document-management page to
    track processing progress and to delete documents. Optionally filtered by
    upload date range (inclusive).
    """
    stmt = (
        select(Document)
        .options(selectinload(Document.course), selectinload(Document.state_logs))
        .order_by(desc(Document.uploaded_at))
    )
    if uploaded_from is not None:
        stmt = stmt.where(Document.uploaded_at >= uploaded_from)
    if uploaded_to is not None:
        stmt = stmt.where(Document.uploaded_at <= uploaded_to)
    if user.role == "reviewer":
        stmt = stmt.join(
            CourseReviewerAssignment,
            CourseReviewerAssignment.course_id == Document.course_id,
        ).where(
            CourseReviewerAssignment.user_id == user.id,
            CourseReviewerAssignment.is_active.is_(True),
        )
    elif user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins or reviewers can manage documents",
        )
    result = await session.scalars(stmt)
    return list(result.all())
```

to:

```python
async def list_documents_for_management(
    session: AsyncSession,
    user: User,
    uploaded_from: datetime | None = None,
    uploaded_to: datetime | None = None,
    status_filter: DocumentStatus | None = None,
    course_code: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> list[Document]:
    """List documents an admin/reviewer oversees, across all pipeline statuses.

    Admins see every document; reviewers see documents in courses they have an
    active assignment for. Used by the admin/reviewer document-management page to
    track processing progress and to delete documents. Optionally filtered by
    upload date range (inclusive), pipeline status, and course code, with
    limit/offset pagination.
    """
    stmt = (
        select(Document)
        .options(selectinload(Document.course), selectinload(Document.state_logs))
        .order_by(desc(Document.uploaded_at))
    )
    if uploaded_from is not None:
        stmt = stmt.where(Document.uploaded_at >= uploaded_from)
    if uploaded_to is not None:
        stmt = stmt.where(Document.uploaded_at <= uploaded_to)
    if status_filter is not None:
        stmt = stmt.where(Document.status == status_filter)
    if course_code is not None:
        stmt = stmt.join(Course, Course.id == Document.course_id).where(Course.code == course_code)
    if user.role == "reviewer":
        stmt = stmt.join(
            CourseReviewerAssignment,
            CourseReviewerAssignment.course_id == Document.course_id,
        ).where(
            CourseReviewerAssignment.user_id == user.id,
            CourseReviewerAssignment.is_active.is_(True),
        )
    elif user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins or reviewers can manage documents",
        )
    if offset is not None:
        stmt = stmt.offset(offset)
    if limit is not None:
        stmt = stmt.limit(limit)
    result = await session.scalars(stmt)
    return list(result.all())
```

(`Course` and `DocumentStatus` are already imported at the top of this file — no new imports needed.)

- [ ] **Step 2: Extend the endpoint**

In `src/backend/app/api/v1/documents.py`, change `list_managed_documents` (currently lines 110-122):

```python
@router.get("/manage", response_model=list[DocumentRead])
async def list_managed_documents(
    session: SessionDep,
    user: ReviewerOrAdminDep,
    uploaded_from: datetime | None = Query(default=None, description="Only documents uploaded at/after this time"),
    uploaded_to: datetime | None = Query(default=None, description="Only documents uploaded at/before this time"),
) -> list[DocumentRead]:
    """List documents an admin/reviewer oversees (all statuses, role-scoped), optionally by upload date range.

    Each item is enriched with the latest AI evaluation summary (recommendation +
    overall score) so reviewers can triage and bulk-approve without opening each report.
    """
    docs = await list_documents_for_management(session, user, uploaded_from, uploaded_to)
```

to:

```python
@router.get("/manage", response_model=list[DocumentRead])
async def list_managed_documents(
    session: SessionDep,
    user: ReviewerOrAdminDep,
    uploaded_from: datetime | None = Query(default=None, description="Only documents uploaded at/after this time"),
    uploaded_to: datetime | None = Query(default=None, description="Only documents uploaded at/before this time"),
    status: DocumentStatus | None = Query(default=None, description="Only documents in this pipeline status"),
    course_code: str | None = Query(default=None, description="Only documents in this course"),
    limit: int | None = Query(default=None, ge=1, le=200),
    offset: int | None = Query(default=None, ge=0),
) -> list[DocumentRead]:
    """List documents an admin/reviewer oversees (all statuses, role-scoped), optionally by upload date range.

    Each item is enriched with the latest AI evaluation summary (recommendation +
    overall score) so reviewers can triage and bulk-approve without opening each report.
    """
    docs = await list_documents_for_management(
        session,
        user,
        uploaded_from,
        uploaded_to,
        status_filter=status,
        course_code=course_code,
        limit=limit,
        offset=offset,
    )
```

(`DocumentStatus` is already imported at the top of `documents.py` — no new import needed. The parameter is named `status` to match the query string the frontend/tester already uses; it shadows the `fastapi.status` module only inside this function body, where it's not otherwise referenced.)

- [ ] **Step 3: Add an e2e regression test**

Add to `src/backend/tests/e2e/test_acceptance_flow.py` (it already defines `BASE_URL`, `RUN_E2E`, `_login`, and the seeded `_REVIEWER_EMAIL`/`_SEED_PASSWORD` constants — reuse them; gate with the existing `pytestmark`-style skip used elsewhere in that file, or a local `pytest.mark.skipif`):

```python
@pytest.mark.skipif(not RUN_E2E, reason="Set RUN_E2E=1 to run against the live docker stack")
@pytest.mark.asyncio
async def test_manage_status_filter_matches_review_queue_count() -> None:
    async with httpx.AsyncClient() as client:
        token = await _login(client, _REVIEWER_EMAIL)
        headers = {"Authorization": f"Bearer {token}"}

        queue_resp = await client.get(f"{BASE_URL}/api/v1/review/queue", headers=headers)
        assert queue_resp.status_code == 200
        queue_ids = {d["id"] for d in queue_resp.json()}

        manage_resp = await client.get(
            f"{BASE_URL}/api/v1/documents/manage",
            params={"status": "NEEDS_REVIEW"},
            headers=headers,
        )
        assert manage_resp.status_code == 200
        manage_docs = manage_resp.json()

        assert {d["id"] for d in manage_docs} == queue_ids
        assert all(d["status"] == "NEEDS_REVIEW" for d in manage_docs)
```

- [ ] **Step 4: Rebuild and restart the backend containers**

Run: `cd src/backend && docker compose build api worker-ocr worker-eval worker-index && docker compose up -d api worker-ocr worker-eval worker-index`
Expected: all four containers report healthy (`docker ps` shows `Up ... (healthy)`).

- [ ] **Step 5: Run the e2e test against the live stack**

Run: `cd src/backend && RUN_E2E=1 python -m pytest tests/e2e/test_acceptance_flow.py::test_manage_status_filter_matches_review_queue_count -v`
Expected: PASS — `/documents/manage?status=NEEDS_REVIEW` now returns exactly the same document set as `/review/queue`.

- [ ] **Step 6: Commit**

```bash
cd src/backend
git add app/services/document_service.py app/api/v1/documents.py tests/e2e/test_acceptance_flow.py
git commit -m "fix: honor status/course_code/limit/offset filters on /documents/manage"
```

---

### Task 4: Make `mark-permanently-failed` actually change document state (P1-3)

**Files:**
- Modify: `src/backend/app/services/admin_service.py:63-177` (`reprocess_document` and `mark_permanently_failed`)
- Modify: `src/backend/app/schemas/documents.py:32-62` (`DocumentRead`)
- Modify: `src/backend/app/workers/recovery_worker.py` (guard against re-enqueuing permanently-failed docs)
- Test: `src/backend/tests/unit/test_state_machine.py`-style unit tests, new file `src/backend/tests/unit/test_admin_service.py`

**Root cause (three parts):**
1. `mark_permanently_failed` sets the `permanently_failed` column but never transitions `status` toward `FAILED`, so a doc stuck in `PARSING` stays `PARSING` forever, contradicting the endpoint's own docstring.
2. `DocumentRead` doesn't expose `permanently_failed` at all, so `GET /documents/{id}` can never show the flag even though it's set.
3. `recover_stale_pending_jobs_for_session` re-enqueues any stale `PENDING` job regardless of `permanently_failed`, so even after the flag is fixed, the OCR/eval worker's stale-job recovery will keep resurrecting the same "permanently failed" document.

- [ ] **Step 1: Write failing unit tests for `mark_permanently_failed`**

Create `src/backend/tests/unit/test_admin_service.py`:

```python
from __future__ import annotations

from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.models.enums import ContributionType, DocumentStatus, DocumentTier, FileFormat
from app.models.tables import AdminAuditLog, Document, DocumentStateLog, User
from app.services.admin_service import mark_permanently_failed


class FakeAdminSession:
    def __init__(self, doc: Document | None) -> None:
        self.doc = doc
        self.added: list[object] = []
        self.committed = False
        self.refreshed: list[object] = []

    async def scalar(self, statement) -> Document | None:
        return self.doc

    def add(self, item: object) -> None:
        self.added.append(item)

    async def flush(self) -> None:
        pass

    async def commit(self) -> None:
        self.committed = True

    async def refresh(self, item: object) -> None:
        self.refreshed.append(item)


def make_document(status: DocumentStatus) -> Document:
    return Document(
        id=uuid4(),
        course_id=uuid4(),
        uploader_id=uuid4(),
        document_tier=DocumentTier.COMMUNITY,
        contribution_type=ContributionType.SUMMARY_NOTE,
        status=status,
        original_filename="stuck.pdf",
        file_format=FileFormat.PDF,
    )


def make_admin() -> User:
    return User(
        id=uuid4(),
        email="admin@example.test",
        hashed_password="hash",
        role="admin",
        full_name="Admin User",
    )


@pytest.mark.asyncio
async def test_mark_permanently_failed_transitions_parsing_to_failed() -> None:
    doc = make_document(DocumentStatus.PARSING)
    session = FakeAdminSession(doc)

    result = await mark_permanently_failed(session, doc.id, make_admin())

    assert result.status == DocumentStatus.FAILED
    assert result.permanently_failed is True
    assert session.committed is True
    state_logs = [item for item in session.added if isinstance(item, DocumentStateLog)]
    assert len(state_logs) == 1
    assert state_logs[0].from_state == DocumentStatus.PARSING
    assert state_logs[0].to_state == DocumentStatus.FAILED
    audit_logs = [item for item in session.added if isinstance(item, AdminAuditLog)]
    assert len(audit_logs) == 1
    assert audit_logs[0].to_state == DocumentStatus.FAILED.value


@pytest.mark.asyncio
async def test_mark_permanently_failed_on_already_failed_just_sets_flag() -> None:
    doc = make_document(DocumentStatus.FAILED)
    session = FakeAdminSession(doc)

    result = await mark_permanently_failed(session, doc.id, make_admin())

    assert result.status == DocumentStatus.FAILED
    assert result.permanently_failed is True
    state_logs = [item for item in session.added if isinstance(item, DocumentStateLog)]
    assert state_logs == []


@pytest.mark.asyncio
async def test_mark_permanently_failed_rejects_approved_document() -> None:
    doc = make_document(DocumentStatus.APPROVED)
    session = FakeAdminSession(doc)

    with pytest.raises(HTTPException) as exc_info:
        await mark_permanently_failed(session, doc.id, make_admin())

    assert exc_info.value.status_code == 409
    assert doc.permanently_failed is False
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd src/backend && python -m pytest tests/unit/test_admin_service.py -v`
Expected: FAIL — current implementation never transitions status and never rejects `APPROVED`.

- [ ] **Step 3: Fix `mark_permanently_failed`**

In `src/backend/app/services/admin_service.py`, change (currently lines 160-177):

```python
async def mark_permanently_failed(session: AsyncSession, document_id: UUID, actor_user: User) -> Document:
    doc = await session.scalar(select(Document).where(Document.id == document_id))
    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found")
    doc.permanently_failed = True
    await log_admin_action(
        session,
        actor_id=actor_user.id,
        action_type="mark_permanently_failed",
        target_entity_type="document",
        target_entity_id=doc.id,
        from_state=doc.status.value,
        to_state=None,
        reason="Admin marked permanently failed",
    )
    await session.commit()
    await session.refresh(doc)
    return doc
```

to:

```python
_TRANSITIONABLE_TO_FAILED = {DocumentStatus.PARSING, DocumentStatus.EVALUATING, DocumentStatus.INDEXING}


async def mark_permanently_failed(session: AsyncSession, document_id: UUID, actor_user: User) -> Document:
    doc = await session.scalar(select(Document).where(Document.id == document_id))
    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found")

    from_state = doc.status
    if from_state in _TRANSITIONABLE_TO_FAILED:
        sm = DocumentStateMachine(session)
        await sm.transition(doc, DocumentStatus.FAILED, actor=actor_user, reason="Admin marked permanently failed")
    elif from_state != DocumentStatus.FAILED:
        raise HTTPException(
            status_code=409,
            detail=f"Cannot mark a document in {from_state.value} state as permanently failed",
        )

    doc.permanently_failed = True
    await log_admin_action(
        session,
        actor_id=actor_user.id,
        action_type="mark_permanently_failed",
        target_entity_type="document",
        target_entity_id=doc.id,
        from_state=from_state.value,
        to_state=DocumentStatus.FAILED.value,
        reason="Admin marked permanently failed",
    )
    await session.commit()
    await session.refresh(doc)
    return doc
```

(`DocumentStateMachine` is already imported at the top of `admin_service.py` via `from app.core.state_machine import DocumentStateMachine, log_admin_action`.)

- [ ] **Step 4: Clear the flag on explicit admin reprocess**

In the same file, in `reprocess_document` (currently lines 79-80):

```python
    if doc.status not in {DocumentStatus.FAILED, DocumentStatus.REJECTED}:
        raise HTTPException(status_code=409, detail="Only FAILED or REJECTED documents can be reprocessed")
```

add one line directly after it:

```python
    if doc.status not in {DocumentStatus.FAILED, DocumentStatus.REJECTED}:
        raise HTTPException(status_code=409, detail="Only FAILED or REJECTED documents can be reprocessed")

    doc.permanently_failed = False
```

(An admin explicitly reprocessing a document is an explicit override of any earlier "permanently failed" marking.)

- [ ] **Step 5: Run tests to verify they pass**

Run: `cd src/backend && python -m pytest tests/unit/test_admin_service.py -v`
Expected: all 3 PASS.

- [ ] **Step 6: Expose the field in `DocumentRead`**

In `src/backend/app/schemas/documents.py`, in `DocumentRead` (currently lines 32-62), add one field next to the other status-related fields:

```python
    no_reviewer_flag: bool
    sla_breached: bool
    permanently_failed: bool
```

- [ ] **Step 7: Guard the recovery worker against permanently-failed documents**

In `src/backend/app/workers/recovery_worker.py`, change the import line:

```python
from app.models import EvaluationJob, ProcessingJob
```

to:

```python
from app.models import Document, EvaluationJob, ProcessingJob
```

Then change the two queries inside `recover_stale_pending_jobs_for_session` (currently):

```python
    processing_jobs = await session.scalars(
        select(ProcessingJob).where(
            ProcessingJob.is_latest.is_(True),
            ProcessingJob.status == JobStatus.PENDING,
            ProcessingJob.created_at <= stale_before,
        )
    )
    evaluation_jobs = await session.scalars(
        select(EvaluationJob).where(
            EvaluationJob.is_latest.is_(True),
            EvaluationJob.status == JobStatus.PENDING,
            EvaluationJob.created_at <= stale_before,
        )
    )
```

to:

```python
    processing_jobs = await session.scalars(
        select(ProcessingJob)
        .join(Document, Document.id == ProcessingJob.document_id)
        .where(
            ProcessingJob.is_latest.is_(True),
            ProcessingJob.status == JobStatus.PENDING,
            ProcessingJob.created_at <= stale_before,
            Document.permanently_failed.is_(False),
        )
    )
    evaluation_jobs = await session.scalars(
        select(EvaluationJob)
        .join(Document, Document.id == EvaluationJob.document_id)
        .where(
            EvaluationJob.is_latest.is_(True),
            EvaluationJob.status == JobStatus.PENDING,
            EvaluationJob.created_at <= stale_before,
            Document.permanently_failed.is_(False),
        )
    )
```

- [ ] **Step 8: Rebuild and restart the backend containers**

Run: `cd src/backend && docker compose build api worker-ocr worker-eval worker-index && docker compose up -d api worker-ocr worker-eval worker-index`
Expected: all four containers healthy.

- [ ] **Step 9: Smoke-test against the live stack (reproduces the exact P1-3 repro from the report)**

```bash
cd src/backend
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@soict.hust.edu.vn","password":"changeme123"}' | python3 -c "import sys,json;print(json.load(sys.stdin)['access_token'])")

# Use the known stuck doc from the test report, or find a fresh PARSING doc:
DOC_ID=62ea6a2e-bcac-4d05-b66a-b3452461d8b1

curl -s -X POST "http://localhost:8000/api/v1/admin/documents/$DOC_ID/mark-permanently-failed" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

curl -s "http://localhost:8000/api/v1/documents/$DOC_ID" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

Expected: the second `curl` now shows `"status": "FAILED"` and `"permanently_failed": true` (previously: `"status": "PARSING"`, `"permanently_failed": null`).

- [ ] **Step 10: Commit**

```bash
cd src/backend
git add app/services/admin_service.py app/schemas/documents.py app/workers/recovery_worker.py tests/unit/test_admin_service.py
git commit -m "fix: mark-permanently-failed now transitions status to FAILED and is respected by recovery worker"
```

---

### Task 5: Wire the global search page to real course data (P1-1)

**Files:**
- Modify: `src/frontend/src/app/search/page.tsx`

**Root cause:** The page imports `mockCourses` from `lib/mockData` and never calls the API; it happens to look correct today only because the mock course list coincidentally matches the seed data.

- [ ] **Step 1: Replace the mock data source with a real `/courses` fetch**

In `src/frontend/src/app/search/page.tsx`, replace the top of the file (imports and the `mockCourses`-typed logic) — current:

```tsx
/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import React, { useState } from "react";
import Link from "next/link";
import AppShell from "../../components/app-shell";
import { mockCourses } from "../../lib/mockData";

export default function GlobalSearchPage() {
  const [query, setQuery] = useState("");
  const [activeFilter, setActiveFilter] = useState<"ALL" | "IT" | "EE" | "MATH">("ALL");
```

with:

```tsx
/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import AppShell from "../../components/app-shell";
import api from "../../lib/api";

interface SearchableCourse {
  course_code: string;
  name: string;
  description: string;
  topic_summary: string;
}

export default function GlobalSearchPage() {
  const [query, setQuery] = useState("");
  const [activeFilter, setActiveFilter] = useState<"ALL" | "IT" | "EE" | "MATH">("ALL");
  const [courses, setCourses] = useState<SearchableCourse[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const data = await api.get<any[]>("/courses");
        // Map backend 'code' to 'course_code' (same convention as dashboard/page.tsx).
        setCourses(
          (data || []).map((c: any) => ({
            course_code: c.code,
            name: c.name,
            description: c.description || "",
            topic_summary: c.topic_summary || "",
          }))
        );
      } catch {
        setCourses([]);
      } finally {
        setLoading(false);
      }
    };
    fetchCourses();
  }, []);
```

Then update the three remaining references to `mockCourses` and its inferred type:

```tsx
  const passesFilter = (course: (typeof mockCourses)[number]) => {
```
→
```tsx
  const passesFilter = (course: SearchableCourse) => {
```

```tsx
  const scored = mockCourses
    .map((course) => {
```
→
```tsx
  const scored = courses
    .map((course) => {
```

Leave everything else (the `tokens`/`scored`/`matchedCourses` logic, the JSX) unchanged — it already only reads `course.course_code`, `course.name`, `course.description`, `course.topic_summary`, all of which the mapped `SearchableCourse` provides.

- [ ] **Step 2: Show a loading state instead of a misleading empty-result message**

Find this block near the end of the file:

```tsx
          {matchedCourses.length === 0 && (
            <div className="bg-white border border-whisper-border rounded-2xl p-12 text-center space-y-2">
              <p className="text-slate-500 font-semibold">
                Không tìm thấy học phần nào khớp với từ khóa tìm kiếm của bạn.
              </p>
```

and change the condition so it doesn't show "no results" while the initial fetch is still in flight:

```tsx
          {!loading && matchedCourses.length === 0 && (
            <div className="bg-white border border-whisper-border rounded-2xl p-12 text-center space-y-2">
              <p className="text-slate-500 font-semibold">
                Không tìm thấy học phần nào khớp với từ khóa tìm kiếm của bạn.
              </p>
```

- [ ] **Step 3: Rebuild the frontend container and verify in browser**

Run: `cd src/frontend && docker compose build frontend && docker compose up -d frontend`

Then use the Playwright MCP tools to log in as `student.anhnv@sis.hust.edu.vn` / `changeme123`, navigate to `/search`, and confirm:
- The page loads real courses (compare a course name against `GET /api/v1/courses` output — not the old mock list).
- Typing a token that only exists in a real seeded course (not in the old mock list) surfaces that course.

- [ ] **Step 4: Commit**

```bash
cd src/frontend
git add src/app/search/page.tsx
git commit -m "fix: global search now reads real courses from the API instead of mock data"
```

---

### Task 6: Remove hardcoded demo `studentId` from the sidebar (P1-4)

**Files:**
- Modify: `src/frontend/src/components/app-shell.tsx:235,373`

**Root cause:** `const studentId = "20226038";` is a leftover demo placeholder shown to every student user regardless of who's actually logged in.

- [ ] **Step 1: Remove the hardcoded ID and always show the real user's email**

In `src/frontend/src/components/app-shell.tsx`, remove line 235:

```tsx
  const studentId = "20226038"; // Standard demo student ID requested
```

And change line 373 from:

```tsx
                {currentRole === "student" ? `MSSV: ${studentId}` : currentUser?.email || ""}
```

to:

```tsx
                {currentUser?.email || ""}
```

- [ ] **Step 2: Rebuild the frontend container and verify in browser**

Run: `cd src/frontend && docker compose build frontend && docker compose up -d frontend`

Use Playwright to log in as `student.anhnv@sis.hust.edu.vn`, confirm the sidebar footer now shows that user's real email instead of "MSSV: 20226038".

- [ ] **Step 3: Commit**

```bash
cd src/frontend
git add src/components/app-shell.tsx
git commit -m "fix: remove hardcoded demo studentId, show real user email in sidebar for all roles"
```

---

### Task 7: Stop falling back to a hardcoded course link on REJECTED docs (P2-6)

**Files:**
- Modify: `src/frontend/src/app/my-documents/page.tsx:495-502`

**Root cause:** When `doc.course_code` is falsy, the "re-upload" CTA links to a hardcoded `it4062`, which is wrong for any other course.

- [ ] **Step 1: Only render the CTA when the real course code is known**

In `src/frontend/src/app/my-documents/page.tsx`, change (currently lines 495-502):

```tsx
                                        <div className="pt-2">
                                          <Link
                                            href={`/courses/${doc.course_code?.toLowerCase() || "it4062"}`}
                                            className="inline-flex items-center gap-2 rounded-lg bg-system-red hover:opacity-90 text-white font-bold text-xs px-3 py-1.5 transition-all shadow-xs cursor-pointer"
                                          >
                                            <UploadCloud className="h-3.5 w-3.5" /> Tải lên lại tài liệu môn này
                                          </Link>
                                        </div>
```

to:

```tsx
                                        {doc.course_code && (
                                          <div className="pt-2">
                                            <Link
                                              href={`/courses/${doc.course_code.toLowerCase()}`}
                                              className="inline-flex items-center gap-2 rounded-lg bg-system-red hover:opacity-90 text-white font-bold text-xs px-3 py-1.5 transition-all shadow-xs cursor-pointer"
                                            >
                                              <UploadCloud className="h-3.5 w-3.5" /> Tải lên lại tài liệu môn này
                                            </Link>
                                          </div>
                                        )}
```

- [ ] **Step 2: Rebuild the frontend container and verify in browser**

Run: `cd src/frontend && docker compose build frontend && docker compose up -d frontend`

Use Playwright to log in as a student with a REJECTED document, open `/my-documents`, confirm the CTA links to the document's actual course.

- [ ] **Step 3: Commit**

```bash
cd src/frontend
git add src/app/my-documents/page.tsx
git commit -m "fix: my-documents re-upload CTA no longer falls back to a hardcoded course link"
```

---

### Task 8: Update the module registry

**Files:**
- Modify: `.agents/context/REGISTRY.md`

Per `CLAUDE.md`, any session that modifies modules must update the registry before finishing.

- [ ] **Step 1: Add a dated entry summarizing the fixes**

Read `.agents/context/REGISTRY.md` first to match its existing entry format, then append an entry for this session covering: tutor postprocess fix, community-upload consent enforcement, `/documents/manage` filters, `mark-permanently-failed` state transition + recovery-worker guard, `/search` wired to real API, sidebar/my-documents hardcoded-value removal.

- [ ] **Step 2: Commit**

```bash
git add .agents/context/REGISTRY.md
git commit -m "docs: registry update for user-feedback bug fixes"
```

---

## Self-Review Notes

- **Spec coverage:** Tasks 1-4 cover all three confirmed P0s plus P1-2 (which also resolves the P0-3/P1-11 artifacts). Tasks 5-7 cover P1-1 and the two cheap hardcoded-value fixes (P1-4, P2-6). Findings determined to be non-bugs during verification (P1-10, P1-12) and lower-value/higher-risk items requiring a DB migration (the fake `file_size_bytes`, cross-cutting #3/#4/#5, P1-7's `ai_overall_score` population, P1-5/P1-6/P1-8/P1-9 reviewer UX polish, admin P1-13/P2-10/P2-11/P2-12) are intentionally out of scope for this plan — flag them as follow-ups if the user wants them next.
- **Placeholder scan:** No TBD/placeholder steps remain; every step has literal code.
- **Type consistency:** `DocumentStatus`, `Document`, `Course` are reused with the same names/imports already present in each file; `SearchableCourse` is a new type used consistently across Task 5's steps; `_TRANSITIONABLE_TO_FAILED` and `mark_permanently_failed`'s signature are unchanged externally (same params), so `admin.py`'s existing caller needs no edit.
