# AI Tutor Evaluation — Report

**Date:** 2026-07-07 · **Judge:** `anthropic/claude-sonnet-4.5` via OpenRouter
(300 calls = 50 questions × 6 metrics; 0 null cells) · **System under test:**
`tutor_query_agent_loop` (production code path of `POST /tutor/query`) against the live
`academic_kb` index (1,359 chunks across the 3 courses after ingesting 24 missing lectures).

## Headline

**Overall 4.26/5.** The tutor answers well when retrieval finds the content
(faithfulness 4.44, relevancy 4.48, correctness 4.36, recall 4.48). The two structural
weak spots are **context precision 3.76** (retrieval returns table-of-contents/outline
chunks as noise) and **citation accuracy 4.04** (good answers that skip inline citations).
A single product bug — the final-answer turn occasionally emitting only the `used_doc_ids`
JSON instead of an answer — accounts for most of the worst scores.

| Metric | Mean | Min | Max |
|---|---|---|---|
| Faithfulness | 4.44 | 1 | 5 |
| Answer Relevancy | 4.48 | 1 | 5 |
| Answer Correctness | 4.36 | 1 | 5 |
| **Context Precision** | **3.76** | 1 | 5 |
| Context Recall | 4.48 | 1 | 5 |
| **Citation Accuracy** | **4.04** | 1 | 5 |

Per course: IT3160E (intro AI) **4.71** · IT3292E (database) **3.97** · IT3020E
(discrete math) **3.96**.

## Failure modes (ranked by impact)

### 1. JSON-only final answers — product bug, 5/50 questions (10%)

`database_05`, `database_08`, `discrete_math_04`, `discrete_math_11`, `discrete_math_19`
returned literally `{"used_doc_ids": ["…"]}` as the answer. The agent's ANSWER turn emitted
only the used-doc-ids suffix and `_postprocess_answer` did not recover an answer from it.
Retrieval was fine in all 5 cases (the correct chunks were fetched). These questions score
1 on relevancy/correctness and drag every mean; excluding them, answer_correctness rises
from 4.36 to ≈4.7. **Fix in `tutor_service.py`**: if stripping the JSON suffix leaves an
empty answer, re-prompt or fall back to a retrieval-grounded template instead of returning
the raw JSON to the student.

### 2. TOC/outline chunks pollute retrieval — context precision 3.76

The indexer stores boilerplate slides ("Learning Map", "Content of Part 2", course/section
outlines) as chunks, and they rank high enough to fill retrieval slots
(e.g. `database_03`: 1 of 8 chunks relevant, the other 7 were learning maps/outlines).
IT3020E is hit hardest (precision 3.3) because its decks repeat the chapter outline on many
slides. **Recommendation:** filter or down-weight outline/TOC chunks at indexing time (they
are recognizable: short, list-only, repeated verbatim across a deck).

### 3. Missing inline citations on substantive answers — citation accuracy 4.04

A recurring pattern: a correct, well-grounded answer that cites nothing
(`database_01`, `database_02`, `intro_to_ai_14` all scored 1–2 here while scoring 4–5 on
correctness). The model answers from the retrieved content but omits the chunk references,
so the student cannot verify sources. **Recommendation:** strengthen the final-answer
instruction to require a citation per factual paragraph, and reject/retry answers with zero
citations when retrieval returned content.

### 4. Parametric-knowledge fill-in when the KB lacks the topic

When the index does not contain the asked content, the tutor does **not** say so — it
answers from model knowledge while looking sourced:

- `discrete_math_07` (Kruskal — the only question whose topic is genuinely absent from the
  course slides, which teach Prim only): all six metrics = 1. The answer blended
  Prim/Kruskal descriptions over Prim-only chunks.
- `discrete_math_12` (pigeonhole): chunks only name the Dirichlet principle in a TOC, yet
  the answer produced a detailed formal statement (ceiling-function general form) not
  present in any chunk — faithfulness 1, citations pointing at TOC entries.
- `discrete_math_06` (safe edge): general MST definition asked, only Prim-specific content
  indexed → answer silently narrowed the definition (correctness 2).

This mirrors the document-processing evaluation's finding (hallucination is the pipeline's
primary failure axis). **Recommendation:** add an explicit "if the retrieved material does
not cover the question, say so" instruction plus a groundedness check before answering.

### 5. Residual ground-truth/KB mismatches (known, minor)

`discrete_math_08` (Θ(n³) never stated on the slides → recall 2) and `database_07` (the
normalization deck shows insertion-anomaly examples but never defines *update* anomaly
explicitly → recall 1) are knowledge-base gaps flagged in
`expected/_review_report.md`, not tutor regressions.

## What went well

- **IT3160E is near-ceiling (4.71 overall)**: 17/20 questions scored ≥4 on every metric —
  when the deck content is clean and on-topic, the full loop (retrieve → answer → cite) works.
- **Retrieval recall 4.48**: after ingesting the 24 missing lectures, the right content is
  almost always fetched (the pre-ingest review predicted this would have failed on 38/50).
- **Zero judge failures**: 300/300 strict-JSON verdicts on the first pass (3-retry budget
  mostly unused).

## Reproduce / artifacts

- Per-question verdicts with evidence: `results/<qid>.json`; aggregates: `results/summary.json`.
- Tutor outputs (answers + citations + every retrieved chunk): `actual/<qid>.json`.
- 50 chat sessions created during generation: `actual/_created_session_ids.json` (cleanup list).
- Method + coverage history: `README.md`, `expected/_review_report.md`,
  spec `docs/superpowers/specs/2026-07-07-ai-tutor-evaluation-design.md`.
