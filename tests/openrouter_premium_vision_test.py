"""
Compare two higher-tier OpenRouter candidates against the mid-priced pick from
tests/openrouter_api_doc.md, using a document-like image (not just a color
swatch) since this project's real use case is OCR/parsing of academic slides.

Models compared:
    - google/gemini-3.1-flash-lite   $0.25/$1.50 per 1M tokens
    - openai/gpt-5.4-mini            $0.75/$4.50 per 1M tokens
    - google/gemini-2.5-flash-lite   $0.10/$0.40 per 1M tokens (current pick, baseline)

Setup:
    # in tests/.env:
    OPENROUTER_API_KEY=sk-or-...

Run:
    python tests/openrouter_premium_vision_test.py
"""

import asyncio
import base64
import io
import os
import time
from pathlib import Path

from openai import AsyncOpenAI
from PIL import Image, ImageDraw, ImageFont


def _load_local_env() -> None:
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

MODEL_LIST = [
    "google/gemini-2.5-flash-lite",
    "google/gemini-3.1-flash-lite",
    "openai/gpt-5.4-mini",
]

SLIDE_TEXT_LINES = [
    "IT4062 - Co so du lieu",
    "Chuong 3: Chuan hoa du lieu (Normalization)",
    "- 1NF: khong co thuoc tinh da tri",
    "- 2NF: khong phu thuoc bo phan vao khoa",
    "- 3NF: khong phu thuoc bac cau",
]

PROMPT = (
    "This is a photo of a lecture slide. Transcribe every line of text exactly "
    "as written, in order, one line per line of output. Do not summarize or translate."
)


def make_slide_image_data_url() -> str:
    img = Image.new("RGB", (800, 450), "white")
    draw = ImageDraw.Draw(img)
    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
        font_body = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 22)
    except OSError:
        font_title = ImageFont.load_default()
        font_body = ImageFont.load_default()

    y = 40
    draw.text((40, y), SLIDE_TEXT_LINES[0], fill="black", font=font_title)
    y += 60
    for line in SLIDE_TEXT_LINES[1:]:
        draw.text((40, y), line, fill="black", font=font_body)
        y += 45

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/png;base64,{b64}"


def score_transcription(content: str) -> tuple[int, int]:
    """(lines_recovered, total_lines) — crude substring match per line."""
    text = (content or "").lower()
    hits = 0
    for line in SLIDE_TEXT_LINES:
        # normalize: drop diacritics/punctuation-heavy comparison isn't needed since
        # source text is already plain ASCII; just check the alnum core survives.
        core = "".join(ch for ch in line.lower() if ch.isalnum())
        found = "".join(ch for ch in text if ch.isalnum())
        if core[:12] in found:
            hits += 1
    return hits, len(SLIDE_TEXT_LINES)


async def test_model(client: AsyncOpenAI, model: str, image_data_url: str) -> None:
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
        response = await client.chat.completions.create(model=model, messages=messages, max_tokens=300, timeout=60.0)
        elapsed = int((time.perf_counter() - t0) * 1000)
        content = response.choices[0].message.content or ""
        usage = response.usage
        hits, total = score_transcription(content)
        cost_in = usage.prompt_tokens if usage else 0
        cost_out = usage.completion_tokens if usage else 0
        print(f"\n=== {model} ===")
        print(f"Latency  : {elapsed}ms | tokens in={cost_in} out={cost_out}")
        print(f"Score    : {hits}/{total} lines recovered")
        print(f"Output   :\n{content}")
    except Exception as e:
        elapsed = int((time.perf_counter() - t0) * 1000)
        status = getattr(e, "status_code", "?")
        print(f"\n=== {model} ===")
        print(f"FAIL ({elapsed}ms) [{status}] {type(e).__name__}: {str(e)[:200]}")


async def main() -> None:
    if not OPENROUTER_API_KEY:
        raise SystemExit("ERROR: OPENROUTER_API_KEY is not set. Add it to tests/.env first.")

    print(f"Base URL : {OPENROUTER_BASE_URL}")
    print(f"Models   : {MODEL_LIST}")
    print("Image    : synthetic lecture-slide screenshot with 5 lines of text (local, no PII)")

    client = AsyncOpenAI(api_key=OPENROUTER_API_KEY, base_url=OPENROUTER_BASE_URL, timeout=60.0)
    image_data_url = make_slide_image_data_url()

    for model in MODEL_LIST:
        await test_model(client, model, image_data_url)


if __name__ == "__main__":
    asyncio.run(main())
