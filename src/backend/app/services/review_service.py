from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.state_machine import DocumentStateMachine, log_admin_action
from app.models import (
    Course,
    CourseReviewerAssignment,
    Document,
    EvaluationReport,
    ProcessingJob,
    ReviewDecision,
    User,
)
from app.models.enums import ContributionType, DocumentStatus, JobStatus, ProcessingJobType
from app.schemas.review import ReviewDecideRequest


async def get_review_queue(session: AsyncSession, user: User) -> list[Document]:
    """Get documents in NEEDS_REVIEW visible to the user."""
    q = (
        select(Document)
        .where(Document.status == DocumentStatus.NEEDS_REVIEW)
        .options(selectinload(Document.course))
    )
    if user.role == "reviewer":
        assigned_courses = await session.scalars(
            select(CourseReviewerAssignment.course_id).where(
                CourseReviewerAssignment.user_id == user.id,
                CourseReviewerAssignment.is_active.is_(True),
            )
        )
        course_ids = list(assigned_courses)
        if not course_ids:
            return []
        q = q.where(Document.course_id.in_(course_ids))
    result = await session.scalars(q)
    return list(result.all())


async def get_review_detail(session: AsyncSession, document_id: UUID, user: User) -> dict[str, Any]:
    """Get full review interface data."""
    doc = await session.scalar(
        select(Document)
        .where(Document.id == document_id)
        .options(
            selectinload(Document.course),
            selectinload(Document.state_logs),
            selectinload(Document.evaluation_reports),
        )
    )
    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found")

    if user.role == "reviewer":
        await _assert_reviewer_can_review(session, user, doc.course_id)

    eval_report = None
    if doc.evaluation_reports:
        latest_report = max(doc.evaluation_reports, key=lambda r: r.generated_at)
        eval_report = {
            "id": str(latest_report.id),
            "agent1_output": latest_report.agent1_output,
            "agent2_output": latest_report.agent2_output,
            "agent3_output": latest_report.agent3_output,
            "final_recommendation": latest_report.final_recommendation,
        }

    return {
        "document_id": doc.id,
        "course_code": doc.course.code,
        "document_tier": doc.document_tier.value,
        "status": doc.status.value,
        "evaluation_report": eval_report,
        "state_logs": [
            {
                "from_state": str(log.from_state),
                "to_state": str(log.to_state),
                "actor_type": log.actor_type,
                "transitioned_at": str(log.transitioned_at),
            }
            for log in doc.state_logs
        ],
    }


async def _assert_reviewer_can_review(session: AsyncSession, user: User, course_id: UUID) -> None:
    assignment = await session.scalar(
        select(CourseReviewerAssignment).where(
            CourseReviewerAssignment.user_id == user.id,
            CourseReviewerAssignment.course_id == course_id,
            CourseReviewerAssignment.is_active.is_(True),
        )
    )
    if assignment is None:
        raise HTTPException(status_code=403, detail="Not assigned to this course")


