# AI Tutor Ablation — Progress Snapshot & Full-Dataset Evaluation Spec

**Date:** 2026-07-12
**Status:** Hard-set 2×2 complete and valid. Next: extend the SAME 2×2 to the full dataset
(50 original + 15 hard = 65 questions) under one judge.
**Related:**
- Design: `docs/superpowers/specs/2026-07-12-ai-tutor-ablation-design.md`
- Plan: `docs/superpowers/plans/2026-07-12-ai-tutor-ablation.md`
- Result: `evaluation/ai_tutor_evaluation/hard/report.md`

---

## Part 1 — What is done (progress snapshot)

### 1.1 The ablation study (hard set, 15 questions) — COMPLETE & VALID

A 2×2 ablation over **retrieval {dense, hybrid} × pipeline {agentic, traditional}**, run on
15 hard difficulty-tagged questions, generated on the live docker stack (generation
OpenCode/Groq, retrieval NVIDIA embed+rerank), judged by **claude-opus-4-8 in-session** —
one judge across all four configs.

**Result (overall / 5):**

| Config | overall | graph | table | multi_intent | long_context |
|---|---|---|---|---|---|
| **Agentic + Hybrid** | **4.82** | 4.88 | 4.79 | 4.83 | 4.78 |
| Agentic + Dense | 4.58 | 4.50 | 4.33 | 4.79 | 4.72 |
| Traditional + Hybrid | 4.47 | 4.42 | 3.88 | 4.83 | 4.83 |
| Traditional + Dense | 4.44 | 4.38 | 3.88 | 4.83 | 4.78 |

**Findings:** (1) Agentic > Traditional — query rewriting avoids raw-query mis-targeting
(traditional answered `table_08` as INSERT/UPDATE/DELETE, pulled minimax figures for
`graph_01`). (2) Hybrid > Dense, gain biggest under agentic — BM25 rescues IT3020E
combinatorics retrieval that dense drowns in `(Lý thuyết tổ hợp)` section stubs. (3) The two
techniques compound; hybrid barely helps traditional (+0.03) because BM25 needs the lexical
terms the agentic rewrite supplies. Weakest metric: citation_accuracy (3.8–4.1).

### 1.2 Production changes shipped (baked into the api image)

