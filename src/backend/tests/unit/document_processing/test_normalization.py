from __future__ import annotations

from app.services.document_processing.config import DocumentProcessingConfig
from app.services.document_processing.models import Block
from app.services.document_processing.normalization import Normalizer

from .conftest import make_chain


def _normalizer(config: DocumentProcessingConfig | None = None) -> Normalizer:
    config = config or DocumentProcessingConfig(enable_real_vision=False)
    return Normalizer(config, provider_chain=make_chain())


def test_rule_based_cleanup_strips_markers() -> None:
    blocks: list[Block] = [
        {
            "kind": "text",
            "content": "Here's a description of image_url\nHere is the table",
        }
    ]
    cleaned = _normalizer().rule_based_cleanup(blocks)
    content = cleaned[0]["content"]
    assert "Here's a description" not in content
    assert "Here is the table" not in content
    assert "image_url" not in content


def test_rule_based_cleanup_strips_whole_response_fence() -> None:
    """A model that accidentally wraps its entire reply in a code fence

    (e.g. ```json ... ```) should have that outer fence stripped.
    """
    blocks: list[Block] = [
        {
            "kind": "text",
            "content": '```json\n{"topic": "x"}\n```',
        }
    ]
    cleaned = _normalizer().rule_based_cleanup(blocks)
    content = cleaned[0]["content"]
    assert "```" not in content
    assert '{"topic": "x"}' in content


def test_rule_based_cleanup_preserves_inline_diagram_fence() -> None:
    """A ```-fenced ASCII diagram inside otherwise-normal content must survive

    cleanup untouched — stripping it turns the diagram into unformatted prose
    that gets mangled by markdown word-wrap in the UI.
    """
    content = (
        "## Slide title\n\n"
        "Some bullet text\n\n"
        "```\n+---+    +---+\n| A |--->| B |\n+---+    +---+\n```\n\n"
        "[Diagram: A feeds into B]\n\n"
        "More text after"
    )
    blocks: list[Block] = [{"kind": "text", "content": content}]
    cleaned = _normalizer().rule_based_cleanup(blocks)
    assert cleaned[0]["content"] == content


def test_batch_blocks_does_not_split_on_slide_boundary() -> None:
    blocks: list[Block] = [
        {"kind": "text", "content": "a", "slide": 1},
        {"kind": "text", "content": "b", "slide": 2},
    ]
    batches = _normalizer().batch_blocks(blocks)
    assert len(batches) == 1


def test_batch_blocks_splits_on_char_budget() -> None:
    config = DocumentProcessingConfig(enable_real_vision=False, normalize_char_budget=10)
    blocks: list[Block] = [
        {"kind": "text", "content": "x" * 8},
        {"kind": "text", "content": "y" * 8},
    ]
    batches = _normalizer(config).batch_blocks(blocks)
    assert len(batches) == 2


def test_normalize_passthrough_when_vision_disabled() -> None:
    blocks: list[Block] = [
        {"kind": "text", "content": "first"},
        {"kind": "text", "content": "second"},
    ]
    markdown, trace, page_map = _normalizer().normalize(blocks)
    assert "first" in markdown
    assert "second" in markdown
    assert trace
    assert all(entry["mode"] == "passthrough_vision_disabled" for entry in trace)


def test_normalize_empty_blocks_returns_empty_marker() -> None:
    markdown, trace, page_map = _normalizer().normalize([])
    assert markdown == "[EMPTY_OUTPUT]"
    assert trace == []
    assert page_map == []


def test_merge_blocks_to_markdown_formats_text_and_vision() -> None:
    blocks: list[Block] = [
        {"kind": "text", "content": "body text", "page": 1},
        {"kind": "vision_placeholder", "content": "an image", "page": 2},
    ]
    md = _normalizer().merge_blocks_to_markdown("doc-1", "src/foo.pdf", blocks)
    assert "# OCR Result: doc-1" in md
    assert "Source: `src/foo.pdf`" in md
    assert "## Segment 1" in md
    assert "body text" in md
    assert "> Vision segment 2: an image" in md
