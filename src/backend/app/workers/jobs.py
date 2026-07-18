from __future__ import annotations

from typing import Literal
from uuid import UUID

import arq
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.models import EvaluationJob, ProcessingJob
from app.models.enums import JobStatus, ProcessingJobType

OCR_QUEUE = "ocr-jobs"
EVAL_QUEUE = "eval-jobs"
INDEX_QUEUE = "index-jobs"

ACTIVE_JOB_STATUSES = {JobStatus.PENDING, JobStatus.RUNNING}

QueueJobKind = Literal["ocr", "eval", "index"]


class DuplicateQueueJobError(RuntimeError):
    """Raised when another latest active DB job already owns the queue slot."""


async def enqueue_job(
    session: AsyncSession,
    *,
    job_kind: QueueJobKind,
    document_id: UUID,
    job_id: UUID,
) -> None:
    """Validate the DB job row and enqueue it with a stable ARQ id."""
    run_number = await _validate_enqueue_request(session, job_kind=job_kind, document_id=document_id, job_id=job_id)
    function_name = _function_name_for(job_kind)
    queue_name = _queue_name_for(job_kind)
    arq_job_id = f"{document_id}:{job_kind}:{run_number}"

    settings = get_settings()
    pool = await arq.create_pool(
        arq.connections.RedisSettings.from_dsn(settings.redis_url),
        default_queue_name=queue_name,
    )
    try:
        queued_job = await pool.enqueue_job(
            function_name,
            {"document_id": str(document_id), _payload_job_id_key(job_kind): str(job_id)},
            _job_id=arq_job_id,
            _queue_name=queue_name,
        )
        if queued_job is None:
            raise DuplicateQueueJobError("Queue job already exists in Redis job/result storage")
    finally:
        await pool.close()


async def enqueue_ocr_job(session: AsyncSession, document_id: UUID, processing_job_id: UUID) -> None:
    """Enqueue a document for OCR processing."""
    await enqueue_job(session, job_kind="ocr", document_id=document_id, job_id=processing_job_id)


async def enqueue_eval_job(session: AsyncSession, document_id: UUID, evaluation_job_id: UUID) -> None:
    """Enqueue a community document for evaluation."""
    await enqueue_job(session, job_kind="eval", document_id=document_id, job_id=evaluation_job_id)


async def enqueue_index_job(session: AsyncSession, document_id: UUID, processing_job_id: UUID) -> None:
    """Enqueue a document for indexing."""
    await enqueue_job(session, job_kind="index", document_id=document_id, job_id=processing_job_id)


async def _validate_enqueue_request(
    session: AsyncSession,
    *,
    job_kind: QueueJobKind,
    document_id: UUID,
    job_id: UUID,
) -> int:
    if job_kind == "eval":
        job = await session.scalar(
            select(EvaluationJob).where(
                EvaluationJob.id == job_id,
                EvaluationJob.document_id == document_id,
            )
        )
        if job is None:
            raise ValueError("Evaluation job does not exist for document")
        active = await session.scalar(
            select(EvaluationJob).where(
                EvaluationJob.document_id == document_id,
                EvaluationJob.is_latest.is_(True),
                EvaluationJob.status.in_(ACTIVE_JOB_STATUSES),
            )
        )
    else:
        processing_type = ProcessingJobType.OCR if job_kind == "ocr" else ProcessingJobType.INDEX
        job = await session.scalar(
            select(ProcessingJob).where(
                ProcessingJob.id == job_id,
                ProcessingJob.document_id == document_id,
                ProcessingJob.job_type == processing_type,
            )
        )
        if job is None:
            raise ValueError("Processing job does not exist for document/job type")
        active = await session.scalar(
            select(ProcessingJob).where(
                ProcessingJob.document_id == document_id,
                ProcessingJob.job_type == processing_type,
                ProcessingJob.is_latest.is_(True),
                ProcessingJob.status.in_(ACTIVE_JOB_STATUSES),
            )
        )

    if not job.is_latest:
        raise DuplicateQueueJobError("Only the latest job run can be enqueued")
    if job.status not in ACTIVE_JOB_STATUSES:
        raise ValueError(f"Cannot enqueue job with status {job.status}")
    if active is not None and active.id != job.id:
        raise DuplicateQueueJobError("Another latest active job is already queued or running")
    return int(job.run_number)


def _function_name_for(job_kind: QueueJobKind) -> str:
    return {
        "ocr": "process_ocr_job",
        "eval": "process_eval_job",
        "index": "process_index_job",
    }[job_kind]


def _queue_name_for(job_kind: QueueJobKind) -> str:
    return {
        "ocr": OCR_QUEUE,
        "eval": EVAL_QUEUE,
        "index": INDEX_QUEUE,
    }[job_kind]


def _payload_job_id_key(job_kind: QueueJobKind) -> str:
    return "evaluation_job_id" if job_kind == "eval" else "processing_job_id"
