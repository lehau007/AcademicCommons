from __future__ import annotations

from pathlib import Path

import fitz  # type: ignore[import-untyped]
import pytest

from app.services.document_processing.layout import PdfLayoutReader, PictureRegion, picture_text

from .conftest import build_scanned_pdf, build_text_pdf, png_bytes


def test_reads_text_pages_with_picture_spans(tmp_path: Path) -> None:
    doc = fitz.open(build_text_pdf(tmp_path / "t.pdf", pages=2))

    pages = PdfLayoutReader().read(doc)

    assert [p.page_number for p in pages] == [1, 2]
    first = pages[0]
    assert "Chapter 1: Graph theory basics" in first.markdown
    assert first.native_text_chars > 40
    assert len(first.pictures) == 2  # figure + logo
    for region in first.pictures:
        start, end = region.span
        assert first.markdown[start:end].lstrip().startswith("**==> picture")


def test_scanned_page_has_no_native_text(tmp_path: Path) -> None:
    doc = fitz.open(build_scanned_pdf(tmp_path / "s.pdf"))

    [page] = PdfLayoutReader().read(doc)

    assert page.native_text_chars == 0


def test_layout_failure_falls_back_to_plain_text(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import pymupdf4llm  # type: ignore[import-untyped]

    def _boom(*args: object, **kwargs: object) -> None:
        raise RuntimeError("layout model crashed")

    monkeypatch.setattr(pymupdf4llm, "to_markdown", _boom)
    doc = fitz.open(build_text_pdf(tmp_path / "t.pdf", pages=2))
    reader = PdfLayoutReader()

    pages = reader.read(doc)

    assert reader.used_fallback is True
    assert "Chapter 2" in pages[1].markdown
    assert pages[1].pictures == []


def test_full_page_image_digest_set_for_scanned_page_and_none_for_text_pdf(tmp_path: Path) -> None:
    scanned_doc = fitz.open(build_scanned_pdf(tmp_path / "s.pdf"))
    [scanned_page] = PdfLayoutReader().read(scanned_doc)
    assert scanned_page.full_page_image_digest is not None

    text_doc = fitz.open(build_text_pdf(tmp_path / "t.pdf", pages=2))
    text_pages = PdfLayoutReader().read(text_doc)
    assert all(p.full_page_image_digest is None for p in text_pages)


def _largest(pictures: list[PictureRegion]) -> PictureRegion:
    return max(pictures, key=lambda r: (r.bbox[2] - r.bbox[0]) * (r.bbox[3] - r.bbox[1]))


def test_picture_regions_carry_the_digests_of_their_raster_images(tmp_path: Path) -> None:
    doc = fitz.open(build_text_pdf(tmp_path / "t.pdf", pages=2, same_position=True, distinct_images=True))

    first, second = (_largest(page.pictures) for page in PdfLayoutReader().read(doc))

    assert len(first.digests) == 1 and len(second.digests) == 1
    assert first.digests != second.digests


def test_vector_regions_have_no_digests_even_over_a_full_page_background(tmp_path: Path) -> None:
    doc = fitz.open()
    page = doc.new_page()
    page.insert_image(page.rect, stream=png_bytes(800, 600, color="gray"), keep_proportion=False)
    page.insert_text((72, 72), "Body text of the slide. " * 4, fontsize=10)
    shape = page.new_shape()
    shape.draw_rect(fitz.Rect(150, 200, 450, 450))
    for k in range(6):
        shape.draw_circle(fitz.Point(200 + 40 * k, 300 + (k % 2) * 60), 15)
    shape.finish(color=(0, 0, 0), fill=(0.8, 0.8, 1), width=2)
    shape.commit()
    path = tmp_path / "bg.pdf"
    doc.save(str(path))
    doc.close()

    [layout] = PdfLayoutReader().read(fitz.open(path))

    assert layout.full_page_image_digest is not None
    assert layout.pictures and all(region.digests == () for region in layout.pictures)


def test_picture_text_extracts_lines() -> None:
    span = (
        "**==> picture [1 x 1] intentionally omitted <==**\n\n"
        "**----- Start of picture text -----**<br>\nu<br>e1<br>v w<br>"
        "**----- End of picture text -----**<br>\n"
    )

    assert picture_text(span) == "u\ne1\nv w"
    assert picture_text("**==> picture [1 x 1] intentionally omitted <==**") == ""
