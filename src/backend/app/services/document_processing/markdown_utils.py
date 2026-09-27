"""Markdown helpers shared by the pipeline (page map, fence stripping)."""

from __future__ import annotations


def build_page_map(outputs: list[str], pages: list[int | None]) -> list[tuple[int, int]]:
    """Map line offsets in ``"\\n\\n".join(outputs)`` to their source page/slide.

    Each output segment starts one blank separator line after the previous one
    (the ``"\\n\\n"`` join), so ``line_cursor`` accounts for that gap. ``None``
    pages carry the last known page forward; consecutive equal pages collapse
    to a single boundary. Line indices are 0-based into the joined string.
    A batch whose page is unknown AND no prior batch established a page stays
    unmapped — returning ``[]`` for an all-``None`` input, never a fabricated
    page number (non-paginated sources must yield ``page_number = NULL``).
    """
    page_map: list[tuple[int, int]] = []
    line_cursor = 0
    last_page: int | None = None
    for idx, text in enumerate(outputs):
        if idx > 0:
            line_cursor += 1  # blank line inserted by the "\n\n" join
        page = pages[idx] if idx < len(pages) and pages[idx] is not None else last_page
        if page is not None and (not page_map or page_map[-1][1] != page):
            page_map.append((line_cursor, page))
        if page is not None:
            last_page = page
        line_cursor += text.count("\n") + 1
    return page_map


def strip_outer_fence(text: str) -> str:
    """Strip a code fence only when it wraps the ENTIRE block (e.g. a model
    accidentally wrapping its whole response in ```json ... ```).

    Fences that appear inside the content — e.g. the ASCII-diagram code blocks
    the vision-OCR prompts intentionally ask for — must be left untouched, or
    the diagram loses its monospace formatting and gets word-wrapped as prose.
    """
    stripped = text.strip()
    if not stripped.startswith("```") or not stripped.endswith("```"):
        return text
    lines = stripped.split("\n")
    if len(lines) < 2 or lines[-1].strip() != "```":
        return text
    inner = lines[1:-1]
    if any(line.strip() == "```" for line in inner):
        # More than one fence pair (or a fence + our own closer) — ambiguous,
        # leave as-is rather than risk eating an intentional diagram fence.
        return text
    return "\n".join(inner)
