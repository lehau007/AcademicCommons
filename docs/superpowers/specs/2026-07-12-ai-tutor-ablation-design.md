# AI Tutor Ablation Study — Design Spec

**Date:** 2026-07-12
**Author:** lehau007 + Claude
**Location:** `evaluation/ai_tutor_evaluation/`
**Related:** `docs/superpowers/specs/2026-07-07-ai-tutor-evaluation-design.md` (base eval harness)

## 1. Goal

Complete an ablation study for the AI tutor that isolates two design choices, on a
deliberately **hard** question set, and produces a defensible comparison table for the
thesis (Chapter 5 ablation):

- **Retrieval axis:** `dense` vs `hybrid` (dense + BM25 fused by RRF).
- **Pipeline axis:** `agentic` (multi-step decision loop with query optimization) vs
  `traditional` (single-shot retrieve → generate).

Run as a **2×2 grid** so each axis can be read with the other held fixed.

Secondary deliverables (requested):
- Fix the **production** tutor system prompt: (a) forbid using general/outside knowledge
  when the retrieved context lacks the answer (except greetings / small-talk / meta), and
  (b) instruct the agent to **optimize the query before retrieval**, with one worked example.
- Add a **backend endpoint** for the traditional (single-shot) path, not wired to the
  frontend, so it exists as a real product surface and is testable by hand.
- Author a **hard dataset** (graphs, tables, multi-intent, long-context) with verifiable
  ground truth.
- **Judge without OpenRouter** (expired): produce a prompt-pack an external agentic coding
  tool consumes to emit RAGAS-style scores.

## 2. Constraints (current stack, honest)

- **OpenRouter API is expired.** No programmatic OpenRouter calls anywhere in the eval path.
- **Generation:** OpenCode (`minimax-m3`) and Groq have credit. Set
  `LLM_PROVIDER_ORDER` so the router uses these. (This is already how the prod tutor runs.)
  Note: `minimax-m3` emits a `<think>` block that eats `max_tokens`; the existing
  `tutor_service` budgets + strip logic already handle this — do not regress it.
- **Embedding + rerank:** NVIDIA NIM (`nv-embedqa-e5-v5`, `llama-nemotron-rerank-vl-1b-v2`),
  both valid. `rerank_enabled=True`.
- **Judge:** no automated API. Uses the prompt-pack flow (§7).
- The old 50-question results (`results/`, `results_hybrid_norerank/`, `results_bm25_rerank/`)
  were produced on the **old** stack (OpenRouter embeddings + cohere rerank + gpt-5.4-mini
  judge). They are **historical** and are NOT mixed into the new 2×2. Kept as-is for the
  base-eval story; the ablation is self-contained on the hard set.
- Everything runs locally against the docker stack (`graduationthesis-*` containers), same
  `docker cp` → `docker exec` pattern as the existing harness.

## 3. Scope decisions (locked)

| Decision | Choice |
|---|---|
| Ablation shape | 2×2 grid (retrieval × pipeline), all 4 configs regenerated fresh on the hard set |
| Traditional RAG | existing `tutor_query` (single-shot), unchanged behavior |
| Traditional runner | in-process, injecting the recording `AblationRetrieval` (needed to capture retrieved context for the judge) |
| Traditional product surface | new `POST /tutor/query-classic` endpoint (parallel deliverable; the runner does NOT use it) |
| Prompt changes | applied to **production** `tutor_service.py` (agentic path) |
| Hard dataset | new `dataset/questions_hard.json`, difficulty-tagged, separate from the 50 |
| Graph/table retrievability | targeted enrichment: append light descriptions to affected chunks in DB, then `reindex-embeddings` (no re-OCR) |
| Judge | prompt-pack for an external agentic tool; no OpenRouter |
| Generation providers | OpenCode (`minimax-m3`) + Groq |

## 4. The 2×2 grid

| Config id | Pipeline | Retrieval | actual dir | results dir |
|---|---|---|---|---|
| `agentic_dense` | `tutor_query_agent_loop` | dense → NVIDIA rerank | `hard/actual_agentic_dense/` | `hard/results_agentic_dense/` |
| `agentic_hybrid` | `tutor_query_agent_loop` | dense+BM25 RRF (no rerank) | `hard/actual_agentic_hybrid/` | `hard/results_agentic_hybrid/` |
| `traditional_dense` | `tutor_query` | dense → NVIDIA rerank | `hard/actual_traditional_dense/` | `hard/results_traditional_dense/` |
| `traditional_hybrid` | `tutor_query` | dense+BM25 RRF (no rerank) | `hard/actual_traditional_hybrid/` | `hard/results_traditional_hybrid/` |

