# Integration Guide — `llm_cost_optimizer` SDK

Hướng dẫn tích hợp SDK `llm_cost_optimizer` vào một eval platform / pipeline có sẵn.
SDK chạy **in-process** (không phải service): caller gọi `EvalOptimizer.invoke(...)`
và nhận về một `InvocationResult` đã chuẩn hoá.

> **Ranh giới trách nhiệm.** SDK chỉ lo *hạ tầng tối ưu*: prompt transform, cache,
> routing/fallback, batch, cost/budget/logging, shadow. Nó **không** sở hữu logic
> nghiệp vụ eval (định nghĩa metric, dataset, ngưỡng pass/fail, aggregation). Verdict
> đúng/sai, rubric, dataset… vẫn do caller giữ.

---

## 1. Cài đặt

> **Lưu ý phân phối:** package `llm-cost-optimizer` (v0.0.1) **chưa publish lên PyPI**. Bạn
> cài nó vào venv từ **source local** (hoặc từ git repo nội bộ), rồi `import` ra dùng —
> không chạy trực tiếp file trong `src/`. Cơ chế dùng giống hệt một package PyPI bình
> thường, chỉ khác ở bước cài.

Chọn cách cài theo việc bạn là người **dùng** SDK trong dự án khác, hay người **phát
triển** chính SDK này.

### 1a. Dùng SDK trong một dự án khác (khuyến nghị)

Bạn **không cần `git clone`** — pip tự clone repo về thư mục tạm rồi build. Trong venv của
**dự án consumer**:

```bash
python -m venv .venv && source .venv/bin/activate

# core
pip install "git+https://github.com/aiop-aickh-a20-ai-eval-observe/Cost-Optimized-Eval.git"

# kèm extra (provider bạn cần) — cú pháp "<pkg>[extra] @ git+..."
pip install "llm-cost-optimizer[bedrock] @ git+https://github.com/aiop-aickh-a20-ai-eval-observe/Cost-Optimized-Eval.git"

# pin theo branch / tag / commit cho build ổn định (thêm @<ref> ở cuối URL)
pip install "llm-cost-optimizer[bedrock] @ git+https://github.com/aiop-aickh-a20-ai-eval-observe/Cost-Optimized-Eval.git@main"
```

Khai báo cố định trong `requirements.txt` của dự án consumer:

```
llm-cost-optimizer[bedrock] @ git+https://github.com/aiop-aickh-a20-ai-eval-observe/Cost-Optimized-Eval.git@main
```

Hoặc trong `pyproject.toml` (PEP 621):

```toml
[project]
dependencies = [
  "llm-cost-optimizer[bedrock] @ git+https://github.com/aiop-aickh-a20-ai-eval-observe/Cost-Optimized-Eval.git@main",
]
```

> - **Pin `@<ref>`** (tag/commit) cho production — không pin sẽ kéo HEAD của default branch,
>   build dễ trôi.
> - Repo **private** → máy cài phải có quyền: dùng PAT (`git+https://<token>@github.com/...`)
>   hoặc SSH (`git+ssh://git@github.com/aiop-aickh-a20-ai-eval-observe/Cost-Optimized-Eval.git`).
> - Consumer **không cần** extra `[dev]` — đó chỉ là pytest/ruff/black để test chính SDK.

### 1b. Phát triển chính SDK (editable)

Chỉ khi bạn muốn **sửa code SDK** và thấy thay đổi phản ánh ngay — clone rồi cài
**editable** (khớp `CLAUDE.md`):

```bash
git clone https://github.com/aiop-aickh-a20-ai-eval-observe/Cost-Optimized-Eval.git
cd Cost-Optimized-Eval
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"        # core + công cụ dev (pytest/ruff/black)
```

### Extras

Core chỉ phụ thuộc `httpx` + `pydantic`. Mỗi provider / tính năng nặng là một **extra**
riêng — thêm khi cần:

| Extra | Bật |
|-------|-----|
| `anthropic` | `AnthropicClient` |
| `openai` | `OpenAIClient` / `BedrockClient` OpenAI-compatible |
| `groq` | `GroqClient` (alias kéo về OpenAI SDK) |
| `google` | `GoogleClient` (Gemini, `google-genai`) |
| `bedrock` | `BedrockConverseClient` (boto3 Converse) |
| `azure` | `AzureOpenAIClient` |
| `semantic-cache` | semantic cache (fastembed) |
| `compression` | LLMLingua compression |
| `redis` | Redis cache backend |

Gộp nhiều extra: `[anthropic,openai,semantic-cache]`. Cú pháp tùy cách cài —
`"<pkg>[extra] @ git+..."` (consumer, §1a) hoặc `".[extra]"` (editable, §1b).

Sau khi cài, import bình thường ở bất kỳ đâu trong venv — không chạy trực tiếp file `src/`:

```python
from llm_cost_optimizer import EvalOptimizer   # chạy được vì đã cài vào venv
```

Yêu cầu Python ≥ 3.10.

---

## 2. Mô hình dữ liệu — 4 input + 1 output

Mọi lần gọi xoay quanh 4 input và trả về 1 output. Tất cả là Pydantic model, import
trực tiếp từ `llm_cost_optimizer`.

