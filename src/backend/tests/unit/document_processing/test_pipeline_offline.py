from __future__ import annotations

import io
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import fitz  # type: ignore[import-untyped]
import pytest
from pptx import Presentation
from pptx.util import Inches

from app.services.document_processing import DocumentProcessingConfig, DocumentProcessingPipeline
from app.services.document_processing.extractors import pdf as pdf_extractor
from app.services.document_processing.layout import LayoutPage, PdfLayoutReader, PictureRegion

from .conftest import ScriptedProvider, build_scanned_pdf, build_text_pdf, png_bytes

DOC = "0b7c6f0e-8d8e-4f1a-9a55-1f0c7d9c2a11"
FIGURE_JSON = json.dumps({"label": "diagram", "caption": "Graph G", "description": "A triangle graph.",
                          "content_markdown": ""})
UNDESCRIBED_JSON = json.dumps({"label": "diagram", "caption": "Graph G", "description": "", "content_markdown": ""})


def _pipeline(responses: dict[str, str] | None = None) -> tuple[DocumentProcessingPipeline, ScriptedProvider | None]:
    if responses is None:
        return DocumentProcessingPipeline(DocumentProcessingConfig()), None
    provider = ScriptedProvider(responses)
    config = DocumentProcessingConfig(enable_real_vision=True, max_concurrency=4)
    return DocumentProcessingPipeline(config, providers=[provider]), provider


def test_text_pdf_offline_keeps_figures_as_assets_without_llm_calls(tmp_path: Path) -> None:
    pipeline, _ = _pipeline()

    result = pipeline.process_document(build_text_pdf(tmp_path / "t.pdf", pages=3), document_id=DOC)

    assert result.route == "text_layer"
    assert "Chapter 1: Graph theory basics" in result.markdown
    assert f"![Figure p1-1](asset://{DOC}/p001-f1.png)" in result.markdown
    assert [a.name for a in result.assets] == ["p001-f1.png", "p002-f1.png", "p003-f1.png"]  # logo filtered
    assert "intentionally omitted" not in result.markdown
    assert result.llm_metrics["total_calls"] == 0
    assert [page for _, page in result.page_map] == [1, 2, 3]
    assert result.stats["figures_filtered"] == 3


def test_text_pdf_with_vision_describes_each_figure_once_and_never_normalizes(tmp_path: Path) -> None:
    pipeline, provider = _pipeline({"figure": FIGURE_JSON})

    result = pipeline.process_document(build_text_pdf(tmp_path / "t.pdf", pages=3, banner=True), document_id=DOC)

    assert provider is not None and provider.calls == ["figure"] * 3  # banner repeated on 3/3 pages → filtered
    assert f"![Graph G](asset://{DOC}/p002-f1.png)\n[Figure: A triangle graph.]" in result.markdown
    assert result.stats["figures_described"] == 3
    assert "normalization" not in result.llm_metrics["by_operation"]


def test_distinct_images_in_the_same_slot_are_not_treated_as_repeated(tmp_path: Path) -> None:
    pipeline, provider = _pipeline({"figure": FIGURE_JSON})
    path = build_text_pdf(tmp_path / "t.pdf", pages=4, same_position=True, distinct_images=True)

    result = pipeline.process_document(path, document_id=DOC)

    assert provider is not None and provider.calls == ["figure"] * 4
    assert [a.name for a in result.assets] == ["p001-f1.png", "p002-f1.png", "p003-f1.png", "p004-f1.png"]
    assert result.stats["figures_described"] == 4
    assert result.stats["figures_filtered"] == 4  # only the tiny logos


def test_identical_image_in_the_same_slot_is_filtered_as_repeated(tmp_path: Path) -> None:
    pipeline, provider = _pipeline({"figure": FIGURE_JSON})
    path = build_text_pdf(tmp_path / "t.pdf", pages=4, same_position=True)

    result = pipeline.process_document(path, document_id=DOC)

    assert provider is not None and provider.calls == []
    assert result.assets == []
    assert result.stats["figures_filtered"] == 8  # 4 repeated figures + 4 tiny logos


def test_pure_vector_figures_in_the_same_slot_are_never_repeated(tmp_path: Path) -> None:
    pipeline, provider = _pipeline({"figure": FIGURE_JSON})
    path = build_text_pdf(tmp_path / "t.pdf", pages=4, same_position=True, vector=True)

    result = pipeline.process_document(path, document_id=DOC)

    assert provider is not None and provider.calls == ["figure"] * 4
    assert [a.name for a in result.assets] == ["p001-f1.png", "p002-f1.png", "p003-f1.png", "p004-f1.png"]


