from __future__ import annotations

import asyncio
import json
import logging
import traceback
from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.state_machine import DocumentStateMachine
from app.db.session import AsyncSessionLocal
from app.llm.embeddings import DeterministicEmbeddingService, EmbeddingService
from app.models import Document, EvaluationReport, MindmapArtifact, ProcessingJob
from app.models.enums import (
    ContributionType,
    DocumentStatus,
    DocumentTier,
    JobStatus,
    MaterialType,
    ProcessingJobType,
    RagNamespace,
)
from app.models.tables import DocumentChunk
from app.services.vote_service import award_contribution_points
from app.storage.client import pagemap_document_key
from app.storage.s3 import S3CompatibleStorage
from app.workers.chunking import Chunk, build_chunks

_log = logging.getLogger(__name__)

INDEX_MAX_TRIES = 3

_NAMESPACE_MAP: dict[str, RagNamespace] = {
    ContributionType.PAST_EXAM: RagNamespace.EXERCISE,
    ContributionType.SOLVED_EXERCISE: RagNamespace.EXERCISE,
    ContributionType.SUMMARY_NOTE: RagNamespace.KNOWLEDGE,
    ContributionType.REVIEW_NOTE: RagNamespace.KNOWLEDGE,
}


async def process_index_job(ctx: dict[str, object], payload: dict[str, str]) -> None:
    document_id = UUID(payload["document_id"])
    processing_job_id = UUID(payload["processing_job_id"])
    job_try = _job_try(ctx)

    try:
        # Phase 1: Claim the job by transitioning to INDEXING and committing immediately.
        # This guarantees that any subsequent failure sees document.status == INDEXING,
        # so _record_index_failure can safely apply the INDEXING→FAILED transition.
        doc_fields = await _claim_indexing(document_id, processing_job_id, job_try)

        # Phase 2: Heavy I/O and computation — outside any DB session.
        embedding_service: EmbeddingService = ctx.get("embedding_service") or DeterministicEmbeddingService()  # type: ignore[assignment]
        from app.config import get_settings

        storage = S3CompatibleStorage(get_settings())
        markdown_bytes = await storage.get_object(str(doc_fields["storage_md_path"]))
        markdown_text = markdown_bytes.decode("utf-8", errors="replace")

        page_map: list[tuple[int, int]] = []
        course_id_val = doc_fields["course_id"]
        if isinstance(course_id_val, UUID):
            pm_key = pagemap_document_key(course_id_val, document_id)
            try:
                pm_bytes = await storage.get_object(pm_key)
                page_map = [(int(s), int(p)) for s, p in json.loads(pm_bytes.decode("utf-8"))]
            except Exception:
                page_map = []  # missing/corrupt sidecar -> page_number stays NULL

        # Embedding/rerank use a blocking HTTP client; run off the event loop so
        # concurrent jobs don't starve asyncpg (which raises MissingGreenlet).
        raw_chunks = await asyncio.to_thread(build_chunks, markdown_text, embedding_service, page_map)
        if not raw_chunks:
            raise ValueError("Document produced no indexable chunks after markdown parsing")

        embeddings = await asyncio.to_thread(
            embedding_service.encode, [c.text for c in raw_chunks], input_type="passage"
        )

        # Phase 3: Write chunks, invalidate mindmap cache, finalize state transition.
        await _finalize_indexed(
            document_id=document_id,
            processing_job_id=processing_job_id,
            doc_fields=doc_fields,
            raw_chunks=raw_chunks,
            embeddings=embeddings,
        )

        # Phase 4: Regenerate the course-wide summary for OFFICIAL docs. This makes
        # a slow LLM call, so it runs in its own session AFTER phase 3 has committed
        # — never pinning the main indexing transaction's DB connection across the
        # LLM latency. Best-effort: the summary is a regenerable cache, so a failure
        # here must not fail an already-indexed document.
        course_id = doc_fields["course_id"]
        if doc_fields["document_tier"] == DocumentTier.OFFICIAL and isinstance(course_id, UUID):
            await _refresh_course_summary(course_id)
    except Exception as exc:
        await _record_index_failure(
            document_id=document_id,
            processing_job_id=processing_job_id,
            exc=exc,
            final_attempt=job_try >= INDEX_MAX_TRIES,
        )
        raise


