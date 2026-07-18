from __future__ import annotations

from pathlib import Path

from app.llm.cost_report import aggregate_records, load_records, render_markdown


def test_aggregate_sums_cost_and_tokens_across_field_shapes() -> None:
    records = [
        {"cost_usd": 0.01, "tokens_in": 100, "tokens_out": 20,
         "metadata": {"flow": "tutor", "provider": "gemini"}, "cache_info": {"hit": False}},
        {"usage": {"input_uncached": 30, "input_cached": 10, "output": 5},
         "metadata": {"flow": "tutor", "provider": "gemini"}, "cache_info": {"tier": "semantic", "hit": True}},
        {"cost": 0.02, "prompt_tokens": 200, "completion_tokens": 40,
         "metadata": {"flow": "summarization", "provider": "bedrock"}, "status": "SUCCESS"},
    ]

    report = aggregate_records(records, group_by=("flow", "provider"))

    assert report.total.calls == 3
    assert abs(report.total.cost_usd - 0.03) < 1e-9
    assert report.total.tokens_in == 100 + 40 + 200
    assert report.total.tokens_out == 20 + 5 + 40
    assert report.total.cache_hits == 1

    tutor = next(s for s in report.groups if s.key == ("tutor", "gemini"))
    assert tutor.calls == 2
    assert tutor.cache_hit_rate == 0.5


def test_groups_sorted_by_cost_desc_and_unknown_dimension() -> None:
    records = [
        {"cost_usd": 0.5, "metadata": {"flow": "a"}},
        {"cost_usd": 0.9, "metadata": {"flow": "b"}},
        {"cost_usd": 0.1},  # no flow -> "unknown"
    ]

    report = aggregate_records(records, group_by=("flow",))

    assert [s.key for s in report.groups] == [("b",), ("a",), ("unknown",)]


def test_load_records_skips_blank_and_malformed_lines(tmp_path: Path) -> None:
    log = tmp_path / "optimizer.jsonl"
    log.write_text(
        '{"cost_usd": 0.1}\n'
        "\n"
        "not-json\n"
        '{"cost_usd": 0.2}\n',
        encoding="utf-8",
    )

    records = load_records(log)

    assert len(records) == 2
    assert load_records(tmp_path / "missing.jsonl") == []


def test_render_markdown_includes_header_and_total_row() -> None:
    report = aggregate_records([{"cost_usd": 0.1, "metadata": {"flow": "tutor"}}], group_by=("flow",))

    rendered = render_markdown(report)

    assert "| flow | calls | cost_usd | tokens_in | tokens_out | cache_hit_rate |" in rendered
    assert "TOTAL" in rendered
