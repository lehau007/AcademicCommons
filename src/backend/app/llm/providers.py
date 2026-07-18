from __future__ import annotations

import asyncio
import json
import re
import time
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from dataclasses import dataclass, field, replace
from typing import Any, Protocol

from google import genai
from google.genai import types as genai_types
from openai import AsyncOpenAI

ChatMessage = dict[str, str]


@dataclass(frozen=True)
class ProviderResult:
    content: str
    tokens_in: int
    tokens_out: int
    latency_ms: int
    cost_usd: float
    provider: str
    model: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class StreamChunk:
    """One streamed step. Non-final chunks carry a text delta; the final chunk
    carries the full ProviderResult and ``done=True``. Concatenating every
    non-final ``text`` reproduces ``result.content``."""

    text: str = ""
    done: bool = False
    result: ProviderResult | None = None


class LLMUnavailable(RuntimeError):
    pass


class OpenAICompletionsClient(Protocol):
    async def create(self, **kwargs: Any) -> Any:
        raise NotImplementedError


class OpenAIChatClient(Protocol):
    completions: OpenAICompletionsClient


class OpenAICompatibleClient(Protocol):
    chat: OpenAIChatClient


class GeminiModelsClient(Protocol):
    def generate_content(self, **kwargs: Any) -> Any:
        raise NotImplementedError


class GeminiClient(Protocol):
    models: GeminiModelsClient


class LLMProvider(ABC):
    provider_name: str
    model: str

    @abstractmethod
    async def chat(
        self,
        messages: list[ChatMessage],
        *,
        schema: dict[str, Any] | None = None,
        max_tokens: int | None = None,
    ) -> ProviderResult:
        raise NotImplementedError

    async def stream(
        self,
        messages: list[ChatMessage],
        *,
        schema: dict[str, Any] | None = None,
        max_tokens: int | None = None,
    ) -> AsyncIterator[StreamChunk]:
        """Default: no native token streaming. Emit the full answer as a single
        delta then the final result. Providers with real streaming override this."""
        result = await self.chat(messages, schema=schema, max_tokens=max_tokens)
        if result.content:
            yield StreamChunk(text=result.content)
        yield StreamChunk(done=True, result=result)


class AzureOpenAIProvider(LLMProvider):
    provider_name = "azure"

    def __init__(
        self,
        *,
        endpoint: str,
        deployment: str,
        api_key: str,
        api_version: str,
        timeout: float = 30.0,
        client: OpenAICompatibleClient | None = None,
    ) -> None:
        self.api_key = api_key
        self.model = deployment
        self.timeout = timeout
        self.endpoint = _normalize_openai_base_url(endpoint)
        self.api_version = api_version
        self.client = client or AsyncOpenAI(base_url=self.endpoint, api_key=api_key, timeout=timeout)

    async def chat(
        self,
        messages: list[ChatMessage],
        *,
        schema: dict[str, Any] | None = None,
        max_tokens: int | None = None,
    ) -> ProviderResult:
        started = time.perf_counter()
        request: dict[str, Any] = {"model": self.model, "messages": messages}
        if max_tokens is not None:
            request["max_tokens"] = max_tokens
        if schema is not None:
            request["response_format"] = {
                "type": "json_schema",
                "json_schema": {"name": "structured_response", "schema": schema},
            }

        try:
            response = await self.client.chat.completions.create(**request)
        except Exception as exc:
            raise RuntimeError(f"Azure OpenAI client failed: {exc}") from exc
        return _openai_result(response, "azure", self.model, started)


class GroqProvider(LLMProvider):
    provider_name = "groq"

    def __init__(
        self,
        *,
        api_key: str,
        model: str = "meta-llama/llama-4-scout-17b-16e-instruct",
        timeout: float = 30.0,
        client: OpenAICompatibleClient | None = None,
    ) -> None:
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self.client = client or AsyncOpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=api_key,
            timeout=timeout,
        )

    async def chat(
        self,
        messages: list[ChatMessage],
        *,
        schema: dict[str, Any] | None = None,
        max_tokens: int | None = None,
    ) -> ProviderResult:
        started = time.perf_counter()
        request: dict[str, Any] = {"model": self.model, "messages": messages}
        if max_tokens is not None:
            request["max_tokens"] = max_tokens
        if schema is not None:
            request["response_format"] = {"type": "json_object"}

        try:
            response = await self.client.chat.completions.create(**request)
        except Exception as exc:
            raise RuntimeError(f"Groq client failed: {exc}") from exc
        return _openai_result(response, "groq", self.model, started)


