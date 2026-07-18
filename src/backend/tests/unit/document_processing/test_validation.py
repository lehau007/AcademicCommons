from __future__ import annotations

import json

from app.services.document_processing.models import Block
from app.services.document_processing.validation import (
    OutputValidator,
    render_deterministic_markdown,
)


def test_canonicalize_structured_blocks_adjacency_matrix() -> None:
    payload = {
        "schema_version": "1.0",
        "content_type": "adjacency_matrix",
        "values": [[0, 1], [1, 0]],
    }
    blocks: list[Block] = [{"kind": "text", "content": json.dumps(payload)}]

    validators = OutputValidator().canonicalize_structured_blocks(blocks)
    assert validators["parseable"] is True
    assert validators["matrix_shape"] is True
    assert validators["binary_values"] is True

    # content rewritten to a deterministic markdown table.
    rewritten = blocks[0]["content"]
    assert rewritten == render_deterministic_markdown(payload)
    assert "schema_version" not in rewritten
    assert "|" in rewritten


def test_canonicalize_ignores_plain_text_blocks() -> None:
    blocks: list[Block] = [{"kind": "text", "content": "just prose"}]
    validators = OutputValidator().canonicalize_structured_blocks(blocks)
    assert validators["parseable"] is None
    assert blocks[0]["content"] == "just prose"


def test_assemble_quality_flags_route_match_and_mismatch() -> None:
    validator = OutputValidator()
    empty_validators = {
        "parseable": None,
        "matrix_shape": None,
        "binary_values": None,
        "table_consistency": None,
    }

    matched = validator.assemble_quality_flags(
        route="direct_text",
        expected_route="direct_text",
        validators=empty_validators,
        raw_markdown="some content",
    )
    assert matched["route_match"] is True
    assert "route_mismatch" not in matched["warnings"]

    mismatched = validator.assemble_quality_flags(
        route="hybrid",
        expected_route="direct_text",
        validators=empty_validators,
        raw_markdown="some content",
    )
    assert mismatched["route_match"] is False
    assert "route_mismatch" in mismatched["warnings"]


def test_assemble_quality_flags_detects_vision_placeholder() -> None:
    flags = OutputValidator().assemble_quality_flags(
        route="vision_only",
        expected_route="vision_only",
        validators={
            "parseable": None,
            "matrix_shape": None,
            "binary_values": None,
            "table_consistency": None,
        },
        raw_markdown="text with [VISION_PLACEHOLDER] inside",
    )
    assert "vision_output_placeholder_detected" in flags["warnings"]
