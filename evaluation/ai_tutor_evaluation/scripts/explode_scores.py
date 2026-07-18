"""Explode a single judge-scores file into per-qid results JSON the compare/validate scripts read.

The in-session judge writes full/scores_<config>.json:
    { "<qid>": { "faithfulness": {"score": 5, "justification": "..."}, ... }, ... }

This writes full/results_<config>/<qid>.json with the {qid, course_code, judge_model, scores}
schema, stamping judge_model uniformly.

    python explode_scores.py --scores ../full/scores_agentic_dense.json \
        --actual ../full/actual_agentic_dense --out ../full/results_agentic_dense \
        --judge "claude-opus-4-8 (in-session RAGAS judge)"
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

METRICS = [
    "faithfulness", "answer_relevancy", "answer_correctness",
    "context_precision", "context_recall", "citation_accuracy",
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scores", required=True)
    ap.add_argument("--actual", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--judge", required=True)
    args = ap.parse_args()

    scores = json.loads(Path(args.scores).read_text())
    course_of = {}
    for p in Path(args.actual).glob("*.json"):
        if p.name.startswith("_"):
            continue
        a = json.loads(p.read_text())
        course_of[a.get("qid", p.stem)] = a.get("course_code", "?")

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    written = 0
    problems = []
    for qid, sc in scores.items():
        missing = [m for m in METRICS if m not in sc or "score" not in sc[m]]
        if missing:
            problems.append(f"{qid}: missing {missing}")
            continue
        (out_dir / f"{qid}.json").write_text(json.dumps({
            "qid": qid,
            "course_code": course_of.get(qid, "?"),
            "judge_model": args.judge,
            "scores": sc,
        }, indent=2, ensure_ascii=False), encoding="utf-8")
        written += 1
    print(f"wrote {written} results to {out_dir}; problems: {problems or 'none'}")


if __name__ == "__main__":
    main()
