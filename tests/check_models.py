"""
Quick check for candidate Bedrock models:
1. Do they respond in Chinese when prompted in Vietnamese/English?
2. Do they support vision (image input)?

Run:
    python tests/check_models.py
"""

import asyncio
import base64
import os
import struct
import zlib

from openai import AsyncOpenAI

API_KEY = os.environ.get("BEDROCK_API_KEY", "")
BASE_URL = "https://bedrock-mantle.us-east-1.api.aws/v1"

MODELS = [
    "minimax.minimax-m2",
    "minimax.minimax-m2.1",
    "minimax.minimax-m2.5",
    "zai.glm-5",
    "zai.glm-4.7",
    "zai.glm-4.7-flash",
    "moonshotai.kimi-k2-thinking",
    "moonshotai.kimi-k2.5",
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


async def test_model(client: AsyncOpenAI, model_id: str) -> dict:
    result = {"model": model_id, "text_ok": False, "chinese_bias": False, "vision_ok": False, "notes": ""}

    # --- Text test ---
    try:
        r = await client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": "Trả lời bằng tiếng Anh: What is 2+2?"}],
            max_tokens=80,
            timeout=30,
        )
        answer = r.choices[0].message.content or ""
        result["text_ok"] = True
        # heuristic: >20% CJK chars → Chinese bias
        cjk = sum(1 for c in answer if "一" <= c <= "鿿")
        result["chinese_bias"] = (cjk / max(len(answer), 1)) > 0.2
        result["notes"] = f'text="{answer[:80].strip()}"'
    except Exception as e:
        result["notes"] = f"text_err={str(e)[:120]}"
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
            timeout=30,
        )
        vision_answer = r.choices[0].message.content or ""
        result["vision_ok"] = True
        result["notes"] += f' | vision="{vision_answer.strip()}"'
    except Exception as e:
        err = str(e)[:100]
        result["notes"] += f" | vision_err={err}"

    return result


async def main() -> None:
    if not API_KEY:
        raise SystemExit("BEDROCK_API_KEY not set")

    client = AsyncOpenAI(api_key=API_KEY, base_url=BASE_URL, timeout=35.0)
    tasks = [test_model(client, m) for m in MODELS]
    results = await asyncio.gather(*tasks)

    print(f"\n{'Model':<35} {'Text':^6} {'ChinBias':^9} {'Vision':^7}  Notes")
    print("-" * 110)
    for r in results:
        text  = "OK" if r["text_ok"] else "FAIL"
        bias  = "YES" if r["chinese_bias"] else "no"
        vis   = "OK" if r["vision_ok"] else "no"
        print(f"{r['model']:<35} {text:^6} {bias:^9} {vis:^7}  {r['notes']}")

    return results


if __name__ == "__main__":
    asyncio.run(main())
