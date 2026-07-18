# Experiment E3 — Mock Test Generation (Run Guide)

This experiment implements the **plan-then-generate** Mock Test pipeline from
`.agent/project_description.md` §6.8. The current implementation is a
**deterministic, template-based stub of LLM behaviour** — it produces artefacts
in the exact contracts (Test Plan v1, Generated Question v1, Citation Object v1)
that the thesis system expects, without making any live LLM API call. Swap the
`templated_*` functions for real LLM calls when integrating Gemini/OpenAI.

## Layout

```
src/experiments/mock_test/
├── mock_test_experiment.py             # main pipeline
├── sample_chunks/intro_to_ai/*.md      # 11 frontmatter-tagged source chunks
├── sample_topic_inventory.json         # produced on first run (topic -> chunks)
├── results/intro_to_ai_test.json       # machine-readable test
├── results/intro_to_ai_test.md         # human-readable rendering
└── run_guide.md
```

## Run

```bash
# from project root, with the project venv active
pip install -r requirements.txt   # sentence-transformers is required
python src/experiments/mock_test/mock_test_experiment.py
```

Optional flags:

```bash
python src/experiments/mock_test/mock_test_experiment.py \
    --course intro_to_ai \
    --total-questions 10 \
    --dedup-threshold 0.85 \
    --model-name sentence-transformers/all-MiniLM-L6-v2 \
    --seed 42
```

The script prints a JSON summary to stdout and writes:
- `sample_topic_inventory.json`
- `results/intro_to_ai_test.json`
- `results/intro_to_ai_test.md`

## Pipeline phases

1. **Topic inventory** — parses each markdown chunk's frontmatter (`topic:`,
   `chunk_id:`, `source:`) and the first `#` heading, splits the body into
   sentences, and groups chunks by topic.
2. **Test plan (deterministic)** — allocates `--total-questions` across topics
   proportionally to chunk count (≥ 1 per topic), then cycles through
   `difficulty ∈ {easy, medium, hard}` and `question_type ∈
   {multiple_choice, short_answer, true_false}` for balanced coverage.
3. **Templated question generation** — for each plan entry:
   - `multiple_choice` → find a definition sentence (`X is Y`/`X means Y`) in a
     topic chunk; stem = "Which of the following best describes 'X'?", correct =
     Y, 3 distractors = definition predicates randomly drawn from *other*
     topics' chunks. Shuffled, labelled A–D.
   - `short_answer` → "What is X?" → answer Y from the same X-is-Y pattern.
     Fallback: any interrogative sentence already in the chunk.
   - `true_false` → 50% true (sentence verbatim), 50% false (swap a capitalised
     noun with one from a different topic to introduce a falsehood).
   Every question carries a Citation Object pointing at the source chunk
   (`chunk_id`, `chunk_order`, `section_title`, `excerpt ≤ 200 chars`,
   `relevance_score` heuristic).
4. **Validation + dedup** — embeds all `question_text`s with MiniLM
   (`sentence-transformers/all-MiniLM-L6-v2`, already in `requirements.txt`)
   and removes any question whose cosine similarity to a previously-kept
   question exceeds `--dedup-threshold` (default `0.85`). Citation validity is
   verified by checking that the excerpt is a substring of the source chunk.

## What is stubbed vs. real

| Aspect                       | Stub (now)                                            | Real (production) |
|------------------------------|-------------------------------------------------------|-------------------|
| Test plan generation         | Deterministic round-robin over topic/difficulty/type  | Single LLM call producing Test Plan v1 JSON |
| Per-topic question generation| Regex templates over `X is Y` sentences + noun swap   | 1 LLM call per topic with chunked context + JSON-schema constrained output |
| Distractors (MCQ)            | Random predicates from other-topic chunks            | LLM-authored plausible distractors |
| True/false falsification     | Capitalised-noun swap from another topic             | LLM-authored counterfactual edit |
| Answer-consistency check     | Skipped (deterministic answers from source sentence)  | LLM spot-check pass |
| Dedup                        | Real MiniLM embeddings + cosine > 0.85                | Same |
| Citation validity            | Substring check (excerpt ⊆ source chunk)              | Same + LLM faithfulness audit |

Anywhere the production system would call an LLM, the stub uses
`random.Random(seed)` for full reproducibility. Replace the
`templated_multiple_choice`, `templated_short_answer`,
`templated_true_false`, and `build_test_plan` functions to swap in real
LLM calls without changing the artefact contracts.

## Evaluation criteria

The pipeline emits a `metrics` block in the output JSON with three primary
scores; these are the criteria the thesis evaluation will track:

1. **Coverage** = `topics_covered / topics_total`. Target ≥ 100% so every
   course topic has at least one question.
2. **Dedup rate** = `removed / generated_pre_dedup`. Lower is better
   (indicates more original questions). The threshold is configurable; the
   default 0.85 is recommended in §6.8.
3. **Citation validity %** = `valid_citations / total_citations`. Target ≥ 90%
   to satisfy §9 (Citation accuracy ≥ 0.90).

Additional counts (`by_topic`, `by_difficulty`, `by_type`) help confirm the
plan was honoured.

## Extending

- **Add more chunks**: drop new `*.md` files into
  `sample_chunks/<course>/` with the same frontmatter keys (`topic`,
  `chunk_id`, `source`). The pipeline auto-discovers them.
- **Plug a real LLM**: replace the three `templated_*` functions and
  `build_test_plan` with calls that return the same dataclass shapes. The
  dedup/validation/rendering downstream stays identical.
- **Different course**: pass `--chunks-dir path/to/chunks --course my_course`.

## Known limitations of the stub

- Only English source material is exercised; Vietnamese chunks need a
  Vietnamese-aware definition regex (the current pattern keys on `is/are/means/
  refers to`).
- Distractor pool is small (definition predicates only); real LLMs will produce
  more topic-relevant distractors.
- True/false noun-swap can occasionally produce statements that remain true
  (e.g. swapping with a semantically-compatible foreign term). A real LLM
  falsification step would catch this.
