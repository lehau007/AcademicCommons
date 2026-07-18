from typing import Any

import pytest

from app.config import Settings
from app.llm import (
    AzureOpenAIProvider,
    BedrockProvider,
    DeterministicEmbeddingService,
    GeminiProvider,
    GroqProvider,
    LLMProvider,
    LLMRouter,
    LLMUnavailable,
    OpenCodeProvider,
    OpenRouterProvider,
    ProviderResult,
)
from app.llm.router import build_llm_router


class FakeOpenAIUsage:
    prompt_tokens = 3
    completion_tokens = 2


class FakeOpenAIMessage:
    content = "{\"ok\": true}"


class FakeOpenAIChoice:
    message = FakeOpenAIMessage()


class FakeOpenAIResponse:
    choices = [FakeOpenAIChoice()]
    usage = FakeOpenAIUsage()


class FakeOpenAICompletions:
    def __init__(self) -> None:
        self.captured: dict[str, Any] = {}

    async def create(self, **kwargs: Any) -> FakeOpenAIResponse:
        self.captured = kwargs
        return FakeOpenAIResponse()


class FakeOpenAIChat:
    def __init__(self) -> None:
        self.completions = FakeOpenAICompletions()


class FakeOpenAIClient:
    def __init__(self) -> None:
        self.chat = FakeOpenAIChat()


class FakeThinkMessage:
    content = "<think>reasoning...</think>\nfinal answer"


class FakeThinkChoice:
    message = FakeThinkMessage()


class FakeThinkResponse:
    choices = [FakeThinkChoice()]
    usage = FakeOpenAIUsage()


class FakeThinkCompletions:
    def __init__(self) -> None:
        self.captured: dict[str, Any] = {}

    async def create(self, **kwargs: Any) -> FakeThinkResponse:
        self.captured = kwargs
        return FakeThinkResponse()


class FakeThinkChat:
    def __init__(self) -> None:
        self.completions = FakeThinkCompletions()


class FakeThinkClient:
    def __init__(self) -> None:
        self.chat = FakeThinkChat()


class FakeGeminiUsage:
    prompt_token_count = 4
    candidates_token_count = 5


class FakeGeminiResponse:
    text = "gemini result"
    usage_metadata = FakeGeminiUsage()


class FakeGeminiModels:
    def __init__(self) -> None:
        self.captured: dict[str, Any] = {}

    def generate_content(self, **kwargs: Any) -> FakeGeminiResponse:
        self.captured = kwargs
        return FakeGeminiResponse()


class FakeGeminiClient:
    def __init__(self) -> None:
        self.models = FakeGeminiModels()


class FakeBedrockClient:
    def __init__(self, *, response: dict[str, Any] | None = None) -> None:
        self.captured: dict[str, Any] = {}
        self.response = response or {
            "output": {"message": {"content": [{"text": "nova result"}]}},
            "usage": {"inputTokens": 7, "outputTokens": 9},
        }

    def converse(self, **kwargs: Any) -> dict[str, Any]:
        self.captured = kwargs
        return self.response


class FakeProvider(LLMProvider):
    def __init__(self, provider_name: str, result: ProviderResult | None = None) -> None:
        self.provider_name = provider_name
        self.model = "fake-model"
        self.result = result
        self.calls = 0

    async def chat(self, messages, *, schema=None, max_tokens=None) -> ProviderResult:
        self.calls += 1
        if self.result is None:
            raise RuntimeError(f"{self.provider_name} failed")
        return self.result


class FakeOptimizerAdapter:
    def __init__(self) -> None:
        self.calls: list[str] = []

    async def chat(self, provider, messages, *, schema=None, max_tokens=None, flow_name=None) -> ProviderResult:
        self.calls.append(provider.provider_name)
        if provider.provider_name == "azure":
            raise RuntimeError("optimized provider failed")
        return ProviderResult(
            content="optimized fallback",
            tokens_in=1,
            tokens_out=1,
            latency_ms=1,
            cost_usd=0.0,
            provider=provider.provider_name,
            model=provider.model,
        )


