"""Instance-based LLM call recorder.

Replaces the experiment's module-level ``_llm_call_records`` / ``_record_llm_call`` /
``_summarize_llm_metrics`` globals so the pipeline carries no shared mutable state.
"""

from __future__ import annotations

from typing import Any


class LlmCallRecorder:
    def __init__(self, input_cost_per_1m: float = 0.15, output_cost_per_1m: float = 0.60) -> None:
        self._records: list[dict[str, Any]] = []
        self._input_rate = input_cost_per_1m
        self._output_rate = output_cost_per_1m

    def record(
        self,
        operation: str,
        provider: str,
        model: str,
        status: str,
        latency_ms: int,
        prompt_tokens: int = 0,
        completion_tokens: int = 0,
        error: str | None = None,
    ) -> None:
        # Cost applies only to Azure calls; others record cost=0 (separate billing).
        if provider == "azure_openai":
            cost = (prompt_tokens / 1_000_000) * self._input_rate + (
                completion_tokens / 1_000_000
            ) * self._output_rate
        else:
            cost = 0.0
        record: dict[str, Any] = {
            "operation": operation,
            "provider": provider,
            "model": model,
            "status": status,
            "latency_ms": latency_ms,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
            "estimated_cost_usd": round(cost, 8),
        }
        if error:
            record["error"] = error
        self._records.append(record)

    def summary(self) -> dict[str, Any]:
        records = list(self._records)
        total = len(records)
        successful = sum(1 for r in records if r["status"] == "success")
        latencies = [r["latency_ms"] for r in records]
        return {
            "total_calls": total,
            "successful_calls": successful,
            "failed_calls": total - successful,
            "total_prompt_tokens": sum(r["prompt_tokens"] for r in records),
            "total_completion_tokens": sum(r["completion_tokens"] for r in records),
            "total_tokens": sum(r["total_tokens"] for r in records),
            "total_cost_usd": round(sum(r["estimated_cost_usd"] for r in records), 8),
            "avg_latency_ms": round(sum(latencies) / max(len(latencies), 1), 1),
            "records": records,
        }
