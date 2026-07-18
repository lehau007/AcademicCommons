# OpenCode API — usage notes (verified 2026-07-02)

## Two different base URLs, two different plans

| Base URL | Plan | Auth | Models | Billing |
|---|---|---|---|---|

| `https://opencode.ai/zen/go/v1` | Go (subscription) | Bearer API key | Restricted catalog, 20 models — **no Claude/GPT/Gemini**, only MiniMax/Kimi/GLM/DeepSeek/Qwen/MiMo/Hy families | Flat subscription, no credits error |

Confirmed by calling `claude-sonnet-5` / `gpt-5` / `gemini-3-flash` against `zen/go/v1`: all return `401 ModelError: Model X is not supported` — the Go plan is a real provider-tier restriction, not a billing issue.

## Client setup

The API is OpenAI-compatible — use the standard `openai` Python SDK, just point `base_url` at OpenCode.

```python
from openai import AsyncOpenAI

client = AsyncOpenAI(
    api_key=OPENCODE_API_KEY,
    base_url="https://opencode.ai/zen/go/v1",  # Go plan
    timeout=45.0,
)
```

Env vars (see `tests/.env`):
```
OPENCODE_API_KEY=sk-...
OPENCODE_BASE_URL=https://opencode.ai/zen/go/v1
```

## Recommended model: `minimax-m3`

Of the 20 models on the Go plan, only 3 reliably handle image input: `minimax-m3`, `kimi-k2.7-code`, `kimi-k2.5`. **`minimax-m3` is the pick** — it also exposes a `<think>...</think>` reasoning trace ahead of the final answer, so parse the content accordingly if you need just the answer.

### Text chat

```python
response = await client.chat.completions.create(
    model="minimax-m3",
    messages=[{"role": "user", "content": "Say hello in one sentence."}],
)
print(response.choices[0].message.content)
```

### Vision (image input)

```python
messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "What shape and what color do you see in this image?"},
            {"type": "image_url", "image_url": {"url": image_data_url}},  # data: URL or https URL
        ],
    }
]
response = await client.chat.completions.create(model="minimax-m3", messages=messages, max_tokens=100)
```

Verified working: `minimax-m3` correctly identified a synthetic red circle test image (see `tests/opencode_vision_test.py`).

Note: `minimax-m3` responses may include a leading `<think>...</think>` block — strip it if you only want the final answer:

```python
import re
content = re.sub(r"<think>.*?</think>\s*", "", raw_content, flags=re.DOTALL).strip()
```

## Known failure modes on the Go plan (`zen/go/v1`)

| Error | Meaning | Seen on |
|---|---|---|
| `401 ModelError: Model X is not supported` | Model not included in this plan | `claude-*`, `gpt-*`, `gemini-*`, `deepseek-v4-flash-free` |
| `400 Upstream request failed` | Model rejected the request (image input not supported) | `glm-5.2`, `glm-5.1`, `glm-5`, `deepseek-v4-pro`, `deepseek-v4-flash`, `mimo-v2-pro`, `mimo-v2-omni` |
| `503 Inference is temporarily unavailable` (`failover_exhausted`) | Provider-side flakiness — retry later, not a hard capability limit | `qwen3.7-max`, `qwen3.7-plus`, `qwen3.6-plus`, `qwen3.5-plus` |
| `502` (Cloudflare) | Upstream/gateway error | `minimax-m2.5`, `mimo-v2.5-pro` |
| Empty `content` (`None`), no error | Model doesn't support the input but doesn't reject it either | `minimax-m2.7`, `kimi-k2.6`, `mimo-v2.5` |
| `400 ... not supported on the lite model list. Use GET /inference...` | Model needs a different discovery endpoint — not investigated | `hy3-preview` |

## Full model list on the Go plan (`zen/go/v1`)

```
minimax-m3, minimax-m2.7, minimax-m2.5
kimi-k2.7-code, kimi-k2.6, kimi-k2.5
glm-5.2, glm-5.1, glm-5
deepseek-v4-pro, deepseek-v4-flash
qwen3.7-max, qwen3.7-plus, qwen3.6-plus, qwen3.5-plus
mimo-v2-pro, mimo-v2-omni, mimo-v2.5-pro, mimo-v2.5
hy3-preview
```

## Format-health comparison across Go-plan models (tested 2026-07-10)

Question investigated: is opencode intentionally degrading the raw API format on
the Go plan? **Answer: no.** The whole Go catalog is Chinese *reasoning* models,
and a reasoning trace over a plain OpenAI-compatible endpoint interacts badly
with a **small `max_tokens`**. Run `tests/opencode_format_compare_test.py`.

Results (max_tokens 120–200, short-answer prompts):

