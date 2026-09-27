from __future__ import annotations

import logging
import time
from collections.abc import AsyncIterator, Callable
from typing import Any

from app.config import Settings
from app.llm.observability import log_event
from app.llm.optimizer_adapter import (
    OptimizerAdapter,
    OptimizerProviderBinding,
    build_optimizer_adapter,
)
from app.llm.providers import (
    AzureOpenAIProvider,
    BedrockProvider,
    ChatMessage,
    GeminiProvider,
    LLMProvider,
    LLMUnavailable,
    OpenCodeProvider,
    OpenRouterProvider,
    ProviderResult,
    StreamChunk,
    VertexGeminiProvider,
)

logger = logging.getLogger(__name__)


def _safe_log_event(event: str, *, level: int = logging.INFO, **fields: object) -> None:
    try:
        log_event(logger, event, level=level, **fields)
    except Exception:
        pass


def _stream_success_fields(
    provider: LLMProvider,
    result: ProviderResult | None,
    *,
    flow: str | None,
    session_id: str | None,
    schema_enabled: bool,
    max_tokens: int | None,
    started: float,
) -> dict[str, object]:
    return {
        "mode": "stream",
        "flow": flow,
        "session_id": session_id,
        "provider": result.provider if result is not None else provider.provider_name,
        "model": result.model if result is not None else getattr(provider, "model", "unknown"),
        "schema_enabled": schema_enabled,
        "max_tokens": max_tokens,
        "latency_ms": result.latency_ms if result is not None else round((time.perf_counter() - started) * 1000),
        "tokens_in": result.tokens_in if result is not None else None,
        "tokens_out": result.tokens_out if result is not None else None,
    }


