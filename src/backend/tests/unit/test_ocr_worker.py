from __future__ import annotations

import asyncio
import uuid

from app.models.enums import FileFormat
from app.services.document_processing.models import DocumentProcessingResult
from app.workers import ocr_worker


class _FakePipeline:
    def __init__(self) -> None:
        self.calls: list[tuple[object, str, str | None]] = []

    def process_document(self, input_path, *, document_id, expected_route=None):  # noqa: ANN001, ANN201
        self.calls.append((input_path, document_id, expected_route))
        return DocumentProcessingResult(markdown="# Hello", route="hybrid", inferred_type="text_pdf")


class _Doc:
    def __init__(self) -> None:
        self.id = uuid.uuid4()
        self.file_format = FileFormat.PDF


def test_run_document_processing_pipeline_delegates_to_native_pipeline(monkeypatch, tmp_path) -> None:
    fake = _FakePipeline()
    monkeypatch.setattr(
        ocr_worker,
        "build_document_processing_pipeline",
        lambda settings, progress_callback=None: fake,  # noqa: ARG005
    )
    input_path = tmp_path / "input.pdf"
    input_path.write_bytes(b"%PDF-1.4")
    doc = _Doc()

    markdown, page_map = asyncio.run(ocr_worker.run_document_processing_pipeline(input_path, doc, trace=None))

    assert markdown == "# Hello"
    assert page_map == []
    # PDF maps to the "hybrid" expected route, passed through to the pipeline.
    assert fake.calls == [(input_path, str(doc.id), "hybrid")]
