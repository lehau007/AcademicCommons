# evaluation/ai_tutor_evaluation/scripts/test_compare_ablation_2x2.py
from __future__ import annotations

import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "compare_ablation_2x2", Path(__file__).with_name("compare_ablation_2x2.py")
)
cmp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cmp)


def _scores(val: int) -> dict:
    return {m: {"score": val} for m in cmp.METRICS}


def test_metric_means_and_overall() -> None:
    scores = {"q1": _scores(4), "q2": _scores(2)}
    means = cmp.metric_means(scores)
    assert means["faithfulness"] == 3.0
    assert means["overall"] == 3.0


def test_by_difficulty_groups() -> None:
    scores = {"q1": _scores(5), "q2": _scores(1)}
    qid_to_type = {"q1": "table", "q2": "graph"}
    grouped = cmp.by_difficulty(scores, qid_to_type)
    assert grouped["table"]["overall"] == 5.0
    assert grouped["graph"]["overall"] == 1.0