@pytest.mark.asyncio
async def test_azure_provider_uses_openai_compatible_shape() -> None:
    client = FakeOpenAIClient()
    provider = AzureOpenAIProvider(
        endpoint="https://example.services.ai.azure.com/openai/v1",
        deployment="gpt-test",
        api_key="secret",
        api_version="2024-08-01-preview",
        client=client,
    )
    result = await provider.chat(
        [{"role": "user", "content": "hello"}],
        schema={"type": "object"},
        max_tokens=12,
    )

    captured = client.chat.completions.captured
    assert provider.endpoint == "https://example.services.ai.azure.com/openai/v1"
    assert captured["model"] == "gpt-test"
    assert captured["messages"] == [{"role": "user", "content": "hello"}]
    assert captured["max_tokens"] == 12
    assert captured["response_format"] == {
        "type": "json_schema",
        "json_schema": {"name": "structured_response", "schema": {"type": "object"}},
    }
    assert result.content == "{\"ok\": true}"
    assert result.tokens_in == 3
    assert result.tokens_out == 2
    assert result.provider == "azure"


def test_azure_provider_normalizes_resource_endpoint_to_openai_base_url() -> None:
    client = FakeOpenAIClient()
    provider = AzureOpenAIProvider(
        endpoint="https://example.services.ai.azure.com",
        deployment="gpt-test",
        api_key="secret",
        api_version="2024-08-01-preview",
        client=client,
    )

    assert provider.endpoint == "https://example.services.ai.azure.com/openai/v1"


@pytest.mark.asyncio
async def test_gemini_provider_uses_generate_content_shape() -> None:
    client = FakeGeminiClient()
    provider = GeminiProvider(api_key="secret", model="gemini-test", client=client)
    result = await provider.chat([{"role": "user", "content": "hello"}], schema={"type": "object"})

    captured = client.models.captured
    assert captured["model"] == "gemini-test"
    assert captured["contents"] == "user: hello"
    assert captured["config"].response_mime_type == "application/json"
    assert captured["config"].response_schema == {"type": "object"}
    assert result.content == "gemini result"
    assert result.tokens_in == 4
    assert result.tokens_out == 5


@pytest.mark.asyncio
async def test_groq_provider_uses_openai_shape() -> None:
    client = FakeOpenAIClient()
    provider = GroqProvider(api_key="secret", model="groq-test", client=client)
    result = await provider.chat([{"role": "user", "content": "hello"}], schema={"type": "object"})

    captured = client.chat.completions.captured
    assert captured["model"] == "groq-test"
    assert captured["messages"] == [{"role": "user", "content": "hello"}]
    assert captured["response_format"] == {"type": "json_object"}
    assert result.content == "{\"ok\": true}"


@pytest.mark.asyncio
async def test_opencode_provider_uses_openai_shape() -> None:
    client = FakeOpenAIClient()
    provider = OpenCodeProvider(api_key="secret", model="minimax-m3", client=client)
    result = await provider.chat([{"role": "user", "content": "hello"}], schema={"type": "object"})

    captured = client.chat.completions.captured
    assert captured["model"] == "minimax-m3"
    assert captured["messages"] == [{"role": "user", "content": "hello"}]
    assert captured["response_format"] == {"type": "json_object"}
    assert result.content == "{\"ok\": true}"
    assert result.provider == "opencode"


@pytest.mark.asyncio
async def test_opencode_provider_strips_think_block() -> None:
    client = FakeThinkClient()
    provider = OpenCodeProvider(api_key="secret", client=client)
    result = await provider.chat([{"role": "user", "content": "hello"}])

    assert result.content == "final answer"


class FakeFencedJsonMessage:
    # minimax-m3 ignores response_format=json_object: emits a <think> trace and
    # wraps the JSON in a ```json fence, so a bare json.loads() fails at char 0.
    content = '<think>let me judge</think>\n```json\n{"relevance": 8}\n```'


class FakeFencedJsonChoice:
    message = FakeFencedJsonMessage()


class FakeFencedJsonResponse:
    choices = [FakeFencedJsonChoice()]
    usage = FakeOpenAIUsage()


class FakeFencedJsonCompletions:
    async def create(self, **kwargs: Any) -> FakeFencedJsonResponse:
        return FakeFencedJsonResponse()


class FakeFencedJsonChat:
    def __init__(self) -> None:
        self.completions = FakeFencedJsonCompletions()


class FakeFencedJsonClient:
    def __init__(self) -> None:
        self.chat = FakeFencedJsonChat()


@pytest.mark.asyncio
async def test_opencode_provider_unwraps_json_fence_in_json_mode() -> None:
    import json

    client = FakeFencedJsonClient()
    provider = OpenCodeProvider(api_key="secret", client=client)
    result = await provider.chat(
        [{"role": "user", "content": "judge"}], schema={"type": "object"}
    )

    # Content must be parseable JSON, not a ```json-fenced string.
    assert json.loads(result.content) == {"relevance": 8}


