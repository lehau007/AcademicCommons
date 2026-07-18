"""Build the retrieval-source ablation comparison table.

Reads the three judged result dirs and prints per-metric means + overall, with deltas
vs the dense+rerank baseline. Also emits retrieval-diagnostic columns (avg chunks/q,
questions with 0 chunks) computed from the matching actual/ dir.

    python evaluation/ai_tutor_evaluation/scripts/compare_ablation.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUESTIONS = json.loads((ROOT / "dataset" / "questions.json").read_text())
QIDS = {q["qid"] for q in QUESTIONS}

METRICS = [
    "faithfulness", "answer_relevancy", "answer_correctness",
    "context_precision", "context_recall", "citation_accuracy",
]

# label -> (results_dir, actual_dir)
CONFIGS = [
    ("Dense + Rerank (baseline)", "results", "actual"),
    ("BM25 + Rerank", "results_bm25_rerank", "actual_bm25_rerank"),
    ("Dense+BM25 hybrid, no rerank", "results_hybrid_norerank", "actual_hybrid_norerank"),
]


def load_scores(results_dir: Path) -> dict[str, dict]:
    out = {}
    for p in results_dir.glob("*.json"):
        if p.name == "summary.json":
            continue
        r = json.loads(p.read_text())
        if r.get("qid") in QIDS:
            out[r["qid"]] = r["scores"]
    return out


def metric_means(scores: dict[str, dict]) -> dict[str, float]:
    res = {}
    for m in METRICS:
        vals = [s[m]["score"] for s in scores.values() if s.get(m) is not None]
        res[m] = round(sum(vals) / len(vals), 2) if vals else float("nan")
    allv = [s[m]["score"] for s in scores.values() for m in METRICS if s.get(m) is not None]
    res["overall"] = round(sum(allv) / len(allv), 2) if allv else float("nan")
    return res


def retrieval_diag(actual_dir: Path) -> tuple[float, int]:
    """avg unique chunks retrieved per question, and #questions with 0 chunks."""
    per_q, zero = [], 0
    for qid in QIDS:
        p = actual_dir / f"{qid}.json"
        if not p.exists():
            continue
        d = json.loads(p.read_text())
        ids = set()
        for call in d.get("retrieval_calls", []):
            for ch in call["chunks"]:
                ids.add(ch["chunk_id"])
        per_q.append(len(ids))
        if len(ids) == 0:
            zero += 1
    avg = round(sum(per_q) / len(per_q), 2) if per_q else float("nan")
    return avg, zero


def main() -> None:
    rows = []
    baseline = None
    for label, rdir, adir in CONFIGS:
        rp, ap = ROOT / rdir, ROOT / adir
        if not rp.exists():
            print(f"[skip] {label}: {rdir} not found yet")
            continue
        scores = load_scores(rp)
        means = metric_means(scores)
        avg_chunks, zero = retrieval_diag(ap) if ap.exists() else (float("nan"), -1)
        rows.append((label, means, len(scores), avg_chunks, zero))
        if baseline is None:
            baseline = means

    cols = METRICS + ["overall"]
    header = "| Config | n | " + " | ".join(m.replace("_", " ") for m in cols) + " | avg chunks/q | q w/ 0 chunks |"
    sep = "|" + "---|" * (len(cols) + 4)
    print("\n### Retrieval-source ablation (judge: claude-sonnet-4.5, 50 Q)\n")
    print(header)
    print(sep)
    for label, means, n, avg_chunks, zero in rows:
        cells = []
        for m in cols:
            v = means[m]
            if baseline and label != rows[0][0]:
                d = round(v - baseline[m], 2)
                cells.append(f"{v:.2f} ({d:+.2f})")
            else:
                cells.append(f"{v:.2f}")
        print(f"| {label} | {n} | " + " | ".join(cells) + f" | {avg_chunks} | {zero} |")
    print("\n(Δ vs Dense+Rerank baseline in parentheses.)")


if __name__ == "__main__":
    main()
