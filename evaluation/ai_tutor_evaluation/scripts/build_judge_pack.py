"""Build an OpenRouter-free judge prompt-pack for one ablation config.

The RAGAS judge used to call OpenRouter; that key is expired. Instead, this emits a
self-contained folder an external agentic coding tool (opencode / gemini-cli / Claude) reads
to produce results_<config>/<qid>.json (the six-metric schema aggregate.py already consumes).

    python build_judge_pack.py --actual ../hard/actual_agentic_dense \
        --questions ../dataset/questions_hard.json --rubric ../metrics/rubric.md \
        --out ../hard/judge_pack_agentic_dense --config agentic_dense
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

METRICS = [
    "faithfulness", "answer_relevancy", "answer_correctness",
    "context_precision", "context_recall", "citation_accuracy",
]

_SCHEMA = {
    "type": "object",
    "properties": {
        "qid": {"type": "string"},
        "scores": {
            "type": "object",
            "properties": {
                m: {
                    "type": "object",
                    "properties": {
                        "score": {"type": "integer", "minimum": 1, "maximum": 5},
                        "reason": {"type": "string"},
                    },
                    "required": ["score", "reason"],
                }
                for m in METRICS
            },
            "required": METRICS,
        },
    },
    "required": ["qid", "scores"],
}


def _bundle_md(actual: dict, ground_truth: str) -> str:
    ctx_blocks = []
    seen = set()
    for call in actual.get("retrieval_calls", []):
        for ch in call.get("chunks", []):
            c = ch.get("content", "")
            if c and c not in seen:
                seen.add(c)
                ctx_blocks.append(f"- {c}")
    ctx = "\n".join(ctx_blocks) if ctx_blocks else "(no chunks retrieved)"
    cites = json.dumps(actual.get("citations", []), ensure_ascii=False, indent=2)
    return (
        f"# {actual.get('qid')}\n\n"
        f"## Question\n{actual.get('question', '')}\n\n"
        f"## Ground truth\n{ground_truth}\n\n"
        f"## Retrieved context (what the tutor saw)\n{ctx}\n\n"
        f"## Tutor answer\n{actual.get('answer', '')}\n\n"
        f"## Citations\n```json\n{cites}\n```\n"
    )


def _instructions_md(config: str) -> str:
    return (
        f"# Judge instructions — config `{config}`\n\n"
        "You are an impartial RAGAS-style grader. For EACH `<qid>.md` bundle in this folder:\n"
        "1. Read `rubric.md` for the six metrics and their 1–5 anchors.\n"
        "2. Score the tutor answer against the ground truth and the retrieved context.\n"
        f"3. Write `../results_{config}/<qid>.json` matching `schema.json` exactly: a `qid`\n"
        "   and a `scores` object with all six metrics, each `{\"score\": 1-5, \"reason\": \"...\"}`.\n\n"
        "Rules: score only from the bundle; never invent facts; if the answer says the\n"
        "materials do not cover the question AND the ground truth is absent from the retrieved\n"
        "context, that is faithful (do not penalise faithfulness). Output valid JSON only.\n"
    )


def build_pack(actual_dir: Path, questions: list[dict], rubric_text: str,
               out_dir: Path, config: str) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "INSTRUCTIONS.md").write_text(_instructions_md(config), encoding="utf-8")
    (out_dir / "rubric.md").write_text(rubric_text, encoding="utf-8")
    (out_dir / "schema.json").write_text(json.dumps(_SCHEMA, indent=2), encoding="utf-8")
    gt = {q["qid"]: q.get("ground_truth", "") for q in questions}
    n = 0
    for p in sorted(actual_dir.glob("*.json")):
        if p.name.startswith("_"):
            continue
        actual = json.loads(p.read_text())
        qid = actual.get("qid", p.stem)
        (out_dir / f"{qid}.md").write_text(_bundle_md(actual, gt.get(qid, "")), encoding="utf-8")
        n += 1
    return n


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--actual", required=True)
    ap.add_argument("--questions", required=True)
    ap.add_argument("--rubric", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    questions = json.loads(Path(args.questions).read_text())
    rubric = Path(args.rubric).read_text()
    n = build_pack(Path(args.actual), questions, rubric, Path(args.out), args.config)
    print(f"wrote {n} bundles to {args.out}")


if __name__ == "__main__":
    main()