@pytest.mark.asyncio
async def test_openrouter_provider_uses_openai_shape() -> None:
    client = FakeOpenAIClient()
    provider = OpenRouterProvider(api_key="secret", model="openai/gpt-5.4-mini", client=client)
    result = await provider.chat([{"role": "user", "content": "hello"}], schema={"type": "object"})

    captured = client.chat.completions.captured
    assert captured["model"] == "openai/gpt-5.4-mini"
    assert captured["messages"] == [{"role": "user", "content": "hello"}]
    assert captured["response_format"] == {"type": "json_object"}
    assert result.content == "{\"ok\": true}"
    assert result.provider == "openrouter"


@pytest.mark.asyncio
async def test_bedrock_provider_uses_converse_shape() -> None:
    client = FakeBedrockClient()
    provider = BedrockProvider(model="amazon.nova-lite-v1:0", region="us-east-1", client=client)
    result = await provider.chat(
        [
            {"role": "system", "content": "be terse"},
            {"role": "user", "content": "hello"},
        ],
        max_tokens=12,
    )

    captured = client.captured
    assert captured["modelId"] == "amazon.nova-lite-v1:0"
    assert captured["system"] == [{"text": "be terse"}]
    assert captured["messages"] == [{"role": "user", "content": [{"text": "hello"}]}]
    assert captured["inferenceConfig"] == {"maxTokens": 12}
    assert "toolConfig" not in captured
    assert result.content == "nova result"
    assert result.tokens_in == 7
    assert result.tokens_out == 9
    assert result.provider == "bedrock"


@pytest.mark.asyncio
async def test_bedrock_provider_uses_tool_use_for_structured_output() -> None:
    response = {
        "output": {"message": {"content": [{"toolUse": {"input": {"ok": True}}}]}},
        "usage": {"inputTokens": 1, "outputTokens": 2},
    }
    client = FakeBedrockClient(response=response)
    provider = BedrockProvider(model="amazon.nova-lite-v1:0", region="us-east-1", client=client)
    result = await provider.chat([{"role": "user", "content": "hello"}], schema={"type": "object"})

    captured = client.captured
    assert captured["toolConfig"]["tools"][0]["toolSpec"]["name"] == "structured_response"
    assert captured["toolConfig"]["tools"][0]["toolSpec"]["inputSchema"] == {"json": {"type": "object"}}
    assert captured["toolConfig"]["toolChoice"] == {"tool": {"name": "structured_response"}}
    assert result.content == "{\"ok\": true}"


def test_build_llm_router_respects_configured_order() -> None:
    settings = Settings(
        _env_file=None,
        azure_ai_api_key="azure-key",
        azure_openai_endpoint="https://example.services.ai.azure.com",
        azure_openai_deployment="gpt-test",
        gemini_api_key="gemini-key",
        groq_api_key="groq-key",
        bedrock_model_id="amazon.nova-lite-v1:0",
        llm_provider_order="bedrock,groq,gemini,azure",
    )

    router = build_llm_router(settings)

    assert [p.provider_name for p in router.providers] == ["bedrock", "groq", "gemini", "azure"]


def test_build_llm_router_defaults_to_bedrock_then_gemini_then_groq() -> None:
    settings = Settings(
        _env_file=None,
        azure_ai_api_key="azure-key",
        azure_openai_endpoint="https://example.services.ai.azure.com",
        azure_openai_deployment="gpt-test",
        gemini_api_key="gemini-key",
        groq_api_key="groq-key",
        bedrock_model_id="amazon.nova-lite-v1:0",
    )

    router = build_llm_router(settings)

    assert [p.provider_name for p in router.providers] == ["bedrock", "gemini", "groq"]


def test_build_llm_router_includes_opencode_when_configured() -> None:
    settings = Settings(
        _env_file=None,
        opencode_api_key="opencode-key",
        gemini_api_key="gemini-key",
        llm_provider_order="opencode,gemini",
    )

    router = build_llm_router(settings)

    assert [p.provider_name for p in router.providers] == ["opencode", "gemini"]


def test_build_llm_router_includes_openrouter_when_configured() -> None:
    settings = Settings(
        _env_file=None,
        openrouter_api_key="openrouter-key",
        gemini_api_key="gemini-key",
        llm_provider_order="openrouter,gemini",
    )

    router = build_llm_router(settings)

    assert [p.provider_name for p in router.providers] == ["openrouter", "gemini"]


