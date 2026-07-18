from __future__ import annotations

import asyncio
import json
import logging
import tempfile
import time
import traceback
from collections.abc import Awaitable, Callable, Iterator
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.core.state_machine import DocumentStateMachine
from app.db.session import AsyncSessionLocal
from app.models import Document, EvaluationJob, ProcessingJob
from app.models.enums import DocumentStatus, DocumentTier, FileFormat, JobStatus, ProcessingJobType
from app.services.document_processing import build_document_processing_pipeline
from app.services.document_summary_service import upsert_document_summary
from app.storage import get_storage
from app.storage.client import markdown_document_key, pagemap_document_key
from app.workers.jobs import enqueue_eval_job, enqueue_index_job

OCR_MAX_TRIES = 3
OcrRunner = Callable[[Path, Document], Awaitable[str]]
logger = logging.getLogger(__name__)


class OcrTrace:
    def __init__(self, document_id: UUID, processing_job_id: UUID, job_try: int) -> None:
        self.document_id = str(document_id)
        self.processing_job_id = str(processing_job_id)
        self.job_try = job_try
        self.started_at = time.monotonic()
        self.current_step: str | None = None
        self._step_stack: list[str] = []
        self.events: list[dict[str, Any]] = []

    @contextmanager
    def step(self, name: str, **details: Any) -> Iterator[None]:
        started = self.start(name, **details)
        try:
            yield
        except BaseException as exc:
            self.error(name, exc, started_at=started)
            raise
        else:
            self.end(name, started_at=started)

    def start(self, name: str, **details: Any) -> float:
        self._step_stack.append(name)
        self.current_step = name
        started = time.monotonic()
        self._append(name, "start", details=details)
        return started

    def end(self, name: str, *, started_at: float, **details: Any) -> None:
        self._append(
            name,
            "end",
            duration_ms=int((time.monotonic() - started_at) * 1000),
            details=details,
        )
        if self._step_stack and self._step_stack[-1] == name:
            self._step_stack.pop()
        elif name in self._step_stack:
            self._step_stack.remove(name)
        self.current_step = self._step_stack[-1] if self._step_stack else None

    def error(self, name: str, exc: BaseException, *, started_at: float | None = None) -> None:
        details: dict[str, Any] = {
            "error_type": exc.__class__.__name__,
            "message": str(exc)[:500],
        }
        duration_ms = int((time.monotonic() - started_at) * 1000) if started_at is not None else None
        self._append(name, "error", duration_ms=duration_ms, details=details)

    def pipeline_progress(self, event: dict[str, Any]) -> None:
        pipeline_event = str(event.get("event", "unknown"))
        self._append(
            "pipeline_progress",
            pipeline_event,
            details={k: v for k, v in event.items() if k != "timestamp"},
        )

    def snapshot(self) -> dict[str, Any]:
        return {
            "document_id": self.document_id,
            "processing_job_id": self.processing_job_id,
            "job_try": self.job_try,
            "current_step": self.current_step,
            "elapsed_ms": int((time.monotonic() - self.started_at) * 1000),
            "events": self.events[-120:],
        }

    def _append(
        self,
        step: str,
        status: str,
        *,
        duration_ms: int | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        event: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "elapsed_ms": int((time.monotonic() - self.started_at) * 1000),
            "step": step,
            "status": status,
        }
        if duration_ms is not None:
            event["duration_ms"] = duration_ms
        if details:
            event["details"] = _json_safe(details)
        self.events.append(event)
        logger.info(
            "ocr_trace document=%s job=%s try=%s step=%s status=%s elapsed_ms=%sms details=%s",
            self.document_id,
            self.processing_job_id,
            self.job_try,
            step,
            status,
            event["elapsed_ms"],
            json.dumps(event.get("details", {}), ensure_ascii=False),
        )


@contextmanager
def _optional_step(trace: OcrTrace | None, name: str, **details: Any) -> Iterator[None]:
    if trace is None:
        yield
        return
    with trace.step(name, **details):
        yield


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, list | tuple | set):
        return [_json_safe(v) for v in value]
    if isinstance(value, str):
        return value[:1000]
    if isinstance(value, int | float | bool) or value is None:
        return value
    return str(value)[:1000]