class LLMRouter:
    def __init__(
        self,
        providers: list[LLMProvider],
        *,
        settings: Settings | None = None,
        optimizer_adapter: OptimizerAdapter | None = None,
    ) -> None:
        self.providers = providers
        self._settings = settings
        self._optimizer_adapter = optimizer_adapter

    async def chat(
        self,
        messages: list[ChatMessage],
        *,
        schema: dict[str, Any] | None = None,
        max_tokens: int | None = None,
        flow: str | None = None,
        session_id: str | None = None,
    ) -> ProviderResult:
        failures: list[str] = []
        for index, provider in enumerate(self.providers):
            started = time.perf_counter()
            _safe_log_event(
                "llm_call_start",
                mode="chat",
                flow=flow,
                session_id=session_id,
                provider=provider.provider_name,
                model=getattr(provider, "model", "unknown"),
                schema_enabled=schema is not None,
                max_tokens=max_tokens,
            )
            try:
                if (
                    self._optimizer_adapter is not None
                    and self._settings is not None
                    and self._settings.llm_optimizer_enabled_for_flow(flow)
                ):
                    result = await self._optimizer_adapter.chat(
                        provider,
                        messages,
                        schema=schema,
                        max_tokens=max_tokens,
                        flow_name=flow,
                    )
                else:
                    result = await provider.chat(messages, schema=schema, max_tokens=max_tokens)
                _safe_log_event(
                    "llm_call_success",
                    mode="chat",
                    flow=flow,
                    session_id=session_id,
                    provider=result.provider,
                    model=result.model,
                    schema_enabled=schema is not None,
                    max_tokens=max_tokens,
                    latency_ms=result.latency_ms,
                    tokens_in=result.tokens_in,
                    tokens_out=result.tokens_out,
                )
                return result
            except RuntimeError as exc:
                failures.append(f"{provider.provider_name}: {exc}")
                _safe_log_event(
                    "llm_call_error",
                    level=logging.WARNING,
                    mode="chat",
                    flow=flow,
                    session_id=session_id,
                    provider=provider.provider_name,
                    model=getattr(provider, "model", "unknown"),
                    schema_enabled=schema is not None,
                    max_tokens=max_tokens,
                    latency_ms=round((time.perf_counter() - started) * 1000),
                    exception_type=type(exc).__name__,
                )
                if index < len(self.providers) - 1:
                    _safe_log_event(
                        "llm_fallback",
                        mode="chat",
                        flow=flow,
                        session_id=session_id,
                        provider=provider.provider_name,
                        model=getattr(provider, "model", "unknown"),
                        schema_enabled=schema is not None,
                        max_tokens=max_tokens,
                        next_provider=self.providers[index + 1].provider_name,
                    )
        raise LLMUnavailable("; ".join(failures) or "No LLM providers configured")

    async def stream(
        self,
        messages: list[ChatMessage],
        *,
        schema: dict[str, Any] | None = None,
        max_tokens: int | None = None,
        flow: str | None = None,
        session_id: str | None = None,
    ) -> AsyncIterator[StreamChunk]:
        failures: list[str] = []
        use_optimizer = (
            self._optimizer_adapter is not None
            and self._settings is not None
            and self._settings.llm_optimizer_enabled_for_flow(flow)
        )
        for index, provider in enumerate(self.providers):
            emitted = False
            result: ProviderResult | None = None
            started = time.perf_counter()
            _safe_log_event(
                "llm_call_start",
                mode="stream",
                flow=flow,
                session_id=session_id,
                provider=provider.provider_name,
                model=getattr(provider, "model", "unknown"),
                schema_enabled=schema is not None,
                max_tokens=max_tokens,
            )
            try:
                if use_optimizer:
                    assert self._optimizer_adapter is not None
                    async for chunk in self._optimizer_adapter.stream(
                        provider, messages, schema=schema, max_tokens=max_tokens, flow_name=flow
                    ):
                        emitted = True
                        if chunk.result is not None:
                            result = chunk.result
                        yield chunk
                        if chunk.done:
                            _safe_log_event(
                                "llm_call_success",
                                **_stream_success_fields(
                                    provider,
                                    result,
                                    flow=flow,
                                    session_id=session_id,
                                    schema_enabled=schema is not None,
                                    max_tokens=max_tokens,
                                    started=started,
                                ),
                            )
                            return
                    _safe_log_event(
                        "llm_call_success",
                        **_stream_success_fields(
                            provider,
                            result,
                            flow=flow,
                            session_id=session_id,
                            schema_enabled=schema is not None,
                            max_tokens=max_tokens,
                            started=started,
                        ),
                    )
                    return
                # No optimizer for this flow: use the provider's own streaming
                # (OpenCode streams natively; others fall back to a single delta).
                async for chunk in provider.stream(messages, schema=schema, max_tokens=max_tokens):
                    emitted = True
                    if chunk.result is not None:
                        result = chunk.result
                    yield chunk
                    if chunk.done:
                        _safe_log_event(
                            "llm_call_success",
                            **_stream_success_fields(
                                provider,
                                result,
                                flow=flow,
                                session_id=session_id,
                                schema_enabled=schema is not None,
                                max_tokens=max_tokens,
                                started=started,
                            ),
                        )
                        return
                _safe_log_event(
                    "llm_call_success",
                    **_stream_success_fields(
                        provider,
                        result,
                        flow=flow,
                        session_id=session_id,
                        schema_enabled=schema is not None,
                        max_tokens=max_tokens,
                        started=started,
                    ),
                )
                return
            except RuntimeError as exc:
                failures.append(f"{provider.provider_name}: {exc}")
                _safe_log_event(
                    "llm_call_error",
                    level=logging.WARNING,
                    mode="stream",
                    flow=flow,
                    session_id=session_id,
                    provider=provider.provider_name,
                    model=getattr(provider, "model", "unknown"),
                    schema_enabled=schema is not None,
                    max_tokens=max_tokens,
                    latency_ms=round((time.perf_counter() - started) * 1000),
                    exception_type=type(exc).__name__,
                )
                if emitted:
                    # Already streamed partial output; cannot cleanly switch providers.
                    raise LLMUnavailable("; ".join(failures)) from exc
                if index < len(self.providers) - 1:
                    _safe_log_event(
                        "llm_fallback",
                        mode="stream",
                        flow=flow,
                        session_id=session_id,
                        provider=provider.provider_name,
                        model=getattr(provider, "model", "unknown"),
                        schema_enabled=schema is not None,
                        max_tokens=max_tokens,
                        next_provider=self.providers[index + 1].provider_name,
                    )
        raise LLMUnavailable("; ".join(failures) or "No LLM providers configured")


