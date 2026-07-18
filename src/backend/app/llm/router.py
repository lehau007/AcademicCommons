from __future__ import annotations

import logging
from collections.abc import AsyncIterator, Callable
from typing import Any

from app.config import Settings
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
    GroqProvider,
    LLMProvider,
    LLMUnavailable,
    OpenCodeProvider,
    OpenRouterProvider,
    ProviderResult,
    StreamChunk,
)

logger = logging.getLogger(__name__)


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
    ) -> ProviderResult:
        failures: list[str] = []
        for provider in self.providers:
            try:
                if (
                    self._optimizer_adapter is not None
                    and self._settings is not None
                    and self._settings.llm_optimizer_enabled_for_flow(flow)
                ):
                    return await self._optimizer_adapter.chat(
                        provider,
                        messages,
                        schema=schema,
                        max_tokens=max_tokens,
                        flow_name=flow,
                    )
                return await provider.chat(messages, schema=schema, max_tokens=max_tokens)
            except RuntimeError as exc:
                failures.append(f"{provider.provider_name}: {exc}")
                logger.warning("chat provider %s failed: %s", provider.provider_name, exc)
        logger.error("chat: all providers failed: %s", "; ".join(failures))
        raise LLMUnavailable("; ".join(failures) or "No LLM providers configured")

    async def stream(
        self,
        messages: list[ChatMessage],
        *,
        schema: dict[str, Any] | None = None,
        max_tokens: int | None = None,
        flow: str | None = None,
    ) -> AsyncIterator[StreamChunk]:
        failures: list[str] = []
        use_optimizer = (
            self._optimizer_adapter is not None
            and self._settings is not None
            and self._settings.llm_optimizer_enabled_for_flow(flow)
        )
        for provider in self.providers:
            emitted = False
            try:
                if use_optimizer:
                    assert self._optimizer_adapter is not None
                    async for chunk in self._optimizer_adapter.stream(
                        provider, messages, schema=schema, max_tokens=max_tokens, flow_name=flow
                    ):
                        emitted = True
                        yield chunk
                        if chunk.done:
                            return
                    return
                # No optimizer for this flow: use the provider's own streaming
                # (OpenCode streams natively; others fall back to a single delta).
                async for chunk in provider.stream(messages, schema=schema, max_tokens=max_tokens):
                    emitted = True
                    yield chunk
                    if chunk.done:
                        return
                return
            except RuntimeError as exc:
                failures.append(f"{provider.provider_name}: {exc}")
                logger.warning("stream provider %s failed: %s", provider.provider_name, exc)
                if emitted:
                    # Already streamed partial output; cannot cleanly switch providers.
                    raise LLMUnavailable("; ".join(failures)) from exc
        logger.error("stream: all providers failed: %s", "; ".join(failures))
        raise LLMUnavailable("; ".join(failures) or "No LLM providers configured")


def build_llm_router(settings: Settings) -> LLMRouter:
    available: dict[str, Callable[[], LLMProvider]] = {}
    optimizer_bindings: dict[str, OptimizerProviderBinding] = {}
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
    if settings.groq_api_key:
        groq_api_key = settings.groq_api_key
        available["groq"] = lambda: GroqProvider(api_key=groq_api_key, model=settings.groq_model)
        optimizer_bindings["groq"] = OptimizerProviderBinding(
            provider_name="groq",
            model_id=settings.groq_model,
            model_version=settings.llm_optimizer_model_version,
            build_client=lambda sdk: sdk.GroqClient(
                api_key=groq_api_key,
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
