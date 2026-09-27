from __future__ import annotations

import json

import pytest

from app.services.document_processing.figures import (
    FigureDescriber,
    FigureDescription,
    parse_figure_json,
    render_figure_block,
)

from .conftest import ScriptedProvider, make_chain

GOOD = {"label": "table", "caption": "Incidence matrix", "description": "Rows are vertices.\nColumns are edges.",
        "content_markdown": "| | e1 |\n|---|---|\n| v | 1 |"}


def test_parse_valid_json_flattens_description_whitespace() -> None:
    desc = parse_figure_json(json.dumps(GOOD))

    assert desc == FigureDescription("table", "Incidence matrix", "Rows are vertices. Columns are edges.",
                                     "| | e1 |\n|---|---|\n| v | 1 |")


@pytest.mark.parametrize(
    "raw",
    ['{"label": "diagram", "caption": "x", "descr', "not json at all", '{"label": "weird", "caption": "c"}'],
)
def test_parse_bad_or_partial_json_never_raises(raw: str) -> None:
    desc = parse_figure_json(raw)

    assert desc.label in {"other", "diagram"}
    assert desc.failed is False


def test_parse_vision_error_marks_failed() -> None:
    assert parse_figure_json("[VISION_ERROR] All vision providers failed (x).").failed is True


def test_render_block_with_description_and_table() -> None:
    block = render_figure_block(
        "asset://d/p001-f1.png", parse_figure_json(json.dumps(GOOD)), fallback_caption="Figure p1-1"
    )

    assert block.splitlines()[0] == "![Incidence matrix](asset://d/p001-f1.png)"
    assert "[Figure: Rows are vertices. Columns are edges.]" in block
    assert "| v | 1 |" in block


def test_render_block_failure_uses_fallback_caption_and_native_text() -> None:
    failed = FigureDescription("other", "", "", "", failed=True)

    block = render_figure_block("asset://d/p001-f1.png", failed, fallback_caption="Figure p1-1", fallback_text="u\ne1")

    assert block == "![Figure p1-1](asset://d/p001-f1.png)\n\nu\ne1"


def test_render_block_escapes_brackets_in_caption() -> None:
    desc = FigureDescription("diagram", "Graph [G]", "d", "")

    assert render_figure_block("asset://d/p001-f1.png", desc, fallback_caption="x").startswith("![Graph (G)](")


def test_describer_makes_one_schema_call() -> None:
    provider = ScriptedProvider({"figure": json.dumps(GOOD)})
    describer = FigureDescriber(make_chain([provider], enable_real_vision=True))

    desc = describer.describe(b"png", figure_text="u e1", page_text="Incidence")

    assert provider.calls == ["figure"]
    assert desc.caption == "Incidence matrix"


def test_describer_disabled_returns_empty_without_calls() -> None:
    provider = ScriptedProvider({"figure": json.dumps(GOOD)})

    describer = FigureDescriber(make_chain([provider], enable_real_vision=False))
    desc = describer.describe(b"p", figure_text="", page_text="")

    assert desc == FigureDescription.empty()
    assert provider.calls == []
