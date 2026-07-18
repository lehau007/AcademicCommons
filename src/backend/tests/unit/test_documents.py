from __future__ import annotations

from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.api.v1.documents import _max_upload_bytes_for, _overall_ai_score
from app.config import get_settings
from app.models.enums import DocumentStatus, FileFormat
from app.models.tables import Document, User
from app.services.document_service import _check_encrypted_pdf, can_view_document, detect_file_format

# ---------------------------------------------------------------------------
# detect_file_format
# ---------------------------------------------------------------------------


def test_detect_file_format_pdf() -> None:
    # PDF magic bytes: %PDF
    result = detect_file_format("lecture.pdf", b"%PDF-1.4 content")
    assert result == FileFormat.PDF


def test_detect_file_format_pptx() -> None:
    # PPTX/ZIP magic bytes: PK\x03\x04
    result = detect_file_format("slides.pptx", b"PK\x03\x04" + b"\x00" * 100)
    assert result == FileFormat.PPTX


def test_detect_file_format_unknown_raises() -> None:
    with pytest.raises(ValueError, match="Unsupported file format"):
        detect_file_format("document.docx", b"\x00\x01\x02\x03")


def test_check_encrypted_pdf_rejects_encrypted() -> None:
    encrypted_content = b"%PDF-1.4 ... /Encrypt << /Filter /Standard >> ..."
    with pytest.raises(HTTPException) as exc_info:
        _check_encrypted_pdf(encrypted_content)
    assert exc_info.value.status_code == 422


def test_check_encrypted_pdf_allows_plain() -> None:
    plain_content = b"%PDF-1.4 ... regular content ..."
    _check_encrypted_pdf(plain_content)  # should not raise


# ---------------------------------------------------------------------------
# can_view_document
# ---------------------------------------------------------------------------


def _make_user(role: str) -> User:
    user = MagicMock(spec=User)
    user.role = role
    user.id = uuid4()
    return user


def _make_document(doc_status: DocumentStatus) -> Document:
    doc = MagicMock(spec=Document)
    doc.status = doc_status
    doc.id = uuid4()
    return doc


def test_can_view_document_admin_sees_all() -> None:
    user = _make_user("admin")
    doc = _make_document(DocumentStatus.PARSING)
    assert can_view_document(user, doc) is True


def test_can_view_document_student_only_indexed() -> None:
    user = _make_user("student")

    doc_needs_review = _make_document(DocumentStatus.NEEDS_REVIEW)
    assert can_view_document(user, doc_needs_review) is False

    doc_indexed = _make_document(DocumentStatus.INDEXED)
    assert can_view_document(user, doc_indexed) is True


def test_can_view_document_reviewer_sees_needs_review() -> None:
    user = _make_user("reviewer")

    doc_needs_review = _make_document(DocumentStatus.NEEDS_REVIEW)
    assert can_view_document(user, doc_needs_review) is True

    doc_parsing = _make_document(DocumentStatus.PARSING)
    assert can_view_document(user, doc_parsing) is False


# ---------------------------------------------------------------------------
# _max_upload_bytes_for (role-based upload cap)
# ---------------------------------------------------------------------------


def test_max_upload_bytes_student_default() -> None:
    settings = get_settings()
    assert _max_upload_bytes_for(_make_user("student")) == settings.max_upload_bytes


@pytest.mark.parametrize("role", ["admin", "reviewer"])
def test_max_upload_bytes_privileged_roles(role: str) -> None:
    settings = get_settings()
    assert _max_upload_bytes_for(_make_user(role)) == settings.max_upload_bytes_privileged


def test_privileged_cap_larger_than_default() -> None:
    settings = get_settings()
    assert settings.max_upload_bytes_privileged > settings.max_upload_bytes


# ---------------------------------------------------------------------------
# _overall_ai_score (AI summary for the management listing)
# ---------------------------------------------------------------------------


def test_overall_ai_score_averages_and_scales_to_100() -> None:
    agent3 = {"scores": {"relevance": 9.0, "completeness": 9.0, "quality": 9.0}}
    assert _overall_ai_score(agent3) == 90.0


def test_overall_ai_score_ignores_non_numeric_and_missing() -> None:
    agent3 = {"scores": {"relevance": 8.0, "completeness": None, "quality": 10.0}}
    # average of 8 and 10 = 9 -> 90.0
    assert _overall_ai_score(agent3) == 90.0


@pytest.mark.parametrize("value", [None, {}, {"scores": {}}, "nope"])
def test_overall_ai_score_none_when_unavailable(value: object) -> None:
    assert _overall_ai_score(value) is None