| Loại | Vai trò |
|------|---------|
| `Prompt` | Prompt judge đã tách cấu trúc để tối ưu |
| `ModelSpec` | Danh tính model + tham số sinh ảnh hưởng reproducibility |
| `RequestParams` | Tham số request của provider |
| `RunContext` | Định danh do caller cấp (run_id, version, metadata) |
| `InvocationResult` | Kết quả chuẩn hoá trả về |

```python
from llm_cost_optimizer import Prompt, ModelSpec, RequestParams, RunContext

prompt = Prompt(
    system="Bạn là factuality judge. Trả JSON {\"verdict\": \"yes|no\", ...}",
    static_context="<phần ít đổi: rubric, few-shot, reference>",  # dễ được prefix-cache
    dynamic_input="Câu hỏi: ...\nCâu trả lời ứng viên: ...",        # phần đổi mỗi sample
    optimization_profile="factuality",  # gate cho compression (xem §6)
)

model = ModelSpec(
    provider="bedrock",                  # khớp với client_factory của bạn
    model_id="amazon.nova-pro-v1:0",
    model_version="default",             # ⚠ ảnh hưởng cache key
    temperature=0.0,
    max_tokens=512,
)

request_params = RequestParams(
    response_format={"type": "json_object"},  # tuỳ provider
)

run_context = RunContext(
    run_id="run-2026-06-10",
    prompt_judge_version="judge-v1",     # ⚠ ảnh hưởng cache key
    metadata={                           # tự do — dùng cho cost breakdown
        "metric_id": "factuality",
        "skill_id": "factual_qa_vn",
        "sample_id": "sample-1a",
    },
)
```

**Lưu ý cache correctness:** kết quả cache chỉ được tái dùng khi `model_version` *và*
`prompt_judge_version` trùng khớp. Đổi rubric/judge → tăng `prompt_judge_version`;
đổi model thật → tăng `model_version`. Nếu không, cache sẽ trả verdict cũ.

`Prompt` và `ModelSpec` là **frozen** (immutable) vì chúng là input của cache key.

---

## 3. Tích hợp tối thiểu (offline, không tốn tiền)

Mặc định không cần API key: `EvalOptimizer` dùng `FakeModelClient`, mọi optimization
**mặc định TẮT**. Đây là baseline an toàn để verify wiring.

```python
from llm_cost_optimizer import EvalOptimizer

optimizer = EvalOptimizer()  # FakeModelClient + tất cả optimization OFF

result = optimizer.invoke(prompt, model, request_params, run_context)

print(result.status)      # Status.SUCCESS
print(result.response)    # text trả về
print(result.cost_usd)    # chi phí tính theo bảng giá nội bộ
```

---

## 4. Nối provider thật

SDK kèm sẵn 7 client. Tất cả import từ `llm_cost_optimizer.clients.*` (hoặc lazy từ
`llm_cost_optimizer.clients`):

| Client | `provider` gợi ý | Cài (extra) | API key đọc từ env |
|--------|------------------|-------------|--------------------|
| `AnthropicClient` | `anthropic` | `[anthropic]` | `ANTHROPIC_API_KEY` |
| `OpenAIClient` | `openai` | `[openai]` | `OPENAI_API_KEY` |
| `AzureOpenAIClient` | `azure`/`openai` | `[azure]` | `AZURE_OPENAI_API_KEY` |
| `BedrockConverseClient` | `bedrock` | `[bedrock]` | AWS creds (profile/SSO) |
| `BedrockClient` | `bedrock` | `[openai]` | `BEDROCK_API_KEY`, `BEDROCK_REGION` / `BEDROCK_BASE_URL` |
| `GroqClient` | `groq` | `[groq]` *(= OpenAI SDK)* | `GROQ_API_KEY` → fallback `OPENAI_API_KEY` |
| `GoogleClient` | `google` | `[google]` | `GOOGLE_API_KEY` |

> **Groq** chạy trên endpoint OpenAI-compatible (`https://api.groq.com/openai/v1`) nên
> dùng chung SDK `openai` — extra `[groq]` chỉ là alias kéo về `openai`. **Google/Gemini**
> dùng package `google-genai` qua extra `[google]`.

### 4a. Một provider

```python
from llm_cost_optimizer import EvalOptimizer
from llm_cost_optimizer.clients.anthropic import AnthropicClient

optimizer = EvalOptimizer(
    client=AnthropicClient(api_key="sk-...", prefix_cache_enabled=True),
)
```

Constructor các client thật:

```python
AnthropicClient(api_key=None, *, prefix_cache_enabled=False)
OpenAIClient(api_key=None, *, prefix_cache_enabled=False)
GroqClient(api_key=None, base_url=None, *, prefix_cache_enabled=False)
GoogleClient(api_key=None, *, prefix_cache_enabled=False)
AzureOpenAIClient(api_key=None, azure_ad_token_provider=None, azure_endpoint=None,
                  api_version=None, base_url=None, *, prefix_cache_enabled=False)
BedrockClient(api_key=None, region=None, base_url=None, *, prefix_cache_enabled=False)
BedrockConverseClient(region=None, profile_name=None, *, client=None,
                      timeout=30.0, prefix_cache_enabled=False)
```

(`api_key=None` → client đọc từ env mặc định của provider, xem bảng trên.)

