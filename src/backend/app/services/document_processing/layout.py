"""Text-layer Markdown per PDF page via pymupdf4llm layout analysis (no OCR)."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)

_PICTURE_TEXT_RE = re.compile(
    r"\*\*----- Start of picture text -----\*\*<br>\n?(?P<body>.*?)\*\*----- End of picture text -----\*\*<br>",
    re.DOTALL,
)

# A page image covering at least this fraction of the page area is a candidate "full-page
# image" (background/scan).
_FULL_PAGE_COVERAGE_THRESHOLD = 0.8
# A raster image belongs to a picture region when at least this share of its own area lies inside it.
_REGION_IMAGE_OVERLAP = 0.5


@dataclass(frozen=True)
class PictureRegion:
    bbox: tuple[float, float, float, float]
    span: tuple[int, int]  # [start, end) into LayoutPage.markdown
    # Sorted hex digests of the raster images inside the region (full-page backgrounds excluded);
    # empty for pure vector art.
    digests: tuple[str, ...] = ()


@dataclass
class LayoutPage:
    page_number: int  # 1-based
    markdown: str
    native_text_chars: int
    width: float
    height: float
    pictures: list[PictureRegion] = field(default_factory=list)
    # Hex digest of the largest image covering >= 80% of the page area, if any (None otherwise).
    full_page_image_digest: str | None = None


def _image_infos(page: Any) -> list[dict[str, Any]]:
    """Raster images on the page with bbox + digest ([] when PyMuPDF cannot list them)."""
    try:
        return list(page.get_image_info(hashes=True))
    except Exception:
        return []


def _bbox(info: dict[str, Any]) -> tuple[float, float, float, float]:
    x0, y0, x1, y1 = (float(v) for v in info.get("bbox", (0.0, 0.0, 0.0, 0.0)))
    return x0, y0, x1, y1


def _intersection_area(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> float:
    width = min(a[2], b[2]) - max(a[0], b[0])
    height = min(a[3], b[3]) - max(a[1], b[1])
    return max(0.0, width) * max(0.0, height)


def _page_coverage(info: dict[str, Any], width: float, height: float) -> float:
    page_area = width * height
    if page_area <= 0:
        return 0.0
    return _intersection_area(_bbox(info), (0.0, 0.0, width, height)) / page_area


def _full_page_image_digest(infos: list[dict[str, Any]], width: float, height: float) -> str | None:
    """Hex digest of the largest image covering >= 80% of the page area, if any."""
    best_coverage = 0.0
    best_digest: str | None = None
    for info in infos:
        coverage = _page_coverage(info, width, height)
        digest = info.get("digest")
        if coverage >= _FULL_PAGE_COVERAGE_THRESHOLD and coverage > best_coverage and digest:
            best_coverage = coverage
            best_digest = digest.hex()
    return best_digest


def _region_digests(
    bbox: tuple[float, float, float, float], infos: list[dict[str, Any]], width: float, height: float
) -> tuple[str, ...]:
    """Digests of the raster images that lie mostly inside ``bbox``, excluding full-page backgrounds."""
    digests: set[str] = set()
    for info in infos:
        digest = info.get("digest")
        image = _bbox(info)
        image_area = max(0.0, image[2] - image[0]) * max(0.0, image[3] - image[1])
        if not digest or image_area <= 0:
            continue
        if _page_coverage(info, width, height) >= _FULL_PAGE_COVERAGE_THRESHOLD:
            continue
        if _intersection_area(image, bbox) >= _REGION_IMAGE_OVERLAP * image_area:
            digests.add(digest.hex())
    return tuple(sorted(digests))


def picture_text(span_markdown: str) -> str:
    """Plain text pymupdf4llm extracted inside a picture region ('' when none)."""
    match = _PICTURE_TEXT_RE.search(span_markdown)
    if match is None:
        return ""
    lines = (line.strip() for line in match.group("body").replace("<br>", "\n").splitlines())
    return "\n".join(line for line in lines if line)


class PdfLayoutReader:
    def __init__(self) -> None:
        self.used_fallback = False

    def read(self, doc: Any) -> list[LayoutPage]:
        native = [len((page.get_text("text") or "").strip()) for page in doc]
        try:
            import pymupdf4llm  # type: ignore[import-untyped]

            chunks = pymupdf4llm.to_markdown(
                doc, page_chunks=True, use_ocr=False, header=False, footer=False, show_progress=False
            )
            if len(chunks) != len(doc):
                raise ValueError(f"layout returned {len(chunks)} chunks for {len(doc)} pages")
        except Exception:
            logger.warning("pymupdf4llm layout failed; falling back to plain text extraction", exc_info=True)
            self.used_fallback = True
            return [
                LayoutPage(
                    i + 1,
                    (page.get_text("text") or "").strip(),
                    native[i],
                    page.rect.width,
                    page.rect.height,
                    full_page_image_digest=_full_page_image_digest(
                        _image_infos(page), page.rect.width, page.rect.height
                    ),
                )
                for i, page in enumerate(doc)
            ]

        pages: list[LayoutPage] = []
        for index, chunk in enumerate(chunks):
            pdf_page = doc[index]
            width, height = pdf_page.rect.width, pdf_page.rect.height
            infos = _image_infos(pdf_page)
            pictures: list[PictureRegion] = []
            for box in chunk.get("page_boxes", []):
                if box.get("class") != "picture":
                    continue
                x0, y0, x1, y1 = (float(v) for v in box["bbox"])
                start, end = (int(v) for v in box["pos"])
                pictures.append(
                    PictureRegion(
                        bbox=(x0, y0, x1, y1),
                        span=(start, end),
                        digests=_region_digests((x0, y0, x1, y1), infos, width, height),
                    )
                )
            pages.append(
                LayoutPage(
                    page_number=index + 1,
                    markdown=str(chunk.get("text", "")),
                    native_text_chars=native[index],
                    width=width,
                    height=height,
                    pictures=pictures,
                    full_page_image_digest=_full_page_image_digest(infos, width, height),
                )
            )
        return pages
