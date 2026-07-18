from __future__ import annotations

import asyncio
import json
import logging
import math
import time
import traceback
from datetime import UTC, datetime
from uuid import UUID

import httpx
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.core.state_machine import DocumentStateMachine
from app.db.session import AsyncSessionLocal
from app.llm.router import build_llm_router
from app.models import Course, CourseReviewerAssignment, Document, DocumentSummary, EvaluationJob
from app.models.enums import ContributionType, DocumentStatus, DocumentTier, JobStatus
from app.services.evaluation_report_service import (
    Agent2OutputPayload,
    Agent2ReferencePayload,
    ExistingSummaryEmbedding,
    build_agent1_output,
    build_agent3_output,
    build_empty_agent2_output,
    upsert_evaluation_report,
)

EVAL_MAX_TRIES = 3


async def process_eval_job(ctx: dict[str, object], payload: dict[str, str]) -> None:
    document_id = UUID(payload["document_id"])
    evaluation_job_id = UUID(payload["evaluation_job_id"])
    job_try = _job_try(ctx)

    try:
        async with AsyncSessionLocal() as session:
            job = await session.scalar(
                select(EvaluationJob).where(
                    EvaluationJob.id == evaluation_job_id,
                    EvaluationJob.document_id == document_id,
                    EvaluationJob.is_latest.is_(True),
                )
            )
            if job is None:
                raise ValueError("Latest evaluation job not found")
            if job.status == JobStatus.COMPLETED:
                return

            document = await session.scalar(select(Document).where(Document.id == document_id))
            if document is None:
                raise ValueError("Document not found")
            if document.status != DocumentStatus.EVALUATING:
                raise ValueError(f"Evaluation job cannot run while document is {document.status}")

            await _mark_eval_running(session, job, job_try)
            summary = await session.scalar(select(DocumentSummary).where(DocumentSummary.document_id == document_id))
            course = await session.scalar(select(Course).where(Course.id == document.course_id))
            if summary is None or course is None:
                raise ValueError("Evaluation requires document summary and course")
            if document.contribution_type is None:
                raise ValueError("Evaluation requires a community contribution type")

            approved_count = await _approved_document_count(session, document.course_id)
            topic_coverage = _topic_coverage(course.topic_tags, summary)

            is_duplicate, duplicate_of_id, similarity_score = await _check_chunk_duplicate(ctx, session, document)
            course_knowledge_state = await _synthesize_course_knowledge_state(session, course)

            agent1 = build_agent1_output(
                syllabus_topic_summary=course.topic_summary,
                existing_document_count=approved_count,
                has_seed_document=bool(course.topic_summary and course.topic_summary.strip()),
                topic_coverage=topic_coverage,
                course_knowledge_state=course_knowledge_state,
                is_duplicate=is_duplicate,
                duplicate_of_document_id=duplicate_of_id,
                similarity_score=similarity_score,
            )
            if agent1.duplicate.is_duplicate:
                agent2 = build_empty_agent2_output(search_status="error", duration_ms=0)
                duplicate_id = agent1.duplicate.duplicate_of_document_id
                similarity = agent1.duplicate.similarity_score
                justification = {
                    "relevance_rationale": "Evaluation bypassed. The document is flagged as a duplicate.",
                    "completeness_rationale": "Evaluation bypassed. The document is flagged as a duplicate.",
                    "quality_rationale": "Evaluation bypassed. The document is flagged as a duplicate.",
                    "overall_rationale": (
                        f"Bypassed. Duplicate of document {duplicate_id} "
                        f"detected with similarity score {similarity:.4f}."
                    ),
                }
                agent3 = build_agent3_output(
                    relevance=0.0,
                    completeness=0.0,
                    quality=0.0,
                    initial_contribution_type=document.contribution_type,
                    suggested_contribution_type=document.contribution_type,
                    label_confidence=1.0,
                    agent1_output=agent1,
                    evaluation_justification=justification,
                )
            else:
                search_query = " ".join(
                    filter(None, [summary.topic, (course.topic_summary or "")[:120]])
                )
                agent2 = await _run_agent2_search(search_query or "academic document")
                relevance, completeness, quality, justification = await _llm_evaluate_scores(
                    course, summary, topic_coverage, course_knowledge_state
                )
                suggested_type = _suggest_contribution_type(summary, document.contribution_type)
                agent3 = build_agent3_output(
                    relevance=relevance,
                    completeness=completeness,
                    quality=quality,
                    initial_contribution_type=document.contribution_type,
                    suggested_contribution_type=suggested_type,
                    label_confidence=0.7,
                    agent1_output=agent1,
                    evaluation_justification=justification,
                )

            await upsert_evaluation_report(
                session,
                document_id=document.id,
                evaluation_job_id=job.id,
                course_code=course.code,
                agent1_output=agent1,
                agent2_output=agent2,
                agent3_output=agent3,
            )

            if not await _course_has_active_reviewer(session, document.course_id):
                document.no_reviewer_flag = True

            await DocumentStateMachine(session).transition(
                document,
                DocumentStatus.NEEDS_REVIEW,
                reason="Evaluation pipeline completed",
            )
            job.status = JobStatus.COMPLETED
            job.completed_at = datetime.now(UTC)
            job.updated_at = datetime.now(UTC)
            await session.commit()
    except Exception as exc:
        await _record_eval_failure(
            document_id=document_id,
            evaluation_job_id=evaluation_job_id,
            exc=exc,
        )
        raise