> **Prefix cache có 2 lớp.** `OptimizerConfig(prefix_cache_enabled=True)` restructure
> prompt để phần static đứng đúng chỗ trong pipeline. Muốn provider thật ghi nhận cache
> billing / cache-control, client tương ứng cũng cần `prefix_cache_enabled=True` khi khởi tạo.

### 4b. Nhiều provider — `client_factory`

Khi dùng fallback/cascade qua nhiều provider, cấp một **factory** ánh xạ `ModelSpec → client`.
SDK gọi factory với spec của tier/fallback đang chạy:

```python
from llm_cost_optimizer.clients.anthropic import AnthropicClient
from llm_cost_optimizer.clients.openai import OpenAIClient
from llm_cost_optimizer.clients.groq import GroqClient
from llm_cost_optimizer.clients.google import GoogleClient
from llm_cost_optimizer.clients.base import ModelClient

_clients: dict[str, ModelClient] = {
    "anthropic": AnthropicClient(api_key="sk-ant-..."),
    "openai": OpenAIClient(api_key="sk-..."),
    "groq": GroqClient(api_key="gsk-..."),
    "google": GoogleClient(api_key="..."),
}

def client_factory(spec: ModelSpec) -> ModelClient:
    try:
        return _clients[spec.provider]
    except KeyError:
        raise ValueError(f"no client for provider {spec.provider}")

optimizer = EvalOptimizer(client_factory=client_factory)
```

`spec.provider` ở đây chính là chuỗi bạn đặt trong `ModelSpec(provider=...)` — nó chỉ là
khoá để factory chọn client, không bị SDK ràng buộc giá trị. Hãy cho khớp với
`allowed_providers` (§6).

> `client` (đơn) và `client_factory` (đa) là hai cách loại trừ nhau — chọn một.

### 4c. Tự viết client

Client chỉ cần thoả `ModelClient` protocol (`llm_cost_optimizer.clients.base`):

```python
class ModelClient(Protocol):
    def invoke(self, prompt, model_spec, request_params, run_context) -> InvocationResult: ...
    async def ainvoke(self, prompt, model_spec, request_params, run_context) -> InvocationResult: ...
```

Trả về `InvocationResult` với `usage` (token), `status`, `response`. SDK lo phần cost,
cache, trace.

### 4d. Public API nhanh

Các entrypoint chính nằm ở facade `EvalOptimizer`:

```python
class EvalOptimizer:
    def __init__(
        self,
        config: OptimizerConfig | None = None,
        client: ModelClient | None = None,
        client_factory: Callable[[ModelSpec], ModelClient] | None = None,
        confidence_fn: Callable[..., float] | None = None,
        log_backends: list[LogBackend] | None = None,
        cache: SemanticCache | None = None,
        shadow_agree_fn: Callable[[str, str], bool] | None = None,
        translator: TranslationService | None = None,
        price_table: dict[tuple[str, str, str], ModelPrice] | None = None,
    ): ...
```

```python
# sync
result = optimizer.invoke(prompt, model_spec, request_params, run_context)

# async
result = await optimizer.ainvoke(prompt, model_spec, request_params, run_context)

# concurrent batch; mỗi prompt vẫn đi qua pipeline đầy đủ
results = optimizer.invoke_many(
    prompts,
    model_spec=model_spec,          # optional nếu config.model_chain có primary
    request_params=request_params,
    run_context=run_context,
    concurrency=4,
)

# streaming
for chunk in optimizer.stream(prompt, model_spec, request_params, run_context): ...
async for chunk in optimizer.astream(prompt, model_spec, request_params, run_context): ...
```

---

## 5. Bật optimization

Tất cả optimization là **opt-in** qua `OptimizerConfig` và đều fall back an toàn về
provider call thường.

```python
from llm_cost_optimizer import OptimizerConfig

config = OptimizerConfig(
    prefix_cache_enabled=True,
    semantic_cache_enabled=True,
    compression_enabled=True,
    cascade_routing_enabled=True,
    provider_fallback_enabled=True,
    budget_cap_usd=5.00,
    on_budget_exceeded="raise",   # "raise" | "skip" | "warn"
)
optimizer = EvalOptimizer(config=config, client_factory=client_factory)
```

Các field cấu hình chính:

| Flag | Mặc định | Tác dụng |
|------|----------|----------|
| `prefix_cache_enabled` | `False` | Restructure prompt để tách phần static; muốn provider billing cache thật thì bật thêm `prefix_cache_enabled=True` trên client provider |
| `semantic_cache_enabled` | `False` | Dùng exact/semantic cache nếu có cache backend |
| `compression_enabled` | `False` | Nén dynamic prompt khi `compression_policy` cho phép profile đó |
| `cascade_routing_enabled` | `False` | Chạy `cascade_models` rẻ → đắt theo `confidence_fn` |
| `batch_enabled` | `False` | Chỉ dùng bởi `AsyncBatchClient` để chọn provider-side overnight batch; `invoke_many()` vẫn là concurrent runner |
| `early_stopping_enabled` | `False` | Flag cấu hình cho caller/orchestrator; SDK hiện cung cấp primitive Wilson-CI, chưa tự dừng `EvalOptimizer.invoke_many()` |
| `vi_en_translation_enabled` | `False` | Dịch prompt judge Vi→En khi có `translator` |
| `shadow_enabled` | `False` | Chạy baseline song song để đo agreement/drift |
| `provider_fallback_enabled` | `False` | Retry theo `model_chain` khi gặp `PROVIDER_ERROR` |
| `budget_cap_usd` | `None` | Trần chi phí phiên chạy; `None` là không giới hạn |
| `on_budget_exceeded` | `"raise"` | `"raise"` / `"skip"` / `"warn"` khi vượt budget |
| `semantic_cache_threshold` | `0.95` | Ngưỡng cosine semantic cache; SDK yêu cầu `> 0.9` |
| `cascade_confidence_threshold` | `0.7` | Dưới ngưỡng này cascade escalate lên model kế |
| `shadow_sample_rate` | `1.0` | Tỷ lệ call chạy thêm baseline shadow |
| `allowed_providers` | `()` | Allowlist provider; rỗng nghĩa là cho phép tất cả |
| `model_chain` | `()` | Ordered chain: phần tử đầu primary, phần còn lại fallback |
| `cascade_models` | `()` | Ordered chain cho cascade routing, thường rẻ → đắt |
| `shadow_baseline_model` | `None` | Model baseline dùng khi `shadow_enabled=True` |

