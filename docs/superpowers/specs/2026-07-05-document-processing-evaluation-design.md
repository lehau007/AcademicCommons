# Document Processing Evaluation Harness — Design Spec

**Date:** 2026-07-05
**Author:** lehau007 + Claude
**Status:** Approved design, pending spec review

## 1. Goal

Evaluate the quality of the system's **document extraction & processing** (OCR / parsing /
normalization) against human-verified ground truth. This is the first of several AI-subsystem
evaluations for the thesis.

Method: for a curated dataset of real documents, compare the pipeline's **actual** output
against **expected** (ground-truth) digitizations, using per-file LLM judges scoring a fixed
metric rubric. Produce an aggregate report.

## 2. Scope & Decisions (locked)

- **Dataset size:** 10 real files, each with **full** ground truth (not sliced).
- **Ground truth ("expected"):** Claude reads each source with its own tools (no API key
  needed) and produces a faithful digitized markdown. **The user verifies each ground-truth
  file before scoring** — this human-in-the-loop step is the quality gate that keeps the
  reference trustworthy.
- **Actual output:** produced by the **real running `src/backend` pipeline** (worker-ocr),
  then read back from the database + object storage. NOT the `src/experiments` script.
- **Trigger:** an in-container Python script that calls the backend's own
  `upload_official_document` / `upload_community_document` service (the same code the HTTP
  endpoint calls) using the existing **admin** user as uploader. No login/JWT/credentials
  needed. This creates the `Document`, stores the raw file in MinIO, and enqueues the OCR job
  that worker-ocr processes with the container's `GEMINI_API_KEY`.
- **Judges:** 10 sub-agents, **one per file**, each scoring the full rubric for its file.
- **Aggregation:** Claude collects the 10 result JSONs into a summary + human-readable report.

## 3. Environment (verified)

- Full stack running in Docker: `graduationthesis-{api,worker-ocr,worker-index,worker-eval,
  postgres,minio,redis}-1`, healthy, up 24h+.
- `api` and `worker-ocr` containers both have `GEMINI_API_KEY` (len 39) and
  `OCR_ENABLE_REAL_VISION=true`.
- App database: **`academic_kb`** on `graduationthesis-postgres-1` (user `postgres`). Contains
  27 courses (incl. all target course codes: IT3020E, IT3160E, IT3210, IT3220, IT3292E, …),
  6 users (1 admin, 2 reviewers, 3 students), 34 already-processed documents.
- Object storage: MinIO. Full processed markdown stored at `documents.storage_md_path`
  (e.g. `documents/<course>/<doc>/markdown/output.md`).

## 4. Directory Layout

```
evaluation/document_processing_evaluation/
├── README.md                 # how to reproduce end-to-end
├── dataset/
│   ├── manifest.json         # per file: id, source_path, course_code, tier, material_type,
│   │                         #   expected_type, expected_route, notes
│   └── <id>.<ext>            # the 10 source files (copied from data/sample or fetched MinIO)
├── expected/
│   └── <id>.md               # ground-truth digitization (Claude writes, USER verifies)
├── actual/
│   └── <id>/
│       ├── output.md         # full markdown pulled from MinIO (documents.storage_md_path)
│       ├── summary.json      # document_summaries row (topic, concepts, language, ocr_quality,
│       │                     #   section_summaries, overall_summary)
│       ├── chunks.json       # document_chunks ordered by chunk_order (if present)
│       └── processing_meta.json  # document_id, status, route/inferred_type (best-effort from
│                             #   worker-ocr logs), job timings
├── metrics/
│   └── rubric.md             # metric definitions + 1–5 scoring guide + JSON output schema
└── results/
    ├── <id>.json             # per-file judge output (strict schema)
    ├── summary.json          # per-metric means, per-file table
    └── report.md             # human-readable findings (strengths, weaknesses, worst offenders)
```

## 5. Dataset — 10 files (diversity-driven; final picks confirmed with user)

Chosen to span **format**, **language**, and **content** so the evaluation stresses every route.
Bias toward smaller files so full ground truth stays faithful.

| # | Axis exercised | Candidate | Course | Route stressed |
|---|----------------|-----------|--------|----------------|
| 1 | EN slides, small baseline | IT3160E `lecture1_presentation` (7p) | IT3160E | digital text |
| 2 | EN slides + diagrams | IT3020E `2_2-GraphPresentation` (17p) | IT3020E | vision (figures) |
| 3 | VN slides + code + diacritics | IT3210 `CLang-Lect13` (16p) | IT3210 | VN OCR + code |
| 4 | Scanned exam (true OCR) | community `Database-giữa kì cô Oanh` | IT3292E | vision_only |
| 5 | Standalone image | `test_image` (png/jpg) | (test) | image route |
| 6 | PPTX | SoICT `IntroInfoSec` pptx | (mapped in manifest) | pptx route |
| 7 | Math / formulas | IT3020E short discrete-math deck | IT3020E | formula fidelity |
| 8 | Tables | IT3292E `01_02_Introduction_RDB` | IT3292E | table structure |
| 9 | EN ML slides | IT3160E `lecture13-MachineLearning` (9p) | IT3160E | mixed |
| 10 | VN intro slides | IT3220 `CIntro-week01` | IT3220 | second VN sample |

Exact files finalized and written into `dataset/manifest.json`; user confirms before ground-truthing.

## 6. Ground-truth Format (`expected/<id>.md`)

Faithful, complete digitization of the source:

