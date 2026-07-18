"""Extractor abstraction + factory by file extension.

Ports experiment ``extract_pdf_text`` / ``extract_pptx_text`` / ``extract_image_text``.
Extractors depend on the :class:`ProviderChain` (for VLM calls) and the
:class:`VisualClassifier` (injected) rather than reaching for module globals.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from app.services.document_processing.classification import VisualClassifier
from app.services.document_processing.config import DocumentProcessingConfig
from app.services.document_processing.models import ExtractionResult
from app.services.document_processing.progress import ProgressEmitter
from app.services.document_processing.providers.chain import ProviderChain

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


class Extractor(ABC):
    def __init__(
        self,
        config: DocumentProcessingConfig,
        *,
        provider_chain: ProviderChain,
        classifier: VisualClassifier,
        emitter: ProgressEmitter,
    ) -> None:
        self._config = config
        self._chain = provider_chain
        self._classifier = classifier
        self._emitter = emitter

    @abstractmethod
    def extract(self, path: Path) -> ExtractionResult:
        raise NotImplementedError


def build_extractor(
    path: Path,
    config: DocumentProcessingConfig,
    *,
    provider_chain: ProviderChain,
    classifier: VisualClassifier,
    emitter: ProgressEmitter,
) -> Extractor:
    """Select the extractor for a file by extension. Raises ValueError if unsupported."""
    from app.services.document_processing.extractors.image import ImageExtractor
    from app.services.document_processing.extractors.pdf import PdfExtractor
    from app.services.document_processing.extractors.pptx import PptxExtractor

    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return PdfExtractor(config, provider_chain=provider_chain, classifier=classifier, emitter=emitter)
    if suffix == ".pptx":
        return PptxExtractor(config, provider_chain=provider_chain, classifier=classifier, emitter=emitter)
    if suffix in IMAGE_EXTENSIONS:
        return ImageExtractor(config, provider_chain=provider_chain, classifier=classifier, emitter=emitter)
    raise ValueError(f"Unsupported extension: {suffix}")
