"""PDF extractor v4: text-layer Markdown via layout analysis; VLM only for figures and scanned pages."""

from __future__ import annotations

import logging
import threading
from collections import Counter, defaultdict
from concurrent.futures import Future, ThreadPoolExecutor
from pathlib import Path
from typing import Any

import fitz  # type: ignore[import-untyped]

from app.services.document_processing.assets import AssetCollector
from app.services.document_processing.extractors.base import Extractor
from app.services.document_processing.figures import FigureDescription, render_figure_block
from app.services.document_processing.layout import LayoutPage, PdfLayoutReader, PictureRegion, picture_text
from app.services.document_processing.models import ExtractionResult, PageSegment
from app.services.document_processing.ocr import insert_page_image
from app.services.document_processing.pdf_figures import is_too_small, region_signature, repeated_signatures, splice

logger = logging.getLogger(__name__)

SCANNED_TEXT_THRESHOLD = 40
# A page whose only "text" comes from a full-page image (layout._FULL_PAGE_COVERAGE_THRESHOLD)
# unique to that page (no other page in the document repeats it — i.e. not a recurring
# lecture-deck background) is still effectively scanned as long as its native text stays below
# this higher ceiling (title slides, cover pages, a scan with a printed header/watermark).
SCANNED_IMAGE_TEXT_CEILING = 200
FIGURE_ZOOM = 2.0
OCR_ZOOM = 2.0
PAGE_ASSET_ZOOM = 1.5
PAGE_ASSET_JPEG_QUALITY = 80
CROP_MARGIN_PT = 4.0

Replacement = tuple[tuple[int, int], str]

# PyMuPDF is not thread-safe: one process-wide lock serializes every MuPDF call made by the
# extractor, across pages and across concurrent OCR jobs. Never acquired while already held.
_PYMUPDF_LOCK = threading.Lock()


def _region_text(page: LayoutPage, region: PictureRegion) -> str:
    start, end = region.span
    return picture_text(page.markdown[start:end])


def _native_markdown(page: LayoutPage) -> str:
    """The page's text-layer Markdown with picture regions reduced to their native text."""
    markdown = splice(page.markdown, [(region.span, _region_text(page, region)) for region in page.pictures])
    return markdown.strip()


def _needs_ocr(page: LayoutPage, digest_counts: Counter[str]) -> bool:
    if page.native_text_chars < SCANNED_TEXT_THRESHOLD:
        return True
    digest = page.full_page_image_digest
    if digest is not None and digest_counts[digest] == 1 and page.native_text_chars < SCANNED_IMAGE_TEXT_CEILING:
        return True
    return False