class OpenCodeProvider(LLMProvider):
    """OpenCode (opencode.ai) Go-plan gateway. OpenAI-compatible; restricted model
    catalog (MiniMax/Kimi/GLM/DeepSeek/Qwen/MiMo/Hy families, no Claude/GPT/Gemini).
    Default model ``minimax-m3`` emits a leading ``<think>...</think>`` reasoning
    trace, which is stripped from the returned content."""

    provider_name = "opencode"

    def __init__(
        self,
        *,
        api_key: str,
        model: str = "minimax-m3",
        base_url: str = "https://opencode.ai/zen/go/v1",
        timeout: float = 90.0,
        client: OpenAICompatibleClient | None = None,
    ) -> None:
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self.client = client or AsyncOpenAI(
            base_url=base_url,
            api_key=api_key,
            timeout=timeout,
            max_retries=1,
        )

    async def chat(
        self,
        messages: list[ChatMessage],
        *,
        schema: dict[str, Any] | None = None,
        max_tokens: int | None = None,
    ) -> ProviderResult:
        started = time.perf_counter()
        request: dict[str, Any] = {"model": self.model, "messages": messages}
        if max_tokens is not None:
            request["max_tokens"] = max_tokens
        if schema is not None:
            request["response_format"] = {"type": "json_object"}

        try:
            response = await self.client.chat.completions.create(**request)
        except Exception as exc:
            raise RuntimeError(f"OpenCode client failed: {exc}") from exc
        result = _strip_think_block(_openai_result(response, "opencode", self.model, started))
        if schema is not None:
            result = replace(result, content=_unwrap_json_content(result.content))
        return result

    async def stream(
        self,
        messages: list[ChatMessage],
        *,
        schema: dict[str, Any] | None = None,
        max_tokens: int | None = None,
    ) -> AsyncIterator[StreamChunk]:
        """Native token streaming. Non-streamed, this model buffers a large
        ``<think>`` reasoning trace plus the answer and can exceed the client
        timeout for long answers; streaming keeps the socket alive (deltas arrive
        every <1s) so the request never hits a single long wall. A stateful filter
        suppresses the leading ``<think>...</think>`` block so the UI only sees the
        answer. JSON-mode (schema) is not streamed — fall back to the buffered path
        where ``_unwrap_json_content`` can post-process a complete payload."""
        if schema is not None:
            async for chunk in super().stream(messages, schema=schema, max_tokens=max_tokens):
                yield chunk
            return

        started = time.perf_counter()
        request: dict[str, Any] = {"model": self.model, "messages": messages, "stream": True}
        if max_tokens is not None:
            request["max_tokens"] = max_tokens

        think_filter = _ThinkStreamFilter()
        parts: list[str] = []
        usage: Any = None
        try:
            stream = await self.client.chat.completions.create(**request)
            async for event in stream:
                if getattr(event, "usage", None):
                    usage = event.usage
                if not getattr(event, "choices", None):
                    continue
                delta = event.choices[0].delta
                piece = getattr(delta, "content", None) if delta else None
                if not piece:
                    continue
                visible = think_filter.feed(piece)
                if visible:
                    parts.append(visible)
                    yield StreamChunk(text=visible)
        except Exception as exc:
            raise RuntimeError(f"OpenCode stream failed: {exc}") from exc

        tail = think_filter.flush()
        if tail:
            parts.append(tail)
            yield StreamChunk(text=tail)

        result = ProviderResult(
            content="".join(parts).strip(),
            tokens_in=int(getattr(usage, "prompt_tokens", 0) or 0),
            tokens_out=int(getattr(usage, "completion_tokens", 0) or 0),
            latency_ms=_elapsed_ms(started),
            cost_usd=0.0,
            provider="opencode",
            model=self.model,
        )
        yield StreamChunk(done=True, result=result)