async def process_ocr_job(ctx: dict[str, object], payload: dict[str, str]) -> None:
    document_id = UUID(payload["document_id"])
    processing_job_id = UUID(payload["processing_job_id"])
    job_try = _job_try(ctx)
    trace = OcrTrace(document_id, processing_job_id, job_try)
    runner_value = ctx.get("ocr_runner")
    custom_runner = cast(OcrRunner, runner_value) if callable(runner_value) else None

    try:
        follow_up: tuple[str, UUID] | None = None
        with trace.step("load_and_mark_job_running"):
            async with AsyncSessionLocal() as session:
                job = await session.scalar(
                    select(ProcessingJob).where(
                        ProcessingJob.id == processing_job_id,
                        ProcessingJob.document_id == document_id,
                        ProcessingJob.job_type == ProcessingJobType.OCR,
                        ProcessingJob.is_latest.is_(True),
                    )
                )
                if job is None:
                    raise ValueError("Latest OCR processing job not found")
                if job.status == JobStatus.COMPLETED:
                    return

                document = await session.scalar(select(Document).where(Document.id == document_id))
                if document is None:
                    raise ValueError("Document not found")
                if document.storage_raw_path is None:
                    raise ValueError("Document raw storage path is missing")

                await _mark_processing_running(session, job, job_try)
                if document.status == DocumentStatus.UPLOADED:
                    await DocumentStateMachine(session).transition(
                        document,
                        DocumentStatus.PARSING,
                        reason="OCR worker picked up document",
                    )
                elif document.status != DocumentStatus.PARSING:
                    raise ValueError(f"OCR job cannot run while document is {document.status}")
                await session.commit()

        storage = get_storage()
        async with AsyncSessionLocal() as session:
            document = await session.scalar(select(Document).where(Document.id == document_id))
            if document is None or document.storage_raw_path is None:
                raise ValueError("Document raw storage path is missing")
            with trace.step("storage_get_raw_object", storage_key=document.storage_raw_path):
                raw_bytes = await storage.get_object(document.storage_raw_path)
            suffix = f".{document.file_format.value}"
            with tempfile.TemporaryDirectory(prefix="phase-c-ocr-") as temp_root:
                input_path = Path(temp_root) / f"input{suffix}"
                with trace.step("write_temp_input", byte_count=len(raw_bytes), suffix=suffix):
                    input_path.write_bytes(raw_bytes)
                with trace.step("run_document_processing_pipeline"):
                    if custom_runner is not None:
                        markdown_text = await custom_runner(input_path, document)
                        page_map: list[tuple[int, int]] = []
                    else:
                        markdown_text, page_map = await run_document_processing_pipeline(
                            input_path, document, trace=trace
                        )

            md_key = markdown_document_key(document.course_id, document.id)
            with trace.step("storage_put_markdown", storage_key=md_key, markdown_chars=len(markdown_text)):
                await storage.put_object(md_key, markdown_text.encode("utf-8"), "text/markdown; charset=utf-8")
            document.storage_md_path = md_key
            if page_map:
                pm_key = pagemap_document_key(document.course_id, document.id)
                with trace.step("storage_put_pagemap", storage_key=pm_key, boundary_count=len(page_map)):
                    await storage.put_object(
                        pm_key, json.dumps(page_map).encode("utf-8"), "application/json"
                    )
            with trace.step("upsert_document_summary"):
                await upsert_document_summary(session, document_id=document.id, markdown_text=markdown_text)

            with trace.step("complete_ocr_and_route_document"):
                job = await session.scalar(select(ProcessingJob).where(ProcessingJob.id == processing_job_id))
                if job is None:
                    raise ValueError("OCR processing job disappeared")
                job.status = JobStatus.COMPLETED
                job.failure_reason = None
                job.raw_failure_output = None
                job.completed_at = datetime.now(UTC)
                job.updated_at = datetime.now(UTC)

                if document.document_tier == DocumentTier.COMMUNITY:
                    await DocumentStateMachine(session).transition(
                        document,
                        DocumentStatus.EVALUATING,
                        reason="OCR and summarization completed",
                    )
                    eval_job = await _create_next_evaluation_job(session, document.id)
                    follow_up = ("eval", eval_job.id)
                else:
                    await DocumentStateMachine(session).transition(
                        document,
                        DocumentStatus.APPROVED,
                        reason="Official material parsed and summarized",
                    )
                    index_job = await _create_next_processing_job(session, document.id, ProcessingJobType.INDEX)
                    follow_up = ("index", index_job.id)

                await session.commit()

        if follow_up is not None:
            with trace.step("enqueue_follow_up_job", follow_up_kind=follow_up[0], follow_up_job_id=str(follow_up[1])):
                async with AsyncSessionLocal() as session:
                    if follow_up[0] == "eval":
                        await enqueue_eval_job(session, document_id, follow_up[1])
                    else:
                        await enqueue_index_job(session, document_id, follow_up[1])
    except asyncio.CancelledError:
        timeout_exc = TimeoutError(f"OCR job was cancelled while current_step={trace.current_step or 'unknown'}")
        trace.error("ocr_job_cancelled", timeout_exc)
        await _record_processing_failure(
            document_id=document_id,
            processing_job_id=processing_job_id,
            job_type=ProcessingJobType.OCR,
            exc=timeout_exc,
            final_attempt=job_try >= OCR_MAX_TRIES,
            trace=trace.snapshot(),
        )
        raise
    except Exception as exc:
        await _record_processing_failure(
            document_id=document_id,
            processing_job_id=processing_job_id,
            job_type=ProcessingJobType.OCR,
            exc=exc,
            final_attempt=job_try >= OCR_MAX_TRIES,
            trace=trace.snapshot(),
        )
        raise