async def _check_chunk_duplicate(
    ctx: dict[str, object],
    session: AsyncSession,
    document: Document,
) -> tuple[bool, UUID | None, float]:
    """
    Checks if the document is a duplicate of any existing approved/indexed document
    using Chunk-Level Set Matching.
    """
    if not document.storage_md_path:
        return False, None, 0.0

    from app.config import get_settings
    from app.services.retrieval_service import build_embedding_service
    from app.storage.s3 import S3CompatibleStorage
    from app.workers.chunking import build_chunks

    settings = get_settings()
    storage = S3CompatibleStorage(settings)

    # Let S3 / embedding errors propagate: swallowing them here would mark a
    # transient outage as "not a duplicate" and push the doc into the approval
    # queue unchecked. Propagation lets process_eval_job record the failure and
    # arq retry the job (up to EVAL_MAX_TRIES).
    markdown_bytes = await storage.get_object(document.storage_md_path)
    markdown_text = markdown_bytes.decode("utf-8", errors="replace")

    # Retrieve embedding service from context (useful for unit tests using DeterministicEmbeddingService)
    from app.llm.embeddings import EmbeddingService
    embedding_service_raw = ctx.get("embedding_service")
    embedding_service: EmbeddingService
    if not embedding_service_raw:
        embedding_service = build_embedding_service(settings)
    else:
        embedding_service = embedding_service_raw  # type: ignore[assignment]

    raw_chunks = await asyncio.to_thread(build_chunks, markdown_text, embedding_service)
    if not raw_chunks:
        return False, None, 0.0
    query_embeddings = await asyncio.to_thread(
        embedding_service.encode, [c.text for c in raw_chunks], input_type="passage"
    )

    # Retrieve all chunk embeddings of approved/indexed docs in the same course
    from app.models.tables import DocumentChunk
    stmt = (
        select(DocumentChunk.document_id, DocumentChunk.embedding)
        .join(Document, Document.id == DocumentChunk.document_id)
        .where(
            Document.course_id == document.course_id,
            Document.id != document.id,
            Document.status.in_([DocumentStatus.APPROVED, DocumentStatus.INDEXING, DocumentStatus.INDEXED]),
            DocumentChunk.embedding.is_not(None),
        )
    )
    db_rows = (await session.execute(stmt)).all()
    if not db_rows:
        return False, None, 0.0

    candidates: dict[UUID, list[list[float]]] = {}
    for doc_id, emb in db_rows:
        if emb:
            if doc_id not in candidates:
                candidates[doc_id] = []
            candidates[doc_id].append(list(emb))

    best_candidate_id: UUID | None = None
    best_ratio = 0.0

    for cand_id, cand_embeddings in candidates.items():
        if not cand_embeddings:
            continue

        matched_chunks = 0
        for q_emb in query_embeddings:
            max_sim = 0.0
            for c_emb in cand_embeddings:
                sim = _cosine_similarity(q_emb, c_emb)
                if sim > max_sim:
                    max_sim = sim
            if max_sim >= 0.85:
                matched_chunks += 1

        ratio = matched_chunks / len(query_embeddings)
        if ratio > best_ratio:
            best_ratio = ratio
            best_candidate_id = cand_id

    is_duplicate = best_ratio >= 0.40
    return is_duplicate, best_candidate_id if is_duplicate else None, best_ratio


