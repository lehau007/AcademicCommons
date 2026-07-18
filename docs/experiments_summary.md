# Core System Experiments — Summary (E1–E4)

**Date:** 2026-05-24
**Scope:** Experiments for core system components beyond the document processing pipeline. All experiments self-generate sample data and avoid live LLM API calls (free-tier constraint). Local embeddings via `sentence-transformers/all-MiniLM-L6-v2` are used where embeddings are needed.

| ID | Component | Path | Status |
|----|-----------|------|--------|
| E1 | RAG Tutor + RAGAS-style harness | `src/experiments/rag_tutor/` | ✅ Ran end-to-end on 3 courses |
| E2 | Mindmap concept extraction (Phase 1+2) | `src/experiments/mindmap/` | ✅ Ran on `intro_to_ai` |
| E3 | Mock Test generation (plan-then-generate) | `src/experiments/mock_test/` | ✅ Ran on `intro_to_ai` |
| E4 | HITL routing + SLA escalation | `src/experiments/hitl_routing/` | ✅ Ran (18/18 assertions passed) |

---

## E1 — RAG Tutor + RAGAS-style Harness

**Goal.** Validate the Virtual Tutor retrieval design from `project_description.md` §6.6 (naive top-k vs MMR vs MMR + tier boost) using the existing golden Q&A in `data/RAG_evaluation_data/`.

**What was built.**
- Corpus self-generated under `src/experiments/rag_tutor/corpus/{intro_to_ai,database,discrete_math}/` (16 markdown docs total) with frontmatter `tier` and `subtype` so the tier-boost path is exercised.
- `rag_tutor_experiment.py` — structure-aware semantic chunking → MiniLM embeddings → Chroma `PersistentClient` (one collection per course) → 3 retrieval strategies → deterministic stub answer (concat top-k with citations) → 4 custom metrics.
- Metrics (LLM-judge-free): `answer_similarity` (cosine vs ground truth), `context_precision`, `context_recall`, `citation_accuracy` (top-1 covers ≥25% of ground-truth content tokens).

**Results (per strategy, averaged):**

| Course | Strategy | answer_sim | ctx_precision | ctx_recall | citation_acc |
|--------|----------|-----------:|--------------:|-----------:|-------------:|
| intro_to_ai | naive_top_k | 0.677 | 0.888 | 0.989 | 1.000 |
| intro_to_ai | mmr | 0.660 | 0.838 | 0.989 | 1.000 |
| intro_to_ai | mmr_tier_boost | **0.679** | 0.888 | 0.989 | 1.000 |
| database | naive_top_k | 0.594 | 0.700 | 0.995 | 1.000 |
| database | mmr | 0.600 | 0.600 | 0.995 | 1.000 |
| database | mmr_tier_boost | 0.595 | 0.700 | 0.995 | 1.000 |
| discrete_math | naive_top_k | 0.596 | 0.888 | 0.995 | 1.000 |
| discrete_math | mmr | **0.603** | **0.900** | **1.000** | 1.000 |
| discrete_math | mmr_tier_boost | 0.593 | 0.875 | 0.995 | 1.000 |

**Observations.**
- On small, narrow corpora (10–20 chunks) the 3 strategies are nearly indistinguishable on this metric set.
- MMR helps recall on `discrete_math` (more topically overlapping content); tier_boost rarely beats plain MMR here because the corpus has few competing same-topic chunks across tiers.
- Citation accuracy is 1.0 across the board — expected since the stub answer is built directly from the retrieved chunks. A real LLM generator is needed to stress this metric.

**Limitations.**
- Generation step is a deterministic stub; `answer_similarity` is a proxy not a true faithfulness measure.
- Corpus is small and hand-authored; a larger corpus with adversarial near-duplicate chunks is needed to make MMR/tier_boost differentiation meaningful.

---

## E2 — Mindmap Concept Extraction (Phase 1 + Phase 2)

**Goal.** Validate the Mindmap pipeline from `project_description.md` §6.7 — Phase 1 collects per-document summaries, Phase 2 builds a concept graph. The "LLM call" in Phase 2 is replaced by a deterministic builder.

**What was built.**
- 6 self-authored `DocumentSummary` JSON files under `sample_summaries/intro_to_ai/` (Search/Agents, CSP, Logic, Planning+Games, ML, RL).
- `sample_course_seed.json` with `topic_summary` covering the same domain.
- `mindmap_experiment.py` — collects summaries → embeds concepts with MiniLM → near-duplicate clustering at cosine ≥ 0.82 → promotes concepts appearing in ≥2 docs to level-1 "topic" nodes → emits v1 Concept Graph (JSON + markdown bullet tree).

**Results.**
- Nodes: 71 (1 course root, 9 level-1 topics, 61 level-2 concepts)
- Edges: 77 (mostly `contains`)
- Max depth: 2 — matches v1 contract
- `topic_coverage_vs_seed`: **0.457** (token-overlap match vs the course seed `topic_summary`)
- Document coverage: 6/6

**Observations.**
- Topic coverage of 0.457 indicates the metric is conservative — many seed concepts appear in docs under paraphrased names that the simple token-overlap check misses (e.g., seed says "uncertainty reasoning", docs say "probabilistic inference"). An embedding-similarity coverage metric would score higher.
- MiniLM at 0.82 threshold does NOT merge acronyms with expansions (`CSP` ↔ `Constraint Satisfaction Problem`, `FOL` ↔ `First Order Logic`). For production, add a lightweight glossary/alias pass.

