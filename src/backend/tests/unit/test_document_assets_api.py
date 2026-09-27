from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.models.enums import DocumentStatus
from app.services import document_service


def _doc(status: DocumentStatus) -> MagicMock:
    doc = MagicMock()
    doc.id, doc.course_id, doc.uploader_id = uuid4(), uuid4(), uuid4()
    doc.status = status
    return doc


def _user(role: str) -> MagicMock:
    user = MagicMock()
    user.role, user.id = role, uuid4()
    return user


@pytest.mark.asyncio
async def test_returns_signed_url_for_viewable_document(monkeypatch: pytest.MonkeyPatch) -> None:
    doc = _doc(DocumentStatus.INDEXED)
    monkeypatch.setattr(document_service, "get_document_or_404", AsyncMock(return_value=doc))
    storage = MagicMock()
    storage.generate_signed_url = AsyncMock(return_value="https://signed")

    url = await document_service.get_asset_signed_url(MagicMock(), storage, doc.id, "p003-f2.png", _user("student"))

    assert url == "https://signed"
    storage.generate_signed_url.assert_awaited_once_with(
        f"documents/{doc.course_id}/{doc.id}/assets/p003-f2.png", ttl=900
    )


@pytest.mark.parametrize("name", ["../raw/lecture.pdf", "p001-f1.png%2F..", "p001-f1.pdf", "output.md", "p1-f1.png"])
@pytest.mark.asyncio
async def test_rejects_invalid_asset_names_before_any_lookup(monkeypatch: pytest.MonkeyPatch, name: str) -> None:
    lookup = AsyncMock()
    monkeypatch.setattr(document_service, "get_document_or_404", lookup)

    with pytest.raises(HTTPException) as exc:
        await document_service.get_asset_signed_url(MagicMock(), MagicMock(), uuid4(), name, _user("admin"))

    assert exc.value.status_code == 422
    lookup.assert_not_awaited()


@pytest.mark.asyncio
async def test_forbidden_when_user_cannot_view_document(monkeypatch: pytest.MonkeyPatch) -> None:
    doc = _doc(DocumentStatus.NEEDS_REVIEW)
    monkeypatch.setattr(document_service, "get_document_or_404", AsyncMock(return_value=doc))

    with pytest.raises(HTTPException) as exc:
        await document_service.get_asset_signed_url(MagicMock(), MagicMock(), doc.id, "p001-f1.png", _user("student"))

    assert exc.value.status_code == 403


def test_route_is_registered() -> None:
    from app.api.v1.documents import router

    assert any(getattr(r, "path", "") == "/documents/{document_id}/assets/{asset_name}/url" for r in router.routes)


@pytest.mark.asyncio
async def test_batch_returns_signed_urls_for_every_name(monkeypatch: pytest.MonkeyPatch) -> None:
    doc = _doc(DocumentStatus.INDEXED)
    lookup = AsyncMock(return_value=doc)
    monkeypatch.setattr(document_service, "get_document_or_404", lookup)
    storage = MagicMock()
    storage.generate_signed_url = AsyncMock(side_effect=lambda key, ttl: f"https://signed/{key}?ttl={ttl}")
    names = ["p001-f1.png", "p002-page.jpg", "p013-f2.png"]

    urls = await document_service.get_asset_signed_urls(MagicMock(), storage, doc.id, names, _user("student"))

    prefix = f"documents/{doc.course_id}/{doc.id}/assets"
    assert urls == {name: f"https://signed/{prefix}/{name}?ttl=900" for name in names}
    lookup.assert_awaited_once()


@pytest.mark.parametrize(
    "names", [["p001-f1.png", "../raw/lecture.pdf"], ["output.md"], [], [f"p{i:03d}-f1.png" for i in range(201)]]
)
@pytest.mark.asyncio
async def test_batch_rejects_invalid_empty_or_oversized_requests_before_lookup(
    monkeypatch: pytest.MonkeyPatch, names: list[str]
) -> None:
    lookup = AsyncMock()
    monkeypatch.setattr(document_service, "get_document_or_404", lookup)

    with pytest.raises(HTTPException) as exc:
        await document_service.get_asset_signed_urls(MagicMock(), MagicMock(), uuid4(), names, _user("admin"))

    assert exc.value.status_code == 422
    lookup.assert_not_awaited()