async def run_document_processing_pipeline(
    input_path: Path,
    document: Document,
    trace: OcrTrace | None = None,
) -> tuple[str, list[tuple[int, int]]]:
    """Run the native OOP document processing pipeline and return (markdown, page_map).

    Replaces the previous dynamic ``importlib`` load of the experiment script. The
    pipeline is synchronous (PyMuPDF/python-pptx + blocking provider SDKs), so it runs
    in a worker thread to avoid blocking the event loop.
    """
    pipeline = build_document_processing_pipeline(
        get_settings(),
        progress_callback=trace.pipeline_progress if trace is not None else None,
    )
    with _optional_step(trace, "run_native_document_processing"):
        result = await asyncio.to_thread(
            pipeline.process_document,
            input_path,
            document_id=str(document.id),
            expected_route=_expected_route(document.file_format),
        )
    if trace is not None:
        trace.pipeline_progress({
            "event": "pipeline_complete",
            "route": result.route,
            "inferred_type": result.inferred_type,
            "normalized_chars": len(result.markdown),
            "llm_metrics": result.llm_metrics,
            "quality_flags": result.quality_flags,
        })
    return result.markdown, result.page_map


async def _create_next_evaluation_job(session: AsyncSession, document_id: UUID) -> EvaluationJob:
    old_jobs = await session.scalars(select(EvaluationJob).where(EvaluationJob.document_id == document_id))
    max_run = 0
    for old_job in old_jobs.all():
        old_job.is_latest = False
        max_run = max(max_run, int(old_job.run_number))

    job = EvaluationJob(document_id=document_id, run_number=max_run + 1, is_latest=True, status=JobStatus.PENDING)
    session.add(job)
    await session.flush()
    return job


async def _create_next_processing_job(
    session: AsyncSession,
    document_id: UUID,
    job_type: ProcessingJobType,
) -> ProcessingJob:
    old_jobs = await session.scalars(
        select(ProcessingJob).where(ProcessingJob.document_id == document_id, ProcessingJob.job_type == job_type)
    )
    max_run = 0
    for old_job in old_jobs.all():
        old_job.is_latest = False
        max_run = max(max_run, int(old_job.run_number))

    job = ProcessingJob(
        document_id=document_id,
        job_type=job_type,
        run_number=max_run + 1,
        is_latest=True,
        status=JobStatus.PENDING,
    )
    session.add(job)
    await session.flush()
    return job


async def _mark_processing_running(session: AsyncSession, job: ProcessingJob, job_try: int) -> None:
    now = datetime.now(UTC)
    job.status = JobStatus.RUNNING
    job.attempt_count = max(int(job.attempt_count or 0), job_try)
    job.started_at = job.started_at or now
    job.updated_at = now
    await session.flush()


async def _record_processing_failure(
    *,
    document_id: UUID,
    processing_job_id: UUID,
    job_type: ProcessingJobType,
    exc: Exception,
    final_attempt: bool,
    trace: dict[str, Any] | None = None,
) -> None:
    async with AsyncSessionLocal() as session:
        job = await session.scalar(select(ProcessingJob).where(ProcessingJob.id == processing_job_id))
        document = await session.scalar(select(Document).where(Document.id == document_id))
        if job is not None:
            job.status = JobStatus.FAILED if final_attempt else JobStatus.PENDING
            job.failure_reason = str(exc)[:1000]
            raw_failure_output: dict[str, Any] = {"traceback_tail": _traceback_tail()}
            if trace is not None:
                raw_failure_output["ocr_trace"] = trace
            job.raw_failure_output = raw_failure_output
            job.completed_at = datetime.now(UTC) if final_attempt else None
            job.updated_at = datetime.now(UTC)
        if (
            final_attempt
            and document is not None
            and document.status in {DocumentStatus.PARSING, DocumentStatus.INDEXING}
        ):
            failed_from_state = document.status
            await DocumentStateMachine(session).transition(
                document,
                DocumentStatus.FAILED,
                reason=f"{job_type.value} job failed after retries from {failed_from_state.value}",
            )
        await session.commit()


def _expected_route(file_format: FileFormat) -> str:
    return "hybrid" if file_format in {FileFormat.PDF, FileFormat.PPTX} else "vision_only"


def _traceback_tail() -> str:
    return "".join(traceback.format_exc(limit=8))[-4000:]


def _job_try(ctx: dict[str, object]) -> int:
    value = ctx.get("job_try", 1)
    return int(value) if isinstance(value, int | str | float) else 1


__all__ = ["process_ocr_job", "run_document_processing_pipeline"]
