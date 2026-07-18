# E1 — RAG Tutor + RAGAS-style Retrieval Harness

This experiment evaluates three retrieval strategies for the Virtual Tutor
(see `.agent/project_description.md` §6.6) against the golden Q&A sets under
`data/RAG_evaluation_data/`.

## 1. Layout

```
src/experiments/rag_tutor/
├── corpus/                # "fake textbook" docs per course (frontmatter: tier, subtype, course_code)
│   ├── intro_to_ai/
│   ├── database/
│   └── discrete_math/
├── rag_tutor_experiment.py
├── run_guide.md
├── chroma_db/<course>/    # generated; reset on every run
└── results/<course>/      # generated reports
```

Each corpus document carries YAML-style frontmatter, e.g.:

```
---
tier: official            # official | community
subtype: lecture_slides   # lecture_slides | summary_note | ...
course_code: IT3160
title: ...
---
```

## 2. Install dependencies (already in `requirements.txt`)

```bash
.venv/bin/pip install -r requirements.txt
```

## 3. Run for one course (default: intro_to_ai)

```bash
.venv/bin/python src/experiments/rag_tutor/rag_tutor_experiment.py --course intro_to_ai
```

Other choices: `--course database`, `--course discrete_math`, or `--course all`.

Tunable flags (defaults match §6.6):

| Flag | Default | Meaning |
|---|---|---|
| `--top-k` | 4 | Chunks sent to the answer assembler. |
| `--fetch-k` | 8 | Candidate pool size before MMR / tier boost. |
| `--mmr-lambda` | 0.7 | MMR trade-off: 1.0 = pure relevance, 0.0 = pure diversity. |
| `--similarity-threshold` | 0.55 | Paragraph-merge threshold during chunking. |
| `--min-chunk-chars` / `--max-chunk-chars` | 350 / 1200 | Chunk size bounds. |

## 4. Output

For each course the script writes:

```
results/<course>/naive_top_k_report.json
results/<course>/mmr_report.json
results/<course>/mmr_tier_boost_report.json
results/<course>/summary.json
```

Each `*_report.json` contains per-question retrieval traces and four
custom RAGAS-like metrics, plus an aggregate mean across all questions.

## 5. Metric definitions (network-free, deterministic)

We avoid live LLM judges to stay within free-tier limits. Instead:

- **answer_similarity** — cosine similarity between the MiniLM embedding of the
  generated stub answer (concatenated top-k chunks) and the ground-truth answer.
- **context_precision** — fraction of retrieved chunks that share at least one
  non-stopword content token with the ground-truth answer.
- **context_recall** — fraction of ground-truth content tokens covered by the
  union of retrieved chunks.
- **citation_accuracy** — 1.0 if the *first cited* chunk covers ≥25 % of the
  ground-truth content tokens, else 0.0. Approximates "did the cited chunk
  actually contain the answer".

## 6. Interpreting the three strategies

- `naive_top_k`: pure cosine top-k. Baseline.
- `mmr`: MMR with k=top_k, fetch_k, λ=0.7. Tests diversification.
- `mmr_tier_boost`: MMR over `fetch_k` candidates, then multiply each
  official-tier chunk's score by 1.15 and re-sort. Tests the tier-aware boost
  described in §6.6.

Look for:

- `answer_similarity`: should be highest when retrieval brings back the
  paragraph that paraphrases the ground truth.
- `context_recall`: directly reflects whether the retrieved set covers the
  answer tokens. Sensitive to chunking + top_k.
- `mmr_tier_boost` vs `mmr`: improvements indicate that official-tier
  documents are genuinely more answer-bearing for that course.
