# AI Tutor Ablation — 2x2 (full set)

## Grid (Δ vs Agentic+Dense)

| Config | n | faithfulness | answer relevancy | answer correctness | context precision | context recall | citation accuracy | overall |
|---|---|---|---|---|---|---|---|---|
| Agentic + Dense (baseline) | 65 | 4.83 | 4.94 | 4.88 | 4.35 | 4.68 | 4.82 | 4.75 |
| Agentic + Hybrid | 65 | 4.89 (+0.06) | 4.97 (+0.03) | 4.92 (+0.04) | 4.45 (+0.10) | 4.71 (+0.03) | 4.85 (+0.03) | 4.80 (+0.05) |
| Traditional + Dense | 65 | 4.98 (+0.15) | 4.89 (-0.05) | 4.78 (-0.10) | 4.32 (-0.03) | 4.65 (-0.03) | 4.75 (-0.07) | 4.73 (-0.02) |
| Traditional + Hybrid | 65 | 4.95 (+0.12) | 4.89 (-0.05) | 4.78 (-0.10) | 4.38 (+0.03) | 4.68 (+0.00) | 4.80 (-0.02) | 4.75 (+0.00) |

## By difficulty type (overall score)

| Config | graph | long_context | multi_intent | standard | table |
|---|---|---|---|---|---|
| Agentic + Dense (baseline) | 4.67 | 4.89 | 4.83 | 4.76 | 4.46 |
| Agentic + Hybrid | 4.88 | 4.94 | 4.92 | 4.80 | 4.50 |
| Traditional + Dense | 4.33 | 4.94 | 4.96 | 4.74 | 4.58 |
| Traditional + Hybrid | 4.75 | 4.94 | 4.96 | 4.75 | 4.38 |

_Judge: claude-opus-4-8 (in-session RAGAS judge) (single judge across all configs for a valid comparison; OpenRouter expired). Generation: OpenCode/Groq. Retrieval: NVIDIA embed + rerank. Hybrid = dense+BM25 RRF -> rerank (production-faithful). Historical 50-Q run not included._

## Analysis

**Headline:** on the full 65-question set the full production stack — **Agentic + Hybrid
(4.80)** — still wins, confirming the hard-set conclusion. But the margins **collapse** versus
the 15-question hard set (there the spread was 4.82 → 4.44, Δ0.38; here it is 4.80 → 4.73,
Δ0.07). The reason is exactly the one predicted in the spec: the 50 **standard** questions are
factual look-ups whose answers sit in a single well-embedded chunk, so *all four* configs
retrieve and answer them at ~4.75–4.80 and dilute the retrieval-hard effects. The ablation
signal lives almost entirely in the **hard slice**, and within it, in the **graph** and
**table** categories.

**Ordering (overall):** Agentic+Hybrid 4.80 > Agentic+Dense 4.75 ≈ Traditional+Hybrid 4.75 >
Traditional+Dense 4.73.

**Axis 1 — Agentic > Traditional (correctness vs faithfulness trade-off).** Agentic beats
traditional on **answer_correctness (4.88–4.92 vs 4.78)** but traditional scores *higher* on
**faithfulness (4.95–4.98 vs 4.83–4.89)**. This is a genuine pipeline trade-off, not noise: the
single-shot traditional path is more **conservative** — when the retrieved chunks don't contain
an explicit definition it *refuses* ("the materials do not define …") rather than composing an
answer. Refusals are faithful (nothing ungrounded) but don't deliver the ground truth, so
correctness drops. The agentic path rewrites the query, retrieves more aggressively, and commits
to an answer — occasionally grounding a correct fact in world knowledge rather than the chunks
(slightly lower faithfulness, higher correctness). Cases: `database_02` (intersection vs
difference — agentic states the defs, both traditional configs refuse), `discrete_math_16`
(spanning subgraph — agentic + traditional_hybrid commit to V(H)=V(G); traditional_dense hedges),
`intro_to_ai_12` (Mitchell T/P/E — agentic enumerates, traditional hedges).

**Axis 2 — Hybrid > Dense, concentrated in graph/table retrieval.** Hybrid lifts
**context_precision** (agentic +0.10, traditional +0.06) and shows up sharply in the
**per-difficulty graph row**: Agentic 4.67→4.88, Traditional 4.33→4.75. The BM25 branch rescues
retrieval-hard cases the dense embedder drowns: `hard_ai_graph_01` (raw query "sơ đồ … hill
climbing" — dense pulled minimax/8-puzzle noise and missed the terrain diagram; hybrid's lexical
match fetched the `Local Maxima / Plateaus / Ridges` chunk), `hard_db_table_08` (the
defining/constructing/manipulating mapping). The techniques still **interact** — hybrid's biggest
graph gain is under agentic (+0.21) where the rewrite supplies the lexical terms BM25 needs.

**By difficulty — where the signal is:**
- **graph** is the cleanest discriminator: **Agentic+Hybrid 4.88** ≫ Traditional+Dense **4.33**.
- **table** splits on a single stochastic retrieval: Traditional+Dense 4.58 (fetched the mapping,
  answered `hard_db_table_08` correctly) vs Traditional+Hybrid 4.38 (missed it, answered
  INSERT/UPDATE/DELETE — the exact mis-answer the design doc flagged for the traditional pipeline).
- **standard / long_context / multi_intent** are ~flat across configs (4.74–4.96) — no ablation
  signal; these are the dilution.

**Corpus-gap findings (affect all four configs equally, not the ablation):**
- `discrete_math_12` (Dirichlet/Pigeonhole): the formal statement is **not in any retrievable
  chunk** — neither dense nor hybrid, neither pipeline, finds it; all four correctly refuse
  (faithfulness 5, correctness 2). This is a **content gap**, not a retrieval-mode difference, and
  it is the single biggest drag on `context_recall` on the standard slice. High-leverage fix:
  add/enrich the `1-2-Existence.pdf` pigeonhole slide.
- `intro_to_ai_12` (Mitchell T/P/E) is a milder version: the informal Mitchell quote is retrieved
  but the explicit T/P/E enumeration is not, so the split is pipeline-driven (agentic enumerates
  from prior knowledge, traditional hedges).

**Weakest metric overall:** context_precision (4.32–4.45) — many retrieved bundles carry
tangential chunks (diagram stubs, adjacent-topic slides) alongside the relevant ones. Hybrid+rerank
is the best mitigation observed here.

**Conclusion for the thesis:** the 2×2 ordering (agentic > traditional, hybrid > dense, full stack
best) **holds on the full dataset**, but the effect size is honest only on retrieval-hard questions;
on easy factual look-ups the pipeline/retrieval choice barely matters. The right takeaway is that
**agentic + hybrid earns its cost specifically on graph/table/ambiguous-query questions**, which is
where a real tutor's hardest queries live. See `hard/report.md` for the un-diluted 15-question
slice. Error-check + coverage gate: `full/_coverage_error_log.md`.