class OpenRouterProvider(LLMProvider):
    """OpenRouter (openrouter.ai) gateway. OpenAI-compatible; aggregates hundreds
    of models across providers (OpenAI, Google, Meta, Mistral, etc). Default
    model ``openai/gpt-5.4-mini``, picked from a mid-priced candidate comparison
    (see tests/openrouter_api_doc.md) for its speed and OCR/vision accuracy."""

    provider_name = "openrouter"

    def __init__(
        self,
        *,
        api_key: str,
        model: str = "openai/gpt-5.4-mini",
        base_url: str = "https://openrouter.ai/api/v1",
        timeout: float = 45.0,
        client: OpenAICompatibleClient | None = None,
    ) -> None:
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self.client = client or AsyncOpenAI(base_url=base_url, api_key=api_key, timeout=timeout)

    async def chat(
        self,
        messages: list[ChatMessage],
        *,
        schema: dict[str, Any] | None = None,
        max_tokens: int | None = None,
    ) -> ProviderResult:
        started = time.perf_counter()
        request: dict[str, Any] = {"model": self.model, "messages": messages}
        if max_tokens is not None:
            request["max_tokens"] = max_tokens
        if schema is not None:
            request["response_format"] = {"type": "json_object"}

        try:
            response = await self.client.chat.completions.create(**request)
        except Exception as exc:
            raise RuntimeError(f"OpenRouter client failed: {exc}") from exc
        return _openai_result(response, "openrouter", self.model, started)


class GeminiProvider(LLMProvider):
    provider_name = "gemini"

    def __init__(
        self,
        *,
        api_key: str,
        model: str = "gemini-3.1-flash-lite",
        timeout: float = 30.0,
        client: GeminiClient | None = None,
    ) -> None:
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self.client = client or genai.Client(
            api_key=api_key,
            http_options=genai_types.HttpOptions(timeout=int(timeout * 1000)),
        )

    async def chat(
        self,
        messages: list[ChatMessage],
        *,
        schema: dict[str, Any] | None = None,
        max_tokens: int | None = None,
    ) -> ProviderResult:
        started = time.perf_counter()
        config: dict[str, Any] = {}
        if max_tokens is not None:
            config["max_output_tokens"] = max_tokens
        if schema is not None:
            config["response_mime_type"] = "application/json"
            config["response_schema"] = schema

        try:
            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model=self.model,
                contents=_messages_to_text(messages),
                config=genai_types.GenerateContentConfig(**config),
            )
        except Exception as exc:
            raise RuntimeError(f"Gemini client failed: {exc}") from exc
        usage = getattr(response, "usage_metadata", None)
        return ProviderResult(
            content=str(getattr(response, "text", "") or ""),
            tokens_in=int(getattr(usage, "prompt_token_count", 0) or 0),
            tokens_out=int(getattr(usage, "candidates_token_count", 0) or 0),
            latency_ms=_elapsed_ms(started),
            cost_usd=0.0,
            provider="gemini",
            model=self.model,
        )


class BedrockProvider(LLMProvider):
    provider_name = "bedrock"

    def __init__(
        self,
        *,
        model: str,
        region: str,
        api_key: str | None = None,
        base_url: str | None = None,
        profile: str | None = None,
        timeout: float = 30.0,
        client: Any | None = None,
    ) -> None:
        self.model = model
        self.region = region
        self.api_key = api_key
        self.profile = profile
        self.timeout = timeout
        if api_key:
            from openai import AsyncOpenAI

            resolved_base_url = base_url or f"https://bedrock-mantle.{region}.api.aws/v1"
            self.client = client or AsyncOpenAI(
                api_key=api_key,
                base_url=resolved_base_url,
                timeout=timeout,
            )
            self._mode = "api_key"
        else:
            self._mode = "boto3"
            if client is None:
                import os

                import boto3

                if profile:
                    session = boto3.Session(profile_name=profile, region_name=region)
                else:
                    # botocore reads AWS_PROFILE straight from the process env even
                    # when profile_name is omitted here, and treats "" as a literal
                    # (invalid) profile name. Scrub blank values defensively so a
                    # misconfigured container env can't crash session creation.
                    for env_key in ("AWS_PROFILE", "AWS_DEFAULT_PROFILE"):
                        if os.environ.get(env_key) == "":
                            os.environ.pop(env_key, None)
                    session = boto3.Session(region_name=region)
                client = session.client("bedrock-runtime")
            self.client = client

    async def chat(
        self,
        messages: list[ChatMessage],
        *,
        schema: dict[str, Any] | None = None,
        max_tokens: int | None = None,
    ) -> ProviderResult:
        started = time.perf_counter()
        request: dict[str, Any]
        if self._mode == "api_key":
            request = {"model": self.model, "messages": messages}
            if max_tokens is not None:
                request["max_tokens"] = max_tokens
            if schema is not None:
                request["response_format"] = {
                    "type": "json_schema",
                    "json_schema": {"name": "structured_response", "schema": schema},
                }

            try:
                response = await self.client.chat.completions.create(**request)
            except Exception as exc:
                raise RuntimeError(f"Bedrock API client failed: {exc}") from exc
            return _openai_result(response, "bedrock", self.model, started)
        else:
            system, conversation = _split_system_messages(messages)
            request = {"modelId": self.model, "messages": conversation}
            if system:
                request["system"] = [{"text": system}]
            if max_tokens is not None:
                request["inferenceConfig"] = {"maxTokens": max_tokens}
            if schema is not None:
                request["toolConfig"] = {
                    "tools": [
                        {
                            "toolSpec": {
                                "name": "structured_response",
                                "inputSchema": {"json": schema},
                            }
                        }
                    ],
                    "toolChoice": {"tool": {"name": "structured_response"}},
                }

            try:
                boto_client: Any = self.client
                response = await asyncio.to_thread(boto_client.converse, **request)
            except Exception as exc:
                raise RuntimeError(f"Bedrock client failed: {exc}") from exc
            return _bedrock_result(response, self.model, started, structured=schema is not None)