`early_stopping_enabled` chưa làm `EvalOptimizer.invoke_many()` tự dừng. Project hiện có
primitive Wilson-CI trong `llm_cost_optimizer.sampling.early_stopping`; caller/orchestrator tự
đếm pass/fail và gọi `should_stop(...)` để quyết định dừng eval loop.

### Preset có sẵn

`llm_cost_optimizer.presets.presets` cung cấp config dựng sẵn:

```python
from llm_cost_optimizer.presets.presets import (
    ci_safe,             # CI: ưu tiên đúng & reproducible, budget overrun → raise
    offline_cost_saving, # batch offline: bật tối đa cache/compression/cascade, overrun → skip
    shadow_calibration,  # so sánh model mới vs baseline, overrun → warn
)
optimizer = EvalOptimizer(config=ci_safe, client_factory=client_factory)
```

---

## 6. Routing: chọn thứ tự provider (primary + fallback)

Việc chọn thứ tự provider gồm **2 mảnh ghép tách rời**, nối nhau qua chuỗi `provider`:

| Mảnh | Trả lời | Khai báo ở đâu |
|------|---------|----------------|
| `model_chain` | **Thứ tự** + danh tính model (primary → fallback) | `OptimizerConfig` |
| `client_factory` | **Client nào** (đang cầm key) chạy mỗi spec | truyền vào `EvalOptimizer` |

SDK đi dọc `model_chain` theo thứ tự; với mỗi `ModelSpec` nó gọi `client_factory(spec)`
để lấy instance client tương ứng rồi invoke. Primary trả `PROVIDER_ERROR` → nhảy sang
spec kế trong chain (lọc theo `allowed_providers`).

> **Vì sao tách 2 mảnh?** SDK **không giữ key** và **không** có registry `provider → client`.
> Bạn tự tạo instance client (cầm key), rồi `client_factory` map chuỗi `provider` sang đúng
> instance. Còn *thứ tự* nằm hoàn toàn ở `model_chain` — đổi thứ tự không đụng factory.

### Ví dụ end-to-end

```python
from llm_cost_optimizer import EvalOptimizer, OptimizerConfig, ModelSpec
from llm_cost_optimizer.clients.anthropic import AnthropicClient
from llm_cost_optimizer.clients.openai import OpenAIClient
from llm_cost_optimizer.clients.bedrock import BedrockConverseClient
from llm_cost_optimizer.clients.base import ModelClient

# 1) BẠN tạo instance client (cầm key/credential)
_anthropic = AnthropicClient(api_key="sk-ant-...")
_openai = OpenAIClient(api_key="sk-...")
_bedrock = BedrockConverseClient(region="us-east-1", profile_name="my-sso")

# 2) factory: map chuỗi provider -> instance đã tạo
def client_factory(spec: ModelSpec) -> ModelClient:
    return {
        "anthropic": _anthropic,
        "openai": _openai,
        "bedrock": _bedrock,
    }[spec.provider]

# 3) THỨ TỰ provider = thứ tự trong model_chain (head=primary, tail=fallback)
m_anthropic = ModelSpec(provider="anthropic", model_id="claude-haiku-4-5-20251001", model_version="v1")
m_openai = ModelSpec(provider="openai", model_id="gpt-4o-mini", model_version="v1")
m_bedrock = ModelSpec(provider="bedrock", model_id="amazon.nova-pro-v1:0", model_version="default")

config = OptimizerConfig(
    provider_fallback_enabled=True,                        # ⚠ bắt buộc, nếu không sẽ KHÔNG fallback
    allowed_providers=("anthropic", "openai", "bedrock"),  # tùy chọn allowlist
    model_chain=(m_anthropic, m_openai, m_bedrock),        # thử anthropic → openai → bedrock
)

optimizer = EvalOptimizer(config=config, client_factory=client_factory)
result = optimizer.invoke(prompt, request_params=rp, run_context=rc)
print(result.fallback_chain)  # vd ["anthropic/claude-haiku-4-5-20251001", "openai/gpt-4o-mini"]
```

### Đổi thứ tự = đổi đúng một dòng

```python
# Ưu tiên Bedrock trước, rồi OpenAI, rồi Anthropic:
model_chain=(m_bedrock, m_openai, m_anthropic)
```

