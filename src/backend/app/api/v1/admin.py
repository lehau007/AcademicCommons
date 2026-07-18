from __future__ import annotations

from datetime import UTC, datetime
from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import hash_password, require_role
from app.core.state_machine import log_admin_action
from app.db.session import get_session
from app.models import Document, User
from app.schemas.admin import AuditLogEntry, AuditLogPage, FailedDocumentEntry, ReprocessRequest, SeedStatusResponse
from app.schemas.auth import UserCreate, UserRead, UserUpdate
from app.services import admin_service

router = APIRouter(prefix="/admin", tags=["admin"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]
AdminOnlyDep = Annotated[User, Depends(require_role("admin"))]


def _doc_to_dict(doc: Document) -> dict[str, Any]:
    return {
        "id": str(doc.id),
        "status": doc.status.value,
        "original_filename": doc.original_filename,
        "document_tier": doc.document_tier.value,
        "uploaded_at": doc.uploaded_at.isoformat(),
        "updated_at": doc.updated_at.isoformat(),
        "permanently_failed": doc.permanently_failed,
    }


@router.get("/dead-letter", response_model=list[FailedDocumentEntry])
async def get_failed_documents(
    session: SessionDep,
    _: AdminOnlyDep,
) -> list[FailedDocumentEntry]:
    """List all FAILED documents with job failure details."""
    items = await admin_service.get_failed_documents(session)
    return [FailedDocumentEntry(**item) for item in items]


@router.post("/documents/{document_id}/reprocess")
async def reprocess_document(
    document_id: UUID,
    payload: ReprocessRequest,
    session: SessionDep,
    user: AdminOnlyDep,
) -> dict[str, Any]:
    """Reset a FAILED or REJECTED document back to PARSING or EVALUATING for reprocessing."""
    doc = await admin_service.reprocess_document(session, document_id, payload.from_state, user)
    return _doc_to_dict(doc)


@router.post("/documents/{document_id}/mark-permanently-failed")
async def mark_permanently_failed(
    document_id: UUID,
    session: SessionDep,
    user: AdminOnlyDep,
) -> dict[str, Any]:
    """Mark a document as permanently failed so it is excluded from retry queues."""
    doc = await admin_service.mark_permanently_failed(session, document_id, user)
    return _doc_to_dict(doc)


@router.get("/audit-log", response_model=AuditLogPage)
async def get_audit_log(
    session: SessionDep,
    _: AdminOnlyDep,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
    actor_id: UUID | None = Query(default=None),
    action_type: str | None = Query(default=None),
    target_entity_id: UUID | None = Query(default=None),
) -> AuditLogPage:
    """Paginated admin audit log with optional filters."""
    logs, total = await admin_service.get_audit_log(
        session,
        page=page,
        page_size=page_size,
        actor_id=actor_id,
        action_type=action_type,
        target_entity_id=target_entity_id,
    )
    return AuditLogPage(
        items=[AuditLogEntry.model_validate(log) for log in logs],
        total=total,
    )


@router.get("/courses/{course_code}/seed-status", response_model=SeedStatusResponse)
async def get_seed_status(
    course_code: str,
    session: SessionDep,
    _: AdminOnlyDep,
) -> SeedStatusResponse:
    """Check if a course has seed data and whether it is in cold-start mode."""
    data = await admin_service.get_seed_status(session, course_code)
    return SeedStatusResponse(**data)


@router.get("/users", response_model=list[UserRead])
async def list_users(
    session: SessionDep,
    _: AdminOnlyDep,
    role: str | None = Query(default=None, description="Filter users by role"),
) -> list[UserRead]:
    """List users for administration/reviewer assignments, optionally filtered by role."""
    query = select(User)
    if role:
        query = query.where(User.role == role)

    result = await session.execute(query)
    users = result.scalars().all()

    return [UserRead.model_validate(u) for u in users]


@router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    session: SessionDep,
    _: AdminOnlyDep,
) -> UserRead:
    """Admin-only creation of staff accounts (reviewer/admin). Students must self-register."""
    if payload.role == "student":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Students must self-register via /auth/register",
        )

    existing = await session.scalar(select(User).where(User.email == payload.email))
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role=payload.role,
        full_name=payload.full_name,
        # Staff accounts are operator-validated by an admin, so skip the
        # email-verification round trip for them.
        is_email_verified=True,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return UserRead.model_validate(user)


@router.patch("/users/{user_id}", response_model=UserRead)
async def update_user(
    user_id: UUID,
    payload: UserUpdate,
    session: SessionDep,
    admin: AdminOnlyDep,
) -> UserRead:
    """Admin-only partial update of a user's role and/or active status."""
    target = await session.scalar(select(User).where(User.id == user_id))
    if target is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    is_self = target.id == admin.id
    would_demote = payload.role is not None and payload.role != "admin"
    would_deactivate = payload.is_active is False
    if is_self and (would_demote or would_deactivate):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admins cannot demote or deactivate their own account",
        )

    old_role = target.role
    old_is_active = target.is_active

    if payload.role is not None:
        target.role = payload.role
    if payload.is_active is not None:
        target.is_active = payload.is_active
    target.updated_at = datetime.now(UTC)

    await log_admin_action(
        session,
        actor_id=admin.id,
        action_type="user_updated",
        target_entity_type="user",
        target_entity_id=target.id,
        from_state=f"role={old_role},is_active={old_is_active}",
        to_state=f"role={target.role},is_active={target.is_active}",
        reason="Admin updated user role/status",
    )

    await session.commit()
    await session.refresh(target)
    return UserRead.model_validate(target)
