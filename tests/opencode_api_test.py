"""
Quick test for the OpenCode (opencode.ai) subscription API — OpenAI-compatible endpoint.

Setup:
    # in tests/.env or exported in the shell:
    export OPENCODE_API_KEY="your-api-key"
    export OPENCODE_BASE_URL="https://opencode.ai/zen/v1"   # confirm against your plan's docs
    export OPENCODE_MODEL=""                                 # optional, leave empty to pick from list_models

Run:
    python tests/opencode_api_test.py
"""

import asyncio
import os
import time
from pathlib import Path

from openai import AsyncOpenAI


def _load_local_env() -> None:
    """Load tests/.env (next to this script) into os.environ without extra deps.

    Existing environment variables win, so `export` / CLI overrides still apply.
    """
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

OPENCODE_API_KEY = os.environ.get("OPENCODE_API_KEY", "")
OPENCODE_BASE_URL = os.environ.get("OPENCODE_BASE_URL", "https://opencode.ai/zen/v1")
OPENCODE_MODEL = os.environ.get("OPENCODE_MODEL", "")


def check_env() -> None:
    if not OPENCODE_API_KEY:
        raise SystemExit("ERROR: OPENCODE_API_KEY is not set. Export it or add it to tests/.env first.")
    print(f"Base URL : {OPENCODE_BASE_URL}")
    print(f"Model    : {OPENCODE_MODEL or '(not set — run test_list_models first)'}")
    print()


async def test_list_models() -> None:
    """Discover which model IDs the subscription actually exposes."""
    client = AsyncOpenAI(api_key=OPENCODE_API_KEY, base_url=OPENCODE_BASE_URL, timeout=30.0)

    print("=== Test 0: List models ===")
    t0 = time.perf_counter()
    models = await client.models.list()
    elapsed = int((time.perf_counter() - t0) * 1000)

    ids = [m.id for m in models.data]
    print(f"Found    : {len(ids)} models")
    for model_id in ids[:20]:
        print(f"  - {model_id}")
    print(f"Latency  : {elapsed}ms")
    print()


async def test_basic_chat() -> None:
    if not OPENCODE_MODEL:
        print("=== Test 1: Basic chat — SKIPPED (OPENCODE_MODEL not set) ===\n")
        return

    client = AsyncOpenAI(api_key=OPENCODE_API_KEY, base_url=OPENCODE_BASE_URL, timeout=30.0)

    messages = [
        {"role": "user", "content": "Say hello in one sentence."},
    ]

    print("=== Test 1: Basic chat ===")
    t0 = time.perf_counter()
    response = await client.chat.completions.create(model=OPENCODE_MODEL, messages=messages)
    elapsed = int((time.perf_counter() - t0) * 1000)

    content = response.choices[0].message.content
    usage = response.usage
    print(f"Response : {content}")
    print(f"Tokens   : in={usage.prompt_tokens} out={usage.completion_tokens}")
    print(f"Latency  : {elapsed}ms")
    print()


async def test_system_message() -> None:
    if not OPENCODE_MODEL:
        print("=== Test 2: System message + Vietnamese — SKIPPED (OPENCODE_MODEL not set) ===\n")
        return

    client = AsyncOpenAI(api_key=OPENCODE_API_KEY, base_url=OPENCODE_BASE_URL, timeout=30.0)

    messages = [
        {"role": "system", "content": "You are a helpful assistant that speaks Vietnamese."},
        {"role": "user", "content": "Giải thích RAG là gì trong 2 câu."},
    ]

    print("=== Test 2: System message + Vietnamese ===")
    t0 = time.perf_counter()
    response = await client.chat.completions.create(model=OPENCODE_MODEL, messages=messages, max_tokens=200)
    elapsed = int((time.perf_counter() - t0) * 1000)

    content = response.choices[0].message.content
    print(f"Response : {content}")
    print(f"Latency  : {elapsed}ms")
    print()


async def main() -> None:
    check_env()
    await test_list_models()
    await test_basic_chat()
    await test_system_message()
    print("All tests passed.")


if __name__ == "__main__":
    asyncio.run(main())
