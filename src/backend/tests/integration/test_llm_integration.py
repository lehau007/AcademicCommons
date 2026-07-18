from __future__ import annotations

import pytest

from app.config import Settings
from app.llm import (
    BedrockProvider,
    GeminiProvider,
    GroqProvider,
    ProviderResult,
)
from app.llm.router import build_llm_router

# Ensure integration tests only run if the necessary credentials are set
settings = Settings()
has_bedrock = bool(settings.bedrock_model_id)
has_gemini = bool(settings.gemini_api_key)
has_groq = bool(settings.groq_api_key)

pytestmark = pytest.mark.skipif(
    not (has_bedrock and has_gemini and has_groq),
    reason="Missing credentials/configurations for Bedrock, Gemini, or Groq integration tests.",
)


@pytest.mark.asyncio
async def test_direct_provider_chat_bedrock() -> None:
    settings = Settings()
    provider = BedrockProvider(
        model=settings.bedrock_model_id,
        region=settings.aws_region,
        api_key=settings.bedrock_api_key,
        base_url=settings.bedrock_base_url,
        profile=settings.aws_profile,
    )
    result = await provider.chat(
        [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello in one word."},
        ],
        max_tokens=10,
    )
    assert isinstance(result, ProviderResult)
    assert result.content.strip() != ""
    assert result.provider == "bedrock"


@pytest.mark.asyncio
async def test_direct_provider_chat_gemini() -> None:
    settings = Settings()
    provider = GeminiProvider(
        api_key=settings.gemini_api_key,
        model=settings.gemini_model,
    )
    result = await provider.chat(
        [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello in one word."},
        ],
        max_tokens=10,
    )
    assert isinstance(result, ProviderResult)
    assert result.content.strip() != ""
    assert result.provider == "gemini"


@pytest.mark.asyncio
async def test_direct_provider_chat_groq() -> None:
    settings = Settings()
    provider = GroqProvider(
        api_key=settings.groq_api_key,
        model=settings.groq_model,
    )
    result = await provider.chat(
        [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello in one word."},
        ],
        max_tokens=10,
    )
    assert isinstance(result, ProviderResult)
    assert result.content.strip() != ""
    assert result.provider == "groq"


@pytest.mark.asyncio
async def test_llm_router_chat_optimizer_disabled() -> None:
    settings = Settings(
        llm_optimizer_enabled=False,
        llm_provider_order="bedrock,gemini,groq",
    )
    router = build_llm_router(settings)
    
    result = await router.chat(
        [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello in one word."},
        ],
        max_tokens=10,
    )
    assert isinstance(result, ProviderResult)
    assert result.content.strip() != ""
    # Should route to the first provider in order, which is Bedrock
    assert result.provider == "bedrock"
    assert "optimizer_status" not in result.metadata


@pytest.mark.asyncio
async def test_llm_router_chat_optimizer_enabled() -> None:
    settings = Settings(
        llm_optimizer_enabled=True,
        llm_optimizer_enabled_flows="tutor",
        llm_provider_order="bedrock,gemini,groq",
    )
    router = build_llm_router(settings)
    
    result = await router.chat(
        [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello in one word."},
        ],
        max_tokens=10,
        flow="tutor",
    )
    assert isinstance(result, ProviderResult)
    assert result.content.strip() != ""
    assert result.provider == "bedrock"
    assert "optimizer_status" in result.metadata
    assert result.metadata["optimizer_status"] in ("SUCCESS", "CACHE_HIT", "FALLBACK_SUCCESS")


@pytest.mark.asyncio
async def test_llm_router_fallback_flow_optimizer_disabled() -> None:
    settings = Settings(
        llm_optimizer_enabled=False,
        # Force Bedrock to fail by setting bedrock_model_id to an invalid ID
        bedrock_model_id="amazon.nonexistent-model-v1:0",
        llm_provider_order="bedrock,gemini,groq",
    )
    router = build_llm_router(settings)
    
    result = await router.chat(
        [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello in one word."},
        ],
        max_tokens=10,
    )
    assert isinstance(result, ProviderResult)
    assert result.content.strip() != ""
    # Handled fallback by routing to Gemini
    assert result.provider == "gemini"


@pytest.mark.asyncio
async def test_llm_router_fallback_flow_optimizer_enabled() -> None:
    settings = Settings(
        llm_optimizer_enabled=True,
        llm_optimizer_enabled_flows="tutor",
        # Force Bedrock to fail by setting bedrock_model_id to an invalid ID
        bedrock_model_id="amazon.nonexistent-model-v1:0",
        llm_provider_order="bedrock,gemini,groq",
    )
    router = build_llm_router(settings)
    
    result = await router.chat(
        [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello in one word."},
        ],
        max_tokens=10,
        flow="tutor",
    )
    assert isinstance(result, ProviderResult)
    assert result.content.strip() != ""
    # Handled fallback by routing to Gemini
    assert result.provider == "gemini"
    assert "optimizer_status" in result.metadata
    assert result.metadata["optimizer_status"] in ("SUCCESS", "CACHE_HIT", "FALLBACK_SUCCESS")
    # Verify fallback_chain is empty in metadata, indicating fallback was handled by LLMRouter and not optimizer SDK
    assert result.metadata.get("fallback_chain") == []
