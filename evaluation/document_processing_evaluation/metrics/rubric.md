# Document Processing Evaluation — Metrics Rubric

Each judge scores **one file**. It receives:

- The **source file** itself (the real ground truth of what the document contains).
- `expected/<id>.md` — the human-verified digitization (reference "correct answer").
- `actual/<id>/output.md` — the pipeline's extracted/normalized markdown (from MinIO).
- `actual/<id>/summary.json` — the persisted `document_summaries` row.
- `actual/<id>/processing_meta.json` — status + best-effort `route`/`inferred_type` from worker logs.
- The manifest entry for the file (`expected_type`, `expected_route`, `language`, `pages`).

Score **6 metrics** on a **1–5** scale. For every metric give a 1–2 sentence justification and,
for any score below 5, **at least one concrete quoted piece of evidence** (a short string that
appears — or is wrongly missing/altered — in `actual/output.md` vs the source/expected).

## Scale anchors (apply to every metric)

- **5 — Excellent:** essentially perfect; no meaningful defect.
- **4 — Good:** minor issues that don't affect understanding.
- **3 — Acceptable:** noticeable issues but the core content is usable.
- **2 — Poor:** significant loss/error; content partially unusable.
- **1 — Failing:** metric essentially not met; content wrong or missing.

Anchor to the **source document**, not to stylistic preference. Do not reward or penalize
formatting choices that both the expected and actual outputs are free to make.

## Metrics

### 1. Classification & Routing
Did the pipeline identify the right document type and processing route?
- Compare `processing_meta.route` / `inferred_type` (best-effort from logs) against the manifest
  `expected_route` / `expected_type`. Use `summary.language` and `summary.ocr_quality` as
  supporting signals.
- **Also output an objective `pass` boolean**: true iff the detected route matches
  `expected_route` (or, if route is unavailable from logs, iff language/type signals are
  consistent with expectations).
- If route/type could not be recovered at all, score from the supporting signals and note it.

### 2. Text Coverage / Completeness
What fraction of the ground-truth **textual content** made it into `output.md`?
- 5 = all substantive text present; 3 = some sections/blocks missing; 1 = large portions absent.
- Evidence: quote specific text present in `expected/<id>.md` (or visible in the source) that is
  missing from `output.md`.

### 3. Extraction Fidelity / OCR Accuracy
Are the extracted characters/words correct?
- Focus on: Vietnamese diacritics intact (no `ô`→`o`, no mojibake), digits/symbols correct, no
  garbled or hallucinated character sequences, word boundaries preserved.
- Evidence: quote a garbled/incorrect string from `output.md` next to the correct source form.

### 4. Structure Preservation
Are headings, bullet/numbered lists, tables, reading order, and page/slide boundaries preserved?
- 5 = structure faithfully reflected; 3 = flattened lists/tables but order intact; 1 = structure
  destroyed or reading order scrambled.
- Evidence: cite a table/list/heading that is lost or reordered.

### 5. Faithfulness / No Hallucination
Does `output.md` contain **only** content actually in the source (no invented text)?
- 5 = nothing invented; 1 = substantial fabricated content.
- **List every hallucination** found (the specific invented string). This is the primary output
  of this metric; the score follows from it.

### 6. Formula / Table / Code Handling
Are math notation, tables, and code captured correctly and legibly?
- Applies where relevant (e.g. code in the VN C-programming deck, tables in exams, graph/chart
  labels). If a file has none of these, score 5 and note "N/A — no formulas/tables/code".
- Evidence: quote a mis-rendered formula/table/code fragment.

## Normalization sanity check (not scored)
Confirm the normalized markdown reads coherently and does not appear to have dropped or corrupted
large spans relative to what the source contains. Report as a short note, not a score.

## Required output — strict JSON to `results/<id>.json`

```json
{
  "file_id": "<id>",
  "scores": {
    "classification_routing":      { "score": 1, "justification": "", "evidence": [] },
    "text_coverage":               { "score": 1, "justification": "", "evidence": [] },
    "extraction_fidelity":         { "score": 1, "justification": "", "evidence": [] },
    "structure_preservation":      { "score": 1, "justification": "", "evidence": [] },
    "faithfulness_no_hallucination": { "score": 1, "justification": "", "evidence": [] },
    "formula_table_code":          { "score": 1, "justification": "", "evidence": [] }
  },
  "classification": {
    "expected_type": "", "expected_route": "",
    "actual_type": "", "actual_route": "",
    "pass": false
  },
  "hallucinations": [],
  "normalization_note": "",
  "overall_comment": ""
}
```

`evidence` entries are short quoted strings. `hallucinations` is a list of invented strings
found in `output.md`. Scores are integers 1–5.
