"""Aggregate results/<qid>.json into results/summary.json (+ markdown table on stdout).

Pure stdlib; run from anywhere:

    python evaluation/ai_tutor_evaluation/scripts/aggregate.py \
        --results evaluation/ai_tutor_evaluation/results \
        --questions evaluation/ai_tutor_evaluation/dataset/questions.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

METRICS = [
    "faithfulness",
    "answer_relevancy",
    "answer_correctness",
    "context_precision",
    "context_recall",
    "citation_accuracy",
]


def stats(values: list[int]) -> dict | None:
    if not values:
        return None
    return {
        "mean": round(sum(values) / len(values), 2),
        "min": min(values),
        "max": max(values),
        "n": len(values),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", required=True)
    parser.add_argument("--questions", required=True)
    args = parser.parse_args()

    results_dir = Path(args.results)
    questions = {q["qid"]: q for q in json.loads(Path(args.questions).read_text())}
    rows = []
    for path in sorted(results_dir.glob("*.json")):
        if path.name == "summary.json":
            continue
        r = json.loads(path.read_text())
        if r.get("qid") in questions:
            rows.append(r)

    def collect(subset: list[dict]) -> dict:
        out = {}
        for m in METRICS:
            vals = [r["scores"][m]["score"] for r in subset
                    if r["scores"].get(m) is not None]
            out[m] = stats(vals)
        all_vals = [r["scores"][m]["score"] for r in subset for m in METRICS
                    if r["scores"].get(m) is not None]
        out["overall"] = stats(all_vals)
        return out

    courses = sorted({r["course_code"] for r in rows})
    summary = {
        "n_questions": len(rows),
        "judge_model": rows[0]["judge_model"] if rows else None,
        "per_metric": collect(rows),
        "per_course": {c: collect([r for r in rows if r["course_code"] == c])
                       for c in courses},
        "null_cells": [
            {"qid": r["qid"], "metric": m}
            for r in rows for m in METRICS if r["scores"].get(m) is None
        ],
        "per_question": {
            r["qid"]: {m: (r["scores"][m]["score"] if r["scores"].get(m) else None)
                       for m in METRICS}
            for r in rows
        },
    }
    out_path = results_dir / "summary.json"
    out_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"wrote {out_path}\n")

    header = "| qid | " + " | ".join(m[:12] for m in METRICS) + " |"
    print(header)
    print("|" + "---|" * (len(METRICS) + 1))
    for r in rows:
        cells = [str(r["scores"][m]["score"]) if r["scores"].get(m) else "–"
                 for m in METRICS]
        print(f"| {r['qid']} | " + " | ".join(cells) + " |")
    pm = summary["per_metric"]
    means = [str(pm[m]["mean"]) if pm[m] else "–" for m in METRICS]
    print(f"| **mean** | " + " | ".join(f"**{v}**" for v in means) + " |")


if __name__ == "__main__":
    main()
