from __future__ import annotations

import importlib
import json
import time
import uuid
import warnings
from collections.abc import AsyncIterator, Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app.config import Settings
from app.llm.providers import ChatMessage, LLMProvider, ProviderResult, StreamChunk

_SUCCESS_STATUSES = {"SUCCESS", "CACHE_HIT", "FALLBACK_SUCCESS"}


@dataclass(frozen=True)
class OptimizerSDK:
    EvalOptimizer: type[Any]
    OptimizerConfig: type[Any]
    Prompt: type[Any]
    ModelSpec: type[Any]
    RequestParams: type[Any]
    RunContext: type[Any]
    BudgetExceededError: type[Exception]
    AzureOpenAIClient: type[Any]
    GoogleClient: type[Any]
    GroqClient: type[Any]
    BedrockConverseClient: type[Any]
    BedrockClient: type[Any]
    JsonlLogBackend: type[Any]
    ModelPrice: type[Any]
    DEFAULT_PRICE_TABLE: dict[tuple[str, str, str], Any]


@dataclass(frozen=True)
class OptimizerProviderBinding:
    provider_name: str
    model_id: str
    model_version: str
    build_client: Callable[[OptimizerSDK], Any]


@dataclass(frozen=True)
class _InvocationPlan:
    optimizer: Any
    prompt: Any
    model_spec: Any
    request_params: Any
    run_context: Any
    optimization_profile: str


