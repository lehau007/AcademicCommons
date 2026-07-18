from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AdminAuditLog, Document, DocumentStateLog, User
from app.models.enums import DocumentStatus

ALLOWED_TRANSITIONS: set[tuple[DocumentStatus | None, DocumentStatus]] = {
    (None, DocumentStatus.UPLOADED),
    (DocumentStatus.UPLOADED, DocumentStatus.PARSING),
    (DocumentStatus.PARSING, DocumentStatus.EVALUATING),
    (DocumentStatus.PARSING, DocumentStatus.APPROVED),
    (DocumentStatus.PARSING, DocumentStatus.FAILED),
    (DocumentStatus.EVALUATING, DocumentStatus.NEEDS_REVIEW),
    (DocumentStatus.EVALUATING, DocumentStatus.FAILED),
    (DocumentStatus.NEEDS_REVIEW, DocumentStatus.APPROVED),
    (DocumentStatus.NEEDS_REVIEW, DocumentStatus.REJECTED),
    (DocumentStatus.APPROVED, DocumentStatus.INDEXING),
    (DocumentStatus.INDEXING, DocumentStatus.INDEXED),
    (DocumentStatus.INDEXING, DocumentStatus.FAILED),
    (DocumentStatus.FAILED, DocumentStatus.PARSING),
    (DocumentStatus.FAILED, DocumentStatus.EVALUATING),
    (DocumentStatus.REJECTED, DocumentStatus.PARSING),
}


class InvalidStateTransition(ValueError):
    pass


def assert_transition_allowed(current: DocumentStatus | None, target: DocumentStatus) -> None:
    if (current, target) not in ALLOWED_TRANSITIONS:
        raise InvalidStateTransition(f"Document transition {current!s} -> {target!s} is not allowed")


def assert_actor_allowed(current: DocumentStatus | None, target: DocumentStatus, actor: User | None) -> None:
    actor_role = actor_type_for(actor)
    if (current, target) in {
        (DocumentStatus.FAILED, DocumentStatus.PARSING),
        (DocumentStatus.FAILED, DocumentStatus.EVALUATING),
        (DocumentStatus.REJECTED, DocumentStatus.PARSING),
    } and actor_role != "admin":
        raise InvalidStateTransition(f"Document transition {current!s} -> {target!s} requires admin actor")

    if (current, target) in {
        (DocumentStatus.NEEDS_REVIEW, DocumentStatus.APPROVED),
        (DocumentStatus.NEEDS_REVIEW, DocumentStatus.REJECTED),
    } and actor_role not in {"reviewer", "admin"}:
        raise InvalidStateTransition(f"Document transition {current!s} -> {target!s} requires reviewer or admin actor")


def actor_type_for(user: User | None) -> str:
    return "system" if user is None else user.role


async def log_state_transition(
    session: AsyncSession,
    *,
    document_id: UUID,
    from_state: DocumentStatus | None,
    to_state: DocumentStatus,
    actor_id: UUID | None,
    actor_type: str,
    reason: str | None = None,
) -> DocumentStateLog:
    log = DocumentStateLog(
        document_id=document_id,
        from_state=from_state,
        to_state=to_state,
        actor_id=actor_id,
        actor_type=actor_type,
        reason=reason,
    )
    session.add(log)
    return log


async def log_admin_action(
    session: AsyncSession,
    *,
    actor_id: UUID,
    action_type: str,
    target_entity_type: str,
    target_entity_id: UUID | None = None,
    from_state: str | None = None,
    to_state: str | None = None,
    reason: str | None = None,
) -> AdminAuditLog:
    log = AdminAuditLog(
        actor_id=actor_id,
        action_type=action_type,
        target_entity_type=target_entity_type,
        target_entity_id=target_entity_id,
        from_state=from_state,
        to_state=to_state,
        reason=reason,
    )
    session.add(log)
    return log


class DocumentStateMachine:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def transition(
        self,
        document: Document,
        to_state: DocumentStatus,
        *,
        actor: User | None = None,
        reason: str | None = None,
    ) -> DocumentStateLog:
        from_state = document.status
        assert_transition_allowed(from_state, to_state)
        assert_actor_allowed(from_state, to_state, actor)

        document.status = to_state
        log = await log_state_transition(
            self.session,
            document_id=document.id,
            from_state=from_state,
            to_state=to_state,
            actor_id=None if actor is None else actor.id,
            actor_type=actor_type_for(actor),
            reason=reason,
        )
        await self.session.flush()
        return log
