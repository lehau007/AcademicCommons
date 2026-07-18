from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.models.enums import ContributionType, DocumentStatus, DocumentTier, FileFormat
from app.models.tables import Document, EvaluationReport, User
from app.schemas.review import ReviewDecideRequest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_user(role: str = "reviewer") -> User:
    return User(
        id=uuid4(),
        email=f"{role}@example.test",
        hashed_password="hash",
        role=role,
        full_name=f"{role.title()} User",
    )


def make_document(status: DocumentStatus = DocumentStatus.NEEDS_REVIEW) -> Document:
    return Document(
        id=uuid4(),
        course_id=uuid4(),
        uploader_id=uuid4(),
        document_tier=DocumentTier.COMMUNITY,
        contribution_type=ContributionType.SUMMARY_NOTE,
        status=status,
        original_filename="test.pdf",
        file_format=FileFormat.PDF,
    )


def make_eval_report(doc: Document) -> EvaluationReport:
    return EvaluationReport(
        id=uuid4(),
        document_id=doc.id,
        evaluation_job_id=uuid4(),
        is_latest=True,
        agent1_output={"quality": "high"},
        agent2_output={"relevance": 8},
        agent3_output={"suggested_contribution_type": "summary_note"},
        final_recommendation="APPROVE",
    )


class FakeSession:
    """Minimal async session stub for pure-logic unit tests."""

    def __init__(self) -> None:
        self.added: list[object] = []
        self.flush_count = 0
        self.commit_count = 0
        self._scalar_map: dict = {}

    def add(self, item: object) -> None:
        self.added.append(item)

    async def flush(self) -> None:
        self.flush_count += 1

    async def commit(self) -> None:
        self.commit_count += 1

    async def refresh(self, item: object) -> None:
        pass

    async def scalar(self, query) -> object:
        return None

    async def scalars(self, query):
        result = MagicMock()
        result.all.return_value = []
        return result


# ---------------------------------------------------------------------------
# B.5 Review service validation tests (pure logic — no DB needed)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_review_decide_validates_note_required_for_override() -> None:
    """OVERRIDE_APPROVE and OVERRIDE_REJECT require a non-empty note."""
    from fastapi import HTTPException

    from app.services import review_service

    doc = make_document(DocumentStatus.NEEDS_REVIEW)
    eval_report = make_eval_report(doc)

    payload = ReviewDecideRequest(
        decision="OVERRIDE_APPROVE",
        final_contribution_type="summary_note",
        note=None,  # missing note — should fail
    )

    session = FakeSession()

    # For admin user the call order is:
    #   1. doc (SELECT FOR UPDATE)
    #   2. eval_report (latest)
    #   3. existing review decision (None → no conflict)
    # The override-note check fires after step 3.
    call_count = 0

    async def fake_scalar(query):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return doc          # document with_for_update
        if call_count == 2:
            return eval_report  # latest eval report
        if call_count == 3:
            return None         # existing review decision (none → FCFS passes)
        return None

    session.scalar = fake_scalar

    admin_user = make_user("admin")

    with pytest.raises(HTTPException) as exc_info:
        await review_service.decide_review(session, doc.id, payload, admin_user)

    assert exc_info.value.status_code == 422
    assert "note required" in exc_info.value.detail.lower()


@pytest.mark.asyncio
async def test_review_decide_validates_final_contribution_type_on_approve() -> None:
    """APPROVE without final_contribution_type must raise HTTP 422."""
    from fastapi import HTTPException

    from app.services import review_service

    doc = make_document(DocumentStatus.NEEDS_REVIEW)
    eval_report = make_eval_report(doc)
    admin_user = make_user("admin")

    payload = ReviewDecideRequest(
        decision="APPROVE",
        final_contribution_type=None,  # missing — must fail
        note="some note",
    )

    session = FakeSession()
    call_count = 0

    # Admin call order:
    #   1. doc (SELECT FOR UPDATE)
    #   2. eval_report (latest)
    #   3. existing review decision (None)
    # approve-without-final_ct check fires after step 3.
    async def fake_scalar(query):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return doc          # document SELECT FOR UPDATE
        if call_count == 2:
            return eval_report  # latest eval report
        if call_count == 3:
            return None         # existing review decision (none)
        return None

    session.scalar = fake_scalar

    with pytest.raises(HTTPException) as exc_info:
        await review_service.decide_review(session, doc.id, payload, admin_user)

    assert exc_info.value.status_code == 422
    assert "final_contribution_type" in exc_info.value.detail