Chỉ hoán vị `model_chain` — **không đụng `client_factory`**. Không có field nào khác chi
phối thứ tự này.

### 3 điểm dễ vướng

1. **`provider_fallback_enabled=True`** mới thực sự thử fallback; nếu `False`, primary lỗi
   là trả `PROVIDER_ERROR` luôn.
2. **Chuỗi `provider` phải khớp** giữa `ModelSpec.provider`, key trong `client_factory`, và
   `allowed_providers`. Lệch một chỗ → factory `KeyError` hoặc bị allowlist chặn.
3. **`model_spec` của `invoke` là tùy chọn** — bỏ trống thì primary = `model_chain[0]`; nếu
   truyền thì nó override primary còn fallback vẫn là `model_chain[1:]`. Vừa không truyền
   `model_spec` vừa để `model_chain` rỗng → `ValueError`.

```python
# Cả hai tương đương khi model_chain[0] == primary:
optimizer.invoke(prompt, request_params=rp, run_context=rc)   # dùng chain head
optimizer.invoke(prompt, m_anthropic, rp, rc)                 # truyền primary tường minh
```

> **Hai biến thể Bedrock.** `BedrockConverseClient` (boto3 converse) và `BedrockClient`
> (OpenAI-compat) mặc định cùng mang `provider="bedrock"` nên factory không phân biệt được.
> Muốn xếp thứ tự cả hai độc lập: đặt chuỗi `provider` khác nhau (vd `"bedrock_converse"`
> vs `"bedrock_openai"` — trường `provider` là string tự do, SDK không ép danh sách cố
> định), khai báo trong `allowed_providers` + branch trong factory như hai provider riêng.

---

## 7. Cascade routing (rẻ trước, escalate khi thiếu tự tin)

Bật `cascade_routing_enabled` + cấp `cascade_models` (rẻ → đắt) + một `confidence_fn`.
SDK chạy model rẻ nhất trước; nếu confidence < `cascade_confidence_threshold` (mặc định
`0.7`, chỉnh trong `OptimizerConfig`) thì escalate lên model kế tiếp. Nếu **mọi** cascade
tier đều thiếu tự tin, SDK fall back về gọi thẳng model được yêu cầu (`model_spec` /
`model_chain[0]`) — không trả về kết quả low-confidence.

```python
from llm_cost_optimizer.routing.cascade import ConfidenceDecision

def confidence_fn(result) -> ConfidenceDecision:
    # caller tự định nghĩa "đủ tự tin" — SDK chỉ route theo score trả về
    import json
    try:
        parsed = json.loads(result.response)
    except Exception:
        return ConfidenceDecision(score=0.0, reason="invalid_json")
    if parsed.get("verdict") not in ("yes", "no"):
        return ConfidenceDecision(score=0.0, reason="missing_verdict")
    return ConfidenceDecision(score=1.0, reason="valid")

config = OptimizerConfig(
    cascade_routing_enabled=True,
    cascade_models=(cheap_model, mid_model, strong_model),
    cascade_confidence_threshold=0.7,   # tuỳ chọn — ngưỡng escalate
)
optimizer = EvalOptimizer(config=config, client_factory=client_factory,
                          confidence_fn=confidence_fn)
```

`confidence_fn` có thể trả `float`, `(score, reason)`, hoặc `ConfidenceDecision`.

> ⚠ Bật cascade mà **không** cấp `confidence_fn` → confidence mặc định `1.0`, tức model
> rẻ nhất luôn thắng và không bao giờ escalate. SDK ghi cảnh báo vào trace
> (`message` của stage `cascade_routing`) nhưng vẫn chạy — hãy luôn cấp `confidence_fn`
> khi dùng cascade thật.

> ⚠ Cascade route theo `cascade_models`; fallback route theo `model_chain`. Hai cơ chế
> độc lập — đừng nhầm.

---

## 8. Semantic cache

Bật `semantic_cache_enabled=True` là đủ để có cache mặc định: khi không truyền `cache=`,
SDK tự dựng một `SemanticCache` in-memory dùng `config.semantic_cache_threshold` (mặc định
`0.95`) và embedder hashing không cần dependency. Ngưỡng phải `> 0.9` (SDK ép buộc) để
tránh hit nhầm.

```python
config = OptimizerConfig(semantic_cache_enabled=True, semantic_cache_threshold=0.97)
optimizer = EvalOptimizer(config=config, client_factory=client_factory)  # cache tự dựng
```

Muốn kiểm soát backend/embedder (Redis, fastembed…) thì tự cấp `cache=` — injection
tường minh luôn thắng config. Lưu ý: `backend_choice` khác `"memory"` **không** auto-dựng
được (SDK raise `ValueError`) — các backend đó phải inject tường minh:

```python
from llm_cost_optimizer.cache.semantic import SemanticCache, FastEmbedEmbedder, HashingNgramEmbedder
from llm_cost_optimizer.cache.backends.memory import MemoryCacheBackend

cache = SemanticCache(
    backend=MemoryCacheBackend(),     # hoặc RedisCacheBackend(url=...)
    threshold=0.95,
    embedder=FastEmbedEmbedder(),     # cần extra [semantic-cache]; fallback HashingNgramEmbedder
)

config = OptimizerConfig(semantic_cache_enabled=True)
optimizer = EvalOptimizer(config=config, cache=cache, client_factory=client_factory)
```

