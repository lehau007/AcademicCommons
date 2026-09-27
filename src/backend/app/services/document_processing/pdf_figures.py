"""Pure helpers for PDF figure candidates: size filter, repeat detection, span splicing."""

from __future__ import annotations

import math
from collections import Counter

from app.services.document_processing.layout import LayoutPage, PictureRegion, picture_text

MIN_FIGURE_AREA_RATIO = 0.015
MIN_FIGURE_SIDE_PT = 40.0
REPEAT_PAGE_RATIO = 0.3


def is_too_small(region: PictureRegion, page: LayoutPage) -> bool:
    x0, y0, x1, y1 = region.bbox
    width, height = max(0.0, x1 - x0), max(0.0, y1 - y0)
    if min(width, height) < MIN_FIGURE_SIDE_PT:
        return True
    page_area = page.width * page.height
    return page_area > 0 and (width * height) / page_area < MIN_FIGURE_AREA_RATIO


def region_signature(region: PictureRegion, page: LayoutPage) -> tuple[object, ...]:
    """Position (5pt grid) + raster image digests + inner text.

    Identical logos/banners share a signature across pages; different images in the same slot do not.
    """
    x0, y0, x1, y1 = region.bbox
    start, end = region.span
    return (
        round(x0 / 5), round(y0 / 5), round(x1 / 5), round(y1 / 5),
        region.digests, picture_text(page.markdown[start:end]),
    )


def _is_identifiable(signature: tuple[object, ...]) -> bool:
    """Pure vector art (no raster digest, no inner text) cannot be told apart, so it never repeats."""
    digests, text = signature[-2], signature[-1]
    return bool(digests) or bool(text)


def repeated_signatures(pages: list[LayoutPage], total_pages: int) -> set[tuple[object, ...]]:
    counts: Counter[tuple[object, ...]] = Counter()
    for page in pages:
        signatures = {region_signature(region, page) for region in page.pictures}
        counts.update(signature for signature in signatures if _is_identifiable(signature))
    threshold = max(2, math.ceil(total_pages * REPEAT_PAGE_RATIO))
    return {signature for signature, count in counts.items() if count >= threshold}


def splice(markdown: str, replacements: list[tuple[tuple[int, int], str]]) -> str:
    """Replace non-overlapping [start, end) spans, right to left so offsets stay valid."""
    result = markdown
    for (start, end), text in sorted(replacements, key=lambda item: item[0][0], reverse=True):
        insert = f"\n\n{text.strip()}\n\n" if text.strip() else "\n"
        result = result[:start] + insert + result[end:]
    return result