# ---------------------------------------------------------------------------
# Batch approve (quick approve) tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_batch_approve_is_atomic_on_error() -> None:
    """If any document cannot be approved, none are committed and a 409 lists errors."""
    from fastapi import HTTPException

    from app.services import review_service

    session = FakeSession()
    session.scalar = AsyncMock(return_value=None)  # doc not in NEEDS_REVIEW
    admin_user = make_user("admin")

    with pytest.raises(HTTPException) as exc_info:
        await review_service.batch_approve_documents(session, [uuid4()], admin_user)

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail["errors"]  # per-document error list present
    assert session.commit_count == 0  # nothing committed


def test_batch_approve_request_rejects_empty_list() -> None:
    """The request schema requires at least one document id."""
    import pydantic

    from app.schemas.review import BatchApproveRequest

    with pytest.raises(pydantic.ValidationError):
        BatchApproveRequest(document_ids=[])


# ---------------------------------------------------------------------------
# B.6 Vote service validation tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_vote_validates_vote_value() -> None:
    """cast_vote must reject values other than 'up', 'down', or None."""
    from fastapi import HTTPException

    from app.services.vote_service import cast_vote

    session = FakeSession()
    user = make_user("student")
    document_id = uuid4()

    with pytest.raises(HTTPException) as exc_info:
        await cast_vote(session, document_id, "sideways", user)

    assert exc_info.value.status_code == 422
    assert "vote" in exc_info.value.detail.lower()


@pytest.mark.asyncio
@pytest.mark.parametrize("valid_vote", ["up", "down", None])
async def test_vote_accepts_valid_values(valid_vote: str | None) -> None:
    """cast_vote should accept 'up', 'down', and None without a validation error."""
    from app.models.enums import DocumentStatus
    from app.services.vote_service import cast_vote

    doc = make_document(DocumentStatus.INDEXED)
    user = make_user("student")

    calls: list[int] = [0]

    async def fake_scalar(query):
        calls[0] += 1
        if calls[0] == 1:
            return doc   # document lookup
        return None      # no existing CommunityVote

    async def fake_commit() -> None:
        pass

    async def fake_refresh(item) -> None:
        pass

    session = FakeSession()
    session.scalar = fake_scalar
    session.commit = fake_commit
    session.refresh = fake_refresh

    cv = await cast_vote(session, doc.id, valid_vote, user)
    assert cv.vote == valid_vote


# ---------------------------------------------------------------------------
# B.6 Contribution points formula test
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_award_contribution_points_formula() -> None:
    """summary_note with relevance_score=7.0 should yield 7.0 points (10 * 7/10)."""
    from app.models.tables import ContributionScore
    from app.services.vote_service import award_contribution_points

    session = FakeSession()
    user_id = uuid4()
    course_id = uuid4()

    # No existing score
    session.scalar = AsyncMock(return_value=None)

    await award_contribution_points(
        session,
        user_id=user_id,
        course_id=course_id,
        contribution_type="summary_note",
        relevance_score=7.0,
    )

    assert session.flush_count == 1
    assert len(session.added) == 1
    added = session.added[0]
    assert isinstance(added, ContributionScore)
    assert added.points == pytest.approx(7.0)


@pytest.mark.asyncio
async def test_award_contribution_points_accumulates() -> None:
    """When a ContributionScore already exists, points are added to the existing total."""
    from app.models.tables import ContributionScore
    from app.services.vote_service import award_contribution_points

    existing_score = ContributionScore(
        id=uuid4(),
        user_id=uuid4(),
        course_id=uuid4(),
        points=5.0,
    )

    session = FakeSession()
    session.scalar = AsyncMock(return_value=existing_score)

    await award_contribution_points(
        session,
        user_id=existing_score.user_id,
        course_id=existing_score.course_id,
        contribution_type="past_exam",
        relevance_score=10.0,
    )

    # 7.0 (past_exam base) * (10/10) = 7.0, added to 5.0 = 12.0
    assert existing_score.points == pytest.approx(12.0)
    assert session.flush_count == 1
    assert session.added == []  # existing was mutated, not added
