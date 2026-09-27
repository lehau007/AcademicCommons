from __future__ import annotations

from app.services.document_processing.markdown_utils import build_page_map, strip_outer_fence


def test_build_page_map_line_offsets_match_joined_output() -> None:
    # Two single-line batches on pages 1 and 5.
    outputs = ["# Slide one\ncontent A", "# Slide five\ncontent B"]
    pages = [1, 5]
    page_map = build_page_map(outputs, pages)
    # batch 0 starts at line 0; batch 1 starts after 2 lines + 1 blank separator = line 3.
    assert page_map == [(0, 1), (3, 5)]
    joined = "\n\n".join(outputs)
    # Line 3 of the joined string is indeed the start of batch 1.
    assert joined.split("\n")[3] == "# Slide five"


def test_build_page_map_collapses_repeats_and_carries_none() -> None:
    outputs = ["a", "b", "c", "d"]
    pages = [2, 2, None, 7]  # page 2 repeats; None carries 2 forward; then 7.
    page_map = build_page_map(outputs, pages)
    assert page_map == [(0, 2), (6, 7)]


def test_build_page_map_empty() -> None:
    assert build_page_map([], []) == []


def test_build_page_map_all_none_pages_returns_empty() -> None:
    # A document with no page/slide metadata at all (e.g. standalone image
    # upload) must yield an empty page_map, never a fabricated page number.
    outputs = ["some content", "more content"]
    pages: list[int | None] = [None, None]
    assert build_page_map(outputs, pages) == []


def test_strip_outer_fence_removes_whole_wrapping_fence_only() -> None:
    assert strip_outer_fence("```markdown\n# Title\nbody\n```") == "# Title\nbody"
    inner = "# Title\n\n```c\nint x;\n```"
    assert strip_outer_fence(inner) == inner
