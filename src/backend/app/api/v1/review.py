from __future__ import annotations

import csv
import io
from datetime import UTC, datetime, timedelta
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.auth import require_role
from app.db.session import get_session
from app.models import (
    Course,
    CourseReviewerAssignment,
    Document,
    DocumentStateLog,
    DocumentStatus,
    EvaluationReport,
    ReviewDecision,
    User,
)
from app.schemas.courses import CourseRead
from app.schemas.review import (
    BatchApproveRequest,
    BatchApproveResponse,
    ReviewAnalyticsResponse,
    ReviewDecideRequest,
    ReviewDecisionRead,
    ReviewDetailResponse,
    ReviewQueueItem,
)
from app.services import review_service

router = APIRouter(prefix="/review", tags=["review"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]
ReviewerOrAdminDep = Annotated[User, Depends(require_role("reviewer", "admin"))]


@router.get("/queue", response_model=list[ReviewQueueItem])
async def get_review_queue(
    session: SessionDep,
    user: ReviewerOrAdminDep,
) -> list[ReviewQueueItem]:
    """List documents in NEEDS_REVIEW visible to the current user."""
    docs = await review_service.get_review_queue(session, user)
    return [
        ReviewQueueItem(
            document_id=doc.id,
            filename=doc.original_filename,
            course_code=doc.course.code,
            document_tier=doc.document_tier.value,
            status=doc.status.value,
            sla_deadline=doc.sla_deadline,
            sla_breached=doc.sla_breached,
            no_reviewer_flag=doc.no_reviewer_flag,
            uploaded_at=doc.uploaded_at,
        )
        for doc in docs
    ]


@router.get("/my-courses", response_model=list[CourseRead])
async def get_uploadable_courses(
    session: SessionDep,
    user: ReviewerOrAdminDep,
) -> list[CourseRead]:
    """List active courses the current user may upload official documents to.

    Admins may upload to every active course; reviewers only to courses they
    have an active assignment for.
    """
    stmt = select(Course).where(Course.is_active.is_(True))
    if user.role == "reviewer":
        stmt = stmt.join(
            CourseReviewerAssignment,
            CourseReviewerAssignment.course_id == Course.id,
        ).where(
            CourseReviewerAssignment.user_id == user.id,
            CourseReviewerAssignment.is_active.is_(True),
        )
    stmt = stmt.order_by(Course.code)
    courses = (await session.execute(stmt)).scalars().all()
    return [CourseRead.model_validate(c) for c in courses]


@router.get("/analytics", response_model=ReviewAnalyticsResponse)
async def get_reviewer_analytics(
    session: SessionDep,
    _: ReviewerOrAdminDep,
) -> ReviewAnalyticsResponse:
    """Get reviewer metrics, including real SLA resolution time per course and AI override/agreement rates."""
    # 1. Configured SLA threshold hours per course (the target, not actual time)
    courses_result = await session.execute(select(Course).where(Course.is_active.is_(True)))
    courses = courses_result.scalars().all()
    sla_threshold_hours_per_course = {c.code: float(c.review_sla_hours) for c in courses}

    # 1b. Real average resolution time (last 7 days) per course.
    week_ago = datetime.now(UTC) - timedelta(days=7)
    recent_query = (
        select(ReviewDecision, EvaluationReport, Document, Course)
        .join(EvaluationReport, ReviewDecision.evaluation_report_id == EvaluationReport.id)
        .join(Document, EvaluationReport.document_id == Document.id)
        .join(Course, Document.course_id == Course.id)
        .where(ReviewDecision.decided_at >= week_ago)
    )
    recent_rows = (await session.execute(recent_query)).all()

    # Batch-load NEEDS_REVIEW state logs for all involved documents (avoid N+1).
    document_ids = {doc.id for _, _, doc, _ in recent_rows}
    needs_review_logs: dict[UUID, list[DocumentStateLog]] = {}
    if document_ids:
        logs_query = (
            select(DocumentStateLog)
            .where(
                DocumentStateLog.document_id.in_(document_ids),
                DocumentStateLog.to_state == DocumentStatus.NEEDS_REVIEW,
            )
            .order_by(DocumentStateLog.transitioned_at)
        )
        for log in (await session.execute(logs_query)).scalars().all():
            needs_review_logs.setdefault(log.document_id, []).append(log)

    resolution_hours_by_course: dict[str, list[float]] = {}
    for decision, _report, doc, course in recent_rows:
        # Determine when the document entered review: latest NEEDS_REVIEW log <= decided_at.
        entered_review_at: datetime | None = None
        for log in needs_review_logs.get(doc.id, []):
            if log.transitioned_at <= decision.decided_at:
                entered_review_at = log.transitioned_at
        # Fallback: derive from sla_deadline minus the configured threshold.
        if entered_review_at is None and doc.sla_deadline is not None:
            entered_review_at = doc.sla_deadline - timedelta(hours=course.review_sla_hours)
        if entered_review_at is None:
            continue
        resolution_hours = (decision.decided_at - entered_review_at).total_seconds() / 3600.0
        resolution_hours_by_course.setdefault(course.code, []).append(resolution_hours)

    average_sla_hours_per_course = {
        code: sum(values) / len(values)
        for code, values in resolution_hours_by_course.items()
    }

    # 2. AI override/agreement rates
    query = select(ReviewDecision).options(selectinload(ReviewDecision.evaluation_report))
    result = await session.execute(query)
    decisions = result.scalars().all()

    total = len(decisions)
    if total == 0:
        agreement_rate = 0.0
        override_rate = 0.0
    else:
        override_count = 0
        agreement_count = 0
        for d in decisions:
            ai_rec = d.evaluation_report.final_recommendation
            is_approval = d.decision in {"APPROVE", "OVERRIDE_APPROVE"}
            is_rejection = d.decision in {"REJECT", "OVERRIDE_REJECT"}
            is_explicit_override = d.decision in {"OVERRIDE_APPROVE", "OVERRIDE_REJECT"}
            
            contradicts_ai = (is_approval and ai_rec == "REJECT") or (is_rejection and ai_rec == "APPROVE")
            
            if is_explicit_override or contradicts_ai:
                override_count += 1
            else:
                agreement_count += 1

        agreement_rate = float(agreement_count) / total
        override_rate = float(override_count) / total

    return ReviewAnalyticsResponse(
        average_sla_hours_per_course=average_sla_hours_per_course,
        sla_threshold_hours_per_course=sla_threshold_hours_per_course,
        ai_agreement_rate=agreement_rate,
        ai_override_rate=override_rate,
    )


@router.post("/batch-approve", response_model=BatchApproveResponse, status_code=201)
async def batch_approve(
    payload: BatchApproveRequest,
    session: SessionDep,
    user: ReviewerOrAdminDep,
) -> BatchApproveResponse:
    """Approve multiple NEEDS_REVIEW documents in one atomic operation.

    Intended for the reviewer "quick approve" action on high-AI-score documents.
    If any document cannot be approved, none are changed (409 with per-doc errors).
    """
    result = await review_service.batch_approve_documents(
        session, payload.document_ids, user, note=payload.note
    )
    return BatchApproveResponse(approved=result["approved"], count=result["count"])


_EXPORT_COLUMNS = [
    "decided_at",
    "document_id",
    "filename",
    "course_code",
    "document_tier",
    "uploaded_at",
    "decision",
    "final_contribution_type",
    "reviewer_id",
    "note",
]


@router.get("/decisions/export")
async def export_decisions(
    session: SessionDep,
    user: ReviewerOrAdminDep,
    date_from: datetime | None = Query(default=None, alias="from"),
    date_to: datetime | None = Query(default=None, alias="to"),
) -> StreamingResponse:
    """Export review decisions in a date range as CSV for monthly reporting."""
    rows = await review_service.get_decision_export_rows(session, user, date_from, date_to)

    buffer = io.StringIO()
    buffer.write("﻿")  # UTF-8 BOM so Excel renders Vietnamese correctly
    writer = csv.DictWriter(buffer, fieldnames=_EXPORT_COLUMNS)
    writer.writeheader()
    writer.writerows(rows)
    buffer.seek(0)

    stamp = datetime.now(UTC).strftime("%Y%m%d")
    filename = f"review-decisions-{stamp}.csv"
    return StreamingResponse(
        iter([buffer.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/{document_id}", response_model=ReviewDetailResponse)
async def get_review_detail(
    document_id: UUID,
    session: SessionDep,
    user: ReviewerOrAdminDep,
) -> ReviewDetailResponse:
    """Get full review interface data for a document."""
    data = await review_service.get_review_detail(session, document_id, user)
    return ReviewDetailResponse(**data)


@router.post("/{document_id}/decide", response_model=ReviewDecisionRead, status_code=201)
async def decide_review(
    document_id: UUID,
    payload: ReviewDecideRequest,
    session: SessionDep,
    user: ReviewerOrAdminDep,
) -> ReviewDecisionRead:
    """Submit a review decision for a document."""
    decision = await review_service.decide_review(session, document_id, payload, user)
    return ReviewDecisionRead(
        id=decision.id,
        document_id=document_id,
        decision=decision.decision,
        final_contribution_type=decision.final_contribution_type.value if decision.final_contribution_type else None,
        note=decision.note,
        decided_at=decision.decided_at,
    )
