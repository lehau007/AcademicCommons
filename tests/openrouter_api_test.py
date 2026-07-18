"""
Test the OpenRouter API (https://openrouter.ai) — OpenAI-compatible endpoint.

Step 1: list every model the account can see (catalog is large — ~340 models).
Step 2: run a text + Chinese-bias + vision check across a curated set of
        mid-priced candidate models (MODEL_LIST below) to decide which one(s)
        to wire in as the OpenRouter provider.

Setup:
    # in tests/.env:
    OPENROUTER_API_KEY=sk-or-...

Run:
    python tests/openrouter_api_test.py
"""

import asyncio
import base64
import os
import struct
import time
import zlib
from pathlib import Path

from openai import AsyncOpenAI


def _load_local_env() -> None:
    """Load tests/.env (next to this script) into os.environ without extra deps."""
    env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.split(" #", 1)[0].strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


_load_local_env()

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

# Curated mid-priced candidates (not free, not premium $1+/M tier) — picked from
# the ~340-model catalog, favoring families already used in this project
# (Gemini, Llama, Mistral) plus other solid mainstream options for comparison.
# Prices are per 1M tokens (prompt/completion) at selection time.
MODEL_LIST = [
    "google/gemini-2.5-flash-lite",          # $0.10/$0.40 — vision
    "google/gemini-3.1-flash-lite",          # $0.25/$1.50 — vision
    "openai/gpt-4.1-nano",                   # $0.10/$0.40 — vision
    "openai/gpt-4o-mini",                    # $0.15/$0.60 — vision
    "meta-llama/llama-4-scout",              # $0.10/$0.30 — vision
    "meta-llama/llama-4-maverick",           # $0.15/$0.60 — vision
    "meta-llama/llama-3.3-70b-instruct",     # $0.10/$0.32 — text only
    "mistralai/mistral-small-3.2-24b-instruct",  # $0.07/$0.20 — vision
    "mistralai/mistral-small-2603",          # $0.15/$0.60 — vision
    "mistralai/mistral-medium-3",            # $0.40/$2.00 — vision
    "qwen/qwen3-30b-a3b-instruct-2507",      # $0.05/$0.19 — text only
    "qwen/qwen3-vl-8b-instruct",             # $0.12/$0.45 — vision
    "qwen/qwen3-vl-32b-instruct",            # $0.10/$0.42 — vision
    "deepseek/deepseek-v4-flash",            # $0.09/$0.18 — text only
    "deepseek/deepseek-chat-v3.1",           # $0.21/$0.79 — text only
    "z-ai/glm-4.5-air",                      # $0.13/$0.85 — text only
    "minimax/minimax-m2.5",                  # $0.12/$0.48 — text only
    "minimax/minimax-01",                    # $0.20/$1.10 — vision
    "moonshotai/kimi-k2.5",                  # $0.38/$2.02 — vision
    "anthropic/claude-3-haiku",              # $0.25/$1.25 — vision, familiar baseline
]


# Minimal 16x16 red square PNG (no external deps)
def _make_test_png_b64() -> str:
    w, h = 16, 16
    raw = b"".join(b"\x00" + b"\xff\x00\x00" * w for _ in range(h))  # RGB red rows

    def chunk(tag: bytes, data: bytes) -> bytes:
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    png = (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw))
        + chunk(b"IEND", b"")
    )
    return base64.b64encode(png).decode()


TEST_IMAGE_B64 = _make_test_png_b64()


async def list_models(client: AsyncOpenAI) -> None:
    print("=== Step 1: List models ===")
    t0 = time.perf_counter()
    models = await client.models.list()
    elapsed = int((time.perf_counter() - t0) * 1000)
    print(f"Found    : {len(models.data)} models total on this account")
    print(f"Latency  : {elapsed}ms")
    print()


async def test_model(client: AsyncOpenAI, model_id: str) -> dict:
    result = {"model": model_id, "text_ok": False, "chinese_bias": False, "vision_ok": False, "notes": ""}

    # --- Text test ---
    try:
        r = await client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": "Trả lời bằng tiếng Anh: What is 2+2?"}],
            max_tokens=80,
            timeout=45,
        )
        answer = r.choices[0].message.content or ""
        result["text_ok"] = True
        cjk = sum(1 for c in answer if "一" <= c <= "鿿")
        result["chinese_bias"] = (cjk / max(len(answer), 1)) > 0.2
        result["notes"] = f'text="{answer[:80].strip()}"'
    except Exception as e:
        result["notes"] = f"text_err={str(e)[:150]}"
        return result

    # --- Vision test ---
    try:
        r = await client.chat.completions.create(
            model=model_id,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": "What color is this image? Answer in one word."},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{TEST_IMAGE_B64}"}},
                ],
            }],
            max_tokens=20,
            timeout=45,
        )
        vision_answer = r.choices[0].message.content or ""
        result["vision_ok"] = bool(vision_answer.strip())
        result["notes"] += f' | vision="{vision_answer.strip()}"'
    except Exception as e:
        err = str(e)[:150]
        result["notes"] += f" | vision_err={err}"

    return result


async def main() -> None:
    if not OPENROUTER_API_KEY:
        raise SystemExit("ERROR: OPENROUTER_API_KEY is not set. Add it to tests/.env first.")

    print(f"Base URL : {OPENROUTER_BASE_URL}")
    print(f"Candidates: {len(MODEL_LIST)}")
    print()

    client = AsyncOpenAI(api_key=OPENROUTER_API_KEY, base_url=OPENROUTER_BASE_URL, timeout=50.0)

    await list_models(client)

    print("=== Step 2: Text + Chinese-bias + Vision check (sequential, one at a time) ===")
    results = []
    for model_id in MODEL_LIST:
        r = await test_model(client, model_id)
        results.append(r)
        text = "OK" if r["text_ok"] else "FAIL"
        bias = "YES" if r["chinese_bias"] else "no"
        vis = "OK" if r["vision_ok"] else "no"
        print(f"{r['model']:<45} text={text:<4} bias={bias:<3} vision={vis:<4} {r['notes']}")

    print()
    print(f"{'Model':<45} {'Text':^6} {'ChinBias':^9} {'Vision':^7}")
    print("-" * 75)
    for r in results:
        text = "OK" if r["text_ok"] else "FAIL"
        bias = "YES" if r["chinese_bias"] else "no"
        vis = "OK" if r["vision_ok"] else "no"
        print(f"{r['model']:<45} {text:^6} {bias:^9} {vis:^7}")


if __name__ == "__main__":
    asyncio.run(main())