def test_build_llm_router_skips_providers_without_credentials() -> None:
    settings = Settings(
        _env_file=None,
        gemini_api_key="gemini-key",
        llm_provider_order="bedrock,azure,gemini,groq",
    )

    router = build_llm_router(settings)

    assert [p.provider_name for p in router.providers] == ["gemini"]


def test_build_llm_router_skips_provider_that_fails_to_construct(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.llm.router as router_module

    class ExplodingBedrockProvider:
        def __init__(self, **kwargs: Any) -> None:
            raise Exception("The config profile () could not be found")  # noqa: TRY002

    monkeypatch.setattr(router_module, "BedrockProvider", ExplodingBedrockProvider)

    settings = Settings(
        _env_file=None,
        gemini_api_key="gemini-key",
        bedrock_model_id="amazon.nova-lite-v1:0",
        llm_provider_order="bedrock,gemini",
    )

    router = build_llm_router(settings)

    assert [p.provider_name for p in router.providers] == ["gemini"]


def test_optimizer_flow_allowlist_is_conservative() -> None:
    settings = Settings(
        _env_file=None,
        llm_optimizer_enabled=True,
        llm_optimizer_enabled_flows="tutor,mock-test",
    )

    assert settings.llm_optimizer_enabled_for_flow("tutor")
    assert settings.llm_optimizer_enabled_for_flow("mock_test")
    assert not settings.llm_optimizer_enabled_for_flow("mindmap")


def test_optimizer_profile_for_flow_uses_flow_specific_override() -> None:
    settings = Settings(
        _env_file=None,
        llm_optimizer_profile_default="default-profile",
        llm_optimizer_profile_tutor="rag-answering",
    )

    assert settings.llm_optimizer_profile_for_flow("tutor") == "rag-answering"
    assert settings.llm_optimizer_profile_for_flow("mindmap") == "default-profile"


def test_build_llm_router_keeps_legacy_route_when_optimizer_sdk_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.llm.optimizer_adapter as optimizer_adapter

    def missing_sdk() -> None:
        raise ModuleNotFoundError("llm_cost_optimizer")

    monkeypatch.setattr(optimizer_adapter, "_load_optimizer_sdk", missing_sdk)
    settings = Settings(
        _env_file=None,
        gemini_api_key="gemini-key",
        llm_provider_order="gemini",
        llm_optimizer_enabled=True,
        llm_optimizer_enabled_flows="tutor",
    )

    with pytest.warns(UserWarning, match="llm_cost_optimizer is not installed"):
        router = build_llm_router(settings)

    assert router._optimizer_adapter is None
    assert [p.provider_name for p in router.providers] == ["gemini"]


@pytest.mark.asyncio
async def test_router_falls_back_to_next_provider() -> None:
    result = ProviderResult(
        content="fallback",
        tokens_in=1,
        tokens_out=1,
        latency_ms=1,
        cost_usd=0.0,
        provider="gemini",
        model="fake-model",
    )
    first = FakeProvider("azure")
    second = FakeProvider("gemini", result=result)
    router = LLMRouter([first, second])

    actual = await router.chat([{"role": "user", "content": "hello"}])

    assert actual is result
    assert first.calls == 1
    assert second.calls == 1


@pytest.mark.asyncio
async def test_router_keeps_provider_fallback_when_optimizer_attempt_fails() -> None:
    settings = Settings(_env_file=None, llm_optimizer_enabled=True)
    first = FakeProvider("azure")
    second = FakeProvider("gemini")
    optimizer_adapter = FakeOptimizerAdapter()
    router = LLMRouter([first, second], settings=settings, optimizer_adapter=optimizer_adapter)

    actual = await router.chat([{"role": "user", "content": "hello"}], flow="tutor")

    assert actual.content == "optimized fallback"
    assert actual.provider == "gemini"
    assert optimizer_adapter.calls == ["azure", "gemini"]
    assert first.calls == 0
    assert second.calls == 0


@pytest.mark.asyncio
async def test_router_raises_when_all_providers_fail() -> None:
    router = LLMRouter([FakeProvider("azure"), FakeProvider("gemini")])

    with pytest.raises(LLMUnavailable):
        await router.chat([{"role": "user", "content": "hello"}])


def test_deterministic_embedding_returns_1024_dimensional_vectors() -> None:
    embeddings = DeterministicEmbeddingService().encode(["alpha", "beta"])

    assert len(embeddings) == 2
    assert len(embeddings[0]) == 1024
    assert len(embeddings[1]) == 1024
    assert embeddings[0] != embeddings[1]
