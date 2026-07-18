"""Data contracts for the document processing pipeline.

Ported from ``src/experiments/document_processing/document_processing_pipeline.py``.
Block/prompt/visual-trace payloads are kept as loose ``dict`` shapes (matching the
experiment) so downstream validators that inspect dict keys keep working; the OOP
seams live at the class boundaries (providers, extractors, normalizer, pipeline).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# A single extracted unit. Keys observed in the experiment include:
#   kind: "text" | "vision_placeholder" | "error"
#   content: str
#   page / slide: int | None
#   ocr_strategy: str (optional)
Block = dict[str, Any]


@dataclass
class ExtractionResult:
    """Output of an :class:`~app.services.document_processing.extractors.base.Extractor`."""

    blocks: list[Block] = field(default_factory=list)
    prompts: list[dict[str, Any]] = field(default_factory=list)
    visual_trace: list[dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class RouteDecision:
    """Routing outcome from :class:`~app.services.document_processing.routing.RouteDecider`."""

    route: str  # one of EXPECTED_ROUTES: direct_text | hybrid | vision_only
    evidence: dict[str, Any] = field(default_factory=dict)


# Visual classification dict shape: {label, learning_value, action, confidence, reason}
VisualClassification = dict[str, Any]


@dataclass
class DocumentProcessingResult:
    """In-memory result returned by ``DocumentProcessingPipeline.process_document``.

    This replaces the experiment's on-disk artifact round-trip: the worker reads
    ``markdown`` directly and may persist ``llm_metrics`` / ``progress`` into its trace.
    """

    markdown: str
    route: str
    inferred_type: str
    blocks: list[Block] = field(default_factory=list)
    prompts: list[dict[str, Any]] = field(default_factory=list)
    visual_trace: list[dict[str, Any]] = field(default_factory=list)
    normalization_trace: list[dict[str, Any]] = field(default_factory=list)
    quality_flags: dict[str, Any] = field(default_factory=dict)
    llm_metrics: dict[str, Any] = field(default_factory=dict)
    progress: list[dict[str, Any]] = field(default_factory=list)
    page_map: list[tuple[int, int]] = field(default_factory=list)