async def decide_review(
    session: AsyncSession,
    document_id: UUID,
    payload: ReviewDecideRequest,
    user: User,
) -> ReviewDecision:
    """Process review decision with FCFS locking."""
    valid_decisions = {"APPROVE", "REJECT", "OVERRIDE_APPROVE", "OVERRIDE_REJECT"}
    if payload.decision not in valid_decisions:
        raise HTTPException(status_code=422, detail=f"Invalid decision. Must be one of {valid_decisions}")

    doc = await session.scalar(
        select(Document)
        .where(Document.id == document_id, Document.status == DocumentStatus.NEEDS_REVIEW)
        .with_for_update()
    )
    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found in NEEDS_REVIEW state")

    if user.role == "reviewer":
        await _assert_reviewer_can_review(session, user, doc.course_id)

    eval_report = await session.scalar(
        select(EvaluationReport).where(
            EvaluationReport.document_id == document_id,
            EvaluationReport.is_latest.is_(True),
        )
    )
    if eval_report is None:
        raise HTTPException(status_code=409, detail="No evaluation report found for this document")

    existing = await session.scalar(
        select(ReviewDecision).where(ReviewDecision.evaluation_report_id == eval_report.id)
    )
    if existing is not None:
        raise HTTPException(status_code=409, detail="Document already reviewed (FCFS)")

    approve_decisions = {"APPROVE", "OVERRIDE_APPROVE"}
    if payload.decision in approve_decisions and payload.final_contribution_type is None:
        raise HTTPException(status_code=422, detail="final_contribution_type required for approval")

    # A note is required when the decision contradicts the AI recommendation OR when the
    # client explicitly signals an override. This prevents bypassing the note by sending
    # "APPROVE" instead of "OVERRIDE_APPROVE" when the AI recommended "REJECT".
    ai_rec = eval_report.final_recommendation  # "APPROVE", "NEEDS_REVIEW", or "REJECT"
    is_approval = payload.decision in approve_decisions
    is_rejection = payload.decision in {"REJECT", "OVERRIDE_REJECT"}
    contradicts_ai = (is_approval and ai_rec == "REJECT") or (is_rejection and ai_rec == "APPROVE")
    is_explicit_override = payload.decision in {"OVERRIDE_APPROVE", "OVERRIDE_REJECT"}

    if (contradicts_ai or is_explicit_override) and not payload.note:
        raise HTTPException(status_code=422, detail="note required when overriding AI recommendation")

    if payload.final_contribution_type and eval_report.agent3_output:
        label_verification = eval_report.agent3_output.get("label_verification", {})
        suggested = eval_report.agent3_output.get("suggested_contribution_type") or label_verification.get(
            "suggested_contribution_type"
        )
        if suggested and suggested != payload.final_contribution_type and not payload.note:
            raise HTTPException(status_code=422, detail="note required when changing contribution type")

    final_ct = None
    if payload.final_contribution_type:
        try:
            final_ct = ContributionType(payload.final_contribution_type)
        except ValueError:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid contribution_type: {payload.final_contribution_type}",
            ) from None

    review_decision = ReviewDecision(
        evaluation_report_id=eval_report.id,
        reviewer_id=user.id,
        initial_contribution_type=doc.contribution_type,
        suggested_contribution_type=(
            _suggested_contribution_type(eval_report.agent3_output) if eval_report.agent3_output else None
        ),
        final_contribution_type=final_ct,
        decision=payload.decision,
        note=payload.note,
    )
    session.add(review_decision)

    sm = DocumentStateMachine(session)
    if payload.decision in approve_decisions:
        await sm.transition(doc, DocumentStatus.APPROVED, actor=user, reason=payload.note)
        if final_ct:
            doc.contribution_type = final_ct
        index_job = ProcessingJob(
            document_id=doc.id,
            job_type=ProcessingJobType.INDEX,
            run_number=1,
            is_latest=True,
            status=JobStatus.PENDING,
        )
        session.add(index_job)
    else:
        await sm.transition(doc, DocumentStatus.REJECTED, actor=user, reason=payload.note)

    if user.role == "admin":
        await log_admin_action(
            session,
            actor_id=user.id,
            action_type=f"review_{payload.decision.lower()}",
            target_entity_type="document",
            target_entity_id=doc.id,
            from_state="NEEDS_REVIEW",
            to_state=doc.status.value,
            reason=payload.note,
        )

    await session.flush()
    await session.commit()
    await session.refresh(review_decision)

    if payload.decision in approve_decisions:
        try:
            from app.workers.jobs import enqueue_index_job
            index_job_fresh = await session.scalar(
                select(ProcessingJob).where(
                    ProcessingJob.document_id == doc.id,
                    ProcessingJob.job_type == ProcessingJobType.INDEX,
                    ProcessingJob.is_latest.is_(True),
                )
            )
            if index_job_fresh:
                await enqueue_index_job(session, doc.id, index_job_fresh.id)
        except Exception:
            pass

    return review_decision


