from __future__ import annotations

import asyncio
import uuid

from app.models.enums import FileFormat
from app.services.document_processing.assets import Asset
from app.services.document_processing.models import DocumentProcessingResult
from app.workers import ocr_worker


class _FakePipeline:
    def __init__(self) -> None:
        self.calls: list[tuple[object, str]] = []

    def process_document(self, input_path, *, document_id):  # noqa: ANN001, ANN201
        self.calls.append((input_path, document_id))
        return DocumentProcessingResult(markdown="# Hello", route="hybrid", inferred_type="text_pdf")


class _RecordingStorage:
    def __init__(self) -> None:
        self.puts: list[tuple[str, bytes, str]] = []

    async def put_object(self, key: str, source: bytes, content_type: str) -> str:
        self.puts.append((key, source, content_type))
        return key


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

    result = asyncio.run(ocr_worker.run_document_processing_pipeline(input_path, doc, trace=None))

    assert result.markdown == "# Hello" and result.page_map == [] and result.assets == []
    assert fake.calls == [(input_path, str(doc.id))]


def test_upload_assets_writes_each_asset_under_document_prefix() -> None:
    storage = _RecordingStorage()
    course_id, document_id = uuid.uuid4(), uuid.uuid4()
    assets = [Asset("p001-f1.png", b"png", "image/png"), Asset("p002-page.jpg", b"jpg!", "image/jpeg")]

    total = asyncio.run(ocr_worker.upload_assets(storage, course_id, document_id, assets))

    assert total == 7
    assert sorted(storage.puts) == [
        (f"documents/{course_id}/{document_id}/assets/p001-f1.png", b"png", "image/png"),
        (f"documents/{course_id}/{document_id}/assets/p002-page.jpg", b"jpg!", "image/jpeg"),
    ]