async def _claim_indexing(document_id: UUID, processing_job_id: UUID, job_try: int) -> dict[str, object]:
    """Transition document APPROVED→INDEXING and commit. Returns document metadata needed for phase 2+."""
    async with AsyncSessionLocal() as session:
        job = await session.scalar(
            select(ProcessingJob).where(
                ProcessingJob.id == processing_job_id,
                ProcessingJob.document_id == document_id,
                ProcessingJob.job_type == ProcessingJobType.INDEX,
                ProcessingJob.is_latest.is_(True),
            )
        )
        if job is None:
            raise ValueError("Latest index processing job not found")
        if job.status == JobStatus.COMPLETED:
            # Return sentinel so caller can short-circuit; we'll never reach phase 2.
            raise _AlreadyCompleted

        document = await session.scalar(select(Document).where(Document.id == document_id))
        if document is None:
            raise ValueError("Document not found")
        if document.storage_md_path is None:
            raise ValueError("Cannot index document without markdown output")

        now = datetime.now(UTC)
        job.status = JobStatus.RUNNING
        job.attempt_count = max(int(job.attempt_count or 0), job_try)
        job.started_at = job.started_at or now
        job.updated_at = now

        state_machine = DocumentStateMachine(session)
        if document.status == DocumentStatus.APPROVED:
            await state_machine.transition(document, DocumentStatus.INDEXING, reason="Index worker picked up document")
        elif document.status != DocumentStatus.INDEXING:
            raise ValueError(f"Index job cannot run while document is {document.status}")

        doc_fields: dict[str, object] = {
            "storage_md_path": document.storage_md_path,
            "course_id": document.course_id,
            "document_tier": document.document_tier,
            "contribution_type": document.contribution_type,
            "material_type": document.material_type,
            "uploader_id": document.uploader_id,
        }
        await session.commit()  # Committed: document is now INDEXING in DB.
        return doc_fields


class _AlreadyCompleted(Exception):
    pass


async def _finalize_indexed(
    *,
    document_id: UUID,
    processing_job_id: UUID,
    doc_fields: dict[str, object],
    raw_chunks: list[Chunk],
    embeddings: list[list[float]],
) -> None:
    async with AsyncSessionLocal() as session:
        document = await session.scalar(select(Document).where(Document.id == document_id))
        job = await session.scalar(select(ProcessingJob).where(ProcessingJob.id == processing_job_id))
        if document is None or job is None:
            raise ValueError("Document or job missing in finalize step")

        await session.execute(delete(DocumentChunk).where(DocumentChunk.document_id == document_id))

        course_id = doc_fields["course_id"]
        rag_namespace = _resolve_namespace_from_fields(doc_fields)
        subtype = _resolve_subtype_from_fields(doc_fields)

        db_chunks = [
            DocumentChunk(
                document_id=document_id,
                course_id=course_id,
                document_tier=doc_fields["document_tier"],
                subtype=subtype,
                rag_namespace=rag_namespace,
                section_title=chunk.section_title,
                page_number=chunk.page,
                chunk_order=chunk.chunk_order,
                content=chunk.text,
                embedding=embeddings[i] if i < len(embeddings) else None,
            )
            for i, chunk in enumerate(raw_chunks)
        ]
        session.add_all(db_chunks)

        await session.execute(
            update(MindmapArtifact)
            .where(MindmapArtifact.course_id == course_id)
            .values(is_cached=False, invalidated_at=datetime.now(UTC))
        )

        await DocumentStateMachine(session).transition(
            document, DocumentStatus.INDEXED, reason="Indexing completed"
        )
        job.status = JobStatus.COMPLETED
        job.completed_at = datetime.now(UTC)
        job.updated_at = datetime.now(UTC)

        contribution_type = doc_fields.get("contribution_type")
        uploader_id = doc_fields.get("uploader_id")
        if (
            doc_fields["document_tier"] == DocumentTier.COMMUNITY
            and isinstance(contribution_type, ContributionType)
            and isinstance(uploader_id, UUID)
            and isinstance(course_id, UUID)
        ):
            relevance = await _latest_relevance_score(session, document_id)
            await award_contribution_points(
                session,
                user_id=uploader_id,
                course_id=course_id,
                contribution_type=contribution_type.value,
                relevance_score=relevance,
            )

        await session.commit()


