"""
Does the OpenCode Go plan actually HONOR format constraints, or ignore them?

Companion to opencode_format_compare_test.py. That one showed the reasoning
trace wrecks output under tight max_tokens. This one isolates FORMAT ADHERENCE:
we give a generous budget (1500) and strip <think> first, then check whether the
model obeys an explicit output-format contract.

Three contracts:
  1. json_mode   : response_format={"type":"json_object"} + "output only JSON"
  2. hard_template: "Answer EXACTLY as: ANSWER: <one line>\\nCONFIDENCE: <0-1>"
  3. exact_count : "List EXACTLY 3 bullet points, nothing else"

For each we score (after stripping <think>):
  - json_mode   : does content parse as JSON? does response_format even get accepted?
  - hard_template: do both required lines appear, in order, and nothing extra?
  - exact_count : exactly 3 bullets? no preamble/epilogue?

Run:
    .venv/bin/python tests/opencode_format_adherence_test.py
"""

import asyncio
import json
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
MAX_TOKENS = 1500

MODELS = ["minimax-m3", "glm-5.2", "kimi-k2.5", "qwen3.7-max", "deepseek-v4-pro"]

THINK_RE = re.compile(r"<think>.*?</think>\s*", re.DOTALL)
FENCE_RE = re.compile(r"^```(?:json)?\s*|\s*```$", re.MULTILINE)


def strip_reasoning(raw: str) -> str:
    return THINK_RE.sub("", raw or "").strip()


def score_json(text: str) -> str:
    body = FENCE_RE.sub("", text).strip()
    try:
        json.loads(body)
        return "PASS" if body == text.strip() else "PASS(had-fence)"
    except Exception:
        # is there any JSON object embedded (i.e. wrapped in prose)?
        m = re.search(r"\{.*\}", body, re.DOTALL)
        if m:
            try:
                json.loads(m.group(0))
                return "FAIL(prose-wrapped-json)"
            except Exception:
                return "FAIL(not-json)"
        return "FAIL(not-json)"


def score_template(text: str) -> str:
    lines = [l for l in text.splitlines() if l.strip()]
    has_answer = any(re.match(r"\s*ANSWER:", l) for l in lines)
    has_conf = any(re.match(r"\s*CONFIDENCE:", l) for l in lines)
    if not (has_answer and has_conf):
        return "FAIL(missing-field)"
    # exactly the two required lines, nothing else?
    extra = [l for l in lines if not re.match(r"\s*(ANSWER|CONFIDENCE):", l)]
    return "PASS" if not extra else f"FAIL(+{len(extra)}-extra-lines)"


def score_count(text: str) -> str:
    bullets = re.findall(r"^\s*(?:[-*•]|\d+[.)])\s+\S", text, re.MULTILINE)
    n = len(bullets)
    if n != 3:
        return f"FAIL({n}-bullets)"
    lines = [l for l in text.splitlines() if l.strip()]
    non_bullet = [l for l in lines if not re.match(r"^\s*(?:[-*•]|\d+[.)])\s+", l)]
    return "PASS" if not non_bullet else f"FAIL(+{len(non_bullet)}-preamble)"


CONTRACTS = [
    {
        "name": "json_mode",
        "use_response_format": True,
        "messages": [
            {"role": "system", "content": "Output ONLY a valid JSON object. No prose, no markdown fences."},
            {"role": "user", "content": 'Return the capital of France as {"capital": "..."}'},
        ],
        "score": score_json,
    },
    {
        "name": "hard_template",
        "use_response_format": False,
        "messages": [
            {"role": "user", "content": (
                "What is 17 * 3? Answer EXACTLY in this format and nothing else:\n"
                "ANSWER: <the number>\nCONFIDENCE: <0-1>"
            )},
        ],
        "score": score_template,
    },
    {
        "name": "exact_count",
        "use_response_format": False,
        "messages": [
            {"role": "user", "content": (
                "List EXACTLY 3 benefits of RAG. Output only 3 bullet points "
                "starting with '- ', no intro, no conclusion."
            )},
        ],
        "score": score_count,
    },
]


async def run_one(client, model, contract):
    kwargs = dict(model=model, messages=contract["messages"],
                  max_tokens=MAX_TOKENS, temperature=0.0)
    rf_note = ""
    if contract["use_response_format"]:
        kwargs["response_format"] = {"type": "json_object"}
    t0 = time.perf_counter()
    try:
        resp = await client.chat.completions.create(**kwargs)
    except Exception as e:
        msg = str(e)
        # retry without response_format to see if THAT was the rejected part
        if contract["use_response_format"]:
            kwargs.pop("response_format")
            try:
                resp = await client.chat.completions.create(**kwargs)
                rf_note = " [response_format REJECTED -> retried without]"
            except Exception as e2:
                return f"ERROR: {type(e2).__name__}: {str(e2)[:80]}", 0
        else:
            return f"ERROR: {type(e).__name__}: {msg[:80]}", 0
    lat = int((time.perf_counter() - t0) * 1000)
    raw = resp.choices[0].message.content or ""
    clean = strip_reasoning(raw)
    verdict = contract["score"](clean)
    leaked = " [<think>leaked]" if "<think>" in raw else ""
    return f"{verdict}{rf_note}{leaked}", lat, clean[:70]


async def main():
    if not API_KEY:
        raise SystemExit("ERROR: OPENCODE_API_KEY not set (tests/.env).")
    print(f"Base URL : {BASE_URL}  max_tokens={MAX_TOKENS} (reasoning stripped before scoring)\n")
    client = AsyncOpenAI(api_key=API_KEY, base_url=BASE_URL, timeout=90.0)

    grid = {}
    for model in MODELS:
        print(f"### {model}")
        for c in CONTRACTS:
            res = await run_one(client, model, c)
            verdict, lat = res[0], res[1]
            preview = res[2] if len(res) > 2 else ""
            grid[(model, c["name"])] = verdict
            print(f"  {c['name']:14s} {verdict:40s} {lat}ms")
            if preview:
                print(f"      -> {preview!r}")
        print()

    print("=" * 78)
    print(f"{'model':16s} | " + " | ".join(f"{c['name']:12s}" for c in CONTRACTS))
    print("-" * 78)
    for model in MODELS:
        cells = []
        for c in CONTRACTS:
            v = grid[(model, c["name"])]
            cells.append(("PASS" if v.startswith("PASS") else "FAIL").ljust(12))
        print(f"{model:16s} | " + " | ".join(cells))


if __name__ == "__main__":
    asyncio.run(main())
