from __future__ import annotations

from collections.abc import Awaitable, Callable
from datetime import UTC, datetime, timedelta
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.models import Document, EvaluationJob, ProcessingJob
from app.models.enums import JobStatus, ProcessingJobType
from app.workers.jobs import enqueue_eval_job, enqueue_index_job, enqueue_ocr_job

PENDING_JOB_RECOVERY_AFTER = timedelta(minutes=10)

ProcessingEnqueuer = Callable[[AsyncSession, UUID, UUID], Awaitable[None]]
EvalEnqueuer = Callable[[AsyncSession, UUID, UUID], Awaitable[None]]


async def recover_stale_pending_jobs(ctx: dict[str, object]) -> dict[str, int]:
    del ctx
    async with AsyncSessionLocal() as session:
        return await recover_stale_pending_jobs_for_session(session)


async def recover_stale_pending_jobs_for_session(
    session: AsyncSession,
    *,
    cutoff: datetime | None = None,
    ocr_enqueuer: ProcessingEnqueuer = enqueue_ocr_job,
    index_enqueuer: ProcessingEnqueuer = enqueue_index_job,
    eval_enqueuer: EvalEnqueuer = enqueue_eval_job,
) -> dict[str, int]:
    stale_before = cutoff or datetime.now(UTC) - PENDING_JOB_RECOVERY_AFTER
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

    recovered = 0
    failed = 0
    for job in processing_jobs.all():
        enqueuer = ocr_enqueuer if job.job_type == ProcessingJobType.OCR else index_enqueuer
        try:
            await enqueuer(session, job.document_id, job.id)
            recovered += 1
        except Exception:
            failed += 1

    for eval_job in evaluation_jobs.all():
        try:
            await eval_enqueuer(session, eval_job.document_id, eval_job.id)
            recovered += 1
        except Exception:
            failed += 1

    return {"recovered": recovered, "failed": failed}


__all__ = ["recover_stale_pending_jobs", "recover_stale_pending_jobs_for_session"]
