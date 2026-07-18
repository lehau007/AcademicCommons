# Design — Integrate the new `llm_cost_optimizer` SDK

Date: 2026-06-29
Status: Implemented

## Goal
Upgrade the in-process LLM cost optimizer to its renamed version and adopt two new
capabilities: **cost reporting & attribution** and **streaming for the Virtual Tutor**.

Reference: `docs/llm_cost_optimizer/integration_guide.md`, `tutor_agent_ui_flow.md`.

## Decisions
- **Drop-in + new features.** Migrate the SDK first, then layer the two features.
- **Cost surface:** JSONL log + offline CLI (no DB schema / no UI), enough to produce
  the cost table for the thesis evaluation chapter.
- **Streaming UX:** SSE emitting two event kinds — `status` (agent progress) and
  `text_delta` (token streaming) — matching `tutor_agent_ui_flow.md`.
- **No "Eval" naming** in our wrapper, since the SDK package was renamed.

## §1 SDK migration
- `pyproject.toml`: `eval-optimizer` → `llm-cost-optimizer[...]@main`
  (real package name verified by resolving/building the git source).
- `optimizer_adapter.py`: import paths `eval_optimizer` → `llm_cost_optimizer`;
  `EvalOptimizerAdapter` → `OptimizerAdapter`; `build_eval_optimizer_adapter` →
  `build_optimizer_adapter`; `_load_eval_optimizer_sdk` → `_load_optimizer_sdk`.
- The SDK facade class is still `EvalOptimizer`; only our wrapper changed.
- Verified offline against the real SDK: loader resolves every submodule path,
  `invoke`/`astream` return `SUCCESS` with `FakeModelClient`.

## §2 Cost reporting & attribution
- New settings `llm_optimizer_logging_enabled` / `llm_optimizer_log_path`.
- `_build_optimizer` passes `log_backends=[JsonlLogBackend(path)]` (or `[]` to disable,
  or `None` for the SDK default). `provider` added to `RunContext.metadata`.
- `app/llm/cost_report.py`: defensive JSONL parser + `aggregate_records` grouping by
  `flow`/`provider` (cost, tokens, cache-hit rate). Field extraction tolerates flat or
  nested (`metadata`/`usage`/`cache_info`) shapes across SDK versions.
- CLI: `python -m app.cli optimizer-report [--log --group-by --json]` → Markdown/JSON table.

## §3 Streaming Virtual Tutor
- `providers.StreamChunk` (`text` delta | terminal `result`).
- `OptimizerAdapter.stream()` over SDK `astream`; `LLMRouter.stream()` falls back to a
  single full-text chunk when the optimizer is off for the flow, and only switches
  provider if nothing was emitted yet.
- `stream_tutor_agent_loop()` runs the agent loop as a stream of UI events:
  - tool-decision turns emit `status` events;
  - the final answer streams as `text_delta` using a **peek-buffer** (first ~40 chars
    decide tool-call vs answer, so tool-call JSON never reaches the user; misclassified
    turns are corrected via `reset` / `_parse_tool_call`);
  - terminal `done` carries the cleaned answer + citations and persists the turn.
  - Shared helpers `_execute_tool` / `_load_agent_context` / `_postprocess_answer` /
    `_persist_and_summarize` are reused by the existing non-stream loop.
- `POST /tutor/query/stream` returns `text/event-stream`; commits after the stream ends.

### SSE contract
`data: <json>\n\n`, `type` ∈ `session | status | text_delta | reset | done | error`.

## Verification
- 178 backend unit tests pass; Ruff clean on changed files.
- Real-SDK offline check (loader + invoke + astream).
- `optimizer-report` CLI smoke test over a synthetic log.
- Frontend SSE UI implemented separately (lint + typecheck gated).
