# AI Tutor Ablation — 2x2 (hard set)

## Grid (Δ vs Agentic+Dense)

| Config | n | faithfulness | answer relevancy | answer correctness | context precision | context recall | citation accuracy | overall |
|---|---|---|---|---|---|---|---|---|
| Agentic + Dense (baseline) | 15 | 4.73 | 5.00 | 5.00 | 4.27 | 4.53 | 3.93 | 4.58 |
| Agentic + Hybrid | 15 | 5.00 (+0.27) | 5.00 (+0.00) | 5.00 (+0.00) | 4.87 (+0.60) | 5.00 (+0.47) | 4.07 (+0.14) | 4.82 (+0.24) |
| Traditional + Dense | 15 | 4.67 (-0.06) | 4.93 (-0.07) | 4.67 (-0.33) | 4.20 (-0.07) | 4.40 (-0.13) | 3.80 (-0.13) | 4.44 (-0.14) |
| Traditional + Hybrid | 15 | 4.67 (-0.06) | 4.93 (-0.07) | 4.67 (-0.33) | 4.33 (+0.06) | 4.40 (-0.13) | 3.80 (-0.13) | 4.47 (-0.11) |

## By difficulty type (overall score)

| Config | graph | long_context | multi_intent | table |
|---|---|---|---|---|
| Agentic + Dense (baseline) | 4.50 | 4.72 | 4.79 | 4.33 |
| Agentic + Hybrid | 4.88 | 4.78 | 4.83 | 4.79 |
| Traditional + Dense | 4.38 | 4.78 | 4.83 | 3.88 |
| Traditional + Hybrid | 4.42 | 4.83 | 4.83 | 3.88 |

_Judge: claude-opus-4-8 (in-session RAGAS judge) (single judge across all configs for a valid comparison; OpenRouter expired). Generation: OpenCode/Groq. Retrieval: NVIDIA embed + rerank. Hybrid = dense+BM25 RRF -> rerank (production-faithful). Historical 50-Q run not included._

## Analysis

**Headline:** the full production stack — **Agentic + Hybrid (4.82)** — wins; the two
techniques compound. Ranking: Agentic+Hybrid 4.82 > Agentic+Dense 4.58 > Traditional+Hybrid
4.47 > Traditional+Dense 4.44.

**Axis 1 — Agentic > Traditional (both retrieval modes).** Agentic beats traditional by
+0.14 (dense) and +0.35 (hybrid), almost entirely on **answer_correctness (5.00 vs 4.67)**.
Cause: the single-shot path retrieves on the *raw* question, which mis-targets on two hard
cases — `hard_db_table_08` (raw query pulled a wrong "Keywords" table -> both traditional
configs answered INSERT/UPDATE/DELETE instead of Defining/Constructing/Manipulating) and
`hard_ai_graph_01` (the word "sơ đồ" pulled minimax game-tree figures). The agentic loop
**rewrites the query first** (query-optimization prompt), avoiding both.

**Axis 2 — Hybrid > Dense, and the gain is biggest under Agentic.** Agentic+Hybrid beats
Agentic+Dense by **+0.24**, driven by **context_precision +0.60** and **context_recall
+0.47**. The combinatorics questions (`hard_dm_graph_09/13/10`, IT3020E) are the story:
dense retrieval drowned in near-empty `(Lý thuyết tổ hợp)` section stubs, while the BM25
branch of hybrid caught the exact technical terms ("3-element subset", "dictionary order")
and pulled the real subset-enumeration table. Under *traditional* the hybrid gain nearly
vanishes (+0.03) — BM25 only helps when the query carries good lexical terms, which is
exactly what the agentic rewrite supplies. **The techniques interact: query rewriting makes
hybrid pay off.**

**By difficulty:** Agentic+Hybrid leads on **graph (4.88)** and **table (4.79)** — the
retrieval-hard categories — and ties everyone on multi_intent (4.83). Table is where
traditional collapses (3.88), from the `table_08` mis-answer plus weaker table retrieval.

**Weakest metric overall:** citation_accuracy (3.8–4.1) — answers are correct and grounded
but often omit inline `used_doc_ids`, so citations are retained conservatively. A
prompt/parse tweak to emit citation ids reliably is the highest-leverage next fix.

**Methodology note (important for the thesis):** an earlier run reported Traditional+Dense
winning at 4.78. That was an artifact of (a) a **split judge** (Opus scored one config,
gemini-flash-lite the other three, more leniently) and (b) the **agent answer-leak bug**
(the loop surfaced a bare `["knowledge"]` / `["<uuid>"]` array as the answer on 2/15
questions). After fixing the bug (`_is_non_answer_output`), switching hybrid to the
production-faithful `hybrid_rerank`, and re-judging **all four configs with one judge**, the
expected ordering (agentic > traditional, hybrid > dense) holds. This is a cautionary tale
about single-judge consistency in LLM-as-judge ablations.
