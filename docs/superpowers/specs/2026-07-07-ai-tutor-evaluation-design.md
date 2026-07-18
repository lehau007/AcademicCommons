# AI Tutor Evaluation Harness — Design Spec

**Date:** 2026-07-07
**Author:** lehau007 + Claude
**Status:** Approved design

## 1. Goal

Evaluate the quality of the **AI tutor** (RAG agent loop, `tutor_query_agent_loop` in
`src/backend/app/services/tutor_service.py` — the exact code path the production endpoint uses)
against human-authored ground-truth Q&A, using RAGAS-style metrics scored by an LLM judge via
OpenRouter. Second AI-subsystem evaluation for the thesis (first:
`evaluation/document_processing_evaluation/`).

## 2. Scope & Decisions (locked)

- **Dataset:** the existing 50 Q&A pairs in `data/RAG_evaluation_data/`
  (intro_to_ai: 20 → IT3160E, discrete_math: 20 → IT3020E, database: 10 → IT3292E).
  All three courses verified to have indexed chunks (59 / 64 / 79).
- **Ground-truth trust:** Claude cross-checks every ground-truth answer against the courses'
  indexed chunks and writes `expected/_review_report.md` flagging suspicious answers;
  **the user verifies this report before any scoring runs** (quality gate).
- **Actual output:** produced by the real backend — an in-container script (in `api`) creates a
  chat session per question's course, wraps `RetrievalService` with a recorder (to capture ALL
  retrieved chunks, not just cited ones), and calls `tutor_query_agent_loop`. No backend code
  changes, no JWT needed.
- **Scoring:** NOT judge sub-agents this time. A script calls the OpenRouter API
  (key already present in the `api` container, len 73): **one call = one metric of one
  question** → 50 × 6 = 300 calls, run in parallel with a concurrency limit.
- **Judge model:** a strong model dedicated to judging (default
  `anthropic/claude-sonnet-4.5`), passed as a script parameter — independent of the backend's
  `OPENROUTER_MODEL`.

## 3. Directory Layout

```
evaluation/ai_tutor_evaluation/
├── README.md                  # how to reproduce end-to-end
├── dataset/
│   ├── manifest.json          # course mapping, question counts, run metadata
│   └── questions.json         # 50 normalized questions:
│                              #   {qid, course_code, question, ground_truth}
│                              #   qid = intro_to_ai_01 … database_10
├── expected/
│   └── _review_report.md      # Claude's cross-check of ground truths vs indexed chunks
│                              #   (per-question verdict OK/suspicious) — USER VERIFIES
├── actual/
│   ├── <qid>.json             # answer, citations (cited chunks), retrieved_chunks (all,
│   │                          #   with scores + text), session_id, timings, iterations
│   └── _created_session_ids.json  # for later DB cleanup
├── metrics/
│   └── rubric.md              # 6 metrics, 1–5 anchors, per-call JSON output schema
├── scripts/
│   ├── run_tutor.py           # in-container generation (light parallelism 2–3, resumable)
│   ├── judge.py               # in-container scoring via OpenRouter (asyncio, semaphore ~8,
│   │                          #   retry + backoff, strict JSON validation)
│   └── aggregate.py           # merge → results/summary.json
└── results/
    ├── <qid>.json             # 6 metric scores + justification + evidence, merged
    ├── summary.json           # per-metric and per-course mean/min/max
    └── report.md              # human-readable findings + recommendations
```

## 4. Metrics (RAGAS-style, matches the thesis evaluation framework)

Each scored 1–5 with justification + quoted evidence (same anchor scale as the
document-processing rubric):

1. **Faithfulness** — the answer contains only claims grounded in the retrieved contexts;
   every ungrounded claim is listed.
2. **Answer Relevancy** — the answer addresses the question actually asked.
3. **Answer Correctness** — factual agreement with the ground-truth answer
   (missing/extra/contradicting content).
4. **Context Precision** — fraction of retrieved chunks that are relevant to the question.
5. **Context Recall** — do the retrieved contexts contain the information needed to produce
   the ground-truth answer?
6. **Citation Accuracy** — do the citations point to chunks that actually support the cited
   statements?

Each judge call receives: one metric definition + anchors, the question, ground truth, the
tutor's answer, all retrieved chunks, and the citations → returns strict JSON
`{score, justification, evidence[]}`.

## 5. Execution Order (gated)

1. Scaffold dirs; normalize `questions.json` + `manifest.json` from `data/RAG_evaluation_data/`.
2. Write `metrics/rubric.md`.
3. Claude cross-checks the 50 ground truths against indexed chunks →
   `expected/_review_report.md`.
4. `run_tutor.py` in the `api` container → 50 × `actual/<qid>.json`
   (session IDs recorded for cleanup).
5. **GATE: user verifies the review report** (and any flagged questions are excluded/fixed).
6. `judge.py` → 300 OpenRouter calls → `results/<qid>.json`.
7. `aggregate.py` + Claude writes `results/report.md`.

## 6. Risks & Mitigations

- **50 sequential tutor runs are slow / burn Gemini quota** → light parallelism (2–3) and
  per-question progress files so the run is resumable.
- **Judge returns malformed JSON** → validate, retry up to 3×, mark the cell `null` and
  continue rather than failing the batch.
- **Live-DB pollution (50 chat sessions)** → record created session IDs in
  `actual/_created_session_ids.json` for later cleanup.
- **Ground truth may cover content that is not indexed** (answers were authored from full
  course material) → that is exactly what the review report + Context Recall metric surface;
  flagged questions can be excluded from scoring at the gate.