class OptimizerAdapter:
    def __init__(
        self,
        *,
        sdk: OptimizerSDK,
        settings: Settings,
        provider_bindings: list[OptimizerProviderBinding],
    ) -> None:
        self._sdk = sdk
        self._settings = settings
        self._binding_by_provider = {binding.provider_name: binding for binding in provider_bindings}
        self._client_by_provider = {binding.provider_name: binding.build_client(sdk) for binding in provider_bindings}
        self._optimizer_cache: dict[tuple[str, int | None, str], Any] = {}
        self._price_table = self._build_price_table()

    async def chat(
        self,
        provider: LLMProvider,
        messages: list[ChatMessage],
        *,
        schema: dict[str, Any] | None = None,
        max_tokens: int | None = None,
        flow_name: str | None = None,
    ) -> ProviderResult:
        plan = self._prepare(provider, messages, schema=schema, max_tokens=max_tokens, flow_name=flow_name)

        started = time.perf_counter()
        try:
            invocation = await plan.optimizer.ainvoke(
                plan.prompt,
                plan.model_spec,
                request_params=plan.request_params,
                run_context=plan.run_context,
            )
        except self._sdk.BudgetExceededError as exc:
            raise RuntimeError(f"optimizer budget exceeded: {exc}") from exc
        except Exception as exc:
            raise RuntimeError(f"optimizer invoke failed: {exc}") from exc

        status = _status_name(getattr(invocation, "status", "SUCCESS"))
        if status not in _SUCCESS_STATUSES:
            raise RuntimeError(_failure_message(invocation, status))
        return _provider_result_from_invocation(
            invocation,
            latency_ms=_elapsed_ms(started),
            optimization_profile=plan.optimization_profile,
        )

    async def stream(
        self,
        provider: LLMProvider,
        messages: list[ChatMessage],
        *,
        schema: dict[str, Any] | None = None,
        max_tokens: int | None = None,
        flow_name: str | None = None,
    ) -> AsyncIterator[StreamChunk]:
        plan = self._prepare(provider, messages, schema=schema, max_tokens=max_tokens, flow_name=flow_name)

        started = time.perf_counter()
        try:
            stream = plan.optimizer.astream(
                plan.prompt,
                plan.model_spec,
                request_params=plan.request_params,
                run_context=plan.run_context,
            )
            async for chunk in stream:
                if getattr(chunk, "done", False):
                    invocation = getattr(chunk, "result", None)
                    status = _status_name(getattr(invocation, "status", "SUCCESS"))
                    if status not in _SUCCESS_STATUSES:
                        raise RuntimeError(_failure_message(invocation, status))
                    yield StreamChunk(
                        done=True,
                        result=_provider_result_from_invocation(
                            invocation,
                            latency_ms=_elapsed_ms(started),
                            optimization_profile=plan.optimization_profile,
                        ),
                    )
                    return
                text = str(getattr(chunk, "text", "") or "")
                if text:
                    yield StreamChunk(text=text)
        except self._sdk.BudgetExceededError as exc:
            raise RuntimeError(f"optimizer budget exceeded: {exc}") from exc
        except RuntimeError:
            raise
        except Exception as exc:
            raise RuntimeError(f"optimizer stream failed: {exc}") from exc

    def _prepare(
        self,
        provider: LLMProvider,
        messages: list[ChatMessage],
        *,
        schema: dict[str, Any] | None,
        max_tokens: int | None,
        flow_name: str | None,
    ) -> _InvocationPlan:
        provider_name = provider.provider_name
        binding = self._binding_by_provider.get(provider_name)
        if binding is None:
            raise RuntimeError(f"optimizer has no binding for provider '{provider_name}'")

        optimization_profile = self._settings.llm_optimizer_profile_for_flow(flow_name)
        cache_key = (provider_name, max_tokens, optimization_profile)
        optimizer = self._optimizer_cache.get(cache_key)
        if optimizer is None:
            optimizer = self._build_optimizer(binding=binding, max_tokens=max_tokens)
            self._optimizer_cache[cache_key] = optimizer

        return _InvocationPlan(
            optimizer=optimizer,
            prompt=self._build_prompt(messages, schema=schema, optimization_profile=optimization_profile),
            model_spec=self._sdk.ModelSpec(
                provider=binding.provider_name,
                model_id=binding.model_id,
                model_version=binding.model_version,
                temperature=0.0,
                max_tokens=max_tokens,
            ),
            request_params=self._build_request_params(schema=schema),
            run_context=self._build_run_context(
                messages=messages,
                max_tokens=max_tokens,
                schema=schema,
                flow_name=flow_name,
                optimization_profile=optimization_profile,
                provider_name=binding.provider_name,
            ),
            optimization_profile=optimization_profile,
        )

    def _build_optimizer(self, *, binding: OptimizerProviderBinding, max_tokens: int | None) -> Any:
        model_spec = self._sdk.ModelSpec(
            provider=binding.provider_name,
            model_id=binding.model_id,
            model_version=binding.model_version,
            temperature=0.0,
            max_tokens=max_tokens,
        )
        config = self._sdk.OptimizerConfig(
            prefix_cache_enabled=self._settings.llm_optimizer_prefix_cache_enabled,
            semantic_cache_enabled=self._settings.llm_optimizer_semantic_cache_enabled,
            compression_enabled=False,
            # Translation (Vi->En prompt judge) is intentionally disabled; the
            # router passes prompts through to providers without rewriting them.
            vi_en_translation_enabled=False,
            cascade_routing_enabled=self._settings.llm_optimizer_cascade_routing_enabled,
            shadow_enabled=self._settings.llm_optimizer_shadow_enabled,
            # Provider fallback is intentionally owned by LLMRouter so each
            # provider attempt has a single, project-visible failure boundary.
            provider_fallback_enabled=False,
            budget_cap_usd=self._settings.llm_optimizer_budget_cap_usd,
            on_budget_exceeded=self._settings.llm_optimizer_on_budget_exceeded,
            allowed_providers=(binding.provider_name,),
            model_chain=(model_spec,),
        )
        return self._sdk.EvalOptimizer(
            config=config,
            client_factory=self._client_factory,
            log_backends=self._build_log_backends(),
            price_table=self._price_table,
        )

    def _build_price_table(self) -> dict[tuple[str, str, str], Any] | None:
        # Merge our configured per-model prices over the SDK defaults so models the
        # default table doesn't cover (e.g. Gemini/Groq) still report real cost.
        raw = self._settings.llm_optimizer_price_table_json.strip()
        if not raw:
            return None
        try:
            overrides = json.loads(raw)
        except json.JSONDecodeError as exc:
            warnings.warn(f"Invalid llm_optimizer_price_table_json, ignoring: {exc}", stacklevel=2)
            return None
        table = dict(self._sdk.DEFAULT_PRICE_TABLE)
        for key, price in overrides.items():
            provider, _, model_id = str(key).partition(":")
            if not provider or not model_id:
                continue
            if isinstance(price, dict):
                model_price = self._sdk.ModelPrice(**price)
            else:
                input_per_mtok, output_per_mtok = price
                model_price = self._sdk.ModelPrice(
                    input_per_mtok=float(input_per_mtok),
                    output_per_mtok=float(output_per_mtok),
                )
            table[(provider, model_id, "*")] = model_price
        return table

    def _build_log_backends(self) -> list[Any] | None:
        # None -> SDK default JSONL file. [] -> logging disabled. A configured
        # path -> stable per-project log we can aggregate for cost reporting.
        if not self._settings.llm_optimizer_logging_enabled:
            return []
        log_path = self._settings.llm_optimizer_log_path.strip()
        if not log_path:
            return None
        Path(log_path).parent.mkdir(parents=True, exist_ok=True)
        return [self._sdk.JsonlLogBackend(log_path)]

    def _client_factory(self, spec: Any) -> Any:
        provider_name = str(getattr(spec, "provider", ""))
        try:
            return self._client_by_provider[provider_name]
        except KeyError as exc:
            raise ValueError(f"optimizer has no client for provider '{provider_name}'") from exc

    def _build_prompt(
        self,
        messages: list[ChatMessage],
        *,
        schema: dict[str, Any] | None,
        optimization_profile: str,
    ) -> Any:
        system_parts: list[str] = []
        dynamic_parts: list[str] = []
        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")
            if role == "system":
                system_parts.append(content)
            else:
                dynamic_parts.append(f"{role}: {content}")

        static_context = ""
        if schema is not None:
            static_context = (
                "Return JSON that matches this schema exactly:\n"
                f"{json.dumps(schema, ensure_ascii=True, sort_keys=True)}"
            )
        return self._sdk.Prompt(
            system="\n\n".join(part for part in system_parts if part),
            static_context=static_context,
            dynamic_input="\n".join(dynamic_parts),
            optimization_profile=optimization_profile,
        )

    def _build_request_params(self, *, schema: dict[str, Any] | None) -> Any:
        kwargs: dict[str, Any] = {}
        if schema is not None:
            kwargs["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": "structured_response",
                    "schema": schema,
                },
            }
        return self._sdk.RequestParams(**kwargs)

    def _build_run_context(
        self,
        *,
        messages: list[ChatMessage],
        max_tokens: int | None,
        schema: dict[str, Any] | None,
        flow_name: str | None,
        optimization_profile: str,
        provider_name: str,
    ) -> Any:
        return self._sdk.RunContext(
            run_id=f"llm-router-{uuid.uuid4()}",
            prompt_judge_version=self._settings.llm_optimizer_prompt_version,
            metadata={
                # The SDK's JSONL backend only persists its canonical attribution
                # keys (metric_id/skill_id/sample_id), so map our flow onto skill_id
                # to keep it groupable in cost reports; the rest are best-effort.
                "skill_id": flow_name or "default",
                "metric_id": optimization_profile,
                "flow": flow_name or "default",
                "provider": provider_name,
                "message_count": str(len(messages)),
                "max_tokens": "" if max_tokens is None else str(max_tokens),
                "optimization_profile": optimization_profile,
                "schema_enabled": str(schema is not None).lower(),
            },
        )


