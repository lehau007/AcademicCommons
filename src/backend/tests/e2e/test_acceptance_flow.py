"""E2E acceptance tests — require a running stack (docker compose up).

Run with:
    RUN_E2E=1 pytest tests/e2e/

The BASE_URL is configurable via the E2E_BASE_URL environment variable
(defaults to http://localhost:8000).
"""

import asyncio
import os
import re

import httpx
import pytest

BASE_URL: str = os.environ.get("E2E_BASE_URL", "http://localhost:8000")
RUN_E2E: bool = os.environ.get("RUN_E2E", "0") == "1"

# Minimal valid single-page PDF (no real content needed for upload tests).
DUMMY_PDF = b"""%PDF-1.4
1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj
2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj
3 0 obj<</Type/Page/Parent 2 0 R/Resources<<>>/MediaBox[0 0 612 792]>>endobj
xref
0 4
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
trailer<</Size 4/Root 1 0 R>>
startxref
190
%%EOF"""

_UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.IGNORECASE,
)

# Seeded test users (deterministic UUIDs from data/seed/users.json)
_ADMIN_EMAIL = "admin@soict.hust.edu.vn"
_STUDENT_EMAIL = "student.anhnv@sis.hust.edu.vn"
_REVIEWER_EMAIL = "reviewer.ducpv@soict.hust.edu.vn"
_REVIEWER_UUID = "d36afc92-ad56-593d-b9a2-e4314938c3c1"
_SEED_PASSWORD = "changeme123"
_TEST_COURSE = "IT3160E"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


