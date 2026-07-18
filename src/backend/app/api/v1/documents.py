from __future__ import annotations

import json
from datetime import datetime
from typing import Annotated, Any

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, Response, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.core.auth import get_current_user, require_role
from app.db.session import get_session
from app.models import Document, DocumentStateLog, EvaluationReport, User
from app.models.enums import ContributionType, DocumentStatus, MaterialType
from app.schemas.documents import (
    DocumentDeleteRequest,
    DocumentRead,
    DocumentUploadResponse,
    SignedUrlResponse,
)
from app.services.document_service import (
    can_view_document,
    get_evaluation_report,
    get_markdown_content,
    get_signed_url,
    hard_delete_document,
    list_documents_for_management,
    upload_community_document,
    upload_official_document,
)
from app.services.failure_hints import get_failure_hints
from app.storage import get_storage
from app.storage.client import StorageClient

router = APIRouter(prefix="/documents", tags=["documents"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]
StorageDep = Annotated[StorageClient, Depends(get_storage)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]
ReviewerOrAdminDep = Annotated[User, Depends(require_role("reviewer", "admin"))]

_PRIVILEGED_ROLES = {"admin", "reviewer"}


def _max_upload_bytes_for(user: User) -> int:
    """Higher upload cap for admin/reviewer, default cap for everyone else."""
    settings = get_settings()
    if user.role in _PRIVILEGED_ROLES:
        return settings.max_upload_bytes_privileged
    return settings.max_upload_bytes


def _overall_ai_score(agent3_output: Any) -> float | None:
    """Average of the AI relevance/completeness/quality sub-scores, on a 0-100 scale."""
    if not isinstance(agent3_output, dict):
        return None
    scores = agent3_output.get("scores") or {}
    values = [scores.get(k) for k in ("relevance", "completeness", "quality")]
    numeric = [v for v in values if isinstance(v, (int, float))]
    if not numeric:
        return None
    return round(sum(numeric) / len(numeric) * 10, 1)


@router.get("", response_model=list[DocumentRead])
async def list_my_documents(
    session: SessionDep,
    user: CurrentUserDep,
) -> list[DocumentRead]:
    """List all documents uploaded by the current user."""
    from sqlalchemy.orm import selectinload
    stmt = (
        select(Document)
        .where(Document.uploader_id == user.id)
        .options(selectinload(Document.course), selectinload(Document.state_logs))
        .order_by(Document.uploaded_at.desc())
    )
    result = await session.execute(stmt)
    docs = list(result.scalars())

    rejected_ids = [d.id for d in docs if d.status == DocumentStatus.REJECTED]
    reasons: dict[Any, str | None] = {}
    if rejected_ids:
        log_stmt = (
            select(DocumentStateLog.document_id, DocumentStateLog.reason)
            .where(
                DocumentStateLog.document_id.in_(rejected_ids),
                DocumentStateLog.to_state == DocumentStatus.REJECTED,
            )
            .order_by(DocumentStateLog.transitioned_at.desc())
        )
        log_result = await session.execute(log_stmt)
        for document_id, reason in log_result.all():
            # Rows are ordered newest-first; keep the latest reason per document.
            if document_id not in reasons:
                reasons[document_id] = reason

    failed_ids = [d.id for d in docs if d.status == DocumentStatus.FAILED]
    failure_hints = await get_failure_hints(session, failed_ids)

    return [
        DocumentRead.model_validate(d).model_copy(
            update={"review_reason": reasons.get(d.id), "failure_hint": failure_hints.get(d.id)}
        )
        for d in docs
    ]


@router.get("/manage", response_model=list[DocumentRead])
async def list_managed_documents(
    session: SessionDep,
    user: ReviewerOrAdminDep,
    uploaded_from: datetime | None = Query(default=None, description="Only documents uploaded at/after this time"),
    uploaded_to: datetime | None = Query(default=None, description="Only documents uploaded at/before this time"),
    status: DocumentStatus | None = Query(default=None, description="Only documents in this pipeline status"),
    course_code: str | None = Query(default=None, description="Only documents in this course"),
    limit: int | None = Query(default=None, ge=1, le=200),
    offset: int | None = Query(default=None, ge=0),
) -> list[DocumentRead]:
    """List documents an admin/reviewer oversees (all statuses, role-scoped), optionally by upload date range.

    Each item is enriched with the latest AI evaluation summary (recommendation +
    overall score) so reviewers can triage and bulk-approve without opening each report.
    """
    docs = await list_documents_for_management(
        session,
        user,
        uploaded_from,
        uploaded_to,
        status_filter=status,
        course_code=course_code,
        limit=limit,
        offset=offset,
    )
    doc_ids = [d.id for d in docs]
    reports: dict[Any, EvaluationReport] = {}
    if doc_ids:
        rows = await session.execute(
            select(EvaluationReport).where(
                EvaluationReport.document_id.in_(doc_ids),
                EvaluationReport.is_latest.is_(True),
            )
        )
        for report in rows.scalars():
            reports[report.document_id] = report

    result: list[DocumentRead] = []
    for d in docs:
        report = reports.get(d.id)
        result.append(
            DocumentRead.model_validate(d).model_copy(
                update={
                    "ai_recommendation": report.final_recommendation if report else None,
                    "ai_overall_score": _overall_ai_score(report.agent3_output) if report else None,
                }
            )
        )
    return result


@router.post("/official", status_code=status.HTTP_201_CREATED, response_model=DocumentUploadResponse)
async def upload_official(
    session: SessionDep,
    storage: StorageDep,
    user: CurrentUserDep,
    course_code: str = Form(...),
    material_type: MaterialType = Form(...),
    file: UploadFile = File(...),
    display_name: str | None = Form(default=None),
) -> DocumentUploadResponse:
    max_bytes = _max_upload_bytes_for(user)
    if file.size is not None and file.size > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds the {max_bytes // (1024 * 1024)}MB upload limit.",
        )
    file_content = await file.read()
    if len(file_content) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds the {max_bytes // (1024 * 1024)}MB upload limit.",
        )
    doc = await upload_official_document(
        session,
        storage,
        course_code,
        material_type,
        file_content,
        file.filename or "upload",
        user,
        display_name=display_name,
    )
    return DocumentUploadResponse(
        document_id=doc.id,
        status=doc.status.value,
        sla_deadline=doc.sla_deadline,
    )


@router.post("/community", status_code=status.HTTP_201_CREATED, response_model=DocumentUploadResponse)
async def upload_community(
    session: SessionDep,
    storage: StorageDep,
    user: CurrentUserDep,
    course_code: str = Form(...),
    contribution_type: ContributionType = Form(...),
    file: UploadFile = File(...),
    shared_rights_confirmed: bool = Form(...),
    topic_tags: str = Form(default="[]"),
    display_name: str | None = Form(default=None),
) -> DocumentUploadResponse:
    if not shared_rights_confirmed:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="You must confirm you have the rights to share this material before uploading.",
        )
    try:
        parsed_tags: list[str] = json.loads(topic_tags)
        if not isinstance(parsed_tags, list):
            parsed_tags = []
    except (json.JSONDecodeError, ValueError):
        parsed_tags = []

    max_bytes = _max_upload_bytes_for(user)
    if file.size is not None and file.size > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds the {max_bytes // (1024 * 1024)}MB upload limit.",
        )
    file_content = await file.read()
    if len(file_content) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds the {max_bytes // (1024 * 1024)}MB upload limit.",
        )
    doc = await upload_community_document(
        session,
        storage,
        course_code,
        contribution_type,
        parsed_tags,
        file_content,
        file.filename or "upload",
        user,
        display_name=display_name,
    )
    return DocumentUploadResponse(
        document_id=doc.id,
        status=doc.status.value,
        sla_deadline=doc.sla_deadline,
    )