def test_decorative_figure_is_dropped_without_asset(tmp_path: Path) -> None:
    decorative = json.dumps({"label": "decorative", "caption": "logo", "description": "", "content_markdown": ""})
    pipeline, _ = _pipeline({"figure": decorative})

    result = pipeline.process_document(build_text_pdf(tmp_path / "t.pdf", pages=1), document_id=DOC)

    assert result.assets == []
    assert "asset://" not in result.markdown
    assert result.stats["figures_decorative"] == 1


def test_scanned_pdf_ocr_with_figure_stores_page_image(tmp_path: Path) -> None:
    pipeline, _ = _pipeline({"ocr": "# Đề thi\n\nCâu 1: ...\n\n[Figure: A graph with 3 nodes.]"})

    result = pipeline.process_document(build_scanned_pdf(tmp_path / "s.pdf"), document_id=DOC)

    assert result.route == "ocr"
    assert f"![Page 1](asset://{DOC}/p001-page.jpg)\n[Figure: A graph with 3 nodes.]" in result.markdown
    assert [(a.name, a.content_type) for a in result.assets] == [("p001-page.jpg", "image/jpeg")]


def test_scanned_page_with_all_providers_failing_degrades_and_is_counted(tmp_path: Path) -> None:
    pipeline, _ = _pipeline({})

    result = pipeline.process_document(build_scanned_pdf(tmp_path / "s.pdf", pages=2), document_id=DOC)

    assert "[OCR_FAILED page 1]" in result.markdown and "[OCR_FAILED page 2]" in result.markdown
    assert result.quality_flags["ocr_failed_pages"] == 2


def test_mixed_pdf_routes_per_page(tmp_path: Path) -> None:
    text = fitz.open(build_text_pdf(tmp_path / "t.pdf", pages=1))
    text.insert_pdf(fitz.open(build_scanned_pdf(tmp_path / "s.pdf")))
    path = tmp_path / "mixed.pdf"
    text.save(str(path))
    pipeline, _ = _pipeline({"figure": FIGURE_JSON, "ocr": "Scanned text"})

    result = pipeline.process_document(path, document_id=DOC)

    assert result.route == "mixed"
    assert result.stats["pages_text"] == 1 and result.stats["pages_ocr"] == 1
    assert "Scanned text" in result.markdown


def test_pptx_builds_markdown_and_picture_assets(tmp_path: Path) -> None:
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Slide Title"
    slide.placeholders[1].text = "Slide body content for testing."
    slide.shapes.add_picture(io.BytesIO(png_bytes()), Inches(5), Inches(4), Inches(3), Inches(2))
    slide.shapes.add_picture(io.BytesIO(png_bytes(40, 40)), Inches(0.1), Inches(0.1), Inches(0.3), Inches(0.3))
    path = tmp_path / "deck.pptx"
    prs.save(str(path))
    pipeline, provider = _pipeline({"figure": FIGURE_JSON})

    result = pipeline.process_document(path, document_id=DOC)

    assert result.route == "pptx"
    assert result.markdown.startswith("## Slide Title\n\nSlide body content for testing.")
    # Pictures are numbered in reading order: the tiny top-left one is f1 (skipped), the real one f2.
    assert f"![Graph G](asset://{DOC}/p001-f2.png)" in result.markdown
    assert "@@FIGURE_" not in result.markdown
    assert provider is not None and provider.calls == ["figure"]  # tiny picture skipped
    assert [page for _, page in result.page_map] == [1]


def test_image_upload_is_ocrd_and_kept_as_asset_when_it_has_figures(tmp_path: Path) -> None:
    path = tmp_path / "photo.png"
    path.write_bytes(png_bytes())
    pipeline, _ = _pipeline({"ocr": "Notes\n\n[Figure: A hand-drawn tree.]"})

    result = pipeline.process_document(path, document_id=DOC)

    assert result.route == "image"
    assert f"![Page 1](asset://{DOC}/p001-page.png)" in result.markdown
    assert result.page_map == []  # non-paginated source → NULL page numbers


