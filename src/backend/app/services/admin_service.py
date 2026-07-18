from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.state_machine import DocumentStateMachine, log_admin_action
from app.models import AdminAuditLog, Document, EvaluationJob, ProcessingJob, User
from app.models.enums import DocumentStatus, JobStatus, ProcessingJobType


async def get_failed_documents(session: AsyncSession) -> list[dict[str, Any]]:
    """Get all failed documents with failure details."""
    docs = await session.scalars(
        select(Document)
        .where(Document.status == DocumentStatus.FAILED)
        .options(selectinload(Document.processing_jobs), selectinload(Document.evaluation_jobs))
    )
    results = []
    for doc in docs.all():
        failed_ocr = next(
            (
                j
                for j in doc.processing_jobs
                if j.job_type == ProcessingJobType.OCR and j.is_latest and j.status == JobStatus.FAILED
            ),
            None,
        )
        failed_index = next(
            (
                j
                for j in doc.processing_jobs
                if j.job_type == ProcessingJobType.INDEX and j.is_latest and j.status == JobStatus.FAILED
            ),
            None,
        )
        failed_eval = next(
            (j for j in doc.evaluation_jobs if j.is_latest and j.status == JobStatus.FAILED),
            None,
        )

        job = failed_ocr or failed_index or failed_eval
        results.append({
            "document_id": str(doc.id),
            "original_filename": doc.original_filename,
            "failure_reason": job.failure_reason if job else None,
            "raw_failure_output": job.raw_failure_output if job else None,
            "attempt_count": job.attempt_count if job else 0,
            "failed_at": job.completed_at if job else None,
            "job_type": (
                "ocr" if failed_ocr else
                "index" if failed_index else
                "eval" if failed_eval else "unknown"
            ),
        })
    return results


async def reprocess_document(
    session: AsyncSession,
    document_id: UUID,
    from_state: str,
    actor_user: User,
) -> Document:
    """Admin reprocess: reset failed document to PARSING or EVALUATING."""
    valid_from = {"PARSING", "EVALUATING"}
    if from_state not in valid_from:
        raise HTTPException(status_code=422, detail=f"from_state must be one of {valid_from}")

    doc = await session.scalar(
        select(Document).where(Document.id == document_id).with_for_update()
    )
    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found")
    if doc.status not in {DocumentStatus.FAILED, DocumentStatus.REJECTED}:
        raise HTTPException(status_code=409, detail="Only FAILED or REJECTED documents can be reprocessed")

    doc.permanently_failed = False
    original_state = doc.status.value
    target_state = DocumentStatus.PARSING if from_state == "PARSING" else DocumentStatus.EVALUATING

    sm = DocumentStateMachine(session)
    await sm.transition(doc, target_state, actor=actor_user, reason="Admin reprocess")
    enqueue_kind: str
    enqueue_job_id: UUID

    if from_state == "PARSING":
        old_jobs = await session.scalars(
            select(ProcessingJob).where(
                ProcessingJob.document_id == document_id,
                ProcessingJob.job_type == ProcessingJobType.OCR,
            )
        )
        max_run = 0
        for pj in old_jobs.all():
            pj.is_latest = False
            max_run = max(max_run, pj.run_number)

        new_job = ProcessingJob(
            document_id=document_id,
            job_type=ProcessingJobType.OCR,
            run_number=max_run + 1,
            is_latest=True,
            status=JobStatus.PENDING,
        )
        session.add(new_job)
        await session.flush()
        enqueue_kind = "ocr"
        enqueue_job_id = new_job.id
    else:
        old_eval_jobs = await session.scalars(
            select(EvaluationJob).where(EvaluationJob.document_id == document_id)
        )
        max_run = 0
        for ej in old_eval_jobs.all():
            ej.is_latest = False
            max_run = max(max_run, ej.run_number)

        new_eval_job = EvaluationJob(
            document_id=document_id,
            run_number=max_run + 1,
            is_latest=True,
            status=JobStatus.PENDING,
        )
        session.add(new_eval_job)
        await session.flush()
        enqueue_kind = "eval"
        enqueue_job_id = new_eval_job.id

    await log_admin_action(
        session,
        actor_id=actor_user.id,
        action_type="reprocess",
        target_entity_type="document",
        target_entity_id=doc.id,
        from_state=original_state,
        to_state=target_state.value,
        reason=f"Admin reprocess from {from_state}",
    )

    await session.commit()
    await session.refresh(doc)

    try:
        if enqueue_kind == "ocr":
            from app.workers.jobs import enqueue_ocr_job
            await enqueue_ocr_job(session, doc.id, enqueue_job_id)
        else:
            from app.workers.jobs import enqueue_eval_job
            await enqueue_eval_job(session, doc.id, enqueue_job_id)
    except Exception:
        pass

    return doc


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


async def get_audit_log(
    session: AsyncSession,
    page: int = 1,
    page_size: int = 50,
    actor_id: UUID | None = None,
    action_type: str | None = None,
    target_entity_id: UUID | None = None,
) -> tuple[list[AdminAuditLog], int]:
    q = select(AdminAuditLog)
    count_q = select(func.count()).select_from(AdminAuditLog)

    if actor_id:
        q = q.where(AdminAuditLog.actor_id == actor_id)
        count_q = count_q.where(AdminAuditLog.actor_id == actor_id)
    if action_type:
        q = q.where(AdminAuditLog.action_type == action_type)
        count_q = count_q.where(AdminAuditLog.action_type == action_type)
    if target_entity_id:
        q = q.where(AdminAuditLog.target_entity_id == target_entity_id)
        count_q = count_q.where(AdminAuditLog.target_entity_id == target_entity_id)

    total = await session.scalar(count_q) or 0
    q = q.order_by(AdminAuditLog.logged_at.desc()).offset((page - 1) * page_size).limit(page_size)
    logs = await session.scalars(q)
    return list(logs.all()), total


async def get_seed_status(session: AsyncSession, course_code: str) -> dict[str, Any]:
    from app.models import Course
    course = await session.scalar(select(Course).where(Course.code == course_code))
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    has_seed = bool(course.topic_summary and course.topic_summary.strip())
    approved_count = (
        await session.scalar(
            select(func.count()).select_from(Document).where(
                Document.course_id == course.id,
                Document.status.in_([DocumentStatus.APPROVED, DocumentStatus.INDEXING, DocumentStatus.INDEXED]),
            )
        )
    ) or 0

    return {
        "course_code": course_code,
        "has_seed": has_seed,
        "approved_doc_count": approved_count,
        "is_cold_start": approved_count < 3,
    }
