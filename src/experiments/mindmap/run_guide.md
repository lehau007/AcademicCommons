# E2 — Mindmap Concept Extraction Experiment

This experiment is the offline / no-LLM stand-in for the Phase 2 mindmap pipeline
described in `.agent/project_description.md` Section 6.7. It demonstrates the
map-reduce data flow end-to-end using a deterministic concept-graph builder so
that the experiment runs without any live LLM API call.

## Layout

```
src/experiments/mindmap/
  mindmap_experiment.py
  sample_course_seed.json
  sample_summaries/intro_to_ai/doc{1..6}.json     # synthetic DocumentSummary inputs
  results/intro_to_ai_graph.json                  # concept graph (v1 contract)
  results/intro_to_ai_graph.md                    # bullet-tree rendering
```

The six sample summaries match `data/schemas/document_summary.schema.json` and
collectively cover Search, CSP, Logic, Planning, ML, and RL — i.e. the topic
surface implied by `data/RAG_evaluation_data/intro_to_ai.json`.

## How to run

From the repo root:

```bash
python3 src/experiments/mindmap/mindmap_experiment.py
```

Optional flags:

| Flag | Default | Purpose |
|---|---|---|
| `--summaries-dir` | `src/experiments/mindmap/sample_summaries/intro_to_ai` | Directory of DocumentSummary JSON files (Phase 1 input) |
| `--course-seed` | `src/experiments/mindmap/sample_course_seed.json` | Course Seed JSON used for topic_summary context |
| `--graph-output` | `…/results/intro_to_ai_graph.json` | Where to write the concept graph |
| `--markdown-output` | `…/results/intro_to_ai_graph.md` | Markdown bullet-tree rendering |
| `--summary-output` | (none) | Optional path for the run stats JSON |
| `--model-name` | `sentence-transformers/all-MiniLM-L6-v2` | Encoder used for near-duplicate clustering |
| `--similarity-threshold` | `0.82` | Cosine threshold for merging near-duplicate concepts |
| `--topic-min-docs` | `2` | A concept appearing in N>=this many documents is promoted from level-2 concept to level-1 cross-cutting topic |

## Pipeline

1. **Phase 1 — collect summaries.** All JSON files in `--summaries-dir` are
   loaded as `DocumentSummary` records (no LLM call, by design).
2. **Phase 2 — deterministic concept-graph build** (stand-in for the single
   LLM call):
   - Collect every `concepts[]` entry across all summaries.
   - Dedupe by a normalized string key (lowercased, punctuation-stripped).
   - Cluster near-duplicates using MiniLM cosine similarity (threshold
     `--similarity-threshold`, default 0.82).
   - Emit a course root (level 0), one topic per `DocumentSummary.topic`
     (level 1), and one node per remaining concept. A concept that appears in
     `>= --topic-min-docs` documents is promoted to a level-1 cross-cutting
     topic attached to the course root and `related` to each parent topic.
   - All other concepts are level-2 and attached `contains`-style to their
     parent topic.
3. **Phase 3 — Render.** A v1-contract JSON graph and a markdown bullet tree
   are written under `results/`.

Phase 3 (selective deep-dive) and Phase 4 (UI render) from §6.7 are out of
scope for this offline experiment.

## Evaluation criteria

- **Topic coverage vs Course Seed.** Fraction of level-1 node labels whose
  normalized form appears verbatim in `course_seed.topic_summary`. Reported by
  `compute_stats` as `topic_coverage_vs_seed`.
- **Hierarchy depth.** `max_depth` in the run stats. v1 expects depth 2-3
  (course → topic → concept).
- **Node count.** Reported as `node_count`; should grow roughly linearly with
  the number of input summaries.
- **Cross-cutting promotion.** Manually inspect any node whose `level == 1` but
  whose label is not a `DocumentSummary.topic` — these are the
  `--topic-min-docs` promotions and should be domain-level cross-cutting
  concepts (e.g. `Heuristic Function`, `Search Problem`, `Intelligent Agent`
  for the bundled intro_to_ai inputs).

## Notes / limitations

- Embedding-based clustering is greedy single-linkage; very large concept sets
  may benefit from a proper clustering algorithm. For the v1 stand-in we keep
  it simple.
- Acronym/expansion pairs (e.g. `CSP` vs `Constraint Satisfaction Problem`,
  `FOL` vs `First Order Logic`) typically do not exceed the 0.82 threshold and
  remain as separate concept nodes. This is acceptable for the offline
  experiment; the real LLM-driven Phase 2 is expected to merge such pairs via
  explicit alias reasoning.
- All summaries here are self-authored synthetic data inspired by the Q&A in
  `data/RAG_evaluation_data/intro_to_ai.json`. They are not extracted from a
  live document processing run.
