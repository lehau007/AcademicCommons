"""PPTX extractor v4: deterministic slide Markdown + one VLM call per picture."""

from __future__ import annotations

import hashlib
import logging
import math
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from pptx import Presentation

from app.services.document_processing.assets import AssetCollector
from app.services.document_processing.extractors.base import Extractor
from app.services.document_processing.figures import FigureDescription, render_figure_block
from app.services.document_processing.models import ExtractionResult, PageSegment
from app.services.document_processing.pptx_markdown import (
    SlideMarkdown,
    SlidePicture,
    normalize_picture,
    slide_to_markdown,
)

logger = logging.getLogger(__name__)

REPEAT_SLIDE_RATIO = 0.3


class PptxExtractor(Extractor):
    def extract(self, path: Path, assets: AssetCollector) -> ExtractionResult:
        presentation = Presentation(str(path))
        slides = [slide_to_markdown(slide, number) for number, slide in enumerate(presentation.slides, start=1)]
        stats: dict[str, int] = {
            "pages_total": len(slides), "pages_text": len(slides), "pages_ocr": 0, "figure_candidates": 0,
            "figures_filtered": 0, "figures_described": 0, "figures_decorative": 0, "figure_failures": 0,
            "ocr_failed_pages": 0,
        }

        hash_counts: Counter[str] = Counter()
        for slide in slides:
            hash_counts.update({hashlib.sha256(p.blob).hexdigest() for p in slide.pictures})
        threshold = max(2, math.ceil(len(slides) * REPEAT_SLIDE_RATIO))

        replacements: dict[str, str] = {}
        jobs: list[tuple[SlideMarkdown, SlidePicture, tuple[bytes, str, str]]] = []
        for slide in slides:
            for picture in slide.pictures:
                stats["figure_candidates"] += 1
                normalized = normalize_picture(picture.blob, picture.ext)
                repeated = hash_counts[hashlib.sha256(picture.blob).hexdigest()] >= threshold
                if picture.too_small or repeated or normalized is None:
                    stats["figures_filtered"] += 1
                    replacements[picture.slot] = ""
                    continue
                jobs.append((slide, picture, normalized))

        def _describe(job: tuple[SlideMarkdown, SlidePicture, tuple[bytes, str, str]]) -> tuple[str, FigureDescription]:
            slide, picture, (data, ext, content_type) = job
            try:
                desc = self._describer.describe(data, figure_text="", page_text=slide.text)
                if desc.is_decorative:
                    return "", desc
                ref = assets.add(f"p{slide.number:03d}-f{picture.index}.{ext}", data, content_type)
                return render_figure_block(ref, desc, fallback_caption=f"Figure p{slide.number}-{picture.index}"), desc
            except Exception:
                logger.warning(
                    "figure description failed on slide %s picture %s", slide.number, picture.index, exc_info=True
                )
                return "", FigureDescription("other", "", "", "", failed=True)

        with ThreadPoolExecutor(max_workers=max(1, self._config.max_concurrency)) as pool:
            for (_slide, picture, _), (block, desc) in zip(jobs, pool.map(_describe, jobs), strict=True):
                replacements[picture.slot] = block
                if desc.is_decorative:
                    stats["figures_decorative"] += 1
                elif desc.failed or (self._config.enable_real_vision and not desc.description):
                    stats["figure_failures"] += 1
                elif desc.description:
                    stats["figures_described"] += 1

        segments: list[PageSegment] = []
        for slide in slides:
            markdown = slide.markdown
            for picture in slide.pictures:
                markdown = markdown.replace(picture.slot, replacements.get(picture.slot, ""))
            segments.append(PageSegment(slide.number, markdown))
        return ExtractionResult(segments=segments, route="pptx", stats=stats)
