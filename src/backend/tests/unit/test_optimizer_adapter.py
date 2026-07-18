from __future__ import annotations

from collections.abc import AsyncIterator

import pytest

from app.config import Settings
from app.llm.optimizer_adapter import OptimizerAdapter, OptimizerProviderBinding, OptimizerSDK
from app.llm.providers import ChatMessage, LLMProvider, LLMUnavailable, ProviderResult, StreamChunk
from app.llm.router import LLMRouter

# --- Fake optimizer SDK -----------------------------------------------------

class _Kw:
    def __init__(self, **kwargs: object) -> None:
        self.__dict__.update(kwargs)


class _Usage:
    input_uncached = 10
    input_cached = 2
    output = 5


class _CacheInfo:
    tier = "none"
    hit = False


class _Trace:
    stages: list = []


class _Invocation:
    def __init__(self, response: str = "answer", status: str = "SUCCESS") -> None:
        self.response = response
        self.status = status
        self.usage = _Usage()
        self.cost_usd = 0.0012
        self.model_spec = _Kw(provider="gemini", model_id="model-x")
        self.cache_info = _CacheInfo()
        self.trace = _Trace()
        self.fallback_chain: list[str] = []


class _StreamChunk:
    def __init__(self, text: str = "", done: bool = False, result: object | None = None) -> None:
        self.text = text
        self.done = done
        self.result = result


class _BudgetExceededError(Exception):
    pass


class _FakeOptimizer:
    def __init__(self, *, config: object = None, client_factory: object = None,
                 log_backends: object = None, price_table: object = None) -> None:
        self.config = config
        self.log_backends = log_backends
        self.price_table = price_table
        self.status = "SUCCESS"

    async def ainvoke(self, prompt, model_spec, *, request_params, run_context):  # noqa: ANN001
        return _Invocation(status=self.status)

    async def astream(self, prompt, model_spec, *, request_params, run_context):  # noqa: ANN001
        for piece in ("an", "swer"):
            yield _StreamChunk(text=piece)
        yield _StreamChunk(done=True, result=_Invocation(response="answer", status=self.status))


def _fake_sdk(optimizer_cls: type = _FakeOptimizer) -> OptimizerSDK:
    return OptimizerSDK(
        EvalOptimizer=optimizer_cls,
        OptimizerConfig=_Kw,
        Prompt=_Kw,
        ModelSpec=_Kw,
        RequestParams=_Kw,
        RunContext=_Kw,
        BudgetExceededError=_BudgetExceededError,
        AzureOpenAIClient=_Kw,
        GoogleClient=_Kw,
        GroqClient=_Kw,
        BedrockConverseClient=_Kw,
        BedrockClient=_Kw,
        JsonlLogBackend=_Kw,
        ModelPrice=_Kw,
        DEFAULT_PRICE_TABLE={},
    )


def _adapter(optimizer_cls: type = _FakeOptimizer) -> OptimizerAdapter:
    settings = Settings(_env_file=None, llm_optimizer_enabled=True, llm_optimizer_logging_enabled=False)
    binding = OptimizerProviderBinding(
        provider_name="gemini",
        model_id="model-x",
        model_version="v1",
        build_client=lambda sdk: object(),
    )
    return OptimizerAdapter(sdk=_fake_sdk(optimizer_cls), settings=settings, provider_bindings=[binding])


class _StubProvider(LLMProvider):
    def __init__(self, provider_name: str) -> None:
        self.provider_name = provider_name
        self.model = "model-x"

    async def chat(self, messages, *, schema=None, max_tokens=None):  # noqa: ANN001
        raise NotImplementedError


_MESSAGES: list[ChatMessage] = [{"role": "user", "content": "hi"}]


# --- adapter.chat / adapter.stream ------------------------------------------

@pytest.mark.asyncio
async def test_adapter_chat_returns_provider_result() -> None:
    result = await _adapter().chat(_StubProvider("gemini"), _MESSAGES, flow_name="tutor")
    assert result.content == "answer"
    assert result.tokens_in == 12  # input_uncached + input_cached
    assert result.tokens_out == 5
    assert result.metadata["optimizer_status"] == "SUCCESS"


@pytest.mark.asyncio
async def test_adapter_chat_raises_on_non_success_status() -> None:
    class _Failing(_FakeOptimizer):
        def __init__(self, **kwargs: object) -> None:
            super().__init__(**kwargs)
            self.status = "PROVIDER_ERROR"

    with pytest.raises(RuntimeError, match="PROVIDER_ERROR"):
        await _adapter(_Failing).chat(_StubProvider("gemini"), _MESSAGES, flow_name="tutor")