- **Prompt** (`app/services/tutor_service.py`, `_TUTOR_SYSTEM_PROMPT_TEMPLATE` +
  `_FINAL_ANSWER_INSTRUCTION`): forbids general/outside-knowledge fallback (exception:
  greetings/small-talk/meta); adds a query-optimization rule ("rewrite the raw question into
  a focused retrieval query before `rag_retrieval_api_tool`") with one worked example. The
  traditional single-shot path is deliberately left WITHOUT rewriting (it is the pipeline
  baseline).
- **Answer-leak bug fix** (`_is_non_answer_output`): the agent loop was surfacing bare JSON
  arrays (`["knowledge"]`, `["<uuid>", …]`) as the final answer because the decision-None
  guard only caught metadata *dicts*. Now catches bare arrays too; applied in
  `tutor_query_agent_loop`, `stream_tutor_agent_loop`, and `_postprocess_answer`. 33 tutor
  unit tests pass.
- **New endpoint** `POST /tutor/query-classic` — single-shot traditional RAG (`tutor_query`),
  backend-only, NOT wired to the frontend.

### 1.3 Evaluation harness (all under `evaluation/ai_tutor_evaluation/`)

| File | Purpose |
|---|---|
| `scripts/ablation_retrieval.py` | Retrieval variants: `dense_rerank`, `hybrid_rerank` (RRF→prod reranker, production-faithful), `hybrid_norerank` (RRF, no rerank — reranker-value probe), `bm25_rerank`. Reuses production `_rerank` (NVIDIA; no OpenRouter). |
| `scripts/run_ablation.py` | Generation runner. `--pipeline {agentic,traditional}` × `--mode {…}`; injects a recording retrieval so the judge sees retrieved context. Output `hard/actual_<pipeline>_<short>/`. Resumable (per-qid skip). |
| `scripts/build_judge_pack.py` | OpenRouter-free judge prompt-pack (INSTRUCTIONS + rubric + schema + per-qid bundle) for an external agentic tool. |
| `scripts/validate_results.py` | Checks the 6-metric schema + qid coverage before aggregation. |
| `scripts/compare_ablation_2x2.py` | Renders the 2×2 grid (Δ vs agentic_dense) + per-`difficulty_type` breakdown + the actual judge model → `hard/report.md`. |
| `scripts/enrich_table_chunks.py` | Targeted DB enrichment: appends `[Table: …]` descriptions to specific table chunks + re-embeds (figures were already `[Diagram: …]`-described by the OCR pipeline; tables were not). |
| `dataset/questions_hard.json` | 15 hard questions (graph/table/multi_intent/long_context), grounded in real chunks. |
| `expected/_hard_review_report.md`, `_hard_enrichment_log.md` | Coverage verdicts + the 4 enriched IT3292E chunk ids. |

### 1.4 Corpus fact worth remembering

The OCR/normalization pipeline already emits `[Diagram: …]` descriptions for figures
(IT3020E 159, IT3160E 145 chunks) so graph questions retrieve as-is. **Tables** lacked any
NL description → 4 IT3292E table chunks were enriched with `[Table: …]` + re-embedded
(`expected/_hard_enrichment_log.md`). IT3020E combinatorics content is stored with many
near-empty `(Lý thuyết tổ hợp)` section-title stubs that pollute *dense* retrieval — the
motivating case for the hybrid finding.

### 1.5 Methodology caveat (do not repeat)

An earlier 2×2 wrongly showed Traditional+Dense winning (4.78). Cause: **split judging**
(Opus scored one config, gemini-flash-lite scored three, more leniently) + the answer-leak
bug. Lesson enforced below: **one judge for every config**, and re-judge whenever actuals
change.

---

## Part 2 — Next: full-dataset evaluation (the task ahead)

### 2.1 Goal

Re-run the SAME 2×2 (4 configs) over the **combined 65-question set** = the 50 original
questions (`dataset/questions.json`) + the 15 hard questions (`dataset/questions_hard.json`),
so the ablation conclusions are backed by the whole dataset, not only the hard slice.

### 2.2 Why a re-run is required (not a merge of old numbers)

The original 50-question results in `actual/`, `results/`, `results_hybrid_norerank/`,
`results_bm25_rerank/` are **historical**: produced on the OLD stack (OpenRouter embeddings +
cohere rerank + gpt-5.4-mini/other judges) and BEFORE the prompt fixes and the answer-leak
fix. They are NOT comparable to the current stack and MUST NOT be merged into the new grid.
The 50 must be regenerated and re-judged under the current stack + single judge.

### 2.3 Dataset assembly

- The 50 (`questions.json`) and 15 (`questions_hard.json`) share schema
  (`qid, course_code, question, ground_truth`); hard adds `difficulty_type`. No qid overlap.
  Same three courses (IT3160E, IT3020E, IT3292E).
- Build `dataset/questions_full.json` = concat of both, adding `difficulty_type: "standard"`
  to each of the 50 originals so the per-difficulty breakdown still renders (buckets:
  standard, graph, table, multi_intent, long_context).
- Keep `questions.json` and `questions_hard.json` untouched as sources.

### 2.4 Coverage check first (gate)

Before generating, verify the 50 originals are still answerable against the CURRENT index
(the corpus/embeddings changed since they were authored). Reuse the
`expected/_review_report.md` process: any question whose ground truth is no longer covered is
flagged (kept but noted), not silently scored. Spot-check via retrieval, not by eye.

### 2.5 Generation

Run `run_ablation.py` for the 4 configs on `questions_full.json`:

```bash
docker cp evaluation/ai_tutor_evaluation graduationthesis-api-1:/tmp/tutor_eval
for pipe in agentic traditional; do for mode in dense_rerank hybrid_rerank; do
  docker exec -e PYTHONPATH=/app -w /tmp/tutor_eval graduationthesis-api-1 \
    python scripts/run_ablation.py --pipeline $pipe --mode $mode \
      --questions dataset/questions_full.json --out hard/full_actual_${pipe}_<short> --concurrency 2
done; done
```

- Use a **distinct output namespace** (e.g. `hard/full_actual_*` and `hard/full_results_*`, or
  a new `full/` sibling dir) so the 65-question run never mixes with the 15-question `hard/`
  artifacts. Decide the dir convention before Task starts and thread it through
  `default_out_dir` / `compare` CONFIGS.
- Pre-flight: `OPENROUTER_API_KEY` must be UNSET in the container (else dense/rerank hard-fail);
  `LLM_PROVIDER_ORDER=opencode,groq,gemini`; NVIDIA key set. Confirm the api image is the
  bug-fixed one (`grep -c _is_non_answer_output` in the container = 3).
- Sanity after generation: `answer-leak count == 0` for every config (bare-array check).

### 2.6 Judging — ONE judge for all 4 (hard constraint)

260 items (65 × 4). Options, pick ONE and apply to all four configs:
- **(A) In-session Opus judge** — highest consistency, no external billing, but 260 gradings
  is heavy; do it config-by-config with a compact dump (the pattern already used for the hard
  set) so context stays bounded.
- **(B) External single model via the prompt-packs** — build 4 `build_judge_pack.py` packs and
  run ALL FOUR through the *same* external model (not a mix). Cheaper attention per item but
  requires the operator to drive it uniformly.

Do NOT split judges across configs. Record `judge_model` in every result (the compare footer
surfaces it).

### 2.7 Aggregate & compare

`compare_ablation_2x2.py` (extended to read the `full_*` dirs) → `full/report.md` with the
2×2 grid + per-difficulty breakdown (now including the `standard` bucket). Expectation to test
against: does the hard-set ordering (Agentic+Hybrid > Agentic+Dense > Traditional*) still hold
when the easier standard questions dilute the retrieval-hard effects? The standard bucket may
compress the gaps — that itself is a finding.

### 2.8 Cost / risk

- Generation: OpenCode/Groq credits, ~24 s/agentic question → 65×4 ≈ 260 generations,
  resumable; run in the background config-by-config.
- Judging: the main effort. If credits/attention run out mid-way, the per-qid design means a
  partial-but-valid subset can still be reported (note n<65 per config in the grid).
- Keep the 15-question `hard/` result intact as the "hard slice" companion to the full run.

### 2.9 Success criteria

- `dataset/questions_full.json` (65) built; coverage report for the 50 originals recorded.
- 4 configs generated on the full set, 0 answer-leaks, retrieved context captured.
- All 4 judged by ONE judge; `validate_results.py` clean (ok=65 each, or documented partial).
- `full/report.md`: 2×2 grid + per-difficulty (incl. `standard`) + analysis vs the hard-set
  result. REGISTRY updated.

---

## Open follow-ups (optional, not blocking the full eval)

- **citation_accuracy** (weakest, 3.8–4.1): answers are correct+grounded but omit inline
  `used_doc_ids`; a prompt/parse tweak to emit citation ids reliably is high-leverage.
- **`hybrid_norerank` column**: add it to isolate the reranker's contribution (dense_rerank vs
  hybrid_rerank vs hybrid_norerank).
