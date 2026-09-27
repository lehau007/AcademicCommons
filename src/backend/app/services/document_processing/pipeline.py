"""Document processing pipeline v4: extract → deterministic cleanup → assemble.

VLM calls happen only inside extractors (figures, scanned pages); there is no LLM normalization.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

from app.config import Settings
from app.services.document_processing.assets import AssetCollector
from app.services.document_processing.cleanup import MarkdownCleaner
from app.services.document_processing.config import DocumentProcessingConfig
from app.services.document_processing.extractors.base import build_extractor
from app.services.document_processing.figures import FigureDescriber
from app.services.document_processing.markdown_utils import build_page_map
from app.services.document_processing.metrics import LlmCallRecorder
from app.services.document_processing.models import DocumentProcessingResult
from app.services.document_processing.ocr import PageOcr
from app.services.document_processing.progress import ProgressEmitter
from app.services.document_processing.providers.base import VisionLanguageProvider
from app.services.document_processing.providers.chain import ProviderChain
from app.services.document_processing.providers.factory import build_vision_providers

STAT_KEYS = (
    "pages_total", "pages_text", "pages_ocr", "figure_candidates", "figures_filtered", "figures_described",
    "figures_decorative", "figure_failures", "ocr_failed_pages", "layout_fallback",
)


class DocumentProcessingPipeline:
    def __init__(
        self,
        config: DocumentProcessingConfig,
        *,
        progress_callback: Callable[[dict[str, Any]], None] | None = None,
        providers: list[VisionLanguageProvider] | None = None,
    ) -> None:
        self._config = config
        self._recorder = LlmCallRecorder(config.input_cost_per_1m, config.output_cost_per_1m)
        self._emitter = ProgressEmitter(progress_callback)
        if providers is None:
            providers = build_vision_providers(config, recorder=self._recorder, emitter=self._emitter)
        self._chain = ProviderChain(
            providers,
            recorder=self._recorder,
            emitter=self._emitter,
            enable_real_vision=config.enable_real_vision,
            global_concurrency=config.global_concurrency,
        )
        self._describer = FigureDescriber(self._chain)
        self._ocr = PageOcr(self._chain)
        self._cleaner = MarkdownCleaner()

    def process_document(self, input_path: Path, *, document_id: str) -> DocumentProcessingResult:
        started = time.monotonic()
        self._emitter.emit("sample_start", sample_id=document_id, input_path=str(input_path))
        extractor = build_extractor(
            input_path, self._config, describer=self._describer, ocr=self._ocr, emitter=self._emitter
        )
        assets = AssetCollector(document_id)
        extraction = extractor.extract(input_path, assets)
        extract_ms = int((time.monotonic() - started) * 1000)

        cleaned = self._cleaner.clean_pages([segment.markdown for segment in extraction.segments])
        outputs: list[str] = []
        pages: list[int | None] = []
        for segment, text in zip(extraction.segments, cleaned, strict=True):
            if text.strip():
                outputs.append(text.strip())
                pages.append(segment.page)
        markdown = "\n\n".join(outputs) if outputs else "[EMPTY_OUTPUT]"

        stats: dict[str, Any] = {key: 0 for key in STAT_KEYS} | dict(extraction.stats)
        asset_items = assets.items()
        stats.update(
            extract_ms=extract_ms,
            total_ms=int((time.monotonic() - started) * 1000),
            asset_count=len(asset_items),
            asset_bytes=sum(len(asset.data) for asset in asset_items),
        )
        quality_flags = {
            "non_empty_output": bool(outputs),
            "ocr_failed_pages": stats["ocr_failed_pages"],
            "figure_failures": stats["figure_failures"],
            "layout_fallback": bool(stats["layout_fallback"]),
        }
        self._emitter.emit("sample_end", sample_id=document_id, status="success", route=extraction.route)
        return DocumentProcessingResult(
            markdown=markdown,
            route=extraction.route,
            inferred_type=extraction.route,
            page_map=build_page_map(outputs, pages),
            assets=asset_items,
            quality_flags=quality_flags,
            llm_metrics=self._recorder.summary(),
            stats=stats,
            progress=self._emitter.records,
        )


def build_document_processing_pipeline(
    settings: Settings,
    *,
    progress_callback: Callable[[dict[str, Any]], None] | None = None,
) -> DocumentProcessingPipeline:
    return DocumentProcessingPipeline(
        DocumentProcessingConfig.from_settings(settings), progress_callback=progress_callback
    )
