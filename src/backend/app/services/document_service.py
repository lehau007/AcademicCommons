from __future__ import annotations

import logging
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import case, delete, desc, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.state_machine import log_admin_action, log_state_transition
from app.models import (
    Citation,
    CommunityVote,
    Course,
    CourseReviewerAssignment,
    Document,
    DocumentChunk,
    DocumentStateLog,
    DocumentSummary,
    EvaluationJob,
    EvaluationReport,
    Notification,
    ProcessingJob,
    ReviewDecision,
    User,
)
from app.models.enums import (
    ContributionType,
    DocumentStatus,
    DocumentTier,
    FileFormat,
    JobStatus,
    MaterialType,
    ProcessingJobType,
)
from app.storage.client import StorageClient, raw_document_key

logger = logging.getLogger(__name__)

# Magic byte signatures for MIME sniffing
_MAGIC_BYTES: dict[bytes, FileFormat] = {
    b"%PDF": FileFormat.PDF,
    b"PK\x03\x04": FileFormat.PPTX,
    b"\xff\xd8": FileFormat.JPG,
    b"\x89PNG": FileFormat.PNG,
}

EXT_TO_FORMAT: dict[str, FileFormat] = {
    "pdf": FileFormat.PDF,
    "pptx": FileFormat.PPTX,
    "jpg": FileFormat.JPG,
    "jpeg": FileFormat.JPG,
    "png": FileFormat.PNG,
}

CONTENT_TYPE_MAP: dict[FileFormat, str] = {
    FileFormat.PDF: "application/pdf",
    FileFormat.PPTX: "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    FileFormat.JPG: "image/jpeg",
    FileFormat.PNG: "image/png",
}


def detect_file_format(filename: str, content: bytes) -> FileFormat:
    """Detect format by magic bytes first, then fall back to extension."""
    for magic, fmt in _MAGIC_BYTES.items():
        if content[: len(magic)] == magic:
            return fmt
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext in EXT_TO_FORMAT:
        return EXT_TO_FORMAT[ext]
    raise ValueError(f"Unsupported file format: {filename}")


def _check_encrypted_pdf(content: bytes) -> None:
    """Raise HTTP 422 if the PDF bytes contain an Encrypt dictionary entry."""
    # Scan a generous portion of the file for the /Encrypt keyword.
    # Real encrypted PDFs always have this in their cross-reference structure.
    sample = content[:65536]
    if b"/Encrypt" in sample:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Encrypted PDFs are not accepted. Please decrypt the file before uploading.",
        )


def can_view_document(user: User, document: Document) -> bool:
    if user.role == "admin":
        return True
    if user.role == "reviewer":
        return document.status in {
            DocumentStatus.NEEDS_REVIEW,
            DocumentStatus.APPROVED,
            DocumentStatus.INDEXING,
            DocumentStatus.INDEXED,
        }
    # Uploaders can always track the status of their own submissions.
    if document.uploader_id == user.id:
        return True
    return document.status == DocumentStatus.INDEXED


async def _assert_reviewer_assigned_to_doc(session: AsyncSession, user: User, document: Document) -> None:
    """For reviewer role: verify they are assigned to the document's course."""
    if user.role != "reviewer":
        return
    assignment = await session.scalar(
        select(CourseReviewerAssignment).where(
            CourseReviewerAssignment.user_id == user.id,
            CourseReviewerAssignment.course_id == document.course_id,
            CourseReviewerAssignment.is_active.is_(True),
        )
    )
    if assignment is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Reviewer not assigned to this course")


async def get_document_or_404(session: AsyncSession, document_id: UUID) -> Document:
    doc = await session.scalar(select(Document).where(Document.id == document_id))
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    return doc


async def _get_course_or_404(session: AsyncSession, course_code: str) -> Course:
    course = await session.scalar(select(Course).where(Course.code == course_code))
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course '{course_code}' not found")
    return course


async def _assert_uploader_is_admin_or_reviewer(session: AsyncSession, user: User, course_id: UUID) -> None:
    if user.role == "admin":
        return
    if user.role != "reviewer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins or assigned reviewers can upload official documents",
        )
    assignment = await session.scalar(
        select(CourseReviewerAssignment).where(
            CourseReviewerAssignment.user_id == user.id,
            CourseReviewerAssignment.course_id == course_id,
            CourseReviewerAssignment.is_active.is_(True),
        )
    )
    if assignment is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Reviewer not assigned to this course")