@pytest.mark.asyncio
async def test_adapter_stream_emits_deltas_then_done() -> None:
    chunks = [c async for c in _adapter().stream(_StubProvider("gemini"), _MESSAGES, flow_name="tutor")]
    text = "".join(c.text for c in chunks if not c.done)
    assert text == "answer"
    assert chunks[-1].done is True
    assert chunks[-1].result is not None
    assert chunks[-1].result.content == "answer"


@pytest.mark.asyncio
async def test_adapter_unknown_provider_raises() -> None:
    with pytest.raises(RuntimeError, match="no binding"):
        await _adapter().chat(_StubProvider("openai"), _MESSAGES, flow_name="tutor")


def test_build_price_table_merges_overrides_over_defaults() -> None:
    settings = Settings(
        _env_file=None,
        llm_optimizer_enabled=True,
        llm_optimizer_logging_enabled=False,
        llm_optimizer_price_table_json='{"gemini:gemini-x":[0.1,0.4]}',
    )
    binding = OptimizerProviderBinding("gemini", "gemini-x", "v1", build_client=lambda sdk: object())
    adapter = OptimizerAdapter(sdk=_fake_sdk(), settings=settings, provider_bindings=[binding])

    table = adapter._price_table
    assert table is not None
    assert ("gemini", "gemini-x", "*") in table
    assert table[("gemini", "gemini-x", "*")].input_per_mtok == 0.1


def test_build_price_table_none_when_unset() -> None:
    assert _adapter()._price_table is None


def test_settings_treats_inline_comment_value_as_unset() -> None:
    settings = Settings(_env_file=None, bedrock_base_url="   # optional, defaults to https://x")
    assert settings.bedrock_base_url is None


# --- router.stream ----------------------------------------------------------

class _FakeProvider(LLMProvider):
    def __init__(self, provider_name: str, result: ProviderResult | None) -> None:
        self.provider_name = provider_name
        self.model = "model-x"
        self._result = result
        self.calls = 0

    async def chat(self, messages, *, schema=None, max_tokens=None):  # noqa: ANN001
        self.calls += 1
        if self._result is None:
            raise RuntimeError(f"{self.provider_name} failed")
        return self._result


def _result(provider: str, content: str = "full answer") -> ProviderResult:
    return ProviderResult(content=content, tokens_in=1, tokens_out=1, latency_ms=1,
                          cost_usd=0.0, provider=provider, model="model-x")


@pytest.mark.asyncio
async def test_router_stream_without_optimizer_emits_single_delta_then_done() -> None:
    provider = _FakeProvider("gemini", _result("gemini", "hello world"))
    router = LLMRouter([provider])

    chunks = [c async for c in router.stream(_MESSAGES, flow="tutor")]

    assert [c.text for c in chunks if not c.done] == ["hello world"]
    assert chunks[-1].done and chunks[-1].result.content == "hello world"


@pytest.mark.asyncio
async def test_router_stream_falls_back_before_emitting() -> None:
    failing = _FakeProvider("azure", None)
    ok = _FakeProvider("gemini", _result("gemini", "recovered"))
    router = LLMRouter([failing, ok])

    chunks = [c async for c in router.stream(_MESSAGES, flow="tutor")]

    assert failing.calls == 1 and ok.calls == 1
    assert chunks[-1].result.content == "recovered"


@pytest.mark.asyncio
async def test_router_stream_uses_optimizer_when_enabled_for_flow() -> None:
    class _FakeAdapter:
        async def stream(  # noqa: ANN001
            self, provider, messages, *, schema=None, max_tokens=None, flow_name=None
        ) -> AsyncIterator[StreamChunk]:
            yield StreamChunk(text="opt ")
            yield StreamChunk(text="answer")
            yield StreamChunk(done=True, result=_result("gemini", "opt answer"))

    settings = Settings(_env_file=None, llm_optimizer_enabled=True, llm_optimizer_enabled_flows="tutor")
    router = LLMRouter([_FakeProvider("gemini", _result("gemini"))],
                       settings=settings, optimizer_adapter=_FakeAdapter())

    chunks = [c async for c in router.stream(_MESSAGES, flow="tutor")]

    assert "".join(c.text for c in chunks if not c.done) == "opt answer"
    assert chunks[-1].done


@pytest.mark.asyncio
async def test_router_stream_raises_when_all_providers_fail() -> None:
    router = LLMRouter([_FakeProvider("azure", None), _FakeProvider("gemini", None)])
    with pytest.raises(LLMUnavailable):
        [c async for c in router.stream(_MESSAGES, flow="tutor")]
