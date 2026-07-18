"""
Compare "format health" of OpenCode Go-plan models against the same prompts.

Motivation: `minimax-m3` keeps producing broken/truncated output during real use
(emits a `<think>...</think>` reasoning block every turn that eats max_tokens →
truncated answers, empty titles). Question: is this a MiniMax-specific quirk, or
does the whole Go plan (opencode) degrade the raw API? Test a few peers.

For each model x each prompt, we measure:
  - empty        : content is None / whitespace only
  - has_think    : output contains a <think> reasoning block
  - truncated    : finish_reason == "length" (ran out of budget)
  - leftover_tag : an UNCLOSED/leftover <think> tag survives into the answer
  - error        : API-level error (status code / message)
  - latency, out_tokens

Run:
    .venv/bin/python tests/opencode_format_compare_test.py
"""

import asyncio
import os
import re
import time
from pathlib import Path

from openai import AsyncOpenAI


def _load_local_env() -> None:
    env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        value = value.split(" #", 1)[0].strip().strip('"').strip("'")
        os.environ.setdefault(key.strip(), value)


_load_local_env()

API_KEY = os.environ.get("OPENCODE_API_KEY", "")
BASE_URL = os.environ.get("OPENCODE_BASE_URL", "https://opencode.ai/zen/go/v1")

# Peers to compare against the minimax-m3 baseline.
MODELS = [
    "minimax-m3",       # baseline (the one that keeps breaking)
    "glm-5.2",
    "kimi-k2.7-code",
    "kimi-k2.5",
    "qwen3.7-max",
    "deepseek-v4-pro",  # extra data point
]

# Prompts chosen to resemble real "defense" usage: short-answer + a strict
# format instruction (the kind of thing that exposes <think>/truncation bugs).
PROMPTS = [
    {
        "name": "short_answer",
        "max_tokens": 120,
        "messages": [
            {"role": "user", "content": "Trả lời NGẮN GỌN trong 1 câu: RAG là gì?"},
        ],
    },
    {
        "name": "strict_json_title",
        "max_tokens": 120,
        "messages": [
            {
                "role": "system",
                "content": "You output ONLY valid JSON, no prose, no markdown fences.",
            },
            {
                "role": "user",
                "content": 'Generate a title for a document about vector databases. '
                'Respond exactly as: {"title": "..."}',
            },
        ],
    },
    {
        "name": "vietnamese_2sent",
        "max_tokens": 200,
        "messages": [
            {"role": "system", "content": "Bạn là trợ lý trả lời bằng tiếng Việt."},
            {"role": "user", "content": "Giải thích context precision trong RAGAS trong đúng 2 câu."},
        ],
    },
]

THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL)
OPEN_THINK_RE = re.compile(r"</?think>")


async def run_one(client: AsyncOpenAI, model: str, prompt: dict) -> dict:
    row = {"model": model, "prompt": prompt["name"]}
    t0 = time.perf_counter()
    try:
        resp = await client.chat.completions.create(
            model=model,
            messages=prompt["messages"],
            max_tokens=prompt["max_tokens"],
            temperature=0.2,
        )
    except Exception as e:  # noqa: BLE001 - we want to catalog every failure mode
        row["error"] = f"{type(e).__name__}: {str(e)[:120]}"
        row["latency_ms"] = int((time.perf_counter() - t0) * 1000)
        return row

    row["latency_ms"] = int((time.perf_counter() - t0) * 1000)
    choice = resp.choices[0]
    content = choice.message.content or ""
    row["finish"] = choice.finish_reason
    row["out_tok"] = getattr(resp.usage, "completion_tokens", None)
    row["empty"] = not content.strip()
    row["has_think"] = bool(THINK_RE.search(content))
    stripped = THINK_RE.sub("", content)
    row["leftover_tag"] = bool(OPEN_THINK_RE.search(stripped))
    row["truncated"] = choice.finish_reason == "length"
    row["preview"] = re.sub(r"\s+", " ", content.strip())[:80]
    return row


async def main() -> None:
    if not API_KEY:
        raise SystemExit("ERROR: OPENCODE_API_KEY not set (tests/.env).")
    print(f"Base URL : {BASE_URL}")
    print(f"Models   : {', '.join(MODELS)}\n")

    client = AsyncOpenAI(api_key=API_KEY, base_url=BASE_URL, timeout=60.0)
    rows = []
    for model in MODELS:
        for prompt in PROMPTS:
            row = await run_one(client, model, prompt)
            rows.append(row)
            flags = []
            if row.get("error"):
                flags.append("ERROR")
            if row.get("empty"):
                flags.append("EMPTY")
            if row.get("has_think"):
                flags.append("THINK")
            if row.get("leftover_tag"):
                flags.append("LEFTOVER<think>")
            if row.get("truncated"):
                flags.append("TRUNCATED")
            status = ",".join(flags) if flags else "ok"
            print(f"[{model:16s}] {row['prompt']:18s} -> {status}")
            if row.get("error"):
                print(f"    err: {row['error']}")
            else:
                print(f"    finish={row.get('finish')} out_tok={row.get('out_tok')} "
                      f"lat={row['latency_ms']}ms")
                print(f"    preview: {row.get('preview')}")
        print()

    # summary
    print("=" * 70)
    print("SUMMARY (per model: #ok / #prompts, and dominant failure)")
    print("=" * 70)
    for model in MODELS:
        mrows = [r for r in rows if r["model"] == model]
        ok = sum(1 for r in mrows if not any(
            r.get(k) for k in ("error", "empty", "leftover_tag", "truncated")))
        issues = []
        for k, label in [("error", "err"), ("empty", "empty"),
                         ("has_think", "think"), ("leftover_tag", "leftover"),
                         ("truncated", "trunc")]:
            c = sum(1 for r in mrows if r.get(k))
            if c:
                issues.append(f"{label}={c}")
        print(f"  {model:16s} clean={ok}/{len(mrows)}  {' '.join(issues) or 'no issues'}")


if __name__ == "__main__":
    asyncio.run(main())
