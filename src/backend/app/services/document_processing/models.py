"""Data contracts for the document processing pipeline (v4)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.services.document_processing.assets import Asset


@dataclass(frozen=True)
class PageSegment:
    page: int | None  # 1-based page/slide; None for non-paginated sources
    markdown: str


@dataclass
class ExtractionResult:
    segments: list[PageSegment]
    route: str  # text_layer | ocr | mixed | pptx | image
    stats: dict[str, int] = field(default_factory=dict)


@dataclass
class DocumentProcessingResult:
    markdown: str
    route: str
    inferred_type: str
    page_map: list[tuple[int, int]] = field(default_factory=list)
    assets: list[Asset] = field(default_factory=list)
    quality_flags: dict[str, Any] = field(default_factory=dict)
    llm_metrics: dict[str, Any] = field(default_factory=dict)
    stats: dict[str, Any] = field(default_factory=dict)
    progress: list[dict[str, Any]] = field(default_factory=list)
