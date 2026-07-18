# Document Processing Evaluation

Evaluates the quality of the system's document extraction / OCR / normalization pipeline
(`src/backend`) against human-authored ground truth, using per-file LLM judges.

## Layout

```
dataset/     10 real source files + manifest.json (id, course, tier, expected_type/route, language)
expected/    <id>.md — human-authored ground-truth digitization (VERIFY before trusting scores)
actual/      <id>/{output.md, summary.json, chunks.json, processing_meta.json} — pulled from DB+MinIO
metrics/     rubric.md — 6 metrics, 1–5 anchors, JSON output schema
results/     <id>.json (per-file judge output) + summary.json + report.md
```

## How `actual` was produced

The live stack (`graduationthesis-*` containers) processes the files via the real backend:

1. `dataset/` + a driver script are copied into the `api` container.
2. The driver calls `upload_community_document(...)` (same code the HTTP endpoint uses) with the
   existing admin user, for each file → creates a `Document`, stores raw bytes in MinIO, enqueues
   an OCR `ProcessingJob`.
3. `worker-ocr` runs the pipeline (`OCR_ENABLE_REAL_VISION=true`, `GEMINI_API_KEY` set) and writes
   the normalized markdown to MinIO + a `document_summaries` row.
4. An extraction script reads `documents.storage_md_path` (→ `output.md`), the summary, chunks, and
   job status back out of `academic_kb` + MinIO into `actual/<id>/`.

Created document ids: `actual/_created_document_ids.json` (for later DB cleanup).

## Scoring

10 judge sub-agents (one per file) each read `metrics/rubric.md`, `expected/<id>.md`, and
`actual/<id>/*`, then write `results/<id>.json`. Aggregate with the summary/report step
(`results/summary.json`, `results/report.md`).

## Headline result

Overall **4.30/5**; routing 10/10; weakest metric = **faithfulness (3.9)** — the pipeline's main
failure mode is hallucinated figure/diagram descriptions on the vision path, plus OCR-fidelity
collapse on low-quality scans. The native-pptx path (`it4015e_access_control_pptx`) is
hallucination-free but degrades structure (footers-as-headings, flattened nesting). See
`results/report.md`.