Lookup là **exact-hash trước, semantic sau**. Cache key phụ thuộc `model_version` +
`prompt_judge_version` (xem §2).

> Cảnh báo dữ liệu: nếu dataset có các cặp prompt **gần giống nhưng verdict ngược nhau**
> (ví dụ cùng context, câu trả lời đúng vs sai), hãy đặt `threshold` cao (≈0.99) kẻo cache
> trả verdict sai.

---

## 9. Đọc kết quả

```python
result = optimizer.invoke(prompt, model, request_params, run_context)

result.response        # str: nội dung model trả
result.status          # Status enum (xem dưới)
result.cost_usd        # float: chi phí thực
result.usage           # Usage: input_uncached / input_cached / output / cache_read / cache_write
result.cache_info      # CacheInfo: tier ("none"|"exact"|"semantic"|"prefix"), hit, similarity
result.model_spec      # model thực sự đã trả lời (có thể là fallback/cascade tier)
result.fallback_chain  # list[str] các model đã thử
result.trace.stages    # list[OptimizationTrace]: từng stage đã làm gì
```

`Status` taxonomy:

| Status | Nghĩa |
|--------|-------|
| `SUCCESS` | gọi thành công bình thường |
| `CACHE_HIT` | trả từ semantic/exact cache |
| `FALLBACK_SUCCESS` | primary lỗi → một fallback thành công |
| `OPTIMIZATION_FAILED_FALLBACK` | primary lỗi và mọi fallback trong `model_chain` cũng lỗi |
| `PROVIDER_ERROR` | provider lỗi, không có fallback |
| `BUDGET_SKIPPED` | vượt budget với `on_budget_exceeded="skip"` |

Trace giúp debug: mỗi stage có `stage`, `enabled`, `applied`, `status`, `detail`.

---

## 10. Chạy nhiều prompt (concurrent / provider batch)

### 10a. Concurrent runner qua `invoke_many`

```python
results = optimizer.invoke_many(
    prompts=[p1, p2, p3, ...],
    model_spec=model,          # tuỳ chọn — bỏ trống dùng model_chain[0]
    request_params=request_params,
    run_context=run_context,
    concurrency=8,
)
```

Trả về `list[InvocationResult]` cùng thứ tự input. Mỗi item đi qua **đầy đủ pipeline**
như `invoke()` (budget, cache, fallback, logging). Gọi được cả từ bên trong một event
loop đang chạy (FastAPI, Jupyter) — SDK tự chạy batch trên worker thread riêng khi cần.

`invoke_many()` không dùng provider-side overnight batch; nó là runner concurrent trong
process, phù hợp CI / demo / batch nhỏ cần kết quả ngay.

### 10b. Provider-side async/overnight batch

Provider batch thật nằm ở `AsyncBatchClient`, không phải `EvalOptimizer.invoke_many()`.
Đường này trả `job_id` trước, poll kết quả sau qua `BatchPoller`/`JobStore`.

```python
from llm_cost_optimizer.batch.api_batch import AsyncBatchClient
from llm_cost_optimizer.batch.job_store import SqliteJobStore
from llm_cost_optimizer.batch.providers.registry import default_provider_factory
from llm_cost_optimizer.batch.runner import BatchItem, BatchRunner

config = OptimizerConfig(batch_enabled=True, workload="offline_scheduled")
runner = BatchRunner(optimizer=optimizer, max_concurrency=8)
batch_client = AsyncBatchClient(
    config=config,
    job_store=SqliteJobStore("batch_jobs.db"),
    provider_factory=default_provider_factory,
    runner=runner,  # fallback khi workload/provider không dùng được async batch
)

items = [
    BatchItem(
        prompt=p,
        model_spec=model,
        request_params=request_params,
        run_context=run_context,
    )
    for p in prompts
]
job_id = batch_client.submit_many(items)
```

Async provider batch chỉ được chọn khi `workload="offline_scheduled"`,
`batch_enabled=True`, và provider báo `supports_batch=True`. Nếu không, SDK fallback về
`BatchRunner` và lưu kết quả ngay trong job store. Nếu bật cả `batch_enabled` và
`prefix_cache_enabled`, SDK cảnh báo vì overnight batch không dùng được provider-side
prefix cache.

---

## 11. Streaming response (UI realtime)

Cho UI nơi QA/QC chạy eval và muốn thấy phán quyết của judge hiện dần theo thời gian
thực. Dùng `stream()` (sync) hoặc `astream()` (async) thay cho `invoke()`. Cả hai trả về
iterator các `StreamChunk`:

- chunk thường: `text` = delta văn bản, `done=False`;
- chunk cuối: `done=True`, `result` = `InvocationResult` đầy đủ (usage/cost/trace).

```python
# async — hợp với web/UI platform
async for chunk in optimizer.astream(prompt, request_params=rp, run_context=rc):
    if chunk.done:
        final = chunk.result        # InvocationResult: cost, usage, trace, status
    else:
        ui.append(chunk.text)       # render delta lên màn hình

# sync — generator thường
for chunk in optimizer.stream(prompt, model, rp, rc):
    if not chunk.done:
        print(chunk.text, end="", flush=True)
    else:
        final = chunk.result
```

