"""Emit one compact markdown per config for in-session single-judge grading.

Keeps the judge's context bounded: question + ground truth + tutor answer + a trimmed,
de-duplicated view of the retrieved context (enough to grade context_precision/recall/
faithfulness). One file holds all N questions so the judge reads it in a single pass.

    python dump_for_judging.py --actual ../full/actual_agentic_dense \
        --questions ../dataset/questions_full.json --config agentic_dense \
        --out ../full/judge_input_agentic_dense.md
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

CTX_CHAR_BUDGET = 1800  # per question, across dedup chunks
CHUNK_CHAR_CAP = 600     # per single chunk


def _context(actual: dict) -> str:
    blocks: list[str] = []
    seen: set[str] = set()
    used = 0
    for call in actual.get("retrieval_calls", []):
        for ch in call.get("chunks", []):
            c = (ch.get("content") or "").strip()
            if not c or c in seen:
                continue
            seen.add(c)
            snippet = c[:CHUNK_CHAR_CAP] + ("…" if len(c) > CHUNK_CHAR_CAP else "")
            if used + len(snippet) > CTX_CHAR_BUDGET and blocks:
                blocks.append(f"- …(+{len(seen)} more chunks, trimmed)")
                return "\n".join(blocks)
            blocks.append(f"- {snippet}")
            used += len(snippet)
    return "\n".join(blocks) if blocks else "(no chunks retrieved)"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--actual", required=True)
    ap.add_argument("--questions", required=True)
    ap.add_argument("--config", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    gt = {q["qid"]: q for q in json.loads(Path(args.questions).read_text())}
    actual_dir = Path(args.actual)
    parts: list[str] = [
        f"# Judge input — config `{args.config}` ({actual_dir.name})\n",
        "Grade every question below on the 6 RAGAS metrics (1–5) per metrics/rubric.md. "
        "Score ONLY from the ground truth + retrieved context + answer shown here.\n",
    ]
    n = 0
    for p in sorted(actual_dir.glob("*.json")):
        if p.name.startswith("_") or p.name == "summary.json":
            continue
        a = json.loads(p.read_text())
        qid = a.get("qid", p.stem)
        q = gt.get(qid, {})
        n += 1
        parts.append(
            f"\n---\n\n## {qid}  ·  {a.get('course_code','?')}  ·  {q.get('difficulty_type','?')}\n\n"
            f"**Q:** {a.get('question','')}\n\n"
            f"**Ground truth:** {q.get('ground_truth','')}\n\n"
            f"**Retrieved context (trimmed):**\n{_context(a)}\n\n"
            f"**Tutor answer:** {a.get('answer','')}\n\n"
            f"**Citations:** {len(a.get('citations',[]))} doc(s)\n"
        )
    Path(args.out).write_text("".join(parts), encoding="utf-8")
    print(f"wrote {n} questions to {args.out} ({Path(args.out).stat().st_size} bytes)")


if __name__ == "__main__":
    main()