@pytest.mark.asyncio
async def test_batch_accepts_exactly_200_names(monkeypatch: pytest.MonkeyPatch) -> None:
    doc = _doc(DocumentStatus.INDEXED)
    monkeypatch.setattr(document_service, "get_document_or_404", AsyncMock(return_value=doc))
    storage = MagicMock()
    storage.generate_signed_url = AsyncMock(return_value="https://signed")
    names = [f"p{i:03d}-f1.png" for i in range(200)]

    urls = await document_service.get_asset_signed_urls(MagicMock(), storage, doc.id, names, _user("admin"))

    assert len(urls) == 200


@pytest.mark.asyncio
async def test_batch_forbidden_when_user_cannot_view_document(monkeypatch: pytest.MonkeyPatch) -> None:
    doc = _doc(DocumentStatus.NEEDS_REVIEW)
    monkeypatch.setattr(document_service, "get_document_or_404", AsyncMock(return_value=doc))
    storage = MagicMock()
    storage.generate_signed_url = AsyncMock()

    with pytest.raises(HTTPException) as exc:
        await document_service.get_asset_signed_urls(
            MagicMock(), storage, doc.id, ["p001-f1.png"], _user("student")
        )

    assert exc.value.status_code == 403
    storage.generate_signed_url.assert_not_awaited()


@pytest.mark.asyncio
async def test_batch_forbidden_for_unassigned_reviewer(monkeypatch: pytest.MonkeyPatch) -> None:
    doc = _doc(DocumentStatus.NEEDS_REVIEW)
    monkeypatch.setattr(document_service, "get_document_or_404", AsyncMock(return_value=doc))
    session = MagicMock()
    session.scalar = AsyncMock(return_value=None)  # no active reviewer assignment

    with pytest.raises(HTTPException) as exc:
        await document_service.get_asset_signed_urls(session, MagicMock(), doc.id, ["p001-f1.png"], _user("reviewer"))

    assert exc.value.status_code == 403


def test_batch_route_is_registered_before_the_single_name_route() -> None:
    from app.api.v1.documents import router

    paths = [getattr(r, "path", "") for r in router.routes]
    batch, single = "/documents/{document_id}/assets/urls", "/documents/{document_id}/assets/{asset_name}/url"
    assert batch in paths and single in paths
    assert paths.index(batch) < paths.index(single)


def test_batch_endpoint_splits_names_and_returns_the_ttl(monkeypatch: pytest.MonkeyPatch) -> None:
    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    from app.api.v1 import documents as documents_api
    from app.core.auth import get_current_user
    from app.db.session import get_session
    from app.storage import get_storage

    doc_id = uuid4()
    service = AsyncMock(return_value={"p001-f1.png": "https://a", "p002-f1.png": "https://b"})
    monkeypatch.setattr(documents_api, "get_asset_signed_urls", service)
    app = FastAPI()
    app.include_router(documents_api.router)
    app.dependency_overrides[get_current_user] = lambda: _user("student")
    app.dependency_overrides[get_session] = lambda: MagicMock()
    app.dependency_overrides[get_storage] = lambda: MagicMock()

    response = TestClient(app).get(f"/documents/{doc_id}/assets/urls", params={"names": "p001-f1.png, p002-f1.png"})

    assert response.status_code == 200
    assert response.json() == {
        "urls": {"p001-f1.png": "https://a", "p002-f1.png": "https://b"},
        "expires_in_seconds": 900,
    }
    _, _, called_doc_id, called_names, _ = service.await_args.args
    assert called_doc_id == doc_id and called_names == ["p001-f1.png", "p002-f1.png"]
