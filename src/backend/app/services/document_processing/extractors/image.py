"""Standalone image upload: verbatim OCR; the image itself becomes the asset when it has figures."""

from __future__ import annotations

from pathlib import Path

from app.services.document_processing.assets import AssetCollector
from app.services.document_processing.extractors.base import Extractor
from app.services.document_processing.models import ExtractionResult, PageSegment
from app.services.document_processing.ocr import insert_page_image


class ImageExtractor(Extractor):
    def extract(self, path: Path, assets: AssetCollector) -> ExtractionResult:
        data = path.read_bytes()
        is_jpeg = path.suffix.lower() in (".jpg", ".jpeg")
        result = self._ocr.transcribe(data)
        stats = {"pages_total": 1, "pages_text": 0, "pages_ocr": 1, "ocr_failed_pages": int(result.failed)}
        if result.failed:
            markdown = "[OCR_FAILED page 1]"
        elif result.has_figures:
            name = "p001-page.jpg" if is_jpeg else "p001-page.png"
            ref = assets.add(name, data, "image/jpeg" if is_jpeg else "image/png")
            markdown = insert_page_image(result.markdown, ref, 1)
        else:
            markdown = result.markdown
        return ExtractionResult(segments=[PageSegment(None, markdown)], route="image", stats=stats)
