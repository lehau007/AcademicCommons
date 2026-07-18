"""
30-call robustness test for minimax-m3 on the OpenCode Go plan with a huge budget.

Goal: with max_tokens removed as a factor (40000), does minimax-m3 CONSISTENTLY
obey forced formats across many calls, or does it occasionally throw format away?

30 calls, cycling 3 format contracts (10 each):
  - json_mode    : response_format=json_object, must json.loads
  - hard_template: ANSWER:/CONFIDENCE: two lines exactly
  - exact_count  : exactly 3 bullets

Per call we track (after stripping <think>):
  - format_ok      : contract satisfied
  - raw_parse_ok   : (json_mode only) does json.loads succeed WITHOUT stripping <think>?
                     -> models the naive app that doesn't strip -> shows real breakage
  - think_leaked   : <think> present in raw content
  - truncated      : finish_reason == length (should be ~never at 40000)
  - out_tok, latency

Run:
    .venv/bin/python tests/opencode_robustness_test.py
"""

import asyncio
import json
import os
import re
import time
from collections import defaultdict
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
MODEL = os.environ.get("ROBUSTNESS_MODEL", "minimax-m3")
MAX_TOKENS = 40000
N_CALLS = 30
CONCURRENCY = 5

THINK_RE = re.compile(r"<think>.*?</think>\s*", re.DOTALL)
FENCE_RE = re.compile(r"^```(?:json)?\s*|\s*```$", re.MULTILINE)


def strip_reasoning(raw: str) -> str:
    return THINK_RE.sub("", raw or "").strip()


def json_ok(text: str) -> bool:
    body = FENCE_RE.sub("", text).strip()
    try:
        json.loads(body)
        return True
    except Exception:
        return False


def template_ok(text: str) -> bool:
    lines = [l for l in text.splitlines() if l.strip()]
    has_a = any(re.match(r"\s*ANSWER:", l) for l in lines)
    has_c = any(re.match(r"\s*CONFIDENCE:", l) for l in lines)
    extra = [l for l in lines if not re.match(r"\s*(ANSWER|CONFIDENCE):", l)]
    return has_a and has_c and not extra


def count_ok(text: str) -> bool:
    bullets = re.findall(r"^\s*(?:[-*•]|\d+[.)])\s+\S", text, re.MULTILINE)
    lines = [l for l in text.splitlines() if l.strip()]
    non_bullet = [l for l in lines if not re.match(r"^\s*(?:[-*•]|\d+[.)])\s+", l)]
    return len(bullets) == 3 and not non_bullet


CONTRACTS = {
    "json_mode": {
        "rf": True,
        "messages": [
            {"role": "system", "content": "Output ONLY a valid JSON object. No prose, no fences."},
            {"role": "user", "content": 'Return the capital of France as {"capital":"..."}'},
        ],
        "score": json_ok,
    },
    "hard_template": {
        "rf": False,
        "messages": [
            {"role": "user", "content": (
                "What is 17 * 3? Answer EXACTLY in this format and nothing else:\n"
                "ANSWER: <the number>\nCONFIDENCE: <0-1>"
            )},
        ],
        "score": template_ok,
    },
    "exact_count": {
        "rf": False,
        "messages": [
            {"role": "user", "content": (
                "List EXACTLY 3 benefits of RAG. Output only 3 bullet points "
                "starting with '- ', no intro, no conclusion."
            )},
        ],
        "score": count_ok,
    },
}

ORDER = ["json_mode", "hard_template", "exact_count"]