Ghép mọi `chunk.text` (các chunk chưa `done`) lại == đúng `final.response`.
SDK preserve cả whitespace khi phát lại response từ cache / non-streaming client.

> **Tự động tắt feature xung đột.** `cascade_routing` và `shadow` bị tự tắt trong
> stream (chúng cần *toàn bộ* output trước khi quyết định escalate / so sánh).
> SDK ghi trace `status="skipped"` + một warning trong `final.trace.warnings`
> để minh bạch. Các stage **vẫn chạy**: budget, prompt transform, prefix-cache,
> semantic-cache, provider-fallback.

**Hành vi từng nhánh:**
- **Cache hit** → phát lại text đã cache dạng stream rồi `done` (status `CACHE_HIT`).
- **Budget skip** → chỉ 1 chunk `done` duy nhất (status `BUDGET_SKIPPED`), không có text.
- **Fallback bật** → SDK buffer từng attempt cho tới khi biết attempt đó thành công.
  Nếu primary lỗi sau khi đã sinh partial text, partial đó bị discard; SDK phát text
  của fallback thành công để giữ invariant `chunk.text` ghép lại == `final.response`.
  `final` có `status=FALLBACK_SUCCESS` và `fallback_chain`.
- **Fallback fail hết** → chỉ trả terminal chunk với
  `status=OPTIMIZATION_FAILED_FALLBACK`; partial text của các attempt lỗi không được emit.
- **Fallback tắt** → nếu provider lỗi giữa stream sau khi đã emit partial text,
  terminal chunk có `status=PROVIDER_ERROR` và `final.response` bằng đúng phần text đã emit.
- **Cache store** → stream chỉ ghi semantic/exact cache cho `SUCCESS`; kết quả
  `FALLBACK_SUCCESS` không được cache dưới key của primary model.

> **Mức hỗ trợ provider.** Tất cả real client đi kèm đều stream **native
> token-by-token** qua `stream()/astream()`: `OpenAIClient` (và các subclass
> OpenAI-compatible `GroqClient`/`AzureOpenAIClient`/`BedrockClient`),
> `AnthropicClient`, `GoogleClient` (Gemini), và `BedrockConverseClient`. Client
> **chưa** hỗ trợ streaming native sẽ **tự fallback**: SDK gọi `invoke()` rồi phát
> cả response thành *một* chunk — vẫn đúng API, chỉ không token-by-token.
> `FakeModelClient` cũng mô phỏng stream (đủ cho test/offline). Nếu
> `provider_fallback_enabled=True`, facade vẫn buffer từng attempt trước khi emit
> dù provider client bên dưới có native token stream.

---

## 12. Budget & cost reporting

```python
config = OptimizerConfig(budget_cap_usd=10.0, on_budget_exceeded="raise")
```

- `"raise"` → ném `llm_cost_optimizer.client.BudgetExceededError` khi vượt cap.
- `"skip"` → trả `Status.BUDGET_SKIPPED`, không gọi provider.
- `"warn"` → log cảnh báo rồi vẫn chạy.

> Vượt budget là **control flow có chủ đích**, không phải fallback của optimization.

`BudgetExceededError` chỉ được raise khi `on_budget_exceeded="raise"`:

```python
from llm_cost_optimizer.client import BudgetExceededError

try:
    result = optimizer.invoke(prompt, model, request_params, run_context)
except BudgetExceededError:
    break  # caller quyết định dừng eval run và báo partial results
```

`Status.PROVIDER_ERROR` không raise exception; caller kiểm tra status sau mỗi call:

```python
result = optimizer.invoke(prompt, model, request_params, run_context)
if result.status == Status.PROVIDER_ERROR:
    failed_samples.append(run_context.metadata["sample_id"])
    continue
```

Cách enforce: trước mỗi call SDK **ước lượng chi phí** từ bảng giá và *reserve* atomic
(thread-safe, an toàn với `invoke_many` concurrent) — call đầu tiên *sẽ vượt* cap đã bị
chặn ngay, không đợi tiêu xong mới biết. Cache hit giải phóng phần reserve (không tốn
budget).

> ⚠ **Giới hạn đã biết:** model không có trong bảng giá thì không ước lượng được —
> SDK chỉ check hồi tố (`spent >= cap`) kèm warning trong `trace.warnings`, và cost
> thực của các call đó không cộng vào budget. Dùng model ngoài bảng giá mặc định →
> cấp bảng giá riêng:

```python
from llm_cost_optimizer.tracking.cost import DEFAULT_PRICE_TABLE, ModelPrice

optimizer = EvalOptimizer(
    config=config,
    client_factory=client_factory,
    price_table={
        **DEFAULT_PRICE_TABLE,   # price_table THAY THẾ bảng mặc định — merge nếu vẫn cần nó
        ("myprovider", "my-model", "*"): ModelPrice(input_per_mtok=1.0, output_per_mtok=3.0),
    },
)
```

Tổng hợp chi phí sau khi chạy:

```python
from llm_cost_optimizer.tracking.cost import aggregate, estimate_cost
from llm_cost_optimizer.tracking.attribution import attribute_savings

estimate_cost(prompt, model)                 # dry-run trước khi gọi
aggregate(results, group_by=("metric_id", "skill_id", "sample_id"))
attribute_savings(results)                   # tách tiết kiệm theo từng optimization
```