def _cosine_similarity(left: list[float], right: list[float]) -> float:
    if len(left) != len(right) or not left:
        return 0.0
    dot = sum(a * b for a, b in zip(left, right, strict=False))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if left_norm == 0.0 or right_norm == 0.0:
        return 0.0
    return max(0.0, min(1.0, dot / (left_norm * right_norm)))


async def _synthesize_course_knowledge_state(
    session: AsyncSession,
    course: Course,
) -> str:
    stmt = (
        select(DocumentSummary)
        .join(Document, Document.id == DocumentSummary.document_id)
        .where(
            Document.course_id == course.id,
            Document.document_tier == DocumentTier.OFFICIAL,
            Document.status == DocumentStatus.INDEXED,
        )
        # Eager-load document: async session forbids lazy-loading s.document below.
        .options(selectinload(DocumentSummary.document))
    )
    db_summaries = (await session.scalars(stmt)).all()

    if not db_summaries:
        return f"Course Seed topic summary: {course.topic_summary or ''}"

    summaries_parts = []
    for s in db_summaries:
        title = s.document.original_filename if s.document else f"Document {s.document_id}"
        concepts_str = ", ".join(s.concepts or [])
        summaries_parts.append(
            f"Document: {title}\n"
            f"Summary: {s.overall_summary or ''}\n"
            f"Key Concepts: {concepts_str}"
        )
    context_text = "\n\n---\n\n".join(summaries_parts)

    prompt = (
        f"Course Code: {course.code}\n"
        f"Course Name: {course.name}\n"
        f"Course Seed topic summary: {course.topic_summary or ''}\n\n"
        "Here are the summaries of official materials in this course:\n"
        f"{context_text}\n\n"
        "Synthesize these into a single, cohesive, high-level summary of the course's curriculum outline "
        "and official knowledge base (the Course Knowledge State) in Vietnamese. "
        "Keep it concise, clear, and professional, summarizing the main concepts taught in the course."
    )

    settings = get_settings()
    router = build_llm_router(settings)
    try:
        res = await router.chat(
            [
                {"role": "system", "content": "You are an academic course knowledge aggregator."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=1000,
            flow="course",
        )
        return res.content.strip()
    except Exception:
        fallback_text = f"Syllabus/Topic Seed Summary: {course.topic_summary or ''}."
        if summaries_parts:
            fallback_text += " Official materials summaries:\n" + "\n".join(
                f"- {s.overall_summary or ''}" for s in db_summaries
            )
        return fallback_text


async def check_sla_breaches(ctx: dict[str, object]) -> int:
    del ctx
    async with AsyncSessionLocal() as session:
        now = datetime.now(UTC)
        docs = await session.scalars(
            select(Document).where(
                Document.status == DocumentStatus.NEEDS_REVIEW,
                Document.sla_breached.is_(False),
                Document.sla_deadline.is_not(None),
                Document.sla_deadline < now,
            )
        )
        count = 0
        for document in docs.all():
            document.sla_breached = True
            count += 1
        await session.commit()
        return count


async def _approved_document_count(session: AsyncSession, course_id: UUID) -> int:
    value = await session.scalar(
        select(func.count())
        .select_from(Document)
        .where(
            Document.course_id == course_id,
            Document.status.in_([DocumentStatus.APPROVED, DocumentStatus.INDEXING, DocumentStatus.INDEXED]),
        )
    )
    return int(value or 0)


async def _approved_summary_embeddings(session: AsyncSession, document: Document) -> list[ExistingSummaryEmbedding]:
    summaries = await session.scalars(
        select(DocumentSummary)
        .join(Document, Document.id == DocumentSummary.document_id)
        .where(
            Document.course_id == document.course_id,
            Document.id != document.id,
            Document.status.in_([DocumentStatus.APPROVED, DocumentStatus.INDEXING, DocumentStatus.INDEXED]),
        )
    )
    return [
        ExistingSummaryEmbedding(document_id=summary.document_id, summary_embedding=summary.summary_embedding)
        for summary in summaries.all()
    ]


async def _course_has_active_reviewer(session: AsyncSession, course_id: UUID) -> bool:
    assignment = await session.scalar(
        select(CourseReviewerAssignment.id).where(
            CourseReviewerAssignment.course_id == course_id,
            CourseReviewerAssignment.is_active.is_(True),
        )
    )
    return assignment is not None


async def _mark_eval_running(session: AsyncSession, job: EvaluationJob, job_try: int) -> None:
    now = datetime.now(UTC)
    job.status = JobStatus.RUNNING
    job.attempt_count = max(int(job.attempt_count or 0), job_try)
    job.started_at = job.started_at or now
    job.updated_at = now
    await session.flush()


async def _record_eval_failure(
    *,
    document_id: UUID,
    evaluation_job_id: UUID,
    exc: Exception,
) -> None:
    # Attempt-count math lives here (not in `_mark_eval_running`) because this is
    # the only session that reliably commits on a failing run: the main
    # `process_eval_job` session rolls back its uncommitted flush when the
    # exception propagates, so a counter bumped there would never persist.
    # This also makes attempts accumulate correctly across separately-enqueued
    # arq jobs (e.g. hourly `recover_stale_pending_jobs` retries), whose fresh
    # `ctx["job_try"]` always starts back at 1 and can't be used as a
    # cross-enqueue retry counter.
    async with AsyncSessionLocal() as session:
        job = await session.scalar(select(EvaluationJob).where(EvaluationJob.id == evaluation_job_id))
        document = await session.scalar(select(Document).where(Document.id == document_id))
        final_attempt = False
        if job is not None:
            job.attempt_count = min(int(job.attempt_count or 0) + 1, EVAL_MAX_TRIES)
            final_attempt = job.attempt_count >= EVAL_MAX_TRIES
            job.status = JobStatus.FAILED if final_attempt else JobStatus.PENDING
            job.failure_reason = str(exc)[:1000]
            job.raw_failure_output = {"traceback_tail": _traceback_tail()}
            job.completed_at = datetime.now(UTC) if final_attempt else None
            job.updated_at = datetime.now(UTC)
        if final_attempt and document is not None and document.status == DocumentStatus.EVALUATING:
            await DocumentStateMachine(session).transition(
                document,
                DocumentStatus.FAILED,
                reason="Evaluation job failed after retries",
            )
        await session.commit()


def _topic_coverage(topic_tags: list[str], summary: DocumentSummary) -> dict[str, str]:
    haystack = " ".join(
        [
            summary.topic or "",
            summary.overall_summary or "",
            " ".join(summary.concepts or []),
        ]
    ).lower()
    return {tag: "covered" if tag.lower() in haystack else "missing" for tag in topic_tags}


def _clamp_score(value: object) -> float:
    try:
        score = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return 0.0
    return round(max(0.0, min(10.0, score)), 2)


async def _llm_evaluate_scores(
    course: Course,
    summary: DocumentSummary,
    topic_coverage: dict[str, str],
    course_knowledge_state: str,
) -> tuple[float, float, float, dict[str, str]]:
    """LLM-as-judge scoring of a community document against its course.

    Returns (relevance, completeness, quality) on a 0-10 scale plus a Vietnamese
    justification dict. Falls back to deterministic heuristics when no LLM is
    configured or the call/parse fails.
    """
    concepts = ", ".join(summary.concepts or [])
    topic_tags = ", ".join(course.topic_tags or [])
    prompt = (
        "Bạn là giám khảo học thuật, đánh giá một tài liệu do sinh viên đóng góp xem có "
        "phù hợp làm tài liệu học tập cho môn học hay không.\n\n"
        f"MÔN HỌC: {course.code} - {course.name}\n"
        f"Tóm tắt chương trình: {course.topic_summary or '(chưa có)'}\n"
        f"Chủ đề trọng tâm: {topic_tags or '(chưa có)'}\n"
        f"Tri thức hiện có của môn: {course_knowledge_state}\n\n"
        "TÀI LIỆU CẦN ĐÁNH GIÁ:\n"
        f"- Chủ đề: {summary.topic or '(không rõ)'}\n"
        f"- Khái niệm chính: {concepts or '(không có)'}\n"
        f"- Tóm tắt nội dung: {summary.overall_summary or '(không có)'}\n"
        f"- Chất lượng OCR: {summary.ocr_quality}\n\n"
        "Chấm điểm trên thang 0-10:\n"
        "- relevance: mức độ liên quan của nội dung với môn học. Nếu tài liệu KHÔNG thuộc "
        "môn học (ví dụ mô tả công việc/JD, quảng cáo, nội dung lạc đề) PHẢI chấm rất thấp (0-3).\n"
        "- completeness: mức độ đầy đủ, bao phủ của nội dung học thuật (đủ hay thiếu ý).\n"
        "- quality: chất lượng học thuật của nội dung — chiều sâu, độ rõ ràng khi giải "
        "thích khái niệm và giá trị sư phạm (có giải thích, lập luận, ví dụ chứ không chỉ "
        "liệt kê). Đây KHÔNG phải điểm về chất lượng OCR hay định dạng. Chỉ đánh giá dựa "
        "trên những gì bản tóm tắt thể hiện, không suy diễn đúng/sai sự thật ngoài phạm vi tóm tắt.\n"
        "Mốc điểm tham chiếu cho cả ba tiêu chí: 9-10 = xuất sắc, đúng trọng tâm môn học; "
        "7-8 = tốt, phù hợp nhưng còn thiếu sót nhỏ; 4-6 = liên quan một phần hoặc chất lượng "
        "trung bình; 0-3 = lạc đề hoặc chất lượng kém.\n"
        "Lưu ý: bạn chỉ được xem bản tóm tắt tự động của tài liệu, không phải toàn văn. "
        "Rationale không được khẳng định vượt quá những gì bản tóm tắt thể hiện.\n"
        "Viết rationale bằng tiếng Việt, ngắn gọn, nêu rõ lý do điểm số. "
        "overall_rationale phải nêu rõ tài liệu có phù hợp với môn học hay không. "
        "Cả 4 trường rationale (relevance_rationale, completeness_rationale, quality_rationale, "
        "overall_rationale) đều BẮT BUỘC phải có nội dung cụ thể, không được để trống."
    )

    schema = {
        "type": "object",
        "properties": {
            "relevance": {"type": "number"},
            "completeness": {"type": "number"},
            "quality": {"type": "number"},
            "relevance_rationale": {"type": "string"},
            "completeness_rationale": {"type": "string"},
            "quality_rationale": {"type": "string"},
            "overall_rationale": {"type": "string"},
        },
        "required": [
            "relevance",
            "completeness",
            "quality",
            "relevance_rationale",
            "completeness_rationale",
            "quality_rationale",
            "overall_rationale",
        ],
    }

    settings = get_settings()
    router = build_llm_router(settings)
    try:
        res = await router.chat(
            [
                {"role": "system", "content": "Bạn là giám khảo đánh giá tài liệu học thuật, chỉ trả về JSON."},
                {"role": "user", "content": prompt},
            ],
            schema=schema,
            # The default judge (minimax-m3) emits a <think> reasoning block
            # before the JSON; 800 tokens got consumed by reasoning alone,
            # truncating the JSON so json.loads() failed and the judge was
            # mistaken for "LLM unavailable". Give the 7-field rationale room.
            max_tokens=4096,
            flow="evaluation",
        )
        data = json.loads(res.content) if isinstance(res.content, str) else res.content
        relevance = _clamp_score(data.get("relevance"))
        completeness = _clamp_score(data.get("completeness"))
        quality = _clamp_score(data.get("quality"))
        # The judge model occasionally fills overall_rationale but leaves one or
        # more of the per-criterion fields as an empty string despite them being
        # "required" in the schema. Backfill those from the score so the UI never
        # shows an empty rationale when we do have a real judged score for it.
        justification = {
            "relevance_rationale": str(data.get("relevance_rationale") or "")
            or f"Relevance score of {relevance:.2f}/10.0 reflects content similarity to topic tags.",
            "completeness_rationale": str(data.get("completeness_rationale") or "")
            or f"Completeness score of {completeness:.2f}/10.0 reflects coverage of syllabus topics.",
            "quality_rationale": str(data.get("quality_rationale") or "")
            or f"Quality score of {quality:.2f}/10.0 reflects academic depth and clarity of the content.",
            "overall_rationale": str(data.get("overall_rationale") or ""),
        }
        return (
            relevance,
            completeness,
            quality,
            justification,
        )
    except Exception:
        logging.getLogger(__name__).warning(
            "LLM-as-judge failed for course=%s; falling back to deterministic scoring",
            course.code,
            exc_info=True,
        )
        relevance, completeness, quality = _deterministic_scores(topic_coverage, summary)
        justification = {
            "relevance_rationale": (
                f"Relevance score of {relevance:.2f}/10.0 reflects content similarity to topic tags."
            ),
            "completeness_rationale": (
                f"Completeness score of {completeness:.2f}/10.0 reflects coverage of syllabus topics."
            ),
            "quality_rationale": (
                f"Quality score of {quality:.2f}/10.0 reflects academic depth and clarity of the content."
            ),
            "overall_rationale": "Automated deterministic evaluation (LLM unavailable).",
        }
        return relevance, completeness, quality, justification


def _deterministic_scores(topic_coverage: dict[str, str], summary: DocumentSummary) -> tuple[float, float, float]:
    covered = sum(status == "covered" for status in topic_coverage.values())
    total = len(topic_coverage)
    relevance = 6.5 if total == 0 else 4.0 + (5.0 * covered / max(total, 1))
    if summary.overall_summary and len(summary.overall_summary.split()) >= 60:
        completeness = 8.0
    elif summary.overall_summary and len(summary.overall_summary.split()) >= 20:
        completeness = 6.5
    else:
        completeness = 5.0
    concept_count = len(summary.concepts or [])
    if concept_count >= 5:
        quality = 8.0
    elif concept_count >= 2:
        quality = 6.5
    else:
        quality = 5.0
    return round(relevance, 2), completeness, quality


def _suggest_contribution_type(summary: DocumentSummary, fallback: ContributionType) -> ContributionType:
    text = " ".join([summary.topic or "", summary.overall_summary or ""]).lower()
    if any(token in text for token in ["exam", "midterm", "final", "đề thi"]):
        return ContributionType.PAST_EXAM
    if any(token in text for token in ["exercise", "solution", "bài tập", "lời giải"]):
        return ContributionType.SOLVED_EXERCISE
    if any(token in text for token in ["review", "revision", "ôn tập"]):
        return ContributionType.REVIEW_NOTE
    return fallback


async def _run_agent2_search(query: str) -> Agent2OutputPayload:
    settings = get_settings()
    if not settings.agent2_enabled or not settings.tavily_api_key:
        return build_empty_agent2_output(search_status="error", duration_ms=0)

    start_ms = int(time.monotonic() * 1000)
    try:
        async with httpx.AsyncClient(timeout=float(settings.agent2_timeout_seconds)) as client:
            resp = await client.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": settings.tavily_api_key,
                    "query": query[:400],
                    "search_depth": "basic",
                    "max_results": 3,
                    "include_answer": False,
                },
            )
            resp.raise_for_status()
            data = resp.json()
    except httpx.TimeoutException:
        duration_ms = int(time.monotonic() * 1000) - start_ms
        return build_empty_agent2_output(search_status="timeout", duration_ms=duration_ms)
    except Exception:
        duration_ms = int(time.monotonic() * 1000) - start_ms
        return build_empty_agent2_output(search_status="error", duration_ms=duration_ms)

    duration_ms = int(time.monotonic() * 1000) - start_ms
    references = [
        Agent2ReferencePayload(
            title=(r.get("title") or "")[:200],
            url=r.get("url") or "",
            snippet=(r.get("content") or r.get("snippet") or "")[:500],
            source_type="web",
        )
        for r in data.get("results", [])
        if r.get("url")
    ]
    return Agent2OutputPayload(
        references=references,
        search_status="success",
        search_duration_ms=duration_ms,
    )


def _traceback_tail() -> str:
    return "".join(traceback.format_exc(limit=8))[-4000:]


def _job_try(ctx: dict[str, object]) -> int:
    value = ctx.get("job_try", 1)
    return int(value) if isinstance(value, int | str | float) else 1


__all__ = ["check_sla_breaches", "process_eval_job"]
