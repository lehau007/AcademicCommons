from __future__ import annotations

from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.models.enums import ContributionType, DocumentStatus, DocumentTier, FileFormat
from app.models.tables import AdminAuditLog, Document, DocumentStateLog, User
from app.services.admin_service import mark_permanently_failed


class FakeAdminSession:
    def __init__(self, doc: Document | None) -> None:
        self.doc = doc
        self.added: list[object] = []
        self.committed = False
        self.refreshed: list[object] = []

    async def scalar(self, statement) -> Document | None:
        return self.doc

    def add(self, item: object) -> None:
        self.added.append(item)

    async def flush(self) -> None:
        pass

    async def commit(self) -> None:
        self.committed = True

    async def refresh(self, item: object) -> None:
        self.refreshed.append(item)


def make_document(status: DocumentStatus) -> Document:
    return Document(
        id=uuid4(),
        course_id=uuid4(),
        uploader_id=uuid4(),
        document_tier=DocumentTier.COMMUNITY,
        contribution_type=ContributionType.SUMMARY_NOTE,
        status=status,
        original_filename="stuck.pdf",
        file_format=FileFormat.PDF,
    )


def make_admin() -> User:
    return User(
        id=uuid4(),
        email="admin@example.test",
        hashed_password="hash",
        role="admin",
        full_name="Admin User",
    )


@pytest.mark.asyncio
async def test_mark_permanently_failed_transitions_parsing_to_failed() -> None:
    doc = make_document(DocumentStatus.PARSING)
    session = FakeAdminSession(doc)

    result = await mark_permanently_failed(session, doc.id, make_admin())

    assert result.status == DocumentStatus.FAILED
    assert result.permanently_failed is True
    assert session.committed is True
    state_logs = [item for item in session.added if isinstance(item, DocumentStateLog)]
    assert len(state_logs) == 1
    assert state_logs[0].from_state == DocumentStatus.PARSING
    assert state_logs[0].to_state == DocumentStatus.FAILED
    audit_logs = [item for item in session.added if isinstance(item, AdminAuditLog)]
    assert len(audit_logs) == 1
    assert audit_logs[0].to_state == DocumentStatus.FAILED.value


@pytest.mark.asyncio
async def test_mark_permanently_failed_on_already_failed_just_sets_flag() -> None:
    doc = make_document(DocumentStatus.FAILED)
    session = FakeAdminSession(doc)

    result = await mark_permanently_failed(session, doc.id, make_admin())

    assert result.status == DocumentStatus.FAILED
    assert result.permanently_failed is True
    state_logs = [item for item in session.added if isinstance(item, DocumentStateLog)]
    assert state_logs == []


@pytest.mark.asyncio
async def test_mark_permanently_failed_rejects_approved_document() -> None:
    doc = make_document(DocumentStatus.APPROVED)
    session = FakeAdminSession(doc)

    with pytest.raises(HTTPException) as exc_info:
        await mark_permanently_failed(session, doc.id, make_admin())

    assert exc_info.value.status_code == 409
    assert not doc.permanently_failed