**Limitations.**
- Phase 3 (selective deep-dive: retrieve chunks for under-specified topics) was not implemented — requires the indexed corpus from E1.
- Deterministic clustering cannot infer non-co-occurring `prerequisite`/`related` edges.

---

## E3 — Mock Test Generation (Plan-then-Generate)

**Goal.** Validate the Mock Test pipeline from `project_description.md` §6.8. The per-topic LLM generation is replaced by deterministic template extraction so the harness can be measured offline.

**What was built.**
- 11 markdown chunks under `sample_chunks/intro_to_ai/` with frontmatter (`topic_id`, `chunk_id`), derived from the 20 Q&A pairs.
- `mock_test_experiment.py` —
  - Phase 1: load chunks → topic inventory.
  - Phase 2: deterministic test plan (proportional topic allocation, round-robin difficulty/type).
  - Phase 3: template-based generation — MCQ from `X is/means Y` regex with cross-topic distractors; short_answer = `What is X?` → `Y`; true_false = verbatim true vs noun-swap from another topic.
  - Phase 4: MiniLM cosine dedup at > 0.85, substring-based citation validity check.

**Results.**
- Questions generated pre-dedup: 10 → after dedup: 9 (dedup rate **10%**)
- Topic coverage: **6/6 (100%)** (CSP, Logic, ML, Planning, RL, Search)
- Citation validity: **9/9 (100%)** — every cited chunk substring matches the source.
- By type: 4 multiple_choice / 2 short_answer / 3 true_false
- By difficulty: 6 easy / 3 medium

**Observations.**
- Deterministic templates work for definition-style questions but cannot generate reasoning-style or multi-step questions — a real LLM is needed for hard difficulty.
- 100% citation validity is expected because chunks ARE the source; the metric becomes interesting when a real LLM is allowed to paraphrase.

**Limitations.**
- Difficulty distribution is not actually controlled — the templater currently picks based on chunk position rather than reasoning depth.
- No coverage of free-text scoring (would need an LLM judge).

---

## E4 — HITL Routing + SLA Escalation

**Goal.** Validate the review-routing logic from `project_description.md` §5 and §6.2: assigned-reviewer fan-out, first-acts-wins, no-reviewer escalation, SLA breach escalation, admin reassign / direct review.

**What was built.**
- `mock_data/` — 4 courses (SLAs 24h/48h/72h), 1 admin + 3 reviewers + 5 students, varied assignments (2 reviewers / 1 / 0 active / 0), 9 docs entering `NEEDS_REVIEW` at fake timestamps.
- `hitl_routing_experiment.py` — stdlib only; functions `route_on_needs_review`, `reviewer_action`, `reassign_to_reviewer`, `tick(now)`. A scripted scenario exercises all 4 paths.

**Results.**
- **18/18 assertions passed.**
- 18 audit entries logged across 4 queue snapshots.
- All 4 routing paths exercised: normal review, first-acts-wins, immediate `no_reviewer` escalation, `sla_breached` escalation. Plus admin reassign and admin direct approval.

**Spec ambiguities documented (chosen defaults):**
1. Admin reassign does NOT reset the SLA clock (anchored to original `needs_review_at`).
2. `no_reviewer` docs do NOT additionally receive `sla_breached` — they are already with admin.
3. Intra-queue ordering: FIFO.
4. Late-actor after first-acts-wins: no-op + audit entry.

These four points should be ratified in SRS / project description before implementation.

---

## Cross-Cutting Notes

- **Reusability.** All 4 experiments share a single conventions baseline (argparse CLI, dataclasses, MiniLM as the embedding model, results under `results/`). They mirror the style of `src/experiments/semantic_chunking/semantic_chunking_chroma_experiment.py`.
- **No live LLM.** Free-tier API exhaustion was avoided. The price is that the experiments measure pipeline behavior, not generation quality. A follow-up pass with a real LLM (Gemini / local Llama) is the next milestone.
- **Sample-data philosophy.** Each experiment self-generates its own samples and documents them in its `run_guide.md`. Replace samples with real `DocumentSummary` / corpus output from the production pipeline once OCR throughput is available.

## How to Re-run Everything

```bash
# from project root, with .venv activated
.venv/bin/python src/experiments/rag_tutor/rag_tutor_experiment.py --course all
.venv/bin/python src/experiments/mindmap/mindmap_experiment.py
.venv/bin/python src/experiments/mock_test/mock_test_experiment.py
.venv/bin/python src/experiments/hitl_routing/hitl_routing_experiment.py
```

## Recommended Next Steps

1. **Scale E1 corpus** to 50+ chunks/course with intentional duplicate content across tiers, to stress-test MMR and tier_boost differentiation.
2. **Replace stub generators** in E1 and E3 with a real LLM call once API quota is available; re-measure faithfulness / citation accuracy.
3. **Implement E2 Phase 3** (selective deep-dive) once an indexed corpus from E1 is reused.
4. **Ratify the 4 HITL spec ambiguities** in `docs/SRS.md` and `.agent/project_description.md`.
