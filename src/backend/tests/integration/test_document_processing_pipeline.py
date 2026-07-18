import os
from pathlib import Path

import pytest

from app.services.document_processing import (
    DocumentProcessingConfig,
    DocumentProcessingPipeline,
)

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_DOC_PROCESSING_INTEGRATION") != "1",
    reason="Set RUN_DOC_PROCESSING_INTEGRATION=1 to run the document processing pipeline "
    "against real sample files (offline, vision disabled).",
)

SAMPLE_DIR = Path(
    "/Users/admin/Desktop/graduation-thesis/GraduationThesis/src/experiments/"
    "document_processing/test_data"
)
VALID_ROUTES = {"direct_text", "hybrid", "vision_only"}


def _sample_files() -> list[Path]:
    return sorted(
        p for p in SAMPLE_DIR.iterdir() if p.suffix.lower() in {".pdf", ".pptx"}
    )


@pytest.mark.parametrize("sample", _sample_files(), ids=lambda p: p.name)
def test_real_sample_produces_markdown_and_valid_route(sample: Path) -> None:
    pipeline = DocumentProcessingPipeline(DocumentProcessingConfig())
    result = pipeline.process_document(sample, document_id=sample.stem)

    assert result.markdown.strip()
    assert result.route in VALID_ROUTES
