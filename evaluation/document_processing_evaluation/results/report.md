# Document Processing Evaluation — Report

**Date:** 2026-07-06
**Dataset:** 10 real documents (`evaluation/document_processing_evaluation/dataset/`)
**Pipeline under test:** live `src/backend` OCR pipeline (worker-ocr, Gemini vision + LLM normalization), output pulled from DB + MinIO.
**Method:** per-file LLM judges (10 sub-agents, one per file) scoring 6 metrics 1–5 against human-authored ground truth (`expected/`). See `metrics/rubric.md`.

> Note: `expected/` ground truth was re-verified against the source files on 2026-07-06 (all 10 files, text + figure coverage). The 4 figure-partial files flagged in the earlier audit have been re-authored. The `it3210_ocr_demo_slides_pptx` demo deck was replaced by the real 58-slide `it4015e_access_control_pptx` deck, which is now scored (previously the demo file's straight-5s were in the aggregate).

## Headline numbers

| | |
|---|---|
| **Overall mean score** | **4.30 / 5** |
| Classification & routing pass rate | **10/10 (100%)** |
| Files with zero hallucinations | 5 / 10 |
| Total hallucinated spans flagged | 46 |

### Per-metric (mean / min / max)

| Metric | Mean | Min | Max |
|---|---|---|---|
| Classification & Routing | **4.7** | 4 | 5 |
| Text Coverage / Completeness | 4.4 | 3 | 5 |
| Extraction Fidelity / OCR | 4.4 | 2 | 5 |
| Structure Preservation | 4.2 | 3 | 5 |
| **Faithfulness / No Hallucination** | **3.9** | 2 | 5 |
| Formula / Table / Code | 4.2 | 3 | 5 |

**Faithfulness is the weakest dimension** — the pipeline's dominant failure mode is *inventing* content, not losing it.

## Per-file results

| File | Format | Route | Class | Cover | Fidel | Struct | Faith | F/T/C | Avg |
|---|---|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| it3210_ocr_demo_chart_png | png | vision | 5 | 5 | 5 | 5 | 5 | 5 | **5.00** |
| it3210_clang_lect13_vi | pdf | hybrid | 5 | 4 | 5 | 5 | 5 | 5 | **4.83** |
| it3160e_intro_ai_presentation | pdf | hybrid | 4 | 5 | 5 | 4 | 5 | 5 | **4.67** |
| it3292e_exam_giuaki_trinh_jpg | jpg | vision | 5 | 5 | 4 | 5 | 5 | 4 | **4.67** |
| it3160e_machine_learning | pdf | hybrid | 5 | 5 | 5 | 4 | 3 | 5 | **4.50** |
| it3292e_exam_giuaki_oanh_pdf | pdf | vision | 5 | 5 | 4 | 4 | 4 | 4 | **4.33** |
| it4015e_access_control_pptx | pptx | hybrid | 5 | 4 | 5 | 3 | 5 | 4 | **4.33** |
| it3160e_ai_introduction | pdf | hybrid | 4 | 5 | 5 | 4 | 3 | 4 | **4.17** |
| it3020e_graph_presentation | pdf | hybrid | 4 | 3 | 4 | 4 | 2 | 3 | **3.33** |
| it3292e_exam_cuoiki_2022_pdf | pdf | vision | 5 | 3 | 2 | 4 | 2 | 3 | **3.17** |

### By route

| Route | Class | Cover | Fidel | Struct | Faith | F/T/C |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| hybrid (digital PDF / pptx) | 4.5 | 4.33 | **4.83** | 4.0 | 3.83 | 4.33 |
| vision_only (scanned / image) | **5.0** | 4.5 | **3.75** | 4.5 | 4.0 | 4.0 |

Routing is picked correctly every time. Digital/hybrid docs extract text with high fidelity but are the most prone to *hallucinated figure captions*; scanned/vision docs are faithful in structure but fidelity collapses when the scan is low-quality.

## What works well

- **Routing & classification: flawless (10/10).** Digital slides → hybrid, scanned exams → vision_only, images → vision_only, pptx → pptx/hybrid, all correct.
- **Text-native extraction is excellent.** Clean English/Vietnamese decks (`intro_ai_presentation`, `clang_lect13_vi`, `machine_learning`) capture essentially all text with correct Vietnamese diacritics — the VN C-deck even *improved* word boundaries over the raw PDF (`"Đểtruy nhập" → "Để truy nhập"`) and preserved all C code verbatim.
- **Vision on clean visuals is faithful.** The standalone chart PNG was described accurately (correct title "Demo KPI Trend", axes, trend) **with no invented numeric values**.
- **Native pptx extraction is clean and hallucination-free.** The 58-slide `it4015e_access_control_pptx` deck captured all slide text with perfect symbol fidelity (`⊆`, `≥`, `¬dom`, `🡪`) and 5 of 6 tables as well-formed markdown, with **zero hallucinations** — the opposite of the vision path's failure mode.
- **Good-quality scans OCR well.** The English midterm JPG captured all 4 questions, both FD sets (arrows intact), all 6 schema relations and 6 queries, in order, zero hallucinations.

## Key weaknesses (ranked)

### 1. Hallucinated figure/diagram descriptions on the vision path (systemic)
When a slide contains a diagram, the pipeline often **invents interpretive text that isn't on the slide**:
- `it3020e_graph_presentation` — **12** fabricated `[Diagram: … This matters because …]` paragraphs (English + Vietnamese editorial commentary); one even describes a matrix it never rendered. (faithfulness **2**)
- `it3160e_ai_introduction` — **5** invented ASCII-art figures + `[Diagram: …]` caption paragraphs asserting analysis absent from the source. (faithfulness **3**)
- `it3160e_machine_learning` — **6 invented category labels** (Business, Entertainment, Science, Sports, Technology, Travel & Tourism) on a slide that only says "Which cat.?", plus 4 fabricated "It matters because…" sentences. (faithfulness **3**)

This is the **single most important defect**: for a RAG knowledge base, invented content is worse than missing content.

### 2. OCR fidelity collapses on low-quality scans
- `it3292e_exam_cuoiki_2022_pdf` (blurry phone photo) — course code misread **IT3092 vs IT3292**, most functional-dependency formulas wrong/fabricated, whole multiple-choice option sets hallucinated (e.g. Câu 12 options `MIDDLEAGE/CONVERT/SHORT` replacing `ROLLBACK/COMMIT/ABORT`; a non-existent "Câu 11 (D) 4NF" added). Macro-structure (3 parts, 16 questions) survived, but technical content is unreliable. (fidelity **2**, faithfulness **2**)

### 3. Table / structure fidelity slips
- `it3292e_exam_giuaki_oanh_pdf` — invented an extra empty column and a non-existent `ThongTin` attribute in the `HocPhan(MaHP, TenHP, soTC, heSoCKy)` schema table.
- `it3292e_exam_giuaki_trinh_jpg` — bold **primary keys** / italic *foreign keys* flattened to plain text, and two relation names lost underscores (`Recipient_Transaction → Recipient Transaction`), so PK/FK can no longer be told apart.
- `it3020e_graph_presentation` — the undirected weight-matrix table (slide 13) was dropped; the directed one downgraded to an ASCII block.
- `it4015e_access_control_pptx` — native pptx path degrades structure: recurring slide footers ("Sep 2009 / Information Security by Van K Nguyen…") are promoted to `##` headings, slide 32's "BLP Axioms 2." heading is left empty with its body scrambled under a footer heading, nested bullet lists are flattened, command pseudo-code is downgraded to bullet lists, and the slide-33 example table is dropped. (structure **3**) This is *lossy formatting*, not fabrication — faithfulness stays 5.
- Minor list-nesting errors on a couple of decks (`Search Algorithms` mis-indented).

## Recommendations

1. **Constrain the vision/figure step to description-only, no interpretation.** Forbid "This matters because…" / "[Diagram: …]" editorializing and speculative labels; instruct it to transcribe only text/labels actually visible, and to emit a neutral `![figure: …]` placeholder otherwise. This alone would lift the three lowest hybrid faithfulness scores.
2. **Gate low-quality scans.** `ocr_quality="low"` is already detected on the failing scan — surface it (the doc did go to `NEEDS_REVIEW`) and consider a higher-resolution re-OCR pass or human review before indexing, so fabricated technical content never reaches RAG.
3. **Preserve tabular structure and emphasis.** Keep markdown tables as tables (don't drop/downgrade to ASCII), and retain PK/FK emphasis (bold/italic) which carries schema semantics.
3b. **Clean up native-pptx structure.** Suppress recurring slide footers instead of promoting them to headings, keep per-slide title→body ordering, and preserve list nesting / pseudo-code blocks (see `it4015e_access_control_pptx`).
4. **Re-run after fixes** against this same harness to measure movement, especially on faithfulness and the two worst files.

## Caveats & limitations

- **Ground truth re-verified against sources on 2026-07-06** (text + figure coverage, all 10 files); the earlier `expected/_audit_report.md` is superseded. One manifest label is still imperfect: `it3292e_exam_giuaki_trinh_jpg` is tagged `language=vi` but the printed exam is English (judged against real content).
- **Route/`inferred_type` are not persisted** to the DB (only in worker traces). The classification metric inferred the route from output characteristics + `summary.language`/`summary.ocr_quality`; it is the least direct metric here.
- **Chunks are empty** for all files: uploaded as community docs, which stop at `EVALUATING` before the INDEX (chunking) step. `actual/<id>/output.md` (full markdown from MinIO) is the primary artifact judged.
- **LLM-as-judge variance:** single judge per file. Scores are directional, not certified; evidence strings in `results/<id>.json` back each deduction.
- **Live-DB footprint:** the 10 documents were uploaded to the running `academic_kb` DB (ids in `actual/_created_document_ids.json`) for later cleanup if desired.