def _openai_result(response: Any, provider: str, model: str, started: float) -> ProviderResult:
    usage = getattr(response, "usage", None)
    message = response.choices[0].message
    return ProviderResult(
        content=str(getattr(message, "content", "") or ""),
        tokens_in=int(getattr(usage, "prompt_tokens", 0) or 0),
        tokens_out=int(getattr(usage, "completion_tokens", 0) or 0),
        latency_ms=_elapsed_ms(started),
        cost_usd=0.0,
        provider=provider,
        model=model,
    )


_THINK_BLOCK_RE = re.compile(r"<think>.*?</think>\s*", re.DOTALL)
_JSON_FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)\s*```", re.DOTALL)


def _unwrap_json_content(content: str) -> str:
    """Normalize a JSON-mode response into a bare JSON payload.

    minimax-m3 ignores ``response_format=json_object`` and wraps the object in a
    ```json ... ``` markdown fence (and sometimes adds surrounding prose), so a
    caller's ``json.loads`` fails at char 0 on the leading backticks. Unwrap the
    fence, else fall back to the first balanced ``{...}``/``[...]`` slice — but ONLY
    when that slice actually parses as JSON. Otherwise the content is a prose/markdown
    answer whose brackets are pseudocode (BFS ``{ ... }``) or array indexing (``a[i]``),
    and slicing would surface a mid-fragment (e.g. an answer rendered as
    ``{ u ← dequeue(Q); ... }``). Compliant providers return bare JSON, so this is a
    no-op for them."""
    text = content.strip()
    # A ```json ... ``` (or plain ```) fence, but only adopt its body when that
    # body is JSON — a plain fence around pseudocode must not be mistaken for the
    # payload.
    fence = _JSON_FENCE_RE.search(text)
    if fence and _is_json(fence.group(1).strip()):
        return fence.group(1).strip()
    if text.startswith(("{", "[")):
        return text
    start = text.find("{")
    end = text.rfind("}")
    if 0 <= start < end and _is_json(text[start : end + 1]):
        return text[start : end + 1]
    if "<invoke" not in text:
        start = text.find("[")
        end = text.rfind("]")
        if 0 <= start < end and _is_json(text[start : end + 1]):
            return text[start : end + 1]
    return text


def _is_json(candidate: str) -> bool:
    try:
        json.loads(candidate)
        return True
    except (ValueError, TypeError):
        return False


