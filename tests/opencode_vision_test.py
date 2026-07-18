"""
Vision test across all models on the OpenCode "Go" plan.

Sends a synthetic test image (generated locally with Pillow, not real academic
material) to each model in MODEL_LIST, one at a time, and checks whether the
model can correctly describe it.

MODEL_LIST is hardcoded below (from `client.models.list()` on the Go plan
endpoint) — OPENCODE_MODEL from .env is intentionally NOT used here.

Setup:
    # in tests/.env:
    OPENCODE_API_KEY=...
    OPENCODE_BASE_URL=https://opencode.ai/zen/go/v1

Run:
    python tests/opencode_vision_test.py
"""

import asyncio
import base64
import io
import os
import time
from pathlib import Path

from openai import AsyncOpenAI
from PIL import Image, ImageDraw

MODEL_LIST = [
    "minimax-m3",
    "minimax-m2.7",
    "minimax-m2.5",
    "kimi-k2.7-code",
    "kimi-k2.6",
    "kimi-k2.5",
    "glm-5.2",
    "glm-5.1",
    "glm-5",
    "deepseek-v4-pro",
    "deepseek-v4-flash",
    "qwen3.7-max",
    "qwen3.7-plus",
    "qwen3.6-plus",
    "qwen3.5-plus",
    "mimo-v2-pro",
    "mimo-v2-omni",
    "mimo-v2.5-pro",
    "mimo-v2.5",
    "hy3-preview",
]


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

OPENCODE_API_KEY = os.environ.get("OPENCODE_API_KEY", "")
OPENCODE_BASE_URL = os.environ.get("OPENCODE_BASE_URL", "https://opencode.ai/zen/go/v1")

PROMPT = "What shape and what color do you see in this image? Answer in one short sentence."


def make_test_image_data_url() -> str:
    """A red circle on a white background — simple enough to verify the answer."""
    img = Image.new("RGB", (300, 300), "white")
    draw = ImageDraw.Draw(img)
    draw.ellipse((60, 60, 240, 240), fill="red")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/png;base64,{b64}"


def classify_answer(content: str) -> str:
    text = (content or "").lower()
    has_color = "red" in text
    has_shape = "circle" in text or "circular" in text or "round" in text
    if has_color and has_shape:
        return "CORRECT"
    if content:
        return "UNCLEAR"
    return "EMPTY"


async def test_model_vision(client: AsyncOpenAI, model: str, image_data_url: str) -> None:
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": PROMPT},
                {"type": "image_url", "image_url": {"url": image_data_url}},
            ],
        }
    ]

    t0 = time.perf_counter()
    try:
        response = await client.chat.completions.create(model=model, messages=messages, max_tokens=100, timeout=45.0)
        elapsed = int((time.perf_counter() - t0) * 1000)
        content = response.choices[0].message.content
        verdict = classify_answer(content)
        print(f"{model:20s} -> {verdict:8s} ({elapsed:5d}ms)  {content!r}")
    except Exception as e:
        elapsed = int((time.perf_counter() - t0) * 1000)
        status = getattr(e, "status_code", "?")
        print(f"{model:20s} -> FAIL     ({elapsed:5d}ms)  [{status}] {type(e).__name__}: {str(e)[:150]}")


async def main() -> None:
    if not OPENCODE_API_KEY:
        raise SystemExit("ERROR: OPENCODE_API_KEY is not set. Add it to tests/.env first.")

    print(f"Base URL : {OPENCODE_BASE_URL}")
    print(f"Models   : {len(MODEL_LIST)}")
    print(f"Image    : synthetic red circle on white (generated locally)")
    print()

    client = AsyncOpenAI(api_key=OPENCODE_API_KEY, base_url=OPENCODE_BASE_URL, timeout=45.0)
    image_data_url = make_test_image_data_url()

    for model in MODEL_LIST:
        await test_model_vision(client, model, image_data_url)


if __name__ == "__main__":
    asyncio.run(main())
