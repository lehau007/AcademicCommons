from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.db.session import get_session
from app.models import Document, DocumentStateLog, Notification, User
from app.models.enums import DocumentStatus
from app.schemas.notifications import NotificationItem

router = APIRouter(prefix="/notifications", tags=["notifications"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]

_DEFAULT_LIMIT = 10
_MAX_LIMIT = 50

# Human-readable Vietnamese messages keyed by the transition target state.
_STATE_MESSAGES: dict[DocumentStatus, str] = {
    DocumentStatus.APPROVED: 'Tài liệu "{name}" đã được duyệt',
    DocumentStatus.REJECTED: 'Tài liệu "{name}" đã bị từ chối',
    DocumentStatus.NEEDS_REVIEW: 'Tài liệu "{name}" đang chờ duyệt',
    DocumentStatus.FAILED: 'Tài liệu "{name}" xử lý thất bại',
    DocumentStatus.INDEXED: 'Tài liệu "{name}" đã được lập chỉ mục',
}


@router.get("", response_model=list[NotificationItem])
async def list_notifications(
    user: CurrentUserDep,
    session: SessionDep,
    limit: int = Query(_DEFAULT_LIMIT, ge=1, le=_MAX_LIMIT),
    offset: int = Query(0, ge=0),
) -> list[NotificationItem]:
    # The feed merges two time-ordered sources, so to return the [offset, offset+limit)
    # slice of the merged stream each source must contribute up to `window` rows.
    window = offset + limit
    items: list[tuple[object, NotificationItem]] = []

    # Persisted, durable notifications addressed to this user.
    persisted = await session.scalars(
        select(Notification)
        .where(Notification.recipient_id == user.id)
        .order_by(desc(Notification.created_at))
        .limit(window)
    )
    for n in persisted:
        items.append(
            (
                n.created_at,
                NotificationItem(
                    id=str(n.id),
                    type=n.type,
                    message=n.message,
                    created_at=n.created_at,
                ),
            )
        )

    # Live status events derived from document state logs.
    log_stmt = (
        select(DocumentStateLog, Document.original_filename)
        .join(Document, Document.id == DocumentStateLog.document_id)
        .order_by(desc(DocumentStateLog.transitioned_at))
        .limit(window)
    )
    if user.role == "student":
        log_stmt = log_stmt.where(Document.uploader_id == user.id)
    else:
        # Reviewers/admins: surface documents entering the review queue.
        log_stmt = log_stmt.where(DocumentStateLog.to_state == DocumentStatus.NEEDS_REVIEW)

    rows = await session.execute(log_stmt)
    for log, filename in rows.all():
        template = _STATE_MESSAGES.get(log.to_state)
        if template is None:
            continue
        items.append(
            (
                log.transitioned_at,
                NotificationItem(
                    id=str(log.id),
                    type=f"status_{log.to_state.value.lower()}",
                    message=template.format(name=filename),
                    created_at=log.transitioned_at,
                ),
            )
        )

    items.sort(key=lambda pair: pair[0], reverse=True)
    return [item for _, item in items[offset : offset + limit]]