def _scans_with_header(tmp_path: Path) -> Path:
    """Three pages, each its OWN full-page image (unique digest) plus a ~55-char native header."""
    doc = fitz.open()
    for color in ("red", "green", "blue"):
        page = doc.new_page()
        page.insert_image(page.rect, stream=png_bytes(800, 600, color=color), keep_proportion=False)
        page.insert_text((72, 72), f"{color} scan header " + "H" * 40, fontsize=10)
    path = tmp_path / "scans.pdf"
    doc.save(str(path))
    doc.close()
    return path


def test_full_page_image_pages_with_short_unique_header_route_to_ocr(tmp_path: Path) -> None:
    # Each page has its OWN full-page image (unique digest) plus a ~50-char header: below the
    # 200-char ceiling and not repeated elsewhere, so the ruling routes it to OCR even though
    # native_text_chars (50) clears the plain SCANNED_TEXT_THRESHOLD (40).
    path = _scans_with_header(tmp_path)
    pipeline, provider = _pipeline({"ocr": "Scanned header page"})

    result = pipeline.process_document(path, document_id=DOC)

    assert result.route == "ocr"
    assert provider is not None and provider.calls == ["ocr"] * 3


def test_full_page_image_repeated_across_pages_stays_text_layer(tmp_path: Path) -> None:
    # The SAME full-page image (e.g. a lecture-deck background) repeats on every page: the
    # digest is not unique to one page, so the ruling must NOT route these pages to OCR.
    doc = fitz.open()
    shared_image = png_bytes(800, 600, color="gray")
    for _ in range(3):
        page = doc.new_page()
        page.insert_image(page.rect, stream=shared_image, keep_proportion=False)
        page.insert_text((72, 72), "Body text of the slide. " * 4, fontsize=10)
    path = tmp_path / "deck_bg.pdf"
    doc.save(str(path))
    doc.close()
    pipeline, _ = _pipeline()

    result = pipeline.process_document(path, document_id=DOC)

    assert result.route == "text_layer"
    assert result.llm_metrics["total_calls"] == 0


def test_figure_job_exception_degrades_without_failing_job(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    pipeline, _ = _pipeline()
    monkeypatch.setattr(
        pipeline._describer, "describe", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("boom"))
    )

    result = pipeline.process_document(build_text_pdf(tmp_path / "t.pdf", pages=1), document_id=DOC)

    assert result.stats["figure_failures"] == 1
    assert result.quality_flags["figure_failures"] == 1


def test_ocr_job_exception_is_recorded_as_ocr_failed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    pipeline, _ = _pipeline()
    monkeypatch.setattr(
        pipeline._ocr, "transcribe", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("boom"))
    )

    result = pipeline.process_document(build_scanned_pdf(tmp_path / "s.pdf"), document_id=DOC)

    assert "[OCR_FAILED page 1]" in result.markdown
    assert result.quality_flags["ocr_failed_pages"] == 1


def test_ocr_failure_keeps_the_native_text_of_the_page(tmp_path: Path) -> None:
    pipeline, _ = _pipeline({})

    result = pipeline.process_document(_scans_with_header(tmp_path), document_id=DOC)

    assert all(f"{color} scan header" in result.markdown for color in ("red", "green", "blue"))
    assert "[OCR_FAILED" not in result.markdown
    assert result.quality_flags["ocr_failed_pages"] == 3


def test_vision_disabled_ocr_page_keeps_native_text_instead_of_placeholder(tmp_path: Path) -> None:
    pipeline, _ = _pipeline()

    result = pipeline.process_document(_scans_with_header(tmp_path), document_id=DOC)

    assert all(f"{color} scan header" in result.markdown for color in ("red", "green", "blue"))
    assert "[VISION_PLACEHOLDER]" not in result.markdown
    assert result.quality_flags["ocr_failed_pages"] == 0


def test_vision_disabled_scan_without_native_text_keeps_placeholder(tmp_path: Path) -> None:
    pipeline, _ = _pipeline()

    result = pipeline.process_document(build_scanned_pdf(tmp_path / "s.pdf"), document_id=DOC)

    assert "[VISION_PLACEHOLDER]" in result.markdown


_PICTURE_WITH_TEXT = (
    "**==> picture [30 x 20] intentionally omitted <==**\n\n"
    "**----- Start of picture text -----**<br>\n{text}<br>**----- End of picture text -----**<br>\n"
)


