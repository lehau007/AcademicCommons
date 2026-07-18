"""Score tutor answers via OpenRouter: one API call = one metric of one question.

Runs INSIDE the `api` container (uses its OPENROUTER_API_KEY):

    docker exec graduationthesis-api-1 python /tmp/tutor_eval/scripts/judge.py \
        --questions /tmp/tutor_eval/dataset/questions.json \
        --actual /tmp/tutor_eval/actual \
        --rubric /tmp/tutor_eval/metrics/rubric.md \
        --out /tmp/tutor_eval/results \
        [--model anthropic/claude-sonnet-4.5] [--concurrency 8] [--only qid,...]

50 questions x 6 metrics = 300 calls, bounded by a semaphore. Resumable: metrics already
present (non-null) in results/<qid>.json are skipped. A metric that still fails after
3 retries is recorded as null and excluded from aggregation.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import random
import re
from pathlib import Path

import httpx

METRICS = [
    "faithfulness",
    "answer_relevancy",
    "answer_correctness",
    "context_precision",
    "context_recall",
    "citation_accuracy",
]
MAX_CHUNK_CHARS = 3000
SYSTEM_PROMPT = (
    "You are a strict, impartial evaluator for a RAG-based AI tutor. Score exactly ONE "
    "metric according to the rubric excerpt provided. Respond with strict JSON only — "
    '{"score": <integer 1-5>, "justification": "<1-2 sentences>", "evidence": ["<short '
    'quoted strings>"]} — no markdown fences, no extra keys, no prose outside the JSON.'
)


def parse_rubric(rubric_text: str) -> tuple[dict[str, str], str]:
    """Return ({metric_key: section_text}, anchors_text) from metrics/rubric.md."""
    sections: dict[str, str] = {}
    for m in re.finditer(r"^### .*?\(`([a-z_]+)`\)\n(.*?)(?=^### |^## )", rubric_text,
                         re.M | re.S):
        sections[m.group(1)] = m.group(0).strip()
    anchors = re.search(r"^## Scale anchors.*?(?=^## )", rubric_text, re.M | re.S)
    if not anchors or set(sections) != set(METRICS):
        missing = set(METRICS) - set(sections)
        raise SystemExit(f"rubric parse failed; missing metrics: {missing or 'anchors'}")
    return sections, anchors.group(0).strip()


def dedupe_chunks(actual: dict) -> list[dict]:
    seen: dict[str, dict] = {}
    for call in actual.get("retrieval_calls", []):
        for ch in call["chunks"]:
            prev = seen.get(ch["chunk_id"])
            if prev is None or ch["final_score"] > prev["final_score"]:
                seen[ch["chunk_id"]] = ch
    return sorted(seen.values(), key=lambda c: c["final_score"], reverse=True)


def build_prompt(metric_section: str, anchors: str, q: dict, actual: dict) -> str:
    chunks = dedupe_chunks(actual)
    chunk_lines = [
        f"[chunk_id={c['chunk_id']} section={c['section_title']!r} "
        f"score={c['final_score']}]\n{c['content'][:MAX_CHUNK_CHARS]}"
        for c in chunks
    ] or ["(no chunks retrieved)"]
    citations = [
        {k: c.get(k) for k in ("chunk_id", "document_title", "section_title", "excerpt")}
        for c in actual.get("citations", [])
    ]
    return "\n\n".join([
        f"# Metric to score\n{metric_section}",
        f"# {anchors}",
        f"# Question\n{q['question']}",
        f"# Ground-truth answer\n{q['ground_truth']}",
        f"# Tutor's answer\n{actual['answer']}",
        f"# Citations attached to the answer\n{json.dumps(citations, ensure_ascii=False, indent=1)}",
        "# All retrieved chunks\n" + "\n\n---\n\n".join(chunk_lines),
    ])


def extract_json(text: str) -> dict:
    text = text.strip()
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end <= start:
        raise ValueError(f"no JSON object in: {text[:200]!r}")
    obj = json.loads(text[start:end + 1])
    score = obj.get("score")
    if not isinstance(score, int) or not 1 <= score <= 5:
        raise ValueError(f"bad score: {score!r}")
    return {
        "score": score,
        "justification": str(obj.get("justification", "")),
        "evidence": [str(e) for e in obj.get("evidence", [])],
    }


async def judge_one(client: httpx.AsyncClient, sem: asyncio.Semaphore, model: str,
                    prompt: str) -> dict | None:
    async with sem:
        for attempt in range(3):
            try:
                resp = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    json={
                        "model": model,
                        "temperature": 0,
                        "max_tokens": 1024,
                        "messages": [
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": prompt},
                        ],
                    },
                    timeout=120,
                )
                resp.raise_for_status()
                content = resp.json()["choices"][0]["message"]["content"]
                return extract_json(content)
            except Exception as exc:  # noqa: BLE001 - retry then record null
                wait = 2 ** (attempt + 1) + random.random()
                print(f"  retry {attempt + 1} after error: {exc}")
                await asyncio.sleep(wait)
    return None


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--questions", required=True)
    parser.add_argument("--actual", required=True)
    parser.add_argument("--rubric", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--model", default="anthropic/claude-sonnet-4.5")
    parser.add_argument("--concurrency", type=int, default=8)
    parser.add_argument("--only", help="comma-separated qids")
    args = parser.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise SystemExit("OPENROUTER_API_KEY not set")

    sections, anchors = parse_rubric(Path(args.rubric).read_text())
    questions = {q["qid"]: q for q in json.loads(Path(args.questions).read_text())}
    if args.only:
        wanted = set(args.only.split(","))
        questions = {k: v for k, v in questions.items() if k in wanted}
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    results: dict[str, dict] = {}
    todo: list[tuple[str, str]] = []
    for qid, q in questions.items():
        actual_path = Path(args.actual) / f"{qid}.json"
        if not actual_path.exists():
            print(f"skip {qid}: no actual output")
            continue
        res_path = out_dir / f"{qid}.json"
        if res_path.exists():
            results[qid] = json.loads(res_path.read_text())
        else:
            results[qid] = {
                "qid": qid, "course_code": q["course_code"], "judge_model": args.model,
                "scores": {m: None for m in METRICS},
            }
        for m in METRICS:
            if results[qid]["scores"].get(m) is None:
                todo.append((qid, m))

    print(f"{len(todo)} judge calls to make")
    sem = asyncio.Semaphore(args.concurrency)
    lock = asyncio.Lock()

    async with httpx.AsyncClient(headers={"Authorization": f"Bearer {api_key}"}) as client:
        async def run(qid: str, metric: str) -> None:
            actual = json.loads((Path(args.actual) / f"{qid}.json").read_text())
            prompt = build_prompt(sections[metric], anchors, questions[qid], actual)
            verdict = await judge_one(client, sem, args.model, prompt)
            async with lock:
                results[qid]["scores"][metric] = verdict
                (out_dir / f"{qid}.json").write_text(
                    json.dumps(results[qid], indent=2, ensure_ascii=False)
                )
            print(f"{'ok  ' if verdict else 'NULL'} {qid} {metric}"
                  + (f" -> {verdict['score']}" if verdict else ""))

        await asyncio.gather(*(run(qid, m) for qid, m in todo))

    nulls = [(qid, m) for qid, r in results.items()
             for m, v in r["scores"].items() if v is None]
    print(f"done; null cells: {nulls or 'none'}")


if __name__ == "__main__":
    asyncio.run(main())
