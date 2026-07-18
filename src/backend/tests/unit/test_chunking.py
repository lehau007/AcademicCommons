from __future__ import annotations

from app.workers.chunking import _split_paragraphs, build_chunks, parse_markdown_sections


class DummyEncoder:
    def encode(self, texts: list[str], input_type: str = "passage") -> list[list[float]]:
        # Return a simple mock embedding for each text
        del input_type
        return [[0.1] * 1024 for _ in texts]


def test_split_paragraphs_tables() -> None:
    text = (
        "Some introduction.\n\n"
        "| Column 1 | Column 2 |\n"
        "|---|---|\n"
        "| Value 1 | Value 2 |\n\n"
        "Some conclusion."
    )
    paragraphs = _split_paragraphs(text)
    assert len(paragraphs) == 3
    assert paragraphs[0] == "Some introduction."
    assert "| Column 1 | Column 2 |" in paragraphs[1]
    assert "| Value 1 | Value 2 |" in paragraphs[1]
    assert paragraphs[2] == "Some conclusion."


def test_split_paragraphs_mermaid() -> None:
    text = (
        "Intro\n\n"
        "```mermaid\n"
        "graph TD\n"
        "  A --> B\n"
        "```\n\n"
        "Outro"
    )
    paragraphs = _split_paragraphs(text)
    assert len(paragraphs) == 3
    assert paragraphs[1] == "```mermaid\ngraph TD\n  A --> B\n```"


def test_split_paragraphs_latex() -> None:
    text = (
        "Intro\n\n"
        "$$\n"
        "x^2 + y^2 = z^2\n"
        "$$\n\n"
        "Outro"
    )
    paragraphs = _split_paragraphs(text)
    assert len(paragraphs) == 3
    assert "$$" in paragraphs[1]
    assert "x^2 + y^2 = z^2" in paragraphs[1]


def test_split_paragraphs_latex_backslash_brackets() -> None:
    text = (
        "Intro\n\n"
        "\\[\n"
        "a + b = c\n"
        "\\]\n\n"
        "Outro"
    )
    paragraphs = _split_paragraphs(text)
    assert len(paragraphs) == 3
    assert "\\[" in paragraphs[1]
    assert "a + b = c" in paragraphs[1]


def test_split_paragraphs_code_blocks() -> None:
    text = (
        "Intro\n\n"
        "```python\n"
        "def hello():\n"
        "    print('world')\n"
        "```\n\n"
        "Outro"
    )
    paragraphs = _split_paragraphs(text)
    assert len(paragraphs) == 3
    assert "```python" in paragraphs[1]
    assert "def hello():" in paragraphs[1]


def test_split_paragraphs_lists() -> None:
    text = (
        "Intro\n\n"
        "- Item A\n"
        "- Item B\n"
        "- Item C\n\n"
        "Outro"
    )
    paragraphs = _split_paragraphs(text)
    assert len(paragraphs) == 3
    assert "- Item A" in paragraphs[1]
    assert "- Item C" in paragraphs[1]


def test_split_paragraphs_mcq() -> None:
    text = (
        "Intro\n\n"
        "Câu 42: What is the capital of France?\n"
        "A. London\n"
        "B. Paris\n"
        "C. Berlin\n"
        "D. Madrid\n\n"
        "Outro"
    )
    paragraphs = _split_paragraphs(text)
    assert len(paragraphs) == 3
    assert "Câu 42:" in paragraphs[1]
    assert "B. Paris" in paragraphs[1]


def test_build_chunks_block_exceeding_max_chars() -> None:
    # A single very large paragraph exceeding max_chunk_chars (e.g., 1500 chars)
    large_paragraph = "A" * 1500
    markdown = f"# Title\n\n{large_paragraph}"

    encoder = DummyEncoder()
    chunks = build_chunks(markdown, encoder, max_chunk_chars=1200)

    # It should form its own dedicated chunk and not get truncated or discarded
    assert len(chunks) == 1
    assert chunks[0].text == large_paragraph
    assert chunks[0].char_count == 1500


def test_parse_markdown_sections_records_start_line() -> None:
    md = "Intro line\n\n# First\nbody one\n\n## Second\nbody two"
    sections = parse_markdown_sections(md)
    # Stripped lines: 0="Intro line",1="",2="# First",3="body one",4="",5="## Second",6="body two"
    titles = {s.title: s.start_line for s in sections}
    assert titles["Document Start"] == 0
    assert titles["First"] == 2
    assert titles["Second"] == 5


def test_build_chunks_assigns_page_from_page_map() -> None:
    # Section "First" starts at line 0 -> page 1; "Second" starts at line 3 -> page 8.
    # Line count: 0="# First", 1="body one...", 2="" (empty), 3="## Second", 4="body two..."
    md = "# First\nbody one is reasonably long text.\n\n## Second\nbody two is also text here."
    page_map = [(0, 1), (3, 8)]
    chunks = build_chunks(md, DummyEncoder(), page_map=page_map, min_chunk_chars=1)
    assert chunks, "expected at least one chunk per section"
    by_section = {c.section_title: c.page for c in chunks}
    assert by_section["First"] == 1
    assert by_section["Second"] == 8


def test_build_chunks_without_page_map_leaves_page_none() -> None:
    md = "# First\nbody one is reasonably long text."
    chunks = build_chunks(md, DummyEncoder(), min_chunk_chars=1)
    assert chunks
    assert all(c.page is None for c in chunks)