def _strip_think_block(result: ProviderResult) -> ProviderResult:
    content = result.content
    if "<think>" not in content:
        return result
    stripped = _THINK_BLOCK_RE.sub("", content).strip()
    if stripped != content.strip():
        return replace(result, content=stripped)
    # Regex did not match: the think block is likely truncated (no closing
    # </think>) because the response hit the model's token limit mid-thought.
    # Try to recover the JSON tail so the caller can still parse it.
    close_idx = content.find("</think>")
    tail = content[close_idx + len("</think>") :].strip() if close_idx >= 0 else ""
    if not tail:
        for opener, closer in (("{", "}"), ("[", "]")):
            start = content.find(opener)
            end = content.rfind(closer)
            if 0 <= start < end:
                tail = content[start : end + 1]
                break
    if tail and tail != content.strip():
        return replace(result, content=tail)
    # Still nothing recoverable: the response is a truncated, never-closed think
    # block with no answer after it. Return the text before `<think>` (usually
    # empty) so callers fall back cleanly instead of rendering raw reasoning.
    prefix = content[: content.find("<think>")].strip()
    return replace(result, content=prefix)


class _ThinkStreamFilter:
    """Incrementally strip a leading ``<think>...</think>`` block from a token
    stream. ``minimax-m3`` always prefixes its reasoning this way; the block can
    span many deltas, so we buffer until we can decide. Providers that never emit
    ``<think>`` pass straight through. Mirrors ``_strip_think_block`` for the
    streaming path (which never sees the full string at once)."""

    _OPEN = "<think>"
    _CLOSE = "</think>"

    def __init__(self) -> None:
        self._state = "start"  # start -> thinking -> passthrough
        self._buf = ""

    def feed(self, delta: str) -> str:
        if self._state == "passthrough":
            return delta
        self._buf += delta
        if self._state == "start":
            head = self._buf.lstrip()
            if not head:
                return ""  # only whitespace so far — keep waiting
            if head.startswith(self._OPEN):
                self._state = "thinking"  # fall through to thinking handling
            elif self._OPEN.startswith(head):
                return ""  # a prefix of "<think>" — could still become the tag
            else:
                self._state = "passthrough"  # no reasoning block; flush what we held
                out, self._buf = self._buf, ""
                return out
        if self._state == "thinking":
            idx = self._buf.find(self._CLOSE)
            if idx >= 0:
                after = self._buf[idx + len(self._CLOSE):]
                self._buf = ""
                self._state = "passthrough"
                return after.lstrip()
            # Keep only a short tail so a </think> split across deltas is still found.
            if len(self._buf) > len(self._CLOSE):
                self._buf = self._buf[-len(self._CLOSE):]
            return ""
        return ""

    def flush(self) -> str:
        """Stream ended. Surface a held partial that never became a ``<think>``
        opener; if we never left the thinking state the reasoning was truncated
        with no answer after it, so emit nothing (matches _strip_think_block)."""
        if self._state == "start":
            leftover = self._buf.strip()
            if leftover and not self._OPEN.startswith(leftover):
                self._buf = ""
                return leftover
        return ""


def _split_system_messages(messages: list[ChatMessage]) -> tuple[str, list[dict[str, Any]]]:
    system_parts: list[str] = []
    conversation: list[dict[str, Any]] = []
    for message in messages:
        if message["role"] == "system":
            system_parts.append(message["content"])
        else:
            conversation.append({"role": message["role"], "content": [{"text": message["content"]}]})
    return "\n".join(system_parts), conversation


def _bedrock_result(response: Any, model: str, started: float, *, structured: bool) -> ProviderResult:
    blocks = response.get("output", {}).get("message", {}).get("content", [])
    if structured:
        content = next(
            (json.dumps(block["toolUse"]["input"]) for block in blocks if "toolUse" in block),
            "",
        )
    else:
        content = "".join(block.get("text", "") for block in blocks)
    usage = response.get("usage", {})
    return ProviderResult(
        content=content,
        tokens_in=int(usage.get("inputTokens", 0) or 0),
        tokens_out=int(usage.get("outputTokens", 0) or 0),
        latency_ms=_elapsed_ms(started),
        cost_usd=0.0,
        provider="bedrock",
        model=model,
    )


def _messages_to_text(messages: list[ChatMessage]) -> str:
    return "\n".join(f"{message['role']}: {message['content']}" for message in messages)


def _normalize_openai_base_url(endpoint: str) -> str:
    normalized = endpoint.rstrip("/")
    if normalized.endswith("/openai/v1"):
        return normalized
    return f"{normalized}/openai/v1"


def _elapsed_ms(started: float) -> int:
    return int((time.perf_counter() - started) * 1000)