async def _login(client: httpx.AsyncClient, email: str, password: str = _SEED_PASSWORD) -> str:
    """Return an access token for the given credentials."""
    resp = await client.post(
        f"{BASE_URL}/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert resp.status_code == 200, f"Login failed for {email}: {resp.text}"
    return resp.json()["access_token"]


async def _poll_document_status(
    client: httpx.AsyncClient,
    token: str,
    document_id: str,
    target_statuses: list[str],
    timeout_seconds: int,
    interval_seconds: int = 5,
) -> str:
    """Poll GET /documents/{id} until status is one of target_statuses."""
    headers = {"Authorization": f"Bearer {token}"}
    deadline = asyncio.get_event_loop().time() + timeout_seconds
    last_status = ""
    while asyncio.get_event_loop().time() < deadline:
        resp = await client.get(f"{BASE_URL}/api/v1/documents/{document_id}", headers=headers)
        assert resp.status_code == 200, f"Document fetch failed: {resp.text}"
        last_status = resp.json().get("status", "")
        if last_status in target_statuses:
            return last_status
        await asyncio.sleep(interval_seconds)
    pytest.fail(
        f"Document {document_id} did not reach {target_statuses} within {timeout_seconds}s. "
        f"Last status: {last_status!r}"
    )


def _assert_valid_uuid(value: str, label: str) -> None:
    assert isinstance(value, str) and _UUID_RE.match(value), (
        f"{label} is not a valid UUID: {value!r}"
    )


async def _ensure_course_and_reviewer(
    client: httpx.AsyncClient,
    admin_headers: dict[str, str],
) -> None:
    """Idempotently ensure test course exists and reviewer is assigned."""
    course_resp = await client.get(
        f"{BASE_URL}/api/v1/courses/{_TEST_COURSE}", headers=admin_headers
    )
    if course_resp.status_code == 404:
        create_resp = await client.post(
            f"{BASE_URL}/api/v1/courses",
            json={
                "course_code": _TEST_COURSE,
                "name": "E2E Test Course",
                "description": "Created by E2E acceptance test",
            },
            headers=admin_headers,
        )
        assert create_resp.status_code in (200, 201), (
            f"Failed to create course {_TEST_COURSE}: {create_resp.text}"
        )
    else:
        assert course_resp.status_code == 200, (
            f"Unexpected status fetching course {_TEST_COURSE}: {course_resp.text}"
        )

    assign_resp = await client.post(
        f"{BASE_URL}/api/v1/courses/{_TEST_COURSE}/reviewers",
        json={"user_id": _REVIEWER_UUID},
        headers=admin_headers,
    )
    assert assign_resp.status_code in (200, 201, 409), (
        f"Unexpected status assigning reviewer: {assign_resp.text}"
    )


async def _upload_community_doc(
    client: httpx.AsyncClient,
    student_headers: dict[str, str],
    filename: str = "test_doc.pdf",
) -> str:
    """Upload a community document and return document_id."""
    resp = await client.post(
        f"{BASE_URL}/api/v1/documents/community",
        headers=student_headers,
        files={"file": (filename, DUMMY_PDF, "application/pdf")},
        data={
            "course_code": _TEST_COURSE,
            "contribution_type": "summary_note",
            "shared_rights_confirmed": "true",
        },
    )
    assert resp.status_code in (200, 201), f"Upload failed: {resp.text}"
    document_id = resp.json()["document_id"]
    assert document_id, "Response missing document_id"
    _assert_valid_uuid(document_id, "document_id")
    return document_id


# ---------------------------------------------------------------------------
# Test: health (always runs)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_health_endpoint_ok() -> None:
    """Smoke-test: /health must return 200 regardless of RUN_E2E."""
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(f"{BASE_URL}/health")
    assert resp.status_code == 200, (
        f"Expected 200 from /health, got {resp.status_code}: {resp.text}"
    )


# ---------------------------------------------------------------------------
# Test: RBAC guards (fast — no upload/poll, just auth checks)
# ---------------------------------------------------------------------------


@pytest.mark.e2e
@pytest.mark.skipif(not RUN_E2E, reason="Set RUN_E2E=1 to run E2E tests")
@pytest.mark.asyncio
async def test_rbac_guards() -> None:
    """Verify unauthenticated and wrong-role access are denied with correct HTTP codes."""
    async with httpx.AsyncClient(timeout=30) as client:
        # Unauthenticated → 401
        resp = await client.get(f"{BASE_URL}/api/v1/auth/me")
        assert resp.status_code == 401, f"Expected 401 without token, got {resp.status_code}"

        student_token = await _login(client, _STUDENT_EMAIL)
        student_headers = {"Authorization": f"Bearer {student_token}"}

        # Student cannot upload official document → 403
        official_resp = await client.post(
            f"{BASE_URL}/api/v1/documents/official",
            headers=student_headers,
            files={"file": ("official.pdf", DUMMY_PDF, "application/pdf")},
            data={"course_code": _TEST_COURSE, "material_type": "lecture_slides"},
        )
        assert official_resp.status_code == 403, (
            f"Student must not upload official docs; got {official_resp.status_code}: {official_resp.text}"
        )

        # Student cannot access admin dead-letter → 403
        dl_resp = await client.get(
            f"{BASE_URL}/api/v1/admin/dead-letter", headers=student_headers
        )
        assert dl_resp.status_code == 403, (
            f"Student must not access admin endpoints; got {dl_resp.status_code}"
        )

        reviewer_token = await _login(client, _REVIEWER_EMAIL)
        reviewer_headers = {"Authorization": f"Bearer {reviewer_token}"}

        # Reviewer cannot access admin dead-letter → 403
        rv_admin_resp = await client.get(
            f"{BASE_URL}/api/v1/admin/dead-letter", headers=reviewer_headers
        )
        assert rv_admin_resp.status_code == 403, (
            f"Reviewer must not access admin endpoints; got {rv_admin_resp.status_code}"
        )

        # Reviewer cannot register new users → 403
        register_resp = await client.post(
            f"{BASE_URL}/api/v1/admin/users",
            json={
                "email": "rbac_test_new@test.edu",
                "password": "pass12345678",
                "full_name": "RBAC Test User",
                "role": "student",
            },
            headers=reviewer_headers,
        )
        assert register_resp.status_code == 403, (
            f"Reviewer must not register users; got {register_resp.status_code}"
        )


# ---------------------------------------------------------------------------
# Test: Reject flow
# ---------------------------------------------------------------------------


@pytest.mark.e2e
@pytest.mark.skipif(not RUN_E2E, reason="Set RUN_E2E=1 to run E2E tests")
@pytest.mark.asyncio
async def test_reject_flow() -> None:
    """Reviewer rejects a community document → status transitions to REJECTED."""
    async with httpx.AsyncClient(timeout=120) as client:
        admin_token = await _login(client, _ADMIN_EMAIL)
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        await _ensure_course_and_reviewer(client, admin_headers)

        student_token = await _login(client, _STUDENT_EMAIL)
        student_headers = {"Authorization": f"Bearer {student_token}"}
        document_id = await _upload_community_doc(client, student_headers, "reject_test.pdf")

        intermediate_status = await _poll_document_status(
            client=client,
            token=student_token,
            document_id=document_id,
            target_statuses=["NEEDS_REVIEW", "APPROVED", "FAILED"],
            timeout_seconds=300,
        )
        assert intermediate_status == "NEEDS_REVIEW", (
            f"Reject-flow test requires NEEDS_REVIEW state, got {intermediate_status!r}. "
            "Ensure the test course has an active reviewer and no auto-approve path."
        )

        reviewer_token = await _login(client, _REVIEWER_EMAIL)
        reviewer_headers = {"Authorization": f"Bearer {reviewer_token}"}
        decide_resp = await client.post(
            f"{BASE_URL}/api/v1/review/{document_id}/decide",
            json={"decision": "REJECT", "note": "Rejected by E2E reject_flow test"},
            headers=reviewer_headers,
        )
        assert decide_resp.status_code in (200, 201), (
            f"Reject decision failed: {decide_resp.text}"
        )

        final_status = await _poll_document_status(
            client=client,
            token=student_token,
            document_id=document_id,
            target_statuses=["REJECTED"],
            timeout_seconds=30,
            interval_seconds=2,
        )
        assert final_status == "REJECTED", f"Expected REJECTED, got {final_status!r}"

        # Verify rejected document is not in reviewer queue anymore
        review_queue_resp = await client.get(
            f"{BASE_URL}/api/v1/review/queue", headers=reviewer_headers
        )
        assert review_queue_resp.status_code == 200, "Failed to fetch review queue"
        queue_ids = {item["document_id"] for item in review_queue_resp.json()}
        assert document_id not in queue_ids, (
            "Rejected document should not appear in the review queue"
        )


# ---------------------------------------------------------------------------
# Test: Full acceptance flow
# ---------------------------------------------------------------------------


@pytest.mark.e2e
@pytest.mark.skipif(not RUN_E2E, reason="Set RUN_E2E=1 to run full E2E acceptance flow")
@pytest.mark.asyncio
async def test_full_acceptance_flow() -> None:
    """Upload → evaluate → review → index → tutor/mindmap/mock-test with deep validation."""
    async with httpx.AsyncClient(timeout=120) as client:

        # ------------------------------------------------------------------
        # Step 1–3: Setup (admin login, course, reviewer)
        # ------------------------------------------------------------------
        admin_token = await _login(client, _ADMIN_EMAIL)
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        await _ensure_course_and_reviewer(client, admin_headers)

        # ------------------------------------------------------------------
        # Step 4–5: Student uploads community document
        # ------------------------------------------------------------------
        student_token = await _login(client, _STUDENT_EMAIL)
        student_headers = {"Authorization": f"Bearer {student_token}"}
        document_id = await _upload_community_doc(client, student_headers)

        # ------------------------------------------------------------------
        # Step 6: Poll until NEEDS_REVIEW / APPROVED / FAILED
        # ------------------------------------------------------------------
        intermediate_status = await _poll_document_status(
            client=client,
            token=student_token,
            document_id=document_id,
            target_statuses=["NEEDS_REVIEW", "APPROVED", "FAILED"],
            timeout_seconds=300,
        )
        assert intermediate_status != "FAILED", (
            f"Document {document_id} entered FAILED state after upload."
        )

        # ------------------------------------------------------------------
        # Step 6b: Verify evaluation report structure (when NEEDS_REVIEW)
        # ------------------------------------------------------------------
        if intermediate_status == "NEEDS_REVIEW":
            eval_resp = await client.get(
                f"{BASE_URL}/api/v1/documents/{document_id}/evaluation-report",
                headers=admin_headers,
            )
            assert eval_resp.status_code == 200, (
                f"Evaluation report fetch failed: {eval_resp.text}"
            )
            eval_data = eval_resp.json()
            if eval_data:
                for key in ("agent1_output", "agent3_output"):
                    assert key in eval_data, f"Evaluation report missing {key!r}"
                agent3 = eval_data["agent3_output"]
                assert agent3.get("recommendation") in ("APPROVE", "NEEDS_REVIEW", "REJECT"), (
                    f"agent3.recommendation invalid: {agent3.get('recommendation')!r}"
                )
                scores = agent3.get("scores", {})
                for score_key in ("relevance", "completeness", "quality"):
                    assert isinstance(scores.get(score_key), (int, float)), (
                        f"agent3.scores.{score_key} missing or non-numeric: {scores}"
                    )
                    assert 0 <= float(scores[score_key]) <= 10, (
                        f"agent3.scores.{score_key} out of [0, 10]: {scores[score_key]}"
                    )

        # ------------------------------------------------------------------
        # Step 7: Reviewer approves
        # ------------------------------------------------------------------
        if intermediate_status == "NEEDS_REVIEW":
            reviewer_token = await _login(client, _REVIEWER_EMAIL)
            reviewer_headers = {"Authorization": f"Bearer {reviewer_token}"}
            decide_resp = await client.post(
                f"{BASE_URL}/api/v1/review/{document_id}/decide",
                json={
                    "decision": "APPROVE",
                    "final_contribution_type": "summary_note",
                    "note": "Approved by E2E acceptance test",
                },
                headers=reviewer_headers,
            )
            assert decide_resp.status_code in (200, 201), (
                f"Review decision failed: {decide_resp.text}"
            )

        # ------------------------------------------------------------------
        # Step 8: Poll until INDEXED
        # ------------------------------------------------------------------
        await _poll_document_status(
            client=client,
            token=student_token,
            document_id=document_id,
            target_statuses=["INDEXED"],
            timeout_seconds=120,
        )

        # ------------------------------------------------------------------
        # Step 9: Tutor query with deep citation validation
        # ------------------------------------------------------------------
        tutor_resp = await client.post(
            f"{BASE_URL}/api/v1/tutor/query",
            json={"course_code": _TEST_COURSE, "question": "What is the definition of machine learning according to Mitchell?"},
            headers=student_headers,
        )
        assert tutor_resp.status_code == 200, f"Tutor query failed: {tutor_resp.text}"
        tutor_data = tutor_resp.json()

        assert "answer" in tutor_data, f"Tutor response missing 'answer': {tutor_data}"
        assert isinstance(tutor_data["answer"], str) and tutor_data["answer"].strip(), (
            "Tutor 'answer' is empty"
        )

        citations = tutor_data.get("citations") or []
        assert len(citations) > 0, (
            f"Expected ≥1 citation in tutor response, got none. "
            f"Answer: {tutor_data['answer']!r}"
        )
        for i, citation in enumerate(citations):
            # chunk_id must be present and a valid UUID
            assert "chunk_id" in citation, f"citation[{i}] missing 'chunk_id': {citation}"
            assert citation["chunk_id"], f"citation[{i}].chunk_id is empty"
            _assert_valid_uuid(str(citation["chunk_id"]), f"citation[{i}].chunk_id")

            # excerpt / snippet must be non-empty text
            excerpt = citation.get("excerpt") or citation.get("snippet") or ""
            assert isinstance(excerpt, str) and excerpt.strip(), (
                f"citation[{i}] has empty excerpt/snippet: {citation}"
            )

            # document_id in citation (if present) must also be a valid UUID
            if "document_id" in citation and citation["document_id"]:
                _assert_valid_uuid(str(citation["document_id"]), f"citation[{i}].document_id")

        # ------------------------------------------------------------------
        # Step 10: Mindmap generation
        # ------------------------------------------------------------------
        mindmap_resp = await client.post(
            f"{BASE_URL}/api/v1/courses/{_TEST_COURSE}/mindmap/generate",
            headers=admin_headers,
        )
        assert mindmap_resp.status_code == 200, (
            f"Mindmap generation failed: {mindmap_resp.text}"
        )
        mindmap_data = mindmap_resp.json()
        assert "concept_graph" in mindmap_data, (
            f"Mindmap response missing 'concept_graph': {mindmap_data}"
        )
        concept_graph = mindmap_data["concept_graph"]
        assert "nodes" in concept_graph and isinstance(concept_graph["nodes"], list), (
            f"concept_graph.nodes missing or not a list: {concept_graph}"
        )
        assert "edges" in concept_graph and isinstance(concept_graph["edges"], list), (
            f"concept_graph.edges missing or not a list: {concept_graph}"
        )

        # ------------------------------------------------------------------
        # Step 11: Mock test generation
        # ------------------------------------------------------------------
        mock_resp = await client.post(
            f"{BASE_URL}/api/v1/courses/{_TEST_COURSE}/mock-tests/generate",
            json={
                "total_questions": 3,
                "difficulty_distribution": {"easy": 1, "medium": 1, "hard": 1},
            },
            headers=student_headers,
        )
        assert mock_resp.status_code == 200, (
            f"Mock test generation failed: {mock_resp.text}"
        )
        mock_data = mock_resp.json()
        assert "test_run_id" in mock_data, (
            f"Mock test response missing 'test_run_id': {mock_data}"
        )
        _assert_valid_uuid(str(mock_data["test_run_id"]), "mock_data.test_run_id")
        assert "questions" in mock_data and isinstance(mock_data["questions"], list), (
            f"Mock test response 'questions' missing or not a list: {mock_data}"
        )

        # Verify mock test can be retrieved by test_run_id
        test_run_id = mock_data["test_run_id"]
        get_mock_resp = await client.get(
            f"{BASE_URL}/api/v1/courses/{_TEST_COURSE}/mock-tests/{test_run_id}",
            headers=student_headers,
        )
        assert get_mock_resp.status_code == 200, (
            f"Failed to retrieve mock test by test_run_id: {get_mock_resp.text}"
        )

        # ------------------------------------------------------------------
        # Step 12: All steps passed
        # ------------------------------------------------------------------
        # If we reach here, the entire flow succeeded including citation
        # validation, mindmap, and mock test.


@pytest.mark.e2e
@pytest.mark.skipif(not RUN_E2E, reason="Set RUN_E2E=1 to run E2E tests")
@pytest.mark.asyncio
async def test_manage_status_filter_matches_review_queue_count() -> None:
    """/documents/manage?status=NEEDS_REVIEW must match /review/queue exactly.

    Regression test for the 2026-07-07 user feedback finding: the status query
    param was silently ignored, so /documents/manage returned every document
    regardless of the filter while /review/queue correctly scoped to
    NEEDS_REVIEW only.
    """
    async with httpx.AsyncClient() as client:
        token = await _login(client, _REVIEWER_EMAIL)
        headers = {"Authorization": f"Bearer {token}"}

        queue_resp = await client.get(f"{BASE_URL}/api/v1/review/queue", headers=headers)
        assert queue_resp.status_code == 200
        queue_ids = {d["document_id"] for d in queue_resp.json()}

        manage_resp = await client.get(
            f"{BASE_URL}/api/v1/documents/manage",
            params={"status": "NEEDS_REVIEW"},
            headers=headers,
        )
        assert manage_resp.status_code == 200
        manage_docs = manage_resp.json()

        assert {d["id"] for d in manage_docs} == queue_ids
        assert all(d["status"] == "NEEDS_REVIEW" for d in manage_docs)