class PdfExtractor(Extractor):
    def extract(self, path: Path, assets: AssetCollector) -> ExtractionResult:
        reader = PdfLayoutReader()
        with _PYMUPDF_LOCK:
            doc = fitz.open(path)
            try:
                pages = reader.read(doc)
            except BaseException:
                doc.close()
                raise
        try:
            digest_counts: Counter[str] = Counter(
                p.full_page_image_digest for p in pages if p.full_page_image_digest
            )
            text_pages = [p for p in pages if not _needs_ocr(p, digest_counts)]
            ocr_pages = [p for p in pages if _needs_ocr(p, digest_counts)]
            stats: dict[str, int] = {
                "pages_total": len(pages), "pages_text": len(text_pages), "pages_ocr": len(ocr_pages),
                "figure_candidates": 0, "figures_filtered": 0, "figures_described": 0,
                "figures_decorative": 0, "figure_failures": 0, "ocr_failed_pages": 0,
                "layout_fallback": int(reader.used_fallback),
            }

            repeated = repeated_signatures(text_pages, len(pages))
            replacements: dict[int, list[Replacement]] = defaultdict(list)
            figure_jobs: list[tuple[LayoutPage, PictureRegion, int]] = []
            for page in text_pages:
                kept = 0
                for region in page.pictures:
                    stats["figure_candidates"] += 1
                    if region_signature(region, page) in repeated:  # logo/banner: drop it with its text
                        stats["figures_filtered"] += 1
                        replacements[page.page_number].append((region.span, ""))
                        continue
                    if is_too_small(region, page):  # no figure, but keep the text printed in it
                        stats["figures_filtered"] += 1
                        replacements[page.page_number].append((region.span, _region_text(page, region)))
                        continue
                    kept += 1
                    figure_jobs.append((page, region, kept))
            self._emitter.emit(
                "layout_done", pages=len(pages), ocr_pages=len(ocr_pages), figures=len(figure_jobs),
                layout_fallback=reader.used_fallback,
            )

            with ThreadPoolExecutor(max_workers=max(1, self._config.max_concurrency)) as pool:
                figure_futures = [
                    (page, region, pool.submit(self._figure, doc, page, region, index, assets))
                    for page, region, index in figure_jobs
                ]
                ocr_futures: dict[int, Future[tuple[PageSegment, bool]]] = {
                    page.page_number: pool.submit(self._ocr_page, doc, page, assets) for page in ocr_pages
                }
                for page, region, future in figure_futures:
                    block, desc = future.result()
                    replacements[page.page_number].append((region.span, block))
                    if desc.is_decorative:
                        stats["figures_decorative"] += 1
                    elif desc.failed or (self._config.enable_real_vision and not desc.description):
                        stats["figure_failures"] += 1
                    elif desc.description:
                        stats["figures_described"] += 1
                segments: list[PageSegment] = []
                for page in pages:
                    if page.page_number in ocr_futures:
                        segment, failed = ocr_futures[page.page_number].result()
                        stats["ocr_failed_pages"] += int(failed)
                        segments.append(segment)
                    else:
                        segments.append(
                            PageSegment(page.page_number, splice(page.markdown, replacements[page.page_number]))
                        )
        finally:
            with _PYMUPDF_LOCK:
                doc.close()

        route = "ocr" if not text_pages else "text_layer" if not ocr_pages else "mixed"
        return ExtractionResult(segments=segments, route=route, stats=stats)

    def _figure(
        self, doc: Any, page: LayoutPage, region: PictureRegion, index: int, assets: AssetCollector
    ) -> tuple[str, FigureDescription]:
        figure_text = _region_text(page, region)
        try:
            x0, y0, x1, y1 = region.bbox
            with _PYMUPDF_LOCK:
                pdf_page = doc[page.page_number - 1]
                clip = fitz.Rect(x0 - CROP_MARGIN_PT, y0 - CROP_MARGIN_PT, x1 + CROP_MARGIN_PT, y1 + CROP_MARGIN_PT)
                png = pdf_page.get_pixmap(
                    matrix=fitz.Matrix(FIGURE_ZOOM, FIGURE_ZOOM), clip=clip & pdf_page.rect
                ).tobytes("png")
                del pdf_page
            desc = self._describer.describe(png, figure_text=figure_text, page_text=page.markdown)
            if desc.is_decorative:
                return "", desc
            ref = assets.add(f"p{page.page_number:03d}-f{index}.png", png, "image/png")
            block = render_figure_block(
                ref, desc, fallback_caption=f"Figure p{page.page_number}-{index}", fallback_text=figure_text
            )
            return block, desc
        except Exception:
            logger.warning("figure extraction failed on page %s figure %s", page.page_number, index, exc_info=True)
            return figure_text, FigureDescription("other", "", "", "", failed=True)

    def _ocr_page(self, doc: Any, page: LayoutPage, assets: AssetCollector) -> tuple[PageSegment, bool]:
        try:
            with _PYMUPDF_LOCK:
                png = doc[page.page_number - 1].get_pixmap(matrix=fitz.Matrix(OCR_ZOOM, OCR_ZOOM)).tobytes("png")
            result = self._ocr.transcribe(png)
            if result.failed:
                return self._ocr_fallback(page, f"[OCR_FAILED page {page.page_number}]"), True
            if result.markdown.startswith("[VISION_PLACEHOLDER]"):
                return self._ocr_fallback(page, result.markdown), False
            markdown = result.markdown
            if result.has_figures:
                with _PYMUPDF_LOCK:
                    jpg = (
                        doc[page.page_number - 1]
                        .get_pixmap(matrix=fitz.Matrix(PAGE_ASSET_ZOOM, PAGE_ASSET_ZOOM))
                        .tobytes("jpeg", jpg_quality=PAGE_ASSET_JPEG_QUALITY)
                    )
                ref = assets.add(f"p{page.page_number:03d}-page.jpg", jpg, "image/jpeg")
                markdown = insert_page_image(markdown, ref, page.page_number)
            return PageSegment(page.page_number, markdown), False
        except Exception:
            logger.warning("OCR failed on page %s", page.page_number, exc_info=True)
            return self._ocr_fallback(page, f"[OCR_FAILED page {page.page_number}]"), True

    @staticmethod
    def _ocr_fallback(page: LayoutPage, placeholder: str) -> PageSegment:
        """Keep whatever native text the page has; the placeholder only when it has none."""
        return PageSegment(page.page_number, _native_markdown(page) or placeholder)
