from __future__ import annotations

from app.services.document_processing.ocr import OCR_PROMPT, PageOcr, insert_page_image

from .conftest import ScriptedProvider, make_chain


def test_prompt_forbids_answering_and_translation() -> None:
    assert "Do NOT answer, solve, summarize, translate" in OCR_PROMPT
    assert "[Figure:" in OCR_PROMPT


def test_prompt_asks_for_a_2_to_4_sentence_figure_description() -> None:
    assert (
        "then add one line: [Figure: <2-4 sentence description of what it shows and which concept it "
        "illustrates; only what is visible>]." in OCR_PROMPT
    )
    assert "1-2 sentence" not in OCR_PROMPT


def test_transcribe_strips_outer_fence_and_detects_figures() -> None:
    provider = ScriptedProvider({"ocr": "```markdown\n# Đề thi\n\n[Figure: a graph with 3 nodes]\n```"})

    result = PageOcr(make_chain([provider], enable_real_vision=True)).transcribe(b"png")

    assert result.markdown == "# Đề thi\n\n[Figure: a graph with 3 nodes]"
    assert result.has_figures is True and result.failed is False


def test_transcribe_all_providers_failing_is_failed() -> None:
    result = PageOcr(make_chain([ScriptedProvider({})], enable_real_vision=True)).transcribe(b"png")

    assert result.failed is True and result.markdown == ""


def test_transcribe_disabled_returns_placeholder() -> None:
    result = PageOcr(make_chain([], enable_real_vision=False)).transcribe(b"png")

    assert result.markdown.startswith("[VISION_PLACEHOLDER]")
    assert result.failed is False and result.has_figures is False


def test_insert_page_image_goes_before_first_figure_line() -> None:
    md = "# T\n\ntext\n\n[Figure: one]\n\n[Figure: two]"

    out = insert_page_image(md, "asset://d/p003-page.jpg", 3)

    assert out == "# T\n\ntext\n\n![Page 3](asset://d/p003-page.jpg)\n[Figure: one]\n\n[Figure: two]"
