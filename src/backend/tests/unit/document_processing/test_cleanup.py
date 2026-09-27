from __future__ import annotations

from app.services.document_processing.cleanup import MarkdownCleaner


def test_removes_leftover_picture_artifacts() -> None:
    page = (
        "## Title\n\n**==> picture [156 x 138] intentionally omitted <==**\n\n"
        "**----- Start of picture text -----**<br>\nu<br>e1<br>**----- End of picture text -----**<br>\n\nBody"
    )

    [cleaned] = MarkdownCleaner().clean_pages([page])

    assert "intentionally omitted" not in cleaned
    assert "picture text" not in cleaned
    assert "## Title" in cleaned and "Body" in cleaned


def test_drops_boilerplate_repeated_on_half_the_pages_but_keeps_tables_images_and_code() -> None:
    pages = [
        f"ĐẠI HỌC BÁCH KHOA HÀ NỘI\n\n## Slide {i}\n\n| a | b |\n| --- | --- |\n\n"
        f"![Figure](asset://d/p00{i}-f1.png)\n\n```c\nint x;\n```"
        for i in range(1, 5)
    ]

    cleaned = MarkdownCleaner().clean_pages(pages)

    for i, page in enumerate(cleaned, start=1):
        assert "ĐẠI HỌC BÁCH KHOA HÀ NỘI" not in page
        assert f"## Slide {i}" in page
        assert "| --- | --- |" in page
        assert "![Figure]" in page
        assert "int x;" in page


def test_boilerplate_needs_at_least_three_pages() -> None:
    pages = ["Header\n\nA", "Header\n\nB"]

    assert MarkdownCleaner().clean_pages(pages) == ["Header\n\nA", "Header\n\nB"]


def test_drops_standalone_page_numbers_outside_code_and_collapses_blank_lines() -> None:
    page = "Text\n\n\n\n**12**\n\n7\n\n```\n42\n```\nEnd   "

    [cleaned] = MarkdownCleaner().clean_pages([page])

    assert cleaned == "Text\n\n```\n42\n```\nEnd"
