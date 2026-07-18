"""Native OOP document processing pipeline (promoted from src/experiments).

Public API: build the pipeline from app Settings and process a single document in memory.
"""

from app.services.document_processing.config import DocumentProcessingConfig
from app.services.document_processing.models import DocumentProcessingResult
from app.services.document_processing.pipeline import (
    DocumentProcessingPipeline,
    build_document_processing_pipeline,
)

__all__ = [
    "DocumentProcessingConfig",
    "DocumentProcessingPipeline",
    "DocumentProcessingResult",
    "build_document_processing_pipeline",
]