def build_optimizer_adapter(
    settings: Settings,
    *,
    provider_bindings: list[OptimizerProviderBinding],
) -> OptimizerAdapter | None:
    if not settings.llm_optimizer_enabled or not provider_bindings:
        return None

    try:
        sdk = _load_optimizer_sdk()
    except ModuleNotFoundError:
        warnings.warn(
            "LLM optimizer is enabled but llm_cost_optimizer is not installed; "
            "falling back to the legacy provider router.",
            stacklevel=2,
        )
        return None

    return OptimizerAdapter(
        sdk=sdk,
        settings=settings,
        provider_bindings=provider_bindings,
    )


def _load_optimizer_sdk() -> OptimizerSDK:
    optimizer_module = importlib.import_module("llm_cost_optimizer")
    client_module = importlib.import_module("llm_cost_optimizer.client")
    azure_module = importlib.import_module("llm_cost_optimizer.clients.azure_openai")
    google_module = importlib.import_module("llm_cost_optimizer.clients.google")
    groq_module = importlib.import_module("llm_cost_optimizer.clients.groq")
    bedrock_module = importlib.import_module("llm_cost_optimizer.clients.bedrock")
    jsonl_log_module = importlib.import_module("llm_cost_optimizer.tracking.log_backends.jsonl")
    cost_module = importlib.import_module("llm_cost_optimizer.tracking.cost")
    return OptimizerSDK(
        EvalOptimizer=optimizer_module.EvalOptimizer,
        OptimizerConfig=optimizer_module.OptimizerConfig,
        Prompt=optimizer_module.Prompt,
        ModelSpec=optimizer_module.ModelSpec,
        RequestParams=optimizer_module.RequestParams,
        RunContext=optimizer_module.RunContext,
        BudgetExceededError=client_module.BudgetExceededError,
        AzureOpenAIClient=azure_module.AzureOpenAIClient,
        GoogleClient=google_module.GoogleClient,
        GroqClient=groq_module.GroqClient,
        BedrockConverseClient=bedrock_module.BedrockConverseClient,
        BedrockClient=bedrock_module.BedrockClient,
        JsonlLogBackend=jsonl_log_module.JsonlLogBackend,
        ModelPrice=cost_module.ModelPrice,
        DEFAULT_PRICE_TABLE=cost_module.DEFAULT_PRICE_TABLE,
    )