`metadata` trong `RunContext` (§2) chính là các field bạn `group_by` được.

### Log backend

Mặc định `EvalOptimizer` ghi JSONL vào `optimizer_logs.jsonl`. Truyền backend riêng nếu
muốn đổi nơi lưu, hoặc truyền list rỗng để tắt logging:

```python
from llm_cost_optimizer.tracking.log_backends.jsonl import JsonlLogBackend

optimizer = EvalOptimizer(
    config=config,
    client_factory=client_factory,
    log_backends=[JsonlLogBackend("runs/eval_logs.jsonl")],
)

optimizer_no_logs = EvalOptimizer(config=config, client_factory=client_factory, log_backends=[])
```

> ⚠ Đọc `attribute_savings`/`reduction_pct` cẩn thận: % tiết kiệm được đo so với một
> **baseline đối chứng = chạy model "requested" (primary) trên toàn bộ tokens gốc, không
> cache, không nén**. Con số cao thường phản ánh chênh giá giữa primary đắt và tier rẻ,
> *cộng* với độ dễ của dataset — không tách rời đánh đổi accuracy.

---

## 13. Shadow mode (đối chiếu / phát hiện drift)

Chạy thêm một baseline model bên cạnh đường optimized để đo mức đồng thuận. Kết quả trả
về vẫn là của đường optimized; baseline chỉ phục vụ so sánh.

```python
config = OptimizerConfig(
    shadow_enabled=True,
    shadow_baseline_model=baseline_model,
    shadow_sample_rate=0.1,   # chỉ 10% call chạy baseline; mặc định 1.0 (mọi call)
)

def agree_fn(optimized: str, baseline: str) -> bool:
    return optimized.strip() == baseline.strip()  # caller định nghĩa "đồng thuận"

optimizer = EvalOptimizer(config=config, client_factory=client_factory,
                          shadow_agree_fn=agree_fn)
```

Kết quả shadow nằm trong `result.trace.stages` (stage `"shadow"`, có `agreement`,
`cost_baseline_usd`, `diff` khi bất đồng; call không được sample có `status="skipped"`).
Theo dõi drift tích luỹ qua cửa sổ trượt:

```python
optimizer.shadow_drift()
# {"window_size": ..., "agreement_rate": 0.97, "alert": False, "alert_threshold": 0.95}
```

> Hai điều cần biết khi bật shadow:
> 1. **Chi phí**: baseline là provider call thật và **được cộng vào budget**. Với
>    `shadow_sample_rate=1.0`, cost mỗi call tăng gấp ~đôi — hạ sample rate khi chạy lớn.
> 2. **Latency**: baseline chạy *đồng bộ* trong call được sample (để agreement/diff nằm
>    ngay trong trace của kết quả), nên latency call đó cộng thêm thời gian baseline.

---

## 14. Ví dụ end-to-end

```python
from llm_cost_optimizer import EvalOptimizer, OptimizerConfig, ModelSpec, Prompt, RequestParams, RunContext
from llm_cost_optimizer.clients.bedrock import BedrockConverseClient
from llm_cost_optimizer.clients.base import ModelClient

primary = ModelSpec(provider="bedrock", model_id="amazon.nova-pro-v1:0",
                    model_version="default", max_tokens=512)
fallback = ModelSpec(provider="bedrock", model_id="amazon.nova-lite-v1:0",
                     model_version="default", max_tokens=512)

_bedrock = BedrockConverseClient(region="us-east-1", prefix_cache_enabled=True)
def client_factory(spec: ModelSpec) -> ModelClient:
    return _bedrock

config = OptimizerConfig(
    prefix_cache_enabled=True,
    provider_fallback_enabled=True,
    allowed_providers=("bedrock",),
    model_chain=(primary, fallback),   # primary → fallback
    budget_cap_usd=5.0,
    on_budget_exceeded="raise",
)

optimizer = EvalOptimizer(config=config, client_factory=client_factory)

prompt = Prompt(
    system="Bạn là factuality judge. Trả JSON {\"verdict\": ...}.",
    static_context="Cần Thơ là thành phố lớn nhất ĐBSCL.",
    dynamic_input="Câu hỏi: Cần Thơ thuộc vùng nào?\nỨng viên: ĐBSCL.",
    optimization_profile="factuality",
)
run_context = RunContext(run_id="run-1", prompt_judge_version="judge-v1",
                         metadata={"metric_id": "factuality", "sample_id": "s1"})

result = optimizer.invoke(prompt, request_params=RequestParams(), run_context=run_context)
print(result.status, result.cost_usd, result.fallback_chain)
```

---

## 15. Design principles

**SDK không biết business logic eval của bạn.** `invoke()` trả về `response` thô. Caller
tự parse verdict, tính accuracy, quyết định pass/fail, aggregate kết quả.

**Optimization là opt-in.** `OptimizerConfig` mặc định tắt mọi optimization. Một
`EvalOptimizer()` mới là đường pass-through an toàn: gọi model, chuẩn hoá result, log nếu
không tắt logging.

**Schema kết quả ổn định giữa các config.** Dù response đến từ cache, fallback hay
cascade, các field top-level như `result.response`, `result.status`, `result.cost_usd`,
`result.usage`, `result.trace` luôn tồn tại. Khác biệt về cách tạo result nằm trong
`result.trace.stages`.

---