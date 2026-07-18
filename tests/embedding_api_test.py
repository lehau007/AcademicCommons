"""
Check whether the Bedrock API key can call any EMBEDDING models.

Strategy:
1. GET /v1/models  -> list everything the gateway exposes, flag likely embedding models.
2. POST /v1/embeddings for a set of candidate model IDs -> see which actually work.

Run:
    export BEDROCK_API_KEY="..."
    python tests/embedding_api_test.py
"""

import asyncio
import os

from openai import AsyncOpenAI

API_KEY = os.environ.get("BEDROCK_API_KEY", "")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
BASE_URL = os.environ.get("BEDROCK_BASE_URL", "") or f"https://bedrock-mantle.{AWS_REGION}.api.aws/v1"

# Common Bedrock embedding model IDs + a few OpenAI-style names to probe the gateway.
CANDIDATES = [
    "amazon.titan-embed-text-v1",
    "amazon.titan-embed-text-v2:0",
    "cohere.embed-english-v3",
    "cohere.embed-multilingual-v3",
    "cohere.embed-v4:0",
    "text-embedding-3-small",
    "text-embedding-3-large",
]


async def list_models(client: AsyncOpenAI) -> None:
    print("=== /v1/models ===")
    try:
        models = await client.models.list()
        ids = sorted(m.id for m in models.data)
        print(f"Total models exposed: {len(ids)}")
        embed_like = [m for m in ids if "embed" in m.lower()]
        print(f"Embedding-looking IDs ({len(embed_like)}): {embed_like or 'NONE'}")
        print("All IDs:")
        for m in ids:
            print(f"  - {m}")
    except Exception as e:
        print(f"models.list FAILED: {type(e).__name__}: {str(e)[:200]}")
    print()


async def try_embedding(client: AsyncOpenAI, model_id: str) -> None:
    try:
        r = await client.embeddings.create(model=model_id, input="Xin chào, đây là một câu kiểm tra embedding.")
        vec = r.data[0].embedding
        print(f"  OK    {model_id:<35} dim={len(vec)} first3={[round(x, 4) for x in vec[:3]]}")
    except Exception as e:
        print(f"  FAIL  {model_id:<35} {type(e).__name__}: {str(e)[:140]}")


async def main() -> None:
    if not API_KEY:
        raise SystemExit("BEDROCK_API_KEY not set")
    print(f"Base URL : {BASE_URL}\n")
    client = AsyncOpenAI(api_key=API_KEY, base_url=BASE_URL, timeout=40.0)

    await list_models(client)

    print("=== POST /v1/embeddings (candidates) ===")
    for m in CANDIDATES:
        await try_embedding(client, m)


if __name__ == "__main__":
    asyncio.run(main())
