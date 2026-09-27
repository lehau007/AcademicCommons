from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.models.enums import DocumentStatus
from app.services import document_service


@pytest.mark.asyncio
async def test_hard_delete_also_removes_asset_prefix(monkeypatch: pytest.MonkeyPatch) -> None:
    doc = MagicMock()
    doc.id, doc.course_id = uuid4(), uuid4()
    doc.status = DocumentStatus.INDEXED
    doc.storage_raw_path, doc.storage_md_path = "raw-key", "md-key"
    monkeypatch.setattr(document_service, "get_document_or_404", AsyncMock(return_value=doc))
    monkeypatch.setattr(document_service, "_assert_uploader_is_admin_or_reviewer", AsyncMock())
    monkeypatch.setattr(document_service, "log_admin_action", AsyncMock())
    session = MagicMock()
    session.execute = AsyncMock()
    session.commit = AsyncMock()
    storage = MagicMock()
    storage.delete_object = AsyncMock()
    storage.delete_prefix = AsyncMock(return_value=3)

    await document_service.hard_delete_document(session, storage, doc.id, "spam", MagicMock())

    storage.delete_prefix.assert_awaited_once_with(f"documents/{doc.course_id}/{doc.id}/assets/")


@pytest.mark.asyncio
async def test_hard_delete_survives_asset_cleanup_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    doc = MagicMock()
    doc.id, doc.course_id = uuid4(), uuid4()
    doc.status = DocumentStatus.INDEXED
    doc.storage_raw_path, doc.storage_md_path = None, None
    monkeypatch.setattr(document_service, "get_document_or_404", AsyncMock(return_value=doc))
    monkeypatch.setattr(document_service, "_assert_uploader_is_admin_or_reviewer", AsyncMock())
    monkeypatch.setattr(document_service, "log_admin_action", AsyncMock())
    session = MagicMock()
    session.execute = AsyncMock()
    session.commit = AsyncMock()
    storage = MagicMock()
    storage.delete_object = AsyncMock()
    storage.delete_prefix = AsyncMock(side_effect=RuntimeError("s3 down"))

    await document_service.hard_delete_document(session, storage, doc.id, "spam", MagicMock())  # no raise
