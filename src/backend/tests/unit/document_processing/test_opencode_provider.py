from __future__ import annotations

from app.services.document_processing.providers.opencode import _strip_think


def test_strip_think_removes_closed_block() -> None:
    content = "<think>let me read the page</think>\n# Junior AI Engineer\nBody text"
    assert _strip_think(content) == "# Junior AI Engineer\nBody text"


def test_strip_think_passes_through_plain_text() -> None:
    assert _strip_think("# Junior AI Engineer\nBody text") == "# Junior AI Engineer\nBody text"


def test_strip_think_drops_truncated_unclosed_block() -> None:
    # minimax hit the token limit mid-thought: no closing </think>, no OCR text
    # after it. We must NOT leak the raw reasoning as if it were document text.
    content = "<think>The page appears to contain a job description. I should transcribe"
    assert _strip_think(content) == ""


def test_strip_think_drops_trailing_unclosed_block() -> None:
    content = "<think>ok</think>\n# Heading\n<think>now the answer got cut off here"
    assert _strip_think(content) == "# Heading"