def _layout_page(number: int, bbox: tuple[float, float, float, float], text: str, **kwargs: object) -> LayoutPage:
    span = _PICTURE_WITH_TEXT.format(text=text)
    markdown = f"## Page {number}\n\nBody text about machine learning on this page.\n\n{span}\nAfter the picture."
    start = markdown.index(span)
    region = PictureRegion(bbox, (start, start + len(span)), **kwargs)  # type: ignore[arg-type]
    return LayoutPage(number, markdown, 120, 612, 792, pictures=[region])


def test_too_small_picture_keeps_its_native_text(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(PdfLayoutReader, "read", lambda self, doc: [_layout_page(1, (20, 20, 50, 40), "Interested?")])
    pipeline, _ = _pipeline()

    result = pipeline.process_document(build_text_pdf(tmp_path / "t.pdf", pages=1), document_id=DOC)

    assert "Interested?" in result.markdown
    assert result.stats["figures_filtered"] == 1


def test_repeated_logo_text_is_still_dropped(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    pages = [_layout_page(n, (100, 100, 400, 300), "HUST", digests=("logo",)) for n in (1, 2)]
    monkeypatch.setattr(PdfLayoutReader, "read", lambda self, doc: pages)
    pipeline, _ = _pipeline()

    result = pipeline.process_document(build_text_pdf(tmp_path / "t.pdf", pages=2), document_id=DOC)

    assert "HUST" not in result.markdown
    assert result.stats["figures_filtered"] == 2


def test_figure_provider_failure_is_counted_and_job_completes(tmp_path: Path) -> None:
    pipeline, provider = _pipeline({})

    result = pipeline.process_document(build_text_pdf(tmp_path / "t.pdf", pages=3), document_id=DOC)

    assert provider is not None and provider.calls == ["figure"] * 3
    assert result.route == "text_layer"
    assert result.stats["figure_failures"] == 3
    assert result.quality_flags["figure_failures"] == 3
    assert [a.name for a in result.assets] == ["p001-f1.png", "p002-f1.png", "p003-f1.png"]


def test_undescribed_pdf_figure_counts_as_failure(tmp_path: Path) -> None:
    pipeline, _ = _pipeline({"figure": UNDESCRIBED_JSON})

    result = pipeline.process_document(build_text_pdf(tmp_path / "t.pdf", pages=3), document_id=DOC)

    assert result.stats["figure_failures"] == 3
    assert result.quality_flags["figure_failures"] == 3
    assert result.stats["figures_described"] == 0


def test_undescribed_pptx_figure_counts_as_failure(tmp_path: Path) -> None:
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Slide Title"
    slide.shapes.add_picture(io.BytesIO(png_bytes()), Inches(5), Inches(4), Inches(3), Inches(2))
    path = tmp_path / "deck.pptx"
    prs.save(str(path))
    pipeline, _ = _pipeline({"figure": UNDESCRIBED_JSON})

    result = pipeline.process_document(path, document_id=DOC)

    assert result.stats["figure_failures"] == 1
    assert result.quality_flags["figure_failures"] == 1


class _SerializingLock:
    """Stands in for the module-level PyMuPDF lock; fails loudly on nested/contended misuse."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.acquisitions = 0

    def __enter__(self) -> _SerializingLock:
        if not self._lock.acquire(timeout=10):
            raise AssertionError("PyMuPDF lock not released (nested acquisition?)")
        self.acquisitions += 1
        return self

    def __exit__(self, *exc: object) -> None:
        self._lock.release()


def test_concurrent_jobs_share_one_module_level_pymupdf_lock(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    lock = _SerializingLock()
    monkeypatch.setattr(pdf_extractor, "_PYMUPDF_LOCK", lock)
    text_pdf = build_text_pdf(tmp_path / "t.pdf", pages=3)
    scanned_pdf = build_scanned_pdf(tmp_path / "s.pdf", pages=2)

    def _run(path: Path) -> str:
        pipeline, _ = _pipeline({"figure": FIGURE_JSON, "ocr": "Scanned text\n\n[Figure: A chart.]"})
        return pipeline.process_document(path, document_id=DOC).markdown

    with ThreadPoolExecutor(max_workers=2) as pool:
        text_md, scanned_md = pool.map(_run, [text_pdf, scanned_pdf])

    assert "[Figure: A triangle graph.]" in text_md and "Scanned text" in scanned_md
    # 3 figure crops + 2 OCR renders + 2 page-image renders, plus open/read and close per document.
    assert lock.acquisitions == 3 + 2 + 2 + 2 * 2
