from uuid import uuid4

import pytest

from app.core.state_machine import (
    ALLOWED_TRANSITIONS,
    DocumentStateMachine,
    DocumentStatus,
    InvalidStateTransition,
    actor_type_for,
    assert_transition_allowed,
    log_admin_action,
)
from app.models import AdminAuditLog, Document, DocumentStateLog, User
from app.models.enums import ContributionType, DocumentTier, FileFormat


class FakeSession:
    def __init__(self) -> None:
        self.added: list[object] = []
        self.flush_count = 0

    def add(self, item: object) -> None:
        self.added.append(item)

    async def flush(self) -> None:
        self.flush_count += 1


def make_document(status: DocumentStatus = DocumentStatus.UPLOADED) -> Document:
    return Document(
        id=uuid4(),
        course_id=uuid4(),
        uploader_id=uuid4(),
        document_tier=DocumentTier.COMMUNITY,
        contribution_type=ContributionType.SUMMARY_NOTE,
        status=status,
        original_filename="summary.pdf",
        file_format=FileFormat.PDF,
    )


def make_user(role: str = "reviewer") -> User:
    return User(
        id=uuid4(),
        email=f"{role}@example.test",
        hashed_password="hash",
        role=role,
        full_name=f"{role.title()} User",
    )


def test_allows_upload_to_parsing() -> None:
    assert_transition_allowed(DocumentStatus.UPLOADED, DocumentStatus.PARSING)


def test_rejects_upload_to_indexed() -> None:
    with pytest.raises(InvalidStateTransition):
        assert_transition_allowed(DocumentStatus.UPLOADED, DocumentStatus.INDEXED)


@pytest.mark.parametrize(("from_state", "to_state"), sorted(ALLOWED_TRANSITIONS, key=lambda item: str(item)))
def test_all_allowed_transitions_are_accepted(
    from_state: DocumentStatus | None,
    to_state: DocumentStatus,
) -> None:
    assert_transition_allowed(from_state, to_state)


@pytest.mark.asyncio
async def test_transition_updates_document_and_adds_state_log() -> None:
    session = FakeSession()
    document = make_document(DocumentStatus.APPROVED)
    actor = make_user("reviewer")

    log = await DocumentStateMachine(session).transition(
        document,
        DocumentStatus.INDEXING,
        actor=actor,
        reason="index worker pickup",
    )

    assert document.status == DocumentStatus.INDEXING
    assert session.flush_count == 1
    assert session.added == [log]
    assert isinstance(log, DocumentStateLog)
    assert log.document_id == document.id
    assert log.from_state == DocumentStatus.APPROVED
    assert log.to_state == DocumentStatus.INDEXING
    assert log.actor_id == actor.id
    assert log.actor_type == "reviewer"
    assert log.reason == "index worker pickup"


@pytest.mark.asyncio
async def test_transition_rejects_invalid_state_without_mutation_or_log() -> None:
    session = FakeSession()
    document = make_document(DocumentStatus.UPLOADED)

    with pytest.raises(InvalidStateTransition):
        await DocumentStateMachine(session).transition(document, DocumentStatus.INDEXED)

    assert document.status == DocumentStatus.UPLOADED
    assert session.added == []
    assert session.flush_count == 0


@pytest.mark.asyncio
async def test_transition_logs_system_actor_for_worker_pickup() -> None:
    session = FakeSession()
    document = make_document(DocumentStatus.UPLOADED)

    log = await DocumentStateMachine(session).transition(
        document,
        DocumentStatus.PARSING,
        reason="ocr worker pickup",
    )

    assert document.status == DocumentStatus.PARSING
    assert log.actor_id is None
    assert log.actor_type == "system"
    assert log.reason == "ocr worker pickup"


@pytest.mark.asyncio
async def test_recovery_transition_requires_admin_actor() -> None:
    session = FakeSession()
    document = make_document(DocumentStatus.FAILED)

    with pytest.raises(InvalidStateTransition):
        await DocumentStateMachine(session).transition(
            document,
            DocumentStatus.PARSING,
            actor=make_user("reviewer"),
            reason="manual retry",
        )

    assert document.status == DocumentStatus.FAILED
    assert session.added == []
    assert session.flush_count == 0

    log = await DocumentStateMachine(session).transition(
        document,
        DocumentStatus.PARSING,
        actor=make_user("admin"),
        reason="manual retry",
    )

    assert document.status == DocumentStatus.PARSING
    assert log.actor_type == "admin"


@pytest.mark.asyncio
async def test_review_transition_requires_reviewer_or_admin_actor() -> None:
    session = FakeSession()
    document = make_document(DocumentStatus.NEEDS_REVIEW)

    with pytest.raises(InvalidStateTransition):
        await DocumentStateMachine(session).transition(
            document,
            DocumentStatus.APPROVED,
            actor=make_user("student"),
            reason="student cannot review",
        )

    assert document.status == DocumentStatus.NEEDS_REVIEW
    assert session.added == []

    log = await DocumentStateMachine(session).transition(
        document,
        DocumentStatus.APPROVED,
        actor=make_user("reviewer"),
        reason="review approved",
    )

    assert document.status == DocumentStatus.APPROVED
    assert log.actor_type == "reviewer"


@pytest.mark.asyncio
async def test_log_admin_action_adds_audit_log() -> None:
    session = FakeSession()
    actor_id = uuid4()
    target_id = uuid4()

    log = await log_admin_action(
        session,
        actor_id=actor_id,
        action_type="reprocess_document",
        target_entity_type="document",
        target_entity_id=target_id,
        from_state=DocumentStatus.FAILED.value,
        to_state=DocumentStatus.PARSING.value,
        reason="manual retry",
    )

    assert session.added == [log]
    assert isinstance(log, AdminAuditLog)
    assert log.actor_id == actor_id
    assert log.action_type == "reprocess_document"
    assert log.target_entity_type == "document"
    assert log.target_entity_id == target_id
    assert log.from_state == DocumentStatus.FAILED.value
    assert log.to_state == DocumentStatus.PARSING.value
    assert log.reason == "manual retry"


def test_actor_type_for_system_and_user() -> None:
    assert actor_type_for(None) == "system"
    assert actor_type_for(make_user("admin")) == "admin"