async def upload_official_document(
    session: AsyncSession,
    storage: StorageClient,
    course_code: str,
    material_type: MaterialType,
    file_content: bytes,
    filename: str,
    uploader: User,
    display_name: str | None = None,
) -> Document:
    course = await _get_course_or_404(session, course_code)
    await _assert_uploader_is_admin_or_reviewer(session, uploader, course.id)

    file_format = detect_file_format(filename, file_content)
    if file_format == FileFormat.PDF:
        _check_encrypted_pdf(file_content)

    existing = await session.scalar(
        select(Document).where(
            Document.course_id == course.id,
            Document.material_type == material_type,
            Document.is_active_version.is_(True),
            Document.document_tier == DocumentTier.OFFICIAL,
        )
    )
    new_version = 1
    if existing is not None:
        existing.is_active_version = False
        new_version = existing.version + 1
        session.add(existing)

    sla_deadline = datetime.now(UTC) + timedelta(hours=course.review_sla_hours)

    doc = Document(
        course_id=course.id,
        uploader_id=uploader.id,
        document_tier=DocumentTier.OFFICIAL,
        material_type=material_type,
        contribution_type=None,
        topic_tags=[],
        status=DocumentStatus.UPLOADED,
        version=new_version,
        is_active_version=True,
        original_filename=filename,
        display_name=display_name,
        file_format=file_format,
        sla_deadline=sla_deadline,
    )
    session.add(doc)
    await session.flush()

    storage_path = raw_document_key(course.id, doc.id, filename)
    content_type = CONTENT_TYPE_MAP.get(file_format, "application/octet-stream")
    await storage.put_object(storage_path, file_content, content_type)
    doc.storage_raw_path = storage_path

    await log_state_transition(
        session,
        document_id=doc.id,
        from_state=None,
        to_state=DocumentStatus.UPLOADED,
        actor_id=uploader.id,
        actor_type=uploader.role,
        reason="Document uploaded",
    )

    processing_job = ProcessingJob(
        document_id=doc.id,
        job_type=ProcessingJobType.OCR,
        run_number=1,
        is_latest=True,
        status=JobStatus.PENDING,
    )
    session.add(processing_job)
    await session.flush()
    await session.commit()
    await session.refresh(doc)
    await session.refresh(processing_job)

    try:
        from app.workers.jobs import enqueue_ocr_job
        await enqueue_ocr_job(session, doc.id, processing_job.id)
    except Exception:
        logger.warning("Failed to enqueue OCR job for document %s; Redis may be unavailable", doc.id)

    return doc


async def upload_community_document(
    session: AsyncSession,
    storage: StorageClient,
    course_code: str,
    contribution_type: ContributionType,
    topic_tags: list[str],
    file_content: bytes,
    filename: str,
    uploader: User,
    display_name: str | None = None,
) -> Document:
    # Only student or admin may upload community documents
    if uploader.role not in {"student", "admin"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students or admins can upload community documents",
        )

    course = await _get_course_or_404(session, course_code)

    if not course.topic_summary:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": "COURSE_NOT_READY", "course_code": course_code},
        )

    file_format = detect_file_format(filename, file_content)
    if file_format == FileFormat.PDF:
        _check_encrypted_pdf(file_content)

    sla_deadline = datetime.now(UTC) + timedelta(hours=course.review_sla_hours)

    doc = Document(
        course_id=course.id,
        uploader_id=uploader.id,
        document_tier=DocumentTier.COMMUNITY,
        material_type=None,
        contribution_type=contribution_type,
        topic_tags=topic_tags,
        status=DocumentStatus.UPLOADED,
        version=1,
        is_active_version=True,
        original_filename=filename,
        display_name=display_name,
        file_format=file_format,
        sla_deadline=sla_deadline,
    )
    session.add(doc)
    await session.flush()

    storage_path = raw_document_key(course.id, doc.id, filename)
    content_type = CONTENT_TYPE_MAP.get(file_format, "application/octet-stream")
    await storage.put_object(storage_path, file_content, content_type)
    doc.storage_raw_path = storage_path

    await log_state_transition(
        session,
        document_id=doc.id,
        from_state=None,
        to_state=DocumentStatus.UPLOADED,
        actor_id=uploader.id,
        actor_type=uploader.role,
        reason="Document uploaded",
    )

    processing_job = ProcessingJob(
        document_id=doc.id,
        job_type=ProcessingJobType.OCR,
        run_number=1,
        is_latest=True,
        status=JobStatus.PENDING,
    )
    session.add(processing_job)
    await session.flush()
    await session.commit()
    await session.refresh(doc)
    await session.refresh(processing_job)

    try:
        from app.workers.jobs import enqueue_ocr_job
        await enqueue_ocr_job(session, doc.id, processing_job.id)
    except Exception:
        logger.warning("Failed to enqueue OCR job for document %s; Redis may be unavailable", doc.id)

    return doc