@router.get("/{document_id}", response_model=DocumentRead)
async def get_document(
    document_id: str,
    session: SessionDep,
    user: CurrentUserDep,
) -> DocumentRead:
    from uuid import UUID
    try:
        doc_uuid = UUID(document_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid document ID") from None

    from sqlalchemy.orm import selectinload
    stmt = (
        select(Document)
        .where(Document.id == doc_uuid)
        .options(selectinload(Document.course), selectinload(Document.state_logs))
    )
    doc = (await session.execute(stmt)).scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    if not can_view_document(user, doc):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    review_reason: str | None = None
    if doc.status == DocumentStatus.REJECTED:
        log_stmt = (
            select(DocumentStateLog.reason)
            .where(
                DocumentStateLog.document_id == doc.id,
                DocumentStateLog.to_state == DocumentStatus.REJECTED,
            )
            .order_by(DocumentStateLog.transitioned_at.desc())
            .limit(1)
        )
        review_reason = (await session.execute(log_stmt)).scalar_one_or_none()

    return DocumentRead.model_validate(doc).model_copy(update={"review_reason": review_reason})


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: str,
    payload: DocumentDeleteRequest,
    session: SessionDep,
    storage: StorageDep,
    user: ReviewerOrAdminDep,
) -> Response:
    from uuid import UUID
    try:
        doc_uuid = UUID(document_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid document ID") from None

    await hard_delete_document(session, storage, doc_uuid, payload.reason, user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{document_id}/markdown")
async def get_document_markdown(
    document_id: str,
    session: SessionDep,
    storage: StorageDep,
    user: CurrentUserDep,
) -> Response:
    from uuid import UUID
    try:
        doc_uuid = UUID(document_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid document ID") from None

    content = await get_markdown_content(session, storage, doc_uuid, user)
    return Response(content=content, media_type="text/plain")


@router.get("/{document_id}/raw-url", response_model=SignedUrlResponse)
async def get_document_raw_url(
    document_id: str,
    session: SessionDep,
    storage: StorageDep,
    user: CurrentUserDep,
) -> SignedUrlResponse:
    from uuid import UUID
    try:
        doc_uuid = UUID(document_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid document ID") from None

    url = await get_signed_url(session, storage, doc_uuid, user)
    return SignedUrlResponse(url=url, expires_in_seconds=900)


@router.get("/{document_id}/evaluation-report")
async def get_document_evaluation_report(
    document_id: str,
    session: SessionDep,
    user: CurrentUserDep,
) -> dict[str, Any]:
    from uuid import UUID
    try:
        doc_uuid = UUID(document_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid document ID") from None

    return await get_evaluation_report(session, doc_uuid, user)
