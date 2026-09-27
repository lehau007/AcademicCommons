from __future__ import annotations

from app.services.document_processing.layout import LayoutPage, PictureRegion
from app.services.document_processing.pdf_figures import (
    is_too_small,
    repeated_signatures,
    splice,
)


def _page(n: int, regions: list[PictureRegion], markdown: str = "") -> LayoutPage:
    return LayoutPage(page_number=n, markdown=markdown, native_text_chars=100, width=612, height=792, pictures=regions)


def test_small_regions_by_side_or_area() -> None:
    page = _page(1, [])
    assert is_too_small(PictureRegion((20, 20, 50, 40), (0, 0)), page) is True  # 20pt side
    assert is_too_small(PictureRegion((0, 0, 60, 60), (0, 0)), page) is True  # 0.7% of page
    assert is_too_small(PictureRegion((150, 200, 450, 450), (0, 0)), page) is False


def test_repeated_signatures_need_threshold_pages() -> None:
    logo = PictureRegion((20, 20, 120, 80), (0, 0), digests=("logo",))
    pages = [
        _page(i, [logo, PictureRegion((100, 100 + 40 * i, 400, 300 + 40 * i), (0, 0), digests=("fig",))])
        for i in range(1, 5)
    ]

    repeated = repeated_signatures(pages, total_pages=4)

    assert len(repeated) == 1  # only the logo (4 pages ≥ max(2, ceil(1.2)))


def test_same_slot_with_different_images_is_not_repeated() -> None:
    pages = [_page(i, [PictureRegion((100, 100, 400, 300), (0, 0), digests=(f"img{i}",))]) for i in range(1, 5)]

    assert repeated_signatures(pages, total_pages=4) == set()


def test_same_slot_with_the_same_image_is_repeated() -> None:
    pages = [_page(i, [PictureRegion((100, 100, 400, 300), (0, 0), digests=("same",))]) for i in range(1, 5)]

    assert len(repeated_signatures(pages, total_pages=4)) == 1


def test_pure_vector_regions_are_never_repeated() -> None:
    pages = [_page(i, [PictureRegion((100, 100, 400, 300), (0, 0))]) for i in range(1, 5)]

    assert repeated_signatures(pages, total_pages=4) == set()


def test_same_slot_with_the_same_picture_text_is_repeated() -> None:
    markdown = (
        "**==> picture [1 x 1] intentionally omitted <==**\n\n"
        "**----- Start of picture text -----**<br>\nHUST<br>**----- End of picture text -----**<br>\n"
    )
    region = PictureRegion((20, 20, 120, 80), (0, len(markdown)))
    pages = [_page(i, [region], markdown) for i in range(1, 5)]

    assert len(repeated_signatures(pages, total_pages=4)) == 1


def test_splice_replaces_spans_right_to_left_and_drops_empty() -> None:
    md = "A [P1] B [P2] C"

    out = splice(md, [((2, 6), "FIG1"), ((9, 13), "")])

    assert out == "A \n\nFIG1\n\n B \n C"