async def get_document_list(
    session: AsyncSession,
    course_code: str | None,
    tier: DocumentTier | None,
    status_filter: DocumentStatus | None,
    sort: str,
    user: User,
    subtype: str | None = None,
    topic_tag: str | None = None,
) -> list[Document]:
    stmt = select(Document)

    if course_code is not None:
        course = await session.scalar(select(Course).where(Course.code == course_code))
        if course is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course '{course_code}' not found")
        stmt = stmt.where(Document.course_id == course.id)

    if tier is not None:
        stmt = stmt.where(Document.document_tier == tier)

    if status_filter is not None:
        stmt = stmt.where(Document.status == status_filter)

    # subtype: material_type for official, contribution_type for community
    if subtype is not None:
        stmt = stmt.where(
            (Document.material_type == subtype) | (Document.contribution_type == subtype)
        )

    # topic_tag: check JSONB array contains the tag
    if topic_tag is not None:
        stmt = stmt.where(Document.topic_tags.contains([topic_tag]))

    # Role-based visibility
    if user.role == "student":
        stmt = stmt.where(Document.status == DocumentStatus.INDEXED)
    elif user.role == "reviewer":
        stmt = stmt.where(
            Document.status.in_([
                DocumentStatus.NEEDS_REVIEW,
                DocumentStatus.APPROVED,
                DocumentStatus.INDEXING,
                DocumentStatus.INDEXED,
            ])
        )
    # admin sees all

    if sort == "votes":
        vote_subq = (
            select(
                CommunityVote.document_id,
                func.sum(
                    case(
                        (CommunityVote.vote == "up", 1),
                        (CommunityVote.vote == "down", -1),
                        else_=0,
                    )
                ).label("net_votes"),
            )
            .group_by(CommunityVote.document_id)
            .subquery()
        )
        stmt = stmt.outerjoin(vote_subq, Document.id == vote_subq.c.document_id)
        stmt = stmt.order_by(func.coalesce(vote_subq.c.net_votes, 0).desc())
    else:
        stmt = stmt.order_by(desc(Document.uploaded_at))

    result = await session.scalars(stmt)
    return list(result.all())


async def list_documents_for_management(
    session: AsyncSession,
    user: User,
    uploaded_from: datetime | None = None,
    uploaded_to: datetime | None = None,
    status_filter: DocumentStatus | None = None,
    course_code: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> list[Document]:
    """List documents an admin/reviewer oversees, across all pipeline statuses.

    Admins see every document; reviewers see documents in courses they have an
    active assignment for. Used by the admin/reviewer document-management page to
    track processing progress and to delete documents. Optionally filtered by
    upload date range (inclusive), pipeline status, and course code, with
    limit/offset pagination.
    """
    stmt = (
        select(Document)
        .options(selectinload(Document.course), selectinload(Document.state_logs))
        .order_by(desc(Document.uploaded_at))
    )
    if uploaded_from is not None:
        stmt = stmt.where(Document.uploaded_at >= uploaded_from)
    if uploaded_to is not None:
        stmt = stmt.where(Document.uploaded_at <= uploaded_to)
    if status_filter is not None:
        stmt = stmt.where(Document.status == status_filter)
    if course_code is not None:
        stmt = stmt.join(Course, Course.id == Document.course_id).where(Course.code == course_code)
    if user.role == "reviewer":
        stmt = stmt.join(
            CourseReviewerAssignment,
            CourseReviewerAssignment.course_id == Document.course_id,
        ).where(
            CourseReviewerAssignment.user_id == user.id,
            CourseReviewerAssignment.is_active.is_(True),
        )
    elif user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins or reviewers can manage documents",
        )
    if offset is not None:
        stmt = stmt.offset(offset)
    if limit is not None:
        stmt = stmt.limit(limit)
    result = await session.scalars(stmt)
    return list(result.all())


