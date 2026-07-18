"""
Quick test for AWS Bedrock API key mode (OpenAI-compatible endpoint).

Setup:
    export BEDROCK_API_KEY="your-api-key"
    export BEDROCK_MODEL_ID="us.amazon.nova-lite-v1:0"   # hoặc model khác
    export AWS_REGION="us-east-1"                         # optional, default us-east-1
    export BEDROCK_BASE_URL=""                            # optional, để trống dùng default

Run:
    python tests/bedrock_api_test.py
"""

import asyncio
import os
import time

from openai import AsyncOpenAI


BEDROCK_API_KEY = os.environ.get("BEDROCK_API_KEY", "")
BEDROCK_MODEL_ID = os.environ.get("BEDROCK_MODEL_ID", "us.amazon.nova-lite-v1:0")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
BEDROCK_BASE_URL = os.environ.get("BEDROCK_BASE_URL", "") or f"https://bedrock-mantle.{AWS_REGION}.api.aws/v1"


def check_env() -> None:
    if not BEDROCK_API_KEY:
        raise SystemExit("ERROR: BEDROCK_API_KEY is not set. Export it first:\n  export BEDROCK_API_KEY=your-key")
    print(f"Model    : {BEDROCK_MODEL_ID}")
    print(f"Region   : {AWS_REGION}")
    print(f"Base URL : {BEDROCK_BASE_URL}")
    print()


async def test_basic_chat() -> None:
    client = AsyncOpenAI(api_key=BEDROCK_API_KEY, base_url=BEDROCK_BASE_URL, timeout=30.0)

    messages = [
        {"role": "user", "content": "Say hello in one sentence."},
    ]

    print("=== Test 1: Basic chat ===")
    t0 = time.perf_counter()
    response = await client.chat.completions.create(model=BEDROCK_MODEL_ID, messages=messages)
    elapsed = int((time.perf_counter() - t0) * 1000)

    content = response.choices[0].message.content
    usage = response.usage
    print(f"Response : {content}")
    print(f"Tokens   : in={usage.prompt_tokens} out={usage.completion_tokens}")
    print(f"Latency  : {elapsed}ms")
    print()


async def test_system_message() -> None:
    client = AsyncOpenAI(api_key=BEDROCK_API_KEY, base_url=BEDROCK_BASE_URL, timeout=30.0)

    messages = [
        {"role": "system", "content": "You are a helpful assistant that speaks Vietnamese."},
        {"role": "user", "content": "Giải thích RAG là gì trong 2 câu."},
    ]

    print("=== Test 2: System message + Vietnamese ===")
    t0 = time.perf_counter()
    response = await client.chat.completions.create(model=BEDROCK_MODEL_ID, messages=messages, max_tokens=200)
    elapsed = int((time.perf_counter() - t0) * 1000)

    content = response.choices[0].message.content
    print(f"Response : {content}")
    print(f"Latency  : {elapsed}ms")
    print()


async def test_json_output() -> None:
    client = AsyncOpenAI(api_key=BEDROCK_API_KEY, base_url=BEDROCK_BASE_URL, timeout=30.0)

    schema = {
        "type": "object",
        "properties": {
            "answer": {"type": "string"},
            "confidence": {"type": "number"},
        },
        "required": ["answer", "confidence"],
    }

    messages = [
        {"role": "user", "content": "What is 2 + 2? Return JSON with answer and confidence."},
    ]

    print("=== Test 3: Structured JSON output ===")
    t0 = time.perf_counter()
    response = await client.chat.completions.create(
        model=BEDROCK_MODEL_ID,
        messages=messages,
        response_format={
            "type": "json_schema",
            "json_schema": {"name": "structured_response", "schema": schema},
        },
    )
    elapsed = int((time.perf_counter() - t0) * 1000)

    content = response.choices[0].message.content
    print(f"Response : {content}")
    print(f"Latency  : {elapsed}ms")
    print()


async def main() -> None:
    check_env()
    await test_basic_chat()
    await test_system_message()
    await test_json_output()
    print("All tests passed.")


if __name__ == "__main__":
    asyncio.run(main())