def _provider_result_from_invocation(
    invocation: Any,
    *,
    latency_ms: int,
    optimization_profile: str,
) -> ProviderResult:
    model_spec = getattr(invocation, "model_spec", None)
    usage = getattr(invocation, "usage", None)
    cache_info = getattr(invocation, "cache_info", None)
    trace = getattr(invocation, "trace", None)
    return ProviderResult(
        content=str(getattr(invocation, "response", "") or ""),
        tokens_in=_int_value(getattr(usage, "input_uncached", 0))
        + _int_value(getattr(usage, "input_cached", 0)),
        tokens_out=_int_value(getattr(usage, "output", 0)),
        latency_ms=latency_ms,
        cost_usd=float(getattr(invocation, "cost_usd", 0.0) or 0.0),
        provider=str(getattr(model_spec, "provider", "optimizer")),
        model=str(getattr(model_spec, "model_id", "unknown")),
        metadata={
            "optimizer_status": _status_name(getattr(invocation, "status", "SUCCESS")),
            "optimization_profile": optimization_profile,
            "fallback_chain": list(getattr(invocation, "fallback_chain", []) or []),
            "cache_tier": getattr(cache_info, "tier", "none"),
            "cache_hit": bool(getattr(cache_info, "hit", False)),
            "trace_stage_count": len(getattr(trace, "stages", []) or []),
        },
    )


def _failure_message(invocation: Any, status_name: str) -> str:
    model_spec = getattr(invocation, "model_spec", None)
    provider = str(getattr(model_spec, "provider", "unknown"))
    model_id = str(getattr(model_spec, "model_id", "unknown"))
    fallback_chain = list(getattr(invocation, "fallback_chain", []) or [])
    return (
        f"optimizer returned {status_name} "
        f"(provider={provider}, model={model_id}, fallback_chain={fallback_chain})"
    )


def _status_name(status: Any) -> str:
    return str(getattr(status, "name", status))


def _int_value(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _elapsed_ms(started: float) -> int:
    return int((time.perf_counter() - started) * 1000)