async def hard_delete_document(
    session: AsyncSession,
    storage: StorageClient,
    document_id: UUID,
    reason: str,
    actor: User,
) -> None:
    """Permanently delete a document, its child rows, and its storage objects.

    Authorization mirrors official upload: admins may delete any document,
    reviewers only documents in courses they are assigned to. The deletion is
    recorded in the admin audit log (which has no FK to documents, so the reason
    survives the hard delete).
    """
    doc = await get_document_or_404(session, document_id)
    await _assert_uploader_is_admin_or_reviewer(session, actor, doc.course_id)

    raw_path = doc.storage_raw_path
    md_path = doc.storage_md_path

    try:
        await log_admin_action(
            session,
            actor_id=actor.id,
            action_type="document_deleted",
            target_entity_type="document",
            target_entity_id=doc.id,
            from_state=doc.status.value,
            reason=reason,
        )

        # Durable notification for the uploader. The notifications table has no
        # FK to documents, so this row survives the hard delete below (after
        # which doc.uploader_id and the state logs are gone).
        session.add(
            Notification(
                recipient_id=doc.uploader_id,
                type="document_deleted",
                message=f'Tài liệu "{doc.original_filename}" đã bị gỡ. Lý do: {reason}',
                related_entity_id=doc.id,
            )
        )

        # Delete grand-child rows first: they reference the document's children,
        # not the document itself. review_decisions -> evaluation_reports, and
        # citations -> document_chunks.
        await session.execute(
            delete(ReviewDecision).where(
                ReviewDecision.evaluation_report_id.in_(
                    select(EvaluationReport.id).where(EvaluationReport.document_id == doc.id)
                )
            )
        )
        await session.execute(
            delete(Citation).where(
                Citation.chunk_id.in_(
                    select(DocumentChunk.id).where(DocumentChunk.document_id == doc.id)
                )
            )
        )

        # Then the document's direct child rows. document_summaries/document_chunks
        # cascade at the DB level, but the rest do not. Order matters:
        # evaluation_reports has a composite FK into evaluation_jobs, so reports
        # must be removed before jobs.
        for model in (
            EvaluationReport,
            EvaluationJob,
            DocumentChunk,
            DocumentSummary,
            ProcessingJob,
            CommunityVote,
            DocumentStateLog,
        ):
            await session.execute(delete(model).where(model.document_id == doc.id))

        await session.execute(delete(Document).where(Document.id == doc.id))
        await session.commit()
    except IntegrityError:
        await session.rollback()
        logger.exception("Failed to hard-delete document %s", document_id)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Không thể xoá tài liệu vì còn dữ liệu liên quan chưa được dọn dẹp.",
        ) from None

    # Best-effort storage cleanup after the row is gone; failures here must not
    # resurrect the document record.
    for key in (raw_path, md_path):
        if key:
            try:
                await storage.delete_object(key)
            except Exception:
                logger.warning("Failed to delete storage object %s for document %s", key, document_id)


async def get_evaluation_report(
    session: AsyncSession,
    document_id: UUID,
    user: User,
) -> dict[str, Any]:
    doc = await get_document_or_404(session, document_id)
    if user.role not in {"reviewer", "admin"}:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    if user.role == "reviewer":
        await _assert_reviewer_assigned_to_doc(session, user, doc)

    report = await session.scalar(
        select(EvaluationReport).where(
            EvaluationReport.document_id == document_id,
            EvaluationReport.is_latest.is_(True),
        )
    )
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No evaluation report found")

    return {
        "id": str(report.id),
        "document_id": str(report.document_id),
        "final_recommendation": report.final_recommendation,
        "agent1_output": report.agent1_output,
        "agent2_output": report.agent2_output,
        "agent3_output": report.agent3_output,
        "schema_version": report.schema_version,
        "generated_at": report.generated_at.isoformat(),
    }


async def get_markdown_content(
    session: AsyncSession,
    storage: StorageClient,
    document_id: UUID,
    user: User,
) -> str:
    doc = await get_document_or_404(session, document_id)
    if not can_view_document(user, doc):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    await _assert_reviewer_assigned_to_doc(session, user, doc)
    if doc.storage_md_path is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Markdown content not available")
    content_bytes = await storage.get_object(doc.storage_md_path)
    return content_bytes.decode("utf-8")


async def get_signed_url(
    session: AsyncSession,
    storage: StorageClient,
    document_id: UUID,
    user: User,
) -> str:
    doc = await get_document_or_404(session, document_id)
    if not can_view_document(user, doc):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    await _assert_reviewer_assigned_to_doc(session, user, doc)
    if doc.storage_raw_path is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Raw file not available")
    return await storage.generate_signed_url(doc.storage_raw_path, ttl=900)