async def one_call(client, sem, idx, cname):
    contract = CONTRACTS[cname]
    kwargs = dict(model=MODEL, messages=contract["messages"],
                  max_tokens=MAX_TOKENS, temperature=0.0)
    if contract["rf"]:
        kwargs["response_format"] = {"type": "json_object"}
    async with sem:
        t0 = time.perf_counter()
        try:
            resp = await client.chat.completions.create(**kwargs)
        except Exception as e:
            return {"idx": idx, "contract": cname, "error": f"{type(e).__name__}: {str(e)[:70]}",
                    "lat": int((time.perf_counter() - t0) * 1000)}
    lat = int((time.perf_counter() - t0) * 1000)
    raw = resp.choices[0].message.content or ""
    clean = strip_reasoning(raw)
    row = {
        "idx": idx, "contract": cname, "lat": lat,
        "out_tok": getattr(resp.usage, "completion_tokens", None),
        "finish": resp.choices[0].finish_reason,
        "truncated": resp.choices[0].finish_reason == "length",
        "think_leaked": "<think>" in raw,
        "format_ok": contract["score"](clean),
    }
    if cname == "json_mode":
        row["raw_parse_ok"] = json_ok(raw)  # naive app: no strip
    return row


async def main():
    if not API_KEY:
        raise SystemExit("ERROR: OPENCODE_API_KEY not set (tests/.env).")
    print(f"Model={MODEL}  max_tokens={MAX_TOKENS}  N={N_CALLS}  concurrency={CONCURRENCY}")
    print(f"Base URL={BASE_URL}\n")

    client = AsyncOpenAI(api_key=API_KEY, base_url=BASE_URL, timeout=180.0)
    sem = asyncio.Semaphore(CONCURRENCY)
    tasks = [one_call(client, sem, i, ORDER[i % 3]) for i in range(N_CALLS)]

    rows = []
    for coro in asyncio.as_completed(tasks):
        r = await coro
        rows.append(r)
        if r.get("error"):
            print(f"  #{r['idx']:02d} {r['contract']:13s} ERROR {r['error']}")
        else:
            tag = "OK " if r["format_ok"] else "FAIL"
            extra = []
            if r.get("think_leaked"):
                extra.append("think")
            if r.get("truncated"):
                extra.append("TRUNC")
            if r["contract"] == "json_mode" and not r.get("raw_parse_ok"):
                extra.append("raw-parse-VOŸ")
            print(f"  #{r['idx']:02d} {r['contract']:13s} fmt={tag} "
                  f"finish={r['finish']:6s} out_tok={r['out_tok']:>4} lat={r['lat']:>6}ms "
                  f"{' '.join(extra)}")

    rows.sort(key=lambda r: r["idx"])
    print("\n" + "=" * 70)
    print(f"SUMMARY over {N_CALLS} calls, {MODEL} @ max_tokens={MAX_TOKENS}")
    print("=" * 70)
    errs = [r for r in rows if r.get("error")]
    good = [r for r in rows if not r.get("error")]
    fmt_pass = sum(1 for r in good if r["format_ok"])
    trunc = sum(1 for r in good if r.get("truncated"))
    leaked = sum(1 for r in good if r.get("think_leaked"))
    print(f"  errors        : {len(errs)}/{N_CALLS}")
    print(f"  format PASS   : {fmt_pass}/{len(good)} (after stripping <think>)")
    print(f"  truncated     : {trunc}/{len(good)}")
    print(f"  <think> leaked: {leaked}/{len(good)}")

    jm = [r for r in good if r["contract"] == "json_mode"]
    raw_ok = sum(1 for r in jm if r.get("raw_parse_ok"))
    print(f"  json_mode raw-parse WITHOUT strip: {raw_ok}/{len(jm)} "
          f"(this is what a naive app sees)")

    # per-contract
    print("\n  per-contract format PASS:")
    by = defaultdict(lambda: [0, 0])
    for r in good:
        by[r["contract"]][1] += 1
        if r["format_ok"]:
            by[r["contract"]][0] += 1
    for c in ORDER:
        p, t = by[c]
        print(f"    {c:13s}: {p}/{t}")

    lats = [r["lat"] for r in good]
    if lats:
        lats.sort()
        print(f"\n  latency ms: min={lats[0]} median={lats[len(lats)//2]} max={lats[-1]}")
    toks = [r["out_tok"] for r in good if r.get("out_tok")]
    if toks:
        print(f"  out_tok    : min={min(toks)} max={max(toks)} "
              f"(cap was {MAX_TOKENS}; none should be near it)")


if __name__ == "__main__":
    asyncio.run(main())
