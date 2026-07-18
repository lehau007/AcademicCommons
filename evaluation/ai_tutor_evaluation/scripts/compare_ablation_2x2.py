"""2x2 (retrieval x pipeline) ablation comparison.

Reads the four <dir>/results_<config> dirs, prints per-metric means + overall with deltas vs
agentic_dense, plus a per-difficulty_type breakdown. Writes <dir>/report.md.

    python compare_ablation_2x2.py                 # hard set (default)
    python compare_ablation_2x2.py --dir full --questions dataset/questions_full.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HARD = ROOT / "hard"

METRICS = [
    "faithfulness", "answer_relevancy", "answer_correctness",
    "context_precision", "context_recall", "citation_accuracy",
]

# (label, config id) — config id names both results_<id> and actual_<id>
CONFIGS = [
    ("Agentic + Dense (baseline)", "agentic_dense"),
    ("Agentic + Hybrid", "agentic_hybrid"),
    ("Traditional + Dense", "traditional_dense"),
    ("Traditional + Hybrid", "traditional_hybrid"),
]


def load_scores(results_dir: Path) -> dict[str, dict]:
    out = {}
    for p in results_dir.glob("*.json"):
        if p.name == "summary.json" or p.name.startswith("_"):
            continue
        r = json.loads(p.read_text())
        out[r.get("qid", p.stem)] = r["scores"]
    return out


def metric_means(scores: dict[str, dict]) -> dict[str, float]:
    res = {}
    for m in METRICS:
        vals = [s[m]["score"] for s in scores.values() if s.get(m) is not None]
        res[m] = round(sum(vals) / len(vals), 2) if vals else float("nan")
    allv = [s[m]["score"] for s in scores.values() for m in METRICS if s.get(m) is not None]
    res["overall"] = round(sum(allv) / len(allv), 2) if allv else float("nan")
    return res


def by_difficulty(scores: dict[str, dict], qid_to_type: dict[str, str]) -> dict[str, dict]:
    groups: dict[str, dict[str, dict]] = {}
    for qid, s in scores.items():
        groups.setdefault(qid_to_type.get(qid, "unknown"), {})[qid] = s
    return {t: metric_means(g) for t, g in groups.items()}


def render(root: Path, sub: str, questions_file: str) -> str:
    questions = json.loads((root / questions_file).read_text())
    qid_to_type = {q["qid"]: q.get("difficulty_type", "unknown") for q in questions}
    hard = root / sub

    lines: list[str] = [f"# AI Tutor Ablation — 2x2 ({sub} set)\n"]
    cols = METRICS + ["overall"]
    lines.append("## Grid (Δ vs Agentic+Dense)\n")
    lines.append("| Config | n | " + " | ".join(c.replace("_", " ") for c in cols) + " |")
    lines.append("|" + "---|" * (len(cols) + 2))

    baseline = None
    means_by_cfg = {}
    for label, cfg in CONFIGS:
        rdir = hard / f"results_{cfg}"
        if not rdir.exists():
            lines.append(f"| {label} | 0 | " + " | ".join(["—"] * len(cols)) + " |")
            continue
        scores = load_scores(rdir)
        means = metric_means(scores)
        means_by_cfg[cfg] = (scores, means)
        if baseline is None:
            baseline = means
        cells = []
        for m in cols:
            v = means[m]
            if baseline and cfg != CONFIGS[0][1]:
                cells.append(f"{v:.2f} ({v - baseline[m]:+.2f})")
            else:
                cells.append(f"{v:.2f}")
        lines.append(f"| {label} | {len(scores)} | " + " | ".join(cells) + " |")

    lines.append("\n## By difficulty type (overall score)\n")
    types = sorted({t for t in qid_to_type.values()})
    lines.append("| Config | " + " | ".join(types) + " |")
    lines.append("|" + "---|" * (len(types) + 1))
    for label, cfg in CONFIGS:
        if cfg not in means_by_cfg:
            continue
        scores, _ = means_by_cfg[cfg]
        grouped = by_difficulty(scores, qid_to_type)
        cells = [f"{grouped[t]['overall']:.2f}" if t in grouped else "—" for t in types]
        lines.append(f"| {label} | " + " | ".join(cells) + " |")

    judges = sorted({
        json.loads(p.read_text()).get("judge_model", "?")
        for cfg in (c for _, c in CONFIGS) if (hard / f"results_{cfg}").exists()
        for p in (hard / f"results_{cfg}").glob("*.json") if p.name != "summary.json"
    })
    lines.append(
        f"\n_Judge: {', '.join(judges) or 'n/a'} (single judge across all configs for a valid "
        "comparison; OpenRouter expired). Generation: OpenCode/Groq. Retrieval: NVIDIA embed + "
        "rerank. Hybrid = dense+BM25 RRF -> rerank (production-faithful). Historical 50-Q run "
        "not included._\n"
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default="hard", help="results subdir (hard | full)")
    parser.add_argument("--questions", default="dataset/questions_hard.json",
                        help="questions file (relative to eval root) for difficulty buckets")
    args = parser.parse_args()

    report = render(ROOT, args.dir, args.questions)
    print(report)
    out = ROOT / args.dir
    out.mkdir(parents=True, exist_ok=True)
    (out / "report.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
