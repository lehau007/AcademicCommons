"""
Reproduce this morning's "constant failures" and separate TWO hypotheses:

  H1 (token/budget): low max_tokens truncates the answer -> deterministic, should
                     fail RIGHT NOW too.
  H2 (provider flakiness): Go plan upstream returns 5xx intermittently -> random,
                           can fail in bursts then recover (explains "morning only").

We use the ACTUAL production strip logic (copied verbatim from
src/backend/app/llm/providers.py) and the ACTUAL production budgets:
  - title path : max_tokens=512   (tutor_service.py:855)
  - eval JSON  : max_tokens=1000  (eval_worker.py:312)
  - answer path: max_tokens=4096  (control — should be healthy)

For each we fire a burst and count: provider errors (5xx = H2), truncated
finish=length, empty-after-strip (H1), and clean successes.

Run:
    .venv/bin/python tests/opencode_prod_repro_test.py
"""

import asyncio
import os
import re
import time
from collections import Counter
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
MODEL = "minimax-m3"

# ---- production strip logic, copied verbatim from providers.py -------------
_THINK_BLOCK_RE = re.compile(r"<think>.*?</think>\s*", re.DOTALL)


def _strip_think_block(content: str) -> str:
    if "<think>" not in content:
        return content
    stripped = _THINK_BLOCK_RE.sub("", content).strip()
    if stripped != content.strip():
        return stripped
    close_idx = content.find("</think>")
    tail = content[close_idx + len("</think>"):].strip() if close_idx >= 0 else ""
    if not tail:
        for opener, closer in (("{", "}"), ("[", "]")):
            start = content.find(opener)
            end = content.rfind(closer)
            if 0 <= start < end:
                tail = content[start:end + 1]
                break
    if tail and tail != content.strip():
        return tail
    return content[:content.find("<think>")].strip()
# ---------------------------------------------------------------------------

SCENARIOS = [
    {"name": "title(512)", "max_tokens": 512, "rf": False,
     "messages": [{"role": "user", "content": "Generate a concise document title (max 8 words) for a lecture on hybrid retrieval in RAG systems. Output only the title."}]},
    {"name": "eval_json(1000)", "max_tokens": 1000, "rf": True,
     "messages": [
         {"role": "system", "content": "You are a strict grader. Output ONLY JSON."},
         {"role": "user", "content": 'Grade this answer for faithfulness 0-1. Answer: "RAG combines retrieval with generation." Return {"score": <float>, "reason": "<short>"}'}]},
    {"name": "answer(4096)", "max_tokens": 4096, "rf": False,
     "messages": [{"role": "user", "content": "Giải thích ngắn gọn context precision trong RAGAS."}]},
]
BURST = 12
CONCURRENCY = 6


async def one(client, sem, sc):
    async with sem:
        t0 = time.perf_counter()
        kwargs = dict(model=MODEL, messages=sc["messages"], max_tokens=sc["max_tokens"], temperature=0.0)
        if sc["rf"]:
            kwargs["response_format"] = {"type": "json_object"}
        try:
            r = await client.chat.completions.create(**kwargs)
        except Exception as e:
            code = getattr(e, "status_code", None)
            klass = "5xx" if (code and 500 <= code < 600) else "4xx" if code else "exc"
            return {"outcome": f"ERROR_{klass}", "detail": f"{code} {str(e)[:60]}",
                    "lat": int((time.perf_counter() - t0) * 1000)}
    lat = int((time.perf_counter() - t0) * 1000)
    raw = r.choices[0].message.content or ""
    final = _strip_think_block(raw).strip()
    if r.choices[0].finish_reason == "length" and not final:
        outcome = "EMPTY_after_strip(H1 token)"
    elif r.choices[0].finish_reason == "length":
        outcome = "TRUNCATED_but_has_text"
    elif not final:
        outcome = "EMPTY(no reason)"
    else:
        outcome = "OK"
    return {"outcome": outcome, "finish": r.choices[0].finish_reason,
            "out_tok": r.usage.completion_tokens, "lat": lat, "preview": final[:50]}


async def main():
    if not API_KEY:
        raise SystemExit("ERROR: OPENCODE_API_KEY not set (tests/.env).")
    print(f"Model={MODEL}  base={BASE_URL}  burst={BURST}/scenario\n")
    client = AsyncOpenAI(api_key=API_KEY, base_url=BASE_URL, timeout=120.0)
    sem = asyncio.Semaphore(CONCURRENCY)

    for sc in SCENARIOS:
        rows = await asyncio.gather(*[one(client, sem, sc) for _ in range(BURST)])
        c = Counter(r["outcome"] for r in rows)
        print(f"=== {sc['name']}  (max_tokens={sc['max_tokens']}) ===")
        for outcome, n in c.most_common():
            print(f"    {outcome:32s} {n}/{BURST}")
        errs = [r for r in rows if r["outcome"].startswith("ERROR")]
        for e in errs[:3]:
            print(f"      err detail: {e['detail']}")
        ok = [r for r in rows if r["outcome"] == "OK"]
        if ok:
            print(f"      sample OK: {ok[0]['preview']!r} (out_tok={ok[0]['out_tok']})")
        print()


if __name__ == "__main__":
    asyncio.run(main())
