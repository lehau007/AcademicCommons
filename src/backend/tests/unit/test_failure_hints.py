from __future__ import annotations

import pytest

from app.services.failure_hints import friendly_failure


@pytest.mark.parametrize(
    "raw,job_type,expected_fragment",
    [
        ("PdfReadError: file has not been decrypted /Encrypt", "ocr", "mã hoá"),
        ("ValueError: Unsupported file format: .docx", "ocr", "không được hỗ trợ"),
        ("cannot identify image file", "ocr", "không được hỗ trợ"),
        ("TimeoutError: OCR timed out after 1800s", "ocr", "thời gian"),
        ("Extraction produced no text content", "ocr", "Không trích xuất"),
        ("PdfReadError: EOF marker not found", "ocr", "bị hỏng"),
    ],
)
def test_friendly_failure_maps_known_patterns(raw: str, job_type: str, expected_fragment: str) -> None:
    assert expected_fragment in friendly_failure(raw, job_type)


def test_friendly_failure_falls_back_by_job_type() -> None:
    assert "OCR" in friendly_failure("some unrecognized traceback", "ocr")
    assert "lập chỉ mục" in friendly_failure("some unrecognized traceback", "index")
    assert "đánh giá" in friendly_failure("some unrecognized traceback", "eval")


def test_friendly_failure_generic_for_unknown_job_type() -> None:
    result = friendly_failure(None, "mystery")
    assert "gặp sự cố" in result