async def batch_approve_documents(
    session: AsyncSession,
    document_ids: list[UUID],
    user: User,
    note: str | None = None,
) -> dict[str, Any]:
    """Approve multiple NEEDS_REVIEW documents atomically.

    Used by the reviewer "quick approve" action for high-AI-score documents.
    Validates every document first; if any one cannot be approved, nothing is
    committed and a 409 is raised listing the per-document errors. Each approved
    document keeps the AI-suggested contribution type (falling back to its
    original type) and is queued for indexing.
    """
    contexts: list[tuple[Document, EvaluationReport, ContributionType]] = []
    errors: list[dict[str, str]] = []

    for document_id in document_ids:
        doc = await session.scalar(
            select(Document)
            .where(Document.id == document_id, Document.status == DocumentStatus.NEEDS_REVIEW)
            .with_for_update()
        )
        if doc is None:
            errors.append({"document_id": str(document_id), "error": "Không tồn tại hoặc không ở trạng thái chờ duyệt"})
            continue
        if user.role == "reviewer":
            assignment = await session.scalar(
                select(CourseReviewerAssignment).where(
                    CourseReviewerAssignment.user_id == user.id,
                    CourseReviewerAssignment.course_id == doc.course_id,
                    CourseReviewerAssignment.is_active.is_(True),
                )
            )
            if assignment is None:
                errors.append({"document_id": str(document_id), "error": "Không được phân công môn học này"})
                continue
        eval_report = await session.scalar(
            select(EvaluationReport).where(
                EvaluationReport.document_id == document_id,
                EvaluationReport.is_latest.is_(True),
            )
        )
        if eval_report is None:
            errors.append({"document_id": str(document_id), "error": "Chưa có báo cáo đánh giá"})
            continue
        existing = await session.scalar(
            select(ReviewDecision).where(ReviewDecision.evaluation_report_id == eval_report.id)
        )
        if existing is not None:
            errors.append({"document_id": str(document_id), "error": "Đã được duyệt"})
            continue
        final_ct = (
            _suggested_contribution_type(eval_report.agent3_output) if eval_report.agent3_output else None
        ) or doc.contribution_type
        if final_ct is None:
            errors.append({"document_id": str(document_id), "error": "Không xác định được loại đóng góp"})
            continue
        contexts.append((doc, eval_report, final_ct))

    if errors:
        raise HTTPException(
            status_code=409,
            detail={
                "message": "Một số tài liệu không thể duyệt; không có thay đổi nào được áp dụng.",
                "errors": errors,
            },
        )

    sm = DocumentStateMachine(session)
    for doc, eval_report, final_ct in contexts:
        session.add(
            ReviewDecision(
                evaluation_report_id=eval_report.id,
                reviewer_id=user.id,
                initial_contribution_type=doc.contribution_type,
                suggested_contribution_type=(
                    _suggested_contribution_type(eval_report.agent3_output)
                    if eval_report.agent3_output
                    else None
                ),
                final_contribution_type=final_ct,
                decision="APPROVE",
                note=note,
            )
        )
        await sm.transition(doc, DocumentStatus.APPROVED, actor=user, reason=note)
        doc.contribution_type = final_ct
        session.add(
            ProcessingJob(
                document_id=doc.id,
                job_type=ProcessingJobType.INDEX,
                run_number=1,
                is_latest=True,
                status=JobStatus.PENDING,
            )
        )
        if user.role == "admin":
            await log_admin_action(
                session,
                actor_id=user.id,
                action_type="review_approve",
                target_entity_type="document",
                target_entity_id=doc.id,
                from_state="NEEDS_REVIEW",
                to_state="APPROVED",
                reason=note,
            )

    await session.flush()
    await session.commit()

    approved_ids: list[UUID] = []
    for doc, _report, _ct in contexts:
        approved_ids.append(doc.id)
        try:
            from app.workers.jobs import enqueue_index_job
            index_job = await session.scalar(
                select(ProcessingJob).where(
                    ProcessingJob.document_id == doc.id,
                    ProcessingJob.job_type == ProcessingJobType.INDEX,
                    ProcessingJob.is_latest.is_(True),
                )
            )
            if index_job:
                await enqueue_index_job(session, doc.id, index_job.id)
        except Exception:
            pass

    return {"approved": approved_ids, "count": len(approved_ids)}


async def get_decision_export_rows(
    session: AsyncSession,
    user: User,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> list[dict[str, Any]]:
    """Row-level review-decision records for CSV export, filtered by decision date.

    Admins see every decision; reviewers only decisions on courses they are
    assigned to.
    """
    query = (
        select(ReviewDecision, Document, Course)
        .join(EvaluationReport, ReviewDecision.evaluation_report_id == EvaluationReport.id)
        .join(Document, EvaluationReport.document_id == Document.id)
        .join(Course, Document.course_id == Course.id)
        .order_by(ReviewDecision.decided_at.desc())
    )
    if date_from is not None:
        query = query.where(ReviewDecision.decided_at >= date_from)
    if date_to is not None:
        query = query.where(ReviewDecision.decided_at <= date_to)
    if user.role == "reviewer":
        assigned = await session.scalars(
            select(CourseReviewerAssignment.course_id).where(
                CourseReviewerAssignment.user_id == user.id,
                CourseReviewerAssignment.is_active.is_(True),
            )
        )
        course_ids = list(assigned)
        if not course_ids:
            return []
        query = query.where(Document.course_id.in_(course_ids))

    rows = (await session.execute(query)).all()
    return [
        {
            "decided_at": decision.decided_at.isoformat() if decision.decided_at else "",
            "document_id": str(document.id),
            "filename": document.original_filename,
            "course_code": course.code,
            "document_tier": document.document_tier.value,
            "uploaded_at": document.uploaded_at.isoformat() if document.uploaded_at else "",
            "decision": decision.decision,
            "final_contribution_type": (
                decision.final_contribution_type.value if decision.final_contribution_type else ""
            ),
            "reviewer_id": str(decision.reviewer_id),
            "note": decision.note or "",
        }
        for decision, document, course in rows
    ]


def _suggested_contribution_type(agent3_output: dict[str, Any]) -> ContributionType | None:
    label_verification = agent3_output.get("label_verification", {})
    suggested = agent3_output.get("suggested_contribution_type") or label_verification.get(
        "suggested_contribution_type"
    )
    if not suggested:
        return None
    try:
        return ContributionType(suggested)
    except ValueError:
        return None
