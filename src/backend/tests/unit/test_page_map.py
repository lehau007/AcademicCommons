from __future__ import annotations

from app.services.document_processing.config import DocumentProcessingConfig
from app.services.document_processing.metrics import LlmCallRecorder
from app.services.document_processing.normalization import Normalizer, build_page_map
from app.services.document_processing.progress import ProgressEmitter
from app.services.document_processing.providers.base import (
    ProviderResponse,
    VisionLanguageProvider,
)
from app.services.document_processing.providers.chain import ProviderChain


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


def _normalizer_vision_off() -> Normalizer:
    # enable_real_vision False -> passthrough mode, no provider calls.
    # Use small char budget to force separate batches.
    config = DocumentProcessingConfig(enable_real_vision=False, normalize_char_budget=10)
    return Normalizer(config, provider_chain=None)  # chain unused in passthrough


def test_normalize_returns_page_map_passthrough() -> None:
    normalizer = _normalizer_vision_off()
    blocks = [
        {"kind": "text", "page": 1, "content": "Alpha on page one."},
        {"kind": "text", "page": 4, "content": "Beta on page four."},
    ]
    markdown, trace, page_map = normalizer.normalize(blocks, doc_type="document")
    assert not markdown.startswith("\n")  # alignment invariant: no leading blank line
    assert page_map[0] == (0, 1)
    assert any(page == 4 for _, page in page_map)


class _LeadingBlankLineProvider(VisionLanguageProvider):
    """A fake LLM provider whose first-batch output has a leading blank line —

    exactly the alignment-invariant violation that must make ``normalize()``
    degrade ``page_map`` to ``[]`` (per Finding 2) without touching the markdown.
    """

    def __init__(self) -> None:
        self.provider_name = "fake"

    def complete(
        self,
        prompt: str,
        *,
        images: list[bytes] | None = None,
        operation: str = "text",
    ) -> ProviderResponse:
        return ProviderResponse(
            text="\nHeading\n\nBody text.",
            provider=self.provider_name,
            model="fake-model",
            status="success",
            latency_ms=1,
        )


def test_normalize_degrades_page_map_when_llm_output_has_leading_blank_line() -> None:
    # real_vision=True routes through the LLM path; the fake provider returns
    # a leading blank line in its very first batch's output, which would
    # silently shift every downstream page-boundary offset (see Finding 2).
    config = DocumentProcessingConfig(enable_real_vision=True)
    chain = ProviderChain(
        [_LeadingBlankLineProvider()],
        recorder=LlmCallRecorder(),
        emitter=ProgressEmitter(),
        enable_real_vision=True,
    )
    normalizer = Normalizer(config, provider_chain=chain)
    blocks = [{"kind": "text", "page": 1, "content": "Raw OCR text."}]

    markdown, trace, page_map = normalizer.normalize(blocks, doc_type="document")

    assert page_map == []
    # The markdown itself must be preserved exactly as the LLM returned it —
    # never stripped or otherwise mutated as a side effect of the degrade.
    assert markdown == "\nHeading\n\nBody text."