def build_llm_router(settings: Settings) -> LLMRouter:
    available: dict[str, Callable[[], LLMProvider]] = {}
    optimizer_bindings: dict[str, OptimizerProviderBinding] = {}
    available["vertex"] = lambda: VertexGeminiProvider(
        model=settings.vertex_chat_model,
        location=settings.vertex_genai_location,
        project_id=settings.vertex_project_id,
        thinking_level=settings.vertex_chat_thinking_level or None,
    )
    if settings.azure_ai_api_key and settings.azure_openai_endpoint and settings.azure_openai_deployment:

        azure_api_key = settings.azure_ai_api_key
        azure_endpoint = settings.azure_openai_endpoint
        azure_deployment = settings.azure_openai_deployment
        available["azure"] = lambda: AzureOpenAIProvider(
            endpoint=azure_endpoint,
            deployment=azure_deployment,
            api_key=azure_api_key,
            api_version=settings.azure_openai_api_version,
        )
        optimizer_bindings["azure"] = OptimizerProviderBinding(
            provider_name="azure",
            model_id=azure_deployment,
            model_version=settings.llm_optimizer_model_version,
            build_client=lambda sdk: sdk.AzureOpenAIClient(
                api_key=azure_api_key,
                azure_endpoint=azure_endpoint,
                api_version=settings.azure_openai_api_version,
                prefix_cache_enabled=settings.llm_optimizer_prefix_cache_enabled,
            ),
        )
    if settings.gemini_api_key:
        gemini_api_key = settings.gemini_api_key
        available["gemini"] = lambda: GeminiProvider(api_key=gemini_api_key, model=settings.gemini_model)
        optimizer_bindings["gemini"] = OptimizerProviderBinding(
            provider_name="gemini",
            model_id=settings.gemini_model,
            model_version=settings.llm_optimizer_model_version,
            build_client=lambda sdk: sdk.GoogleClient(
                api_key=gemini_api_key,
                prefix_cache_enabled=settings.llm_optimizer_prefix_cache_enabled,
            ),
        )
    if settings.opencode_api_key:
        opencode_api_key = settings.opencode_api_key
        available["opencode"] = lambda: OpenCodeProvider(
            api_key=opencode_api_key,
            model=settings.opencode_model,
            base_url=settings.opencode_base_url,
        )
        # No optimizer binding: OpenCode is not wired into the eval_optimizer SDK.
    if settings.openrouter_api_key:
        openrouter_api_key = settings.openrouter_api_key
        available["openrouter"] = lambda: OpenRouterProvider(
            api_key=openrouter_api_key,
            model=settings.openrouter_model,
            base_url=settings.openrouter_base_url,
        )
        # No optimizer binding: OpenRouter is not wired into the eval_optimizer SDK.
    if settings.bedrock_model_id:
        bedrock_model_id = settings.bedrock_model_id
        if settings.bedrock_api_key:
            available["bedrock"] = lambda: BedrockProvider(
                model=bedrock_model_id,
                region=settings.aws_region,
                api_key=settings.bedrock_api_key,
                base_url=settings.bedrock_base_url,
            )
            optimizer_bindings["bedrock"] = OptimizerProviderBinding(
                provider_name="bedrock",
                model_id=bedrock_model_id,
                model_version=settings.llm_optimizer_model_version,
                build_client=lambda sdk: sdk.BedrockClient(
                    api_key=settings.bedrock_api_key,
                    region=settings.aws_region,
                    base_url=settings.bedrock_base_url,
                    prefix_cache_enabled=settings.llm_optimizer_prefix_cache_enabled,
                ),
            )
        else:
            available["bedrock"] = lambda: BedrockProvider(
                model=bedrock_model_id,
                region=settings.aws_region,
                profile=settings.aws_profile,
            )
            optimizer_bindings["bedrock"] = OptimizerProviderBinding(
                provider_name="bedrock",
                model_id=bedrock_model_id,
                model_version=settings.llm_optimizer_model_version,
                build_client=lambda sdk: sdk.BedrockConverseClient(
                    region=settings.aws_region,
                    profile_name=settings.aws_profile,
                    prefix_cache_enabled=settings.llm_optimizer_prefix_cache_enabled,
                ),
            )

    providers: list[LLMProvider] = []
    ordered_optimizer_bindings: list[OptimizerProviderBinding] = []
    seen: set[str] = set()
    for name in settings.llm_provider_order_list:
        if name in available and name not in seen:
            seen.add(name)
            try:
                provider = available[name]()
            except Exception:
                logger.warning("Skipping LLM provider %r: failed to initialize", name, exc_info=True)
                continue
            providers.append(provider)
            if name in optimizer_bindings:
                ordered_optimizer_bindings.append(optimizer_bindings[name])

    optimizer_adapter = build_optimizer_adapter(
        settings,
        provider_bindings=ordered_optimizer_bindings,
    )
    return LLMRouter(providers, settings=settings, optimizer_adapter=optimizer_adapter)
