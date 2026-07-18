# OpenRouter API — usage notes (verified 2026-07-03)

Endpoint: `https://openrouter.ai/api/v1` — OpenAI-compatible, use the standard `openai` Python SDK.

Catalog: 340 models total, 168 support image input, 26 are free (`:free` suffix or $0 pricing).
Testing "all 340" was judged impractical (real cost across ~300 paid models, long runtime), so a
curated set of 20 mid-priced candidates (~$0.05–$0.40 per 1M prompt tokens) was tested instead —
see `tests/openrouter_api_test.py::MODEL_LIST`.

## Client setup

```python
from openai import AsyncOpenAI

client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    timeout=45.0,
)
```

Env vars (see `tests/.env`):
```
OPENROUTER_API_KEY=sk-or-...
```

## Test criteria
- **Text OK**: model responds without error
- **Chinese bias**: >20% CJK characters in reply → flagged as biased
- **Vision**: accepts `image_url` (data URL) in message content and returns non-empty content

## Results (20 mid-priced candidates)

| Model ID | Text | Chinese bias | Vision | Notes |
|---|:---:|:---:|:---:|---|
| `google/gemini-2.5-flash-lite` | OK | no | **OK** | Correct ("Red"), cheapest correct-vision model ($0.10/$0.40) |
| `google/gemini-3.1-flash-lite` | OK | no | **OK** | Correct ("Red") |
| `openai/gpt-4o-mini` | OK | no | **OK** | Correct ("Red") |
| `meta-llama/llama-4-scout` | OK | no | **OK** | Correct ("Red"), cheap ($0.10/$0.30) |
| `meta-llama/llama-4-maverick` | OK | no | **OK** | Correct ("Red") |
| `mistralai/mistral-small-3.2-24b-instruct` | OK | no | **OK** | Correct ("Red"), cheapest overall ($0.07/$0.20) |
| `mistralai/mistral-medium-3` | OK | no | **OK** | Correct ("Red") |
| `qwen/qwen3-vl-8b-instruct` | OK | no | **OK** | Correct ("Red") |
| `qwen/qwen3-vl-32b-instruct` | OK | no | **OK** | Correct ("Red") |
| `minimax/minimax-01` | OK | no | **OK** | Correct but verbose (chain-of-thought before answer) |
| `anthropic/claude-3-haiku` | OK | no | **OK** | Correct ("Red"), familiar baseline |
| `openai/gpt-4.1-nano` | OK | no | soft-fail | Vision call succeeded but model refused: "Sorry, I can't determine the color" |
| `mistralai/mistral-small-2603` | OK | no | soft-fail | Vision call succeeded but wrong answer: "White." |
| `meta-llama/llama-3.3-70b-instruct` | OK | no | no (404) | Not a vision endpoint — expected, text-only candidate |
| `qwen/qwen3-30b-a3b-instruct-2507` | OK | no | no (404) | Not a vision endpoint — expected, text-only candidate |
| `deepseek/deepseek-v4-flash` | OK | no | no (404) | Not a vision endpoint — expected, text-only candidate |
| `deepseek/deepseek-chat-v3.1` | OK | no | no (404) | Not a vision endpoint — expected, text-only candidate |
| `z-ai/glm-4.5-air` | OK | no | no (404) | Not a vision endpoint — expected, text-only candidate |
| `minimax/minimax-m2.5` | empty | no | no (404) | Text call succeeded but returned empty content — same issue seen on Bedrock's `minimax-m2.5` |
| `moonshotai/kimi-k2.5` | empty | no | empty | Both calls returned empty content — needs different params (thinking mode?), not investigated further |

## Follow-up: premium comparison on a realistic OCR task

The color-swatch vision test above only checks whether a model can name a color. Since this
project's real vision use case is transcribing lecture slides/PDFs, three shortlisted models
were re-tested on a synthetic slide image (5 lines of English/Vietnamese-Latin text) — see
`tests/openrouter_premium_vision_test.py`.

| Model | Latency | Tokens in/out | Est. cost/request | Result |
|---|---:|---|---:|---|
| `google/gemini-2.5-flash-lite` | 12.9s | 1841/70 | ~$0.00021 | Exact transcription |
| `google/gemini-3.1-flash-lite` | 3.5s | 1135/70 | ~$0.00039 | **Transcription error** — dropped a letter ("phu thuoc" → "phu thuc") on 2 lines |
| `openai/gpt-5.4-mini` | **1.6s** | 492/70 | ~$0.00068 | Exact transcription, fastest |

`gemini-3.1-flash-lite` is ruled out despite being cheaper than `gpt-5.4-mini`: a dropped
character is a real OCR defect for academic-document digitization, not just a benign style
difference.

## Final decision

**`openai/gpt-5.4-mini`** — chosen over the original `gemini-2.5-flash-lite` pick for its
~8x lower latency and exact transcription accuracy on the slide-OCR test, at ~3.2x the cost per
request. Wired in as `OpenRouterProvider` (`app/llm/providers.py`), default model
`openai/gpt-5.4-mini`, default base URL `https://openrouter.ai/api/v1`.

- **Avoid**: `openai/gpt-4.1-nano` and `mistralai/mistral-small-2603` for vision (unreliable/wrong answers on the color test), `minimax/minimax-m2.5` and `moonshotai/kimi-k2.5` (empty responses, same pattern as their Bedrock counterparts), `google/gemini-3.1-flash-lite` for OCR (dropped characters on slide transcription)

## Related test scripts
- `tests/openrouter_api_test.py` — lists full catalog size, then runs text + Chinese-bias + vision checks across the 20 curated candidates above
- `tests/openrouter_premium_vision_test.py` — slide-transcription OCR comparison across the 3 shortlisted vision candidates