All new artifacts live under a `hard/` subfolder of `evaluation/ai_tutor_evaluation/` to keep
them clearly separated from the historical 50-question run.

Every other knob (k / prefetch_k, outline filter, official-tier boost, community votes,
cosine floor for the dense config) is identical across configs so deltas are attributable to
the two axes only.

## 5. Production prompt changes (`src/backend/app/services/tutor_service.py`)

Target: `_TUTOR_SYSTEM_PROMPT_TEMPLATE` (the agentic path) and, for consistency,
`_FINAL_ANSWER_INSTRUCTION`.

### 5.1 No outside knowledge (strengthen)

Replace the current soft rule ("If the retrieved context does not contain the answer, say so
explicitly … Do not invent information.") with an explicit boundary:

> Answer using **ONLY** the retrieved context. You MUST NOT fall back to general/outside/
> pre-trained knowledge to fill gaps. If the gathered context does not contain the answer,
> state explicitly that the course materials do not cover it — do not answer from general
> knowledge. **Exception:** ordinary greetings, small-talk, and meta-questions about the
> conversation itself may be answered normally without retrieval.

Mirror the same sentence in `_FINAL_ANSWER_INSTRUCTION`.

### 5.2 Query optimization before retrieval (new rule + one example)

Add a rule instructing the agent to rewrite the student's raw question into an optimized
retrieval query before calling `rag_retrieval_api_tool` (expand abbreviations, add domain
terms, drop chit-chat, and split multi-intent questions into separate retrievals — the
existing multi-topic rule already covers splitting). Include exactly **one** worked example:

> Before retrieving, rewrite the student's question into a focused retrieval query: expand
> abbreviations, add the key domain terms, and strip conversational filler. Retrieve with the
> rewritten query, not the raw sentence.
> Example — student asks: "ê giải thích giúp t cái bảng so sánh BFS với DFS trong slide đi".
> Optimized query: "so sánh BFS và DFS: độ phức tạp thời gian, bộ nhớ, tính đầy đủ, tối ưu".
> Decision turn:
> `{"thought": "Rewrite to a focused query about the BFS vs DFS comparison table.",
>   "action": "call_tool", "tool_name": "rag_retrieval_api_tool",
>   "arguments": {"query": "so sánh BFS và DFS: độ phức tạp thời gian, bộ nhớ, tính đầy đủ, tối ưu", "namespaces": ["knowledge"]}}`

The **traditional** path (`_SYSTEM_PROMPT` / `tutor_query`) is intentionally left without query
rewriting — it retrieves on the raw question. This is precisely what the pipeline axis
measures: agentic query optimization + multi-step vs single-shot raw retrieval.

**Regression guard:** the identity rules, the DECISION/ANSWER turn contract, the JSON decision
schema, the `used_doc_ids` block, and the token budgets must remain intact. The prompt edit is
additive/replacement of the two rules only.

## 6. Traditional RAG endpoint

`POST /tutor/query-classic` in `src/backend/app/api/v1/tutor.py`:
- Auth: `get_current_user` (same as `/tutor/query`).
- Body: reuse `TutorQueryRequest` (`course_code`, `question`, optional `include_exercise`;
  add `include_exercise: bool = False` to the schema if not present). `session_id`/
  `document_ids` are ignored for the classic path.
- Calls `tutor_query(...)` (single-shot) and returns `TutorQueryResponse`.
- **Not** imported or linked anywhere in the frontend. No new frontend code.

This endpoint is a product surface + manual test hook. The eval runner does NOT call it (it
runs `tutor_query` in-process to capture retrieved context — §8).

## 7. Judge without OpenRouter — prompt-pack

New script `scripts/build_judge_pack.py`:
- Input: a config's `actual_*` dir + `dataset/questions_hard.json` + `metrics/rubric.md`.
- Output: `hard/judge_pack_<config>/`:
  - `INSTRUCTIONS.md` — exactly what the external agent must do: read each `<qid>.md`, score
    the 6 metrics per the rubric anchors, write `results_<config>/<qid>.json` in the schema.
  - `rubric.md` (copied) and `schema.json` (the per-question 6-metric JSON schema).
  - `<qid>.md` per question — a self-contained bundle: question, ground_truth, the **retrieved
    context** (from `retrieval_calls`), the tutor answer, and citations.
- The user feeds `judge_pack_<config>/` to any agentic coding tool (opencode / gemini-cli /
  Claude) which writes `hard/results_<config>/<qid>.json`.

New script `scripts/validate_results.py`: checks each results file against the schema, reports
missing metrics / nulls / qid coverage before aggregation. (Replaces the trust the automated
judge used to give.)

`aggregate.py` and `compare_ablation.py` are reused; `compare_ablation.py` gets a new CONFIGS
list for the 2×2 (4 rows) plus a per-`difficulty_type` breakdown table.

## 8. Ablation runner (generation)

Extend the existing `scripts/run_ablation.py` with a `--pipeline {agentic,traditional}` flag:
- `agentic` → `tutor_query_agent_loop` (current behavior).
- `traditional` → `tutor_query(session, course_code, question, include_exercise=False,
  llm_router, retrieval_service=recorder, settings)`.
- Both inject the same `AblationRetrieval` recorder (records retrieval calls for the judge).
- `--mode {dense_rerank,hybrid_norerank}` (bm25 kept but not part of the 2×2).
- Output dir defaults to `hard/actual_<pipeline>_<mode-short>/`.
- Resumable (existing per-qid skip).

`scripts/ablation_retrieval.py` fix: `_rerank` currently hardcodes `OpenRouterRerank`. Change
the reranked configs to use the **same rerank service production uses now** (NVIDIA rerank via
the production retrieval-service path) so `dense_rerank` runs without OpenRouter and matches
prod. `hybrid_norerank` is unaffected (no rerank).

## 9. Hard dataset

New `dataset/questions_hard.json`, same schema plus a tag:
`{qid, course_code, question, ground_truth, difficulty_type}` where
`difficulty_type ∈ {graph, table, multi_intent, long_context}`.

Target size: **~12–20** questions, authored **against the real indexed corpus** (query the DB
inside the container to see actual chunk content), so every ground truth is traceable to
indexed chunks. Distribution roughly balanced across the four difficulty types.

Verification: write `expected/_hard_review_report.md` — for each qid, the chunk(s)/document(s)
that cover the ground truth and a coverage verdict (covered / partial / impossible), mirroring
the existing `_review_report.md` process. Questions whose answer is not present in any chunk
(even after enrichment) are marked and excluded or flagged, never silently scored.

### 9.1 Graph/table enrichment (targeted)

For `graph`/`table` questions, the underlying figure/table must be retrievable as text. Process:
1. Inspect candidate chunks (DB query) to find the figures/tables to cover.
2. Append a light (1–2 sentence) natural-language description of the figure/table to the
   relevant chunk's `content` (what it shows, axes/columns, the key values/trend), so dense +
   BM25 can match a question about it. Keep it factual and minimal — no invented data.
3. Run `python -m app.cli reindex-embeddings` (re-embeds changed chunk content with NVIDIA).
4. Record every edited chunk (id, before/after snippet) in `expected/_hard_enrichment_log.md`
   for reproducibility and thesis honesty.

## 10. Execution order

1. Prompt changes (§5) → user review → rebuild api image (baked; see memory).
2. Add `/tutor/query-classic` endpoint (§6).
3. Fix ablation rerank to NVIDIA (§8).
4. Enrich graph/table chunks + reindex (§9.1).
5. Author `questions_hard.json` + `_hard_review_report.md` (§9).
6. Generate 4 configs (§8) → `hard/actual_*` (OpenCode/Groq generation; resumable).
7. Build judge packs (§7) → user runs external agent → `hard/results_*`.
8. Validate + aggregate + compare (§7) → 2×2 table + difficulty breakdown → `hard/report.md`.

Credit note: generation uses OpenCode/Groq (available). Judge is offloaded to the external
agent (no billing). Dataset size is the main cost knob; start small and extend.

## 11. Success criteria

- All 4 configs generate answers for every hard qid (or documented failures), with retrieved
  context captured.
- Prompt changes verified: a query that has no coverage yields an explicit "not in course
  materials" answer (no general-knowledge fallback); a messy multi-intent query shows a
  rewritten retrieval query in the agent trace.
- `/tutor/query-classic` returns a single-shot answer; frontend untouched.
- Graph/table hard questions retrieve the enriched chunk (chunk appears in `retrieval_calls`).
- Final `hard/report.md` shows the 2×2 metric means with deltas and a per-difficulty_type
  breakdown, plus honest caveats (judge = external agent, not the old sonnet judge).

## 12. Out of scope

- No frontend changes.
- No re-ingestion / re-OCR (targeted DB enrichment only).
- The historical 50-question results are not re-run or merged.
- No new retrieval technique beyond dense / hybrid / (existing) bm25.
