"""Extractor abstraction + factory by file extension."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from app.services.document_processing.assets import AssetCollector
from app.services.document_processing.config import DocumentProcessingConfig
from app.services.document_processing.figures import FigureDescriber
from app.services.document_processing.models import ExtractionResult
from app.services.document_processing.ocr import PageOcr
from app.services.document_processing.progress import ProgressEmitter

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


class Extractor(ABC):
    def __init__(
        self,
        config: DocumentProcessingConfig,
        *,
        describer: FigureDescriber,
        ocr: PageOcr,
        emitter: ProgressEmitter,
    ) -> None:
        self._config = config
        self._describer = describer
        self._ocr = ocr
        self._emitter = emitter

    @abstractmethod
    def extract(self, path: Path, assets: AssetCollector) -> ExtractionResult:
        raise NotImplementedError


def build_extractor(
    path: Path,
    config: DocumentProcessingConfig,
    *,
    describer: FigureDescriber,
    ocr: PageOcr,
    emitter: ProgressEmitter,
) -> Extractor:
    from app.services.document_processing.extractors.image import ImageExtractor
    from app.services.document_processing.extractors.pdf import PdfExtractor
    from app.services.document_processing.extractors.pptx import PptxExtractor

    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return PdfExtractor(config, describer=describer, ocr=ocr, emitter=emitter)
    if suffix == ".pptx":
        return PptxExtractor(config, describer=describer, ocr=ocr, emitter=emitter)
    if suffix in IMAGE_EXTENSIONS:
        return ImageExtractor(config, describer=describer, ocr=ocr, emitter=emitter)
    raise ValueError(f"Unsupported extension: {suffix}")
