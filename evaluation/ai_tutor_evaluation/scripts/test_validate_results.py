from __future__ import annotations

import json
from pathlib import Path

import importlib.util

_spec = importlib.util.spec_from_file_location(
    "validate_results", Path(__file__).with_name("validate_results.py")
)
vr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(vr)

_GOOD = {"qid": "q1", "scores": {m: {"score": 4, "reason": "ok"} for m in vr.METRICS}}


def test_valid_results_pass(tmp_path: Path) -> None:
    (tmp_path / "q1.json").write_text(json.dumps(_GOOD))
    report = vr.validate(tmp_path, {"q1"})
    assert report["missing_qids"] == []
    assert report["invalid"] == []
    assert report["ok"] == 1


def test_detects_missing_and_invalid(tmp_path: Path) -> None:
    bad = {"qid": "q2", "scores": {"faithfulness": {"score": 9, "reason": "x"}}}
    (tmp_path / "q2.json").write_text(json.dumps(bad))
    report = vr.validate(tmp_path, {"q1", "q2"})
    assert "q1" in report["missing_qids"]
    assert any(item["qid"] == "q2" for item in report["invalid"])  # missing metrics + out-of-range


def test_non_dict_json_recorded_invalid(tmp_path: Path) -> None:
    (tmp_path / "q3.json").write_text("[1, 2, 3]")
    report = vr.validate(tmp_path, {"q3"})
    assert any(item["qid"] == "q3" for item in report["invalid"])