- All text in natural reading order.
- Headings as `#` / `##`; bullet/numbered lists preserved.
- Tables as markdown tables.
- Formulas in LaTeX-ish inline/block form.
- Code in fenced code blocks.
- Page/slide boundaries marked, e.g. `<!-- slide 3 -->`.
- Figures/diagrams noted as `![figure: <concise description>]` (describe, don't invent text).
- **No invented content.** Only what is actually in the document.

This is the "correct answer." **User verifies each file before any scoring runs.**

## 7. Actual Generation (backend + DB)

1. **Prepare uploader:** load the existing admin `User` from `academic_kb`.
2. **Trigger (per file):** in-container script calls
   `upload_official_document(session, storage, course_code, material_type, file_content,
   filename, uploader=admin)` (or `upload_community_document` for the scanned exam / image as
   community past_exam). This persists the `Document`, uploads raw bytes to MinIO, and enqueues
   the OCR `ProcessingJob`.
3. **Wait:** poll `academic_kb.processing_jobs` for `job_type=OCR`,
   `status=COMPLETED` (or FAILED) for each document.
4. **Extract actual:**
   - `output.md` ← MinIO object at `documents.storage_md_path`.
   - `summary.json` ← `document_summaries` row for the document.
   - `chunks.json` ← `document_chunks` where `document_id=…` ordered by `chunk_order` (present
     for official docs after the INDEX job; may be empty for community docs still evaluating).
   - `processing_meta.json` ← document id/status + `route`/`inferred_type` scraped best-effort
     from `docker logs graduationthesis-worker-ocr-1` around the processing window.
5. Land everything under `actual/<id>/`.

**Cleanup note:** these 10 uploads add rows to the live DB. The script records created document
IDs to `actual/_created_document_ids.json` so they can be identified/removed later if desired.

## 8. Metrics (`metrics/rubric.md`)

Each metric scored **1–5** with a one–two sentence justification and **concrete quoted
evidence** for any deduction. Metric 1 additionally yields an objective pass/fail.

1. **Classification & Routing** — did the pipeline pick the right doc type / route?
   Source: best-effort from worker-ocr logs (`route`, `inferred_type`) + `summary.language` +
   `summary.ocr_quality`. Compared to `expected_type` / `expected_route` in the manifest.
   *(Caveat: route/type are not persisted as DB columns, only in worker trace/logs.)*
2. **Text Coverage / Completeness** — proportion of ground-truth textual content present in
   `output.md` (recall of content).
3. **Extraction Fidelity / OCR Accuracy** — character/word correctness; Vietnamese diacritics
   intact; no garbling or mojibake.
4. **Structure Preservation** — headings, lists, tables, reading order, page/slide boundaries.
5. **Faithfulness / No Hallucination** — nothing in `output.md` that is not in the source;
   hallucinations flagged explicitly.
6. **Formula / Table / Code Handling** — math notation, tables, and code captured correctly.

Plus a **normalization sanity check** (not a scored metric): confirm the normalized markdown did
not drop or corrupt content relative to the raw extraction (judged from `output.md` coherence).

## 9. Judge Protocol (10 sub-agents, 1 per file)

Each sub-agent receives:
- The **source file** (readable — the real ground truth of what the document contains).
- `expected/<id>.md` (verified ground-truth digitization).
- `actual/<id>/*` (pipeline output).
- `metrics/rubric.md`.

It must:
- Score each of the 6 metrics 1–5 with justification + quoted evidence.
- Flag any hallucinations (Metric 5) with the specific invented text.
- Emit **strict JSON** to `results/<id>.json` matching the schema in `rubric.md`
  (`{file_id, scores:{metric:{score, justification, evidence[]}}, classification:{expected,
  actual, pass}, hallucinations:[], overall_comment}`).

Instructions bias toward low variance: cite evidence, prefer the rubric anchors, no free-form
rescaling.

## 10. Aggregation & Report

Claude collects the 10 `results/<id>.json` and produces:
- `results/summary.json` — per-metric mean/min/max, per-file score table, classification
  accuracy (pass rate), hallucination count.
- `results/report.md` — human-readable: overall picture, per-metric findings, per-route
  breakdown (digital vs scanned vs image vs pptx), worst offenders with evidence, and concrete
  recommendations.
- (Optional) a visual Artifact version of the report.

## 11. Execution Order (each phase gated)

1. Scaffold dirs; select 10 files; write `dataset/manifest.json`; copy/fetch sources
   → **user confirms selection**.
2. Write `metrics/rubric.md`.
3. Produce `expected/<id>.md` for all 10 → **user verifies** (main quality gate).
4. Run the in-container trigger script; wait for OCR completion; extract `actual/<id>/*` from
   DB + MinIO.
5. Dispatch 10 judge sub-agents → `results/<id>.json`.
6. Aggregate → `results/summary.json` + `results/report.md`.

## 12. Risks & Mitigations

- **Ground-truth effort is large** (10 full docs). Mitigation: bias to smaller files; user
  verifies; can trim a file if a source is unexpectedly huge.
- **Route/type not persisted.** Mitigation: scrape worker-ocr logs best-effort; if unreliable,
  Metric 1 degrades to language/ocr_quality signals + a note (does not block metrics 2–6).
- **Live-DB pollution** from 10 uploads. Mitigation: record created document IDs for later
  cleanup; uploads use the normal product path so they are valid rows, not corrupt state.
- **Judge as both nothing-vs-something:** judges see the real source file, so ground truth is
  anchored to the document itself, not only to Claude's transcription.
- **Container missing deps** for a route: worker-ocr already processed 34 docs, so the
  production deps are present; low risk.
```