| Model | Behaviour with tight `max_tokens` | Root cause |
|---|---|---|
| `minimax-m3` | `<think>…</think>` leaks into `content`, then truncates | reasoning trace written into `content`, not a separate channel |
| `kimi-k2.5` | meta-reasoning ("The user wants…") leaks into `content`, truncates | same leak, no `<think>` tags |
| `glm-5.2` | **empty** `content`, `finish=length`, tokens billed | reasoning consumed on a hidden channel; budget gone before any visible answer |
| `deepseek-v4-pro` | **empty** `content`, `finish=length` | same hidden-reasoning drain |
| `qwen3.7-max` | clean 3/3 — but **ignores** the small cap (out_tok 1200+, 25 s) | doesn't enforce small `max_tokens`; runs to completion |
| `kimi-k2.7-code` | hard `400 Upstream request failed` | broken/vision-oriented endpoint, not a format issue |

**Confirming fix:** re-running the "empty/truncated" models with `max_tokens=1500`
makes `minimax-m3`, `glm-5.2`, `deepseek-v4-pro` all return **clean correct answers**
(`finish=stop`). So it is a budget + reasoning-channel interaction, not sabotage.

### Format adherence: honored, but `<think>` breaks strict parsers (tested 2026-07-10)

Follow-up question: does the Go plan *ignore* forced formats (JSON mode / hard
templates / exact counts)? Run `tests/opencode_format_adherence_test.py` — at
`max_tokens=1500` with `<think>` stripped, **all 5 models PASS all 3 contracts**:

| Contract | minimax-m3 | glm-5.2 | kimi-k2.5 | qwen3.7-max | deepseek-v4-pro |
|---|---|---|---|---|---|
| `response_format` json_object | PASS | PASS | PASS | PASS | PASS |
| hard `ANSWER:/CONFIDENCE:` template | PASS | PASS | PASS | PASS | PASS |
| exactly-3-bullets | PASS | PASS | PASS | PASS | PASS |

`response_format={"type":"json_object"}` is **accepted** by the endpoint (not rejected).
So the format instruction is *not* ignored. The catch: **`minimax-m3` still prepends
`<think>…</think>` even in JSON mode**, so the raw content is
`<think>…</think>{"capital":"Paris"}` — and `json.loads(raw)` throws
`Expecting value: line 1 column 1`. That parse failure is what *looks* like
"the model threw my format in the trash". Strip `<think>` first and it parses fine.
(glm/kimi/qwen/deepseek did **not** leak `<think>` into content on these prompts.)

### 30-call robustness at `max_tokens=40000` (tested 2026-07-10)

`tests/opencode_robustness_test.py` — 30 calls to `minimax-m3`, budget 40000,
cycling the 3 format contracts:

```
errors        : 0/30
format PASS   : 30/30   (after stripping <think>)  json 10/10, template 10/10, count 10/10
truncated     : 0/30    (40000 removes truncation entirely)
<think> leaked: 30/30   (EVERY call prepends <think> — 100%, not occasional)
json raw-parse WITHOUT strip: 0/10   (naive app: fails every time)
out_tok       : min=19 max=102   (cap 40000 never approached)
```

Two conclusions that matter:

1. **minimax-m3 obeys forced formats 100% of the time (30/30).** It genuinely
   "listens". The earlier failures were budget/`<think>`, never format-ignoring.
2. **`<think>` leaks on 100% of calls — bumping the budget does NOT remove it.**
   `max_tokens=40000` eliminates *truncation* (0/30) but the `<think>…</think>`
   prefix is still there every single call, so raw `json.loads` fails 10/10.
   **Stripping `<think>` is mandatory, not optional** — big budget alone is
   necessary but not sufficient. Also note `out_tok` maxed at 102: 40000 is a
   harmless ceiling you never touch, not a cost problem (billing follows actual
   output tokens), but it is not the fix by itself.

### Practical guidance for using the Go plan as a raw API

1. **Always give a large `max_tokens`** (≥1500). Reasoning tokens are billed against
   completion budget (visibly for minimax/kimi, invisibly for glm/deepseek).
2. **Strip the reasoning block** from `content` before use:
   `re.sub(r"<think>.*?</think>\s*", "", raw, flags=re.DOTALL).strip()`.
3. **Cleanest raw-API picks:** `qwen3.7-max` (clean but slow/expensive — 11–25 s,
   ignores small caps), or `glm-5.2` with a big budget (empty content is purely a
   budget artifact). `minimax-m3` is fine *if* you strip `<think>` and budget large.
4. Avoid `kimi-k2.7-code` for text (upstream 400s).

## Related test scripts

- `tests/opencode_api_test.py` — basic connectivity smoke test (chat + system message), against `OPENCODE_MODEL` from `.env`
- `tests/opencode_vision_test.py` — vision test across all 20 Go-plan models, hardcoded `MODEL_LIST` (not `.env`-driven)
- `tests/opencode_format_compare_test.py` — format-health comparison (empty/think/truncated/error) across Go-plan models
