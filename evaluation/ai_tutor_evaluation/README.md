# AI Tutor Evaluation

Evaluates the AI tutor (`tutor_query_agent_loop` in `src/backend` — the exact code path of
`POST /tutor/query`) against 50 ground-truth Q&A pairs, using RAGAS-style metrics scored by
an LLM judge via OpenRouter. Companion to `evaluation/document_processing_evaluation/`.

Design spec: `docs/superpowers/specs/2026-07-07-ai-tutor-evaluation-design.md`.

## Layout

```
dataset/     questions.json (50 normalized Q&A: qid, course_code, question, ground_truth)
             + manifest.json. Source: data/RAG_evaluation_data/ (intro_to_ai→IT3160E,
             discrete_math→IT3020E, database→IT3292E)
expected/    _review_report.md — cross-check of every ground truth vs the indexed chunks
             (VERIFY before trusting scores; contains the coverage verdicts)
actual/      <qid>.json — tutor answer, citations, ALL retrieved chunks (with scores),
             session_id + _created_session_ids.json (for DB cleanup)
metrics/     rubric.md — 6 metrics (faithfulness, answer_relevancy, answer_correctness,
             context_precision, context_recall, citation_accuracy), 1–5 anchors, JSON schema
scripts/     run_tutor.py (generation), judge.py (scoring), aggregate.py (summary)
results/     <qid>.json (merged 6-metric judge output) + summary.json + report.md
```

## How to reproduce

Everything runs against the live stack (`graduationthesis-*` containers).

```bash
# 0. copy the harness into the api container
docker cp evaluation/ai_tutor_evaluation graduationthesis-api-1:/tmp/tutor_eval

# 1. generate actuals (real agent loop; ~2 concurrent; resumable)
docker exec graduationthesis-api-1 python /tmp/tutor_eval/scripts/run_tutor.py \
  --questions /tmp/tutor_eval/dataset/questions.json --out /tmp/tutor_eval/actual
docker cp graduationthesis-api-1:/tmp/tutor_eval/actual evaluation/ai_tutor_evaluation/

# 2. judge (300 calls = 50 questions x 6 metrics; uses container's OPENROUTER_API_KEY)
docker exec graduationthesis-api-1 python /tmp/tutor_eval/scripts/judge.py \
  --questions /tmp/tutor_eval/dataset/questions.json \
  --actual /tmp/tutor_eval/actual \
  --rubric /tmp/tutor_eval/metrics/rubric.md \
  --out /tmp/tutor_eval/results \
  --model anthropic/claude-sonnet-4.5
docker cp graduationthesis-api-1:/tmp/tutor_eval/results evaluation/ai_tutor_evaluation/

# 3. aggregate
python3 evaluation/ai_tutor_evaluation/scripts/aggregate.py \
  --results evaluation/ai_tutor_evaluation/results \
  --questions evaluation/ai_tutor_evaluation/dataset/questions.json
```

Cleanup: the runner creates one `chat_sessions` row per question (admin user); IDs are in
`actual/_created_session_ids.json`.

## Headline result

Overall **4.26/5** (judge `anthropic/claude-sonnet-4.5`, 300 calls, 0 nulls). Strong where
retrieval finds content; weakest metrics = **context_precision 3.76** (TOC/outline chunks
pollute retrieval) and **citation_accuracy 4.04** (correct answers without inline
citations). Biggest single defect: a product bug where 5/50 answers were literally the
`{"used_doc_ids": …}` JSON instead of an answer. See `results/report.md`.

## Coverage history (see `expected/_review_report.md`)

The initial review found only **11/50** ground truths covered by the then-indexed chunks
(each course had only 2–4 lectures indexed). At the gate the user chose to ingest the 24
missing lecture decks from `data/sample/official/` through the real pipeline
(`scripts/ingest_missing_lectures.py`; official tier skips HITL: OCR → APPROVED → INDEX).
After ingest: 46/50 covered, 3 partial, 1 impossible (Kruskal — the course slides teach
Prim only).