async def _refresh_course_summary(course_id: UUID) -> None:
    """Regenerate the cached course-wide summary in a standalone session/transaction.

    Kept separate from the indexing transaction so the LLM call inside
    ``tutor_course_summary`` doesn't hold the main indexing connection open.
    """
    from app.config import get_settings
    from app.llm.router import build_llm_router
    from app.services.tutor_service import tutor_course_summary

    try:
        async with AsyncSessionLocal() as session:
            await tutor_course_summary(session, course_id, build_llm_router(get_settings()))
            await session.commit()
    except Exception:
        _log.exception("course summary refresh failed course_id=%s", course_id)


def _resolve_namespace_from_fields(fields: dict[str, object]) -> RagNamespace:
    if fields["document_tier"] == DocumentTier.OFFICIAL:
        return RagNamespace.KNOWLEDGE
    contrib = fields.get("contribution_type")
    if isinstance(contrib, ContributionType):
        return _NAMESPACE_MAP.get(contrib, RagNamespace.KNOWLEDGE)
    return RagNamespace.KNOWLEDGE


def _resolve_subtype_from_fields(fields: dict[str, object]) -> str | None:
    if fields["document_tier"] == DocumentTier.OFFICIAL:
        mat = fields.get("material_type")
        return mat.value if isinstance(mat, MaterialType) else None
    contrib = fields.get("contribution_type")
    return contrib.value if isinstance(contrib, ContributionType) else None


async def _latest_relevance_score(session: AsyncSession, document_id: UUID) -> float:
    report = await session.scalar(
        select(EvaluationReport).where(
            EvaluationReport.document_id == document_id,
            EvaluationReport.is_latest.is_(True),
        )
    )
    if report is None:
        return 10.0
    scores = report.agent3_output.get("scores", {})
    return float(scores.get("relevance", 10.0))


async def _record_index_failure(
    *,
    document_id: UUID,
    processing_job_id: UUID,
    exc: Exception,
    final_attempt: bool,
) -> None:
    async with AsyncSessionLocal() as session:
        job = await session.scalar(select(ProcessingJob).where(ProcessingJob.id == processing_job_id))
        document = await session.scalar(select(Document).where(Document.id == document_id))
        if job is not None:
            job.status = JobStatus.FAILED if final_attempt else JobStatus.PENDING
            job.failure_reason = str(exc)[:1000]
            job.raw_failure_output = {"traceback_tail": _traceback_tail()}
            job.completed_at = datetime.now(UTC) if final_attempt else None
            job.updated_at = datetime.now(UTC)
        # After Phase 1 commits, document is always INDEXING when we reach here.
        # INDEXING→FAILED is a valid transition so no state machine bypass is needed.
        if final_attempt and document is not None and document.status == DocumentStatus.INDEXING:
            await DocumentStateMachine(session).transition(
                document,
                DocumentStatus.FAILED,
                reason="Index job failed after retries",
            )
        await session.commit()


def _traceback_tail() -> str:
    return "".join(traceback.format_exc(limit=8))[-4000:]


def _job_try(ctx: dict[str, object]) -> int:
    value = ctx.get("job_try", 1)
    return int(value) if isinstance(value, int | str | float) else 1


__all__ = ["process_index_job"]
