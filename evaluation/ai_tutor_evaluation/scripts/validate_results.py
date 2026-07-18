"""Validate externally-judged results before aggregation (replaces the automated judge's trust).

    python validate_results.py --results ../hard/results_agentic_dense \
        --questions ../dataset/questions_hard.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

METRICS = [
    "faithfulness", "answer_relevancy", "answer_correctness",
    "context_precision", "context_recall", "citation_accuracy",
]


def validate(results_dir: Path, expected_qids: set[str]) -> dict:
    found: set[str] = set()
    invalid: list[dict] = []
    for p in sorted(results_dir.glob("*.json")):
        if p.name in {"summary.json"} or p.name.startswith("_"):
            continue
        try:
            r = json.loads(p.read_text())
        except json.JSONDecodeError as exc:
            invalid.append({"qid": p.stem, "problem": f"bad json: {exc}"})
            continue
        if not isinstance(r, dict):
            invalid.append({"qid": p.stem, "problem": "top-level JSON not an object"})
            continue
        qid = r.get("qid", p.stem)
        found.add(qid)
        scores = r.get("scores")
        if not isinstance(scores, dict):
            invalid.append({"qid": qid, "problem": "missing scores object"})
            continue
        problems = []
        for m in METRICS:
            cell = scores.get(m)
            if not isinstance(cell, dict) or "score" not in cell:
                problems.append(f"missing metric {m}")
                continue
            s = cell["score"]
            if not isinstance(s, int) or not (1 <= s <= 5):
                problems.append(f"{m} score out of range: {s!r}")
        if problems:
            invalid.append({"qid": qid, "problem": "; ".join(problems)})
    return {
        "missing_qids": sorted(expected_qids - found),
        "invalid": invalid,
        "ok": len(found) - len({i["qid"] for i in invalid}),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", required=True)
    ap.add_argument("--questions", required=True)
    args = ap.parse_args()
    qids = {q["qid"] for q in json.loads(Path(args.questions).read_text())}
    report = validate(Path(args.results), qids)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if report["missing_qids"] or report["invalid"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
