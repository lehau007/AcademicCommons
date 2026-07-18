# Document Processing Experimentation and Testing Plan (Inventory-First)

This document defines a detailed plan to implement and validate the OCR and parsing proof-of-concept before backend service development begins.

The plan follows a strict rule:
- Reuse existing real samples first.
- Do not auto-generate files for courses that already have usable sample coverage.
- Fill only missing edge-case gaps needed to evaluate routing and extraction quality.

## 1. Objectives

1. Validate routing logic for PDF, PPTX, and image inputs.
2. Validate hybrid extraction quality for mixed-content documents.
3. Produce reproducible outputs and logs for later backend integration.
4. Keep experiments course-scoped and traceable.

## 2. Non-Negotiable Policies

1. Inventory-first policy:
   - All experiments start from files that already exist in `data/sample/`.
2. No blind generation:
   - If a course already has usable files for a required case, do not generate more test files for that case.
3. Gap-only synthesis:
   - Synthetic documents are allowed only when a required edge-case category is missing from the current inventory.
4. Manifest-driven execution:
   - The runner processes only files listed in a manifest file.

## 3. Current Inventory Snapshot (Observed)

Based on workspace inspection:

1. Official samples with real files present:
   - IT3020E
   - IT3160E
   - IT3210
   - IT3220
   - IT3292E
2. Community samples with real files present:
   - IT3292E (`past_exam`) with both PDF and JPG.

Implication:
- Initial OCR experiments can run immediately on existing data without any auto-generation step.

## 4. Required Edge-Case Matrix

The experiment must cover these input categories at least once:

1. Text-rich PDF.
2. Scanned PDF (image-only or nearly no text layer).
3. Mixed-content PDF (text + table/diagram/formula).
4. PPTX (text + embedded images if available).
5. Standalone image (`.jpg` or `.png`).

Coverage rule:
- Categories can be satisfied by any course.
- Do not force every course to contain all five categories in phase 1.

## 5. Dataset Manifest Design

Create `src/experiments/document_processing/dataset_manifest.json` (manual curation, no auto-generation):

Each entry should contain:

1. `id`: stable sample id.
2. `course_code`: SoICT course code.
3. `tier`: `official` or `community`.
4. `input_path`: relative path to source file.
5. `expected_type`: `text_pdf | scanned_pdf | mixed_pdf | pptx | image`.
6. `expected_route`: `direct_text | hybrid | vision_only`.
7. `notes`: optional reviewer notes.

Example entry:

```json
{
  "id": "it3292e_midterm_img_01",
  "course_code": "IT3292E",
  "tier": "community",
  "input_path": "data/sample/community/IT3292E/past_exam/Database - giua ki co Trinh.jpg",
  "expected_type": "image",
  "expected_route": "vision_only",
  "notes": "Community past exam image"
}
```

## 6. Pipeline Implementation Plan

Implement in `src/experiments/document_processing/document_processing_pipeline.py`.

### 6.1 Runtime Modes

1. `inventory`
   - Scan `data/sample/` and report available formats by course and tier.
   - Output: `data/pipeline_outputs/document_processing_experiments/inventory_report.json`.
2. `gap-report`
   - Compare inventory against required edge-case matrix.
   - Output: `data/pipeline_outputs/document_processing_experiments/gap_report.json`.
   - Must not create synthetic files automatically.
3. `run`
   - Execute only files listed in manifest.
   - Output one folder per run id with per-file artifacts.

### 6.2 Routing Logic

1. PDF:
   - Extract text with PyMuPDF.
   - Compute text density and image presence.
   - Route:
     - `direct_text`: sufficient text, low visual complexity.
     - `hybrid`: text present and image blocks detected.
     - `vision_only`: near-empty text layer.
2. PPTX:
   - Extract slide text and notes with `python-pptx`.
   - Extract embedded images and pass images to Gemini vision step.
3. Images:
   - Always route to Gemini vision step.

### 6.3 Hybrid Merge Contract

1. Preserve approximate reading order using page/slide index and bounding boxes.
2. Convert visual content to text with explicit format instructions:
   - Tables -> markdown table.
   - Formulas -> LaTeX.
   - Diagrams -> structured bullet explanation.
3. Produce a single normalized markdown output per file.

## 7. Output Structure

All run artifacts are written under:

`data/pipeline_outputs/document_processing_experiments/{run_id}/`

Per input file include:

1. `result.md`: merged normalized markdown.
2. `metadata.json`: route, timing, model, file hashes.
3. `vision_prompts.json`: prompts and image references used.
4. `quality_flags.json`: heuristic quality checks and warnings.

Run-level files:

1. `run_summary.json`.
2. `coverage_report.json`.
3. `errors.json`.

## 8. Execution Steps

1. Build manifest from existing files first.
2. Run inventory mode and review report.
3. Run gap-report mode.
4. If gaps remain, add only minimum manual samples required.
5. Run full pipeline mode on manifest entries.
6. Review outputs and label pass/fail per case.

## 9. Verification Plan

### Automated Checks

1. Routing classification aligns with `expected_route` in manifest.
2. No runtime crash across all manifest entries.
3. Required edge-case categories all covered in coverage report.
4. Markdown output exists and is non-empty for each successful item.

### Manual Checks

1. Compare source vs markdown for semantic completeness.
2. Verify table formatting quality.
3. Verify formula conversion correctness.
4. Verify text-image stitching coherence and reading flow.

## 10. Acceptance Criteria

Phase 1 is accepted when all conditions hold:

1. Manifest exists and is traceable to real files.
2. Inventory and gap reports are generated.
3. All required edge-case categories are covered.
4. At least one successful run produces complete artifacts in output folder.
5. No automatic synthetic generation occurred for courses already having usable samples.

## 11. Open Decisions for Reviewer

1. Multi-column reading order strictness for phase 1 (`best-effort` vs `strict`).
2. Gemini API key availability in local environment.
3. Whether to add optional benchmark metrics (CER/WER proxies) in this phase.

## 12. Immediate Next Actions

1. Create `dataset_manifest.json` from current real samples.
2. Implement `inventory` mode first (fast validation value).
3. Add `gap-report` mode before full OCR run mode.
4. Run first end-to-end batch on IT3292E community + one official course.

## 13. Sub-Agent Execution Plan

This section translates the implementation plan into coordinated sub-agent work units.

### 13.1 Agent Topology

1. `SA-0 Orchestrator`
   - Owns run lifecycle, dependency checks, and final run status.
2. `SA-1 Inventory Agent`
   - Scans `data/sample/` and emits inventory report.
3. `SA-2 Manifest Agent`
   - Validates curated manifest entries against real files and schema.
4. `SA-3 Gap Analysis Agent`
   - Computes coverage gaps against required edge-case matrix.
5. `SA-4 Routing Agent`
   - Computes route decision (`direct_text | hybrid | vision_only`) per file.
6. `SA-5 Extractor Agent`
   - Executes format-specific extraction (PDF/PPTX/Image).
7. `SA-6 Merge and Normalize Agent`
   - Merges text and vision outputs into one normalized markdown result.
8. `SA-7 Quality Agent`
   - Runs heuristics, flags quality risks, and checks expected route match.
9. `SA-8 Reporting Agent`
   - Produces run-level summaries (`run_summary.json`, `coverage_report.json`, `errors.json`).

### 13.2 Agent Contracts

1. `SA-0 Orchestrator`
   - Input: runtime mode + optional run id + manifest path.
   - Output: run folder bootstrap, task graph, aggregate status.
   - Done when: all required downstream agents complete or terminal failure is recorded.

2. `SA-1 Inventory Agent`
   - Input: `data/sample/` root.
   - Output: `inventory_report.json` with counts by `course_code`, `tier`, format.
   - Done when: scan completes without missing-path errors.

3. `SA-2 Manifest Agent`
   - Input: `dataset_manifest.json`.
   - Output: `manifest_validation.json` containing valid/invalid entries and reasons.
   - Done when: every entry is resolved to an existing file or explicitly marked invalid.

4. `SA-3 Gap Analysis Agent`
   - Input: inventory report + edge-case matrix.
   - Output: `gap_report.json` with covered/missing categories.
   - Done when: each required category has status `covered` or `missing`.

5. `SA-4 Routing Agent`
   - Input: manifest entry + lightweight file probes.
   - Output: route decision and route evidence in per-file `metadata.json`.
   - Done when: route is assigned with explicit evidence fields.

6. `SA-5 Extractor Agent`
   - Input: manifest entry + route decision.
   - Output: raw extraction artifacts (text blocks, image OCR output, slide text).
   - Done when: extraction output exists for all successful files.

7. `SA-6 Merge and Normalize Agent`
   - Input: extractor artifacts.
   - Output: per-file `result.md` and `vision_prompts.json`.
   - Done when: normalized markdown exists and is non-empty.

8. `SA-7 Quality Agent`
   - Input: `result.md`, metadata, expected route from manifest.
   - Output: `quality_flags.json`, route match status, warnings.
   - Done when: quality checks run and output is serialized even for warning-only cases.

9. `SA-8 Reporting Agent`
   - Input: all per-file outcomes.
   - Output: run-level summary files.
   - Done when: totals and pass/fail counters are internally consistent.

### 13.3 Execution Graph by Mode

1. `inventory` mode
   - Flow: `SA-0 -> SA-1 -> SA-8`.
   - Required output: inventory report and minimal run summary.

2. `gap-report` mode
   - Flow: `SA-0 -> SA-1 -> SA-3 -> SA-8`.
   - Required output: gap report without creating synthetic files.

3. `run` mode
   - Flow: `SA-0 -> SA-2 -> (SA-4 -> SA-5 -> SA-6 -> SA-7) x N -> SA-8`.
   - Parallelism: per-file chain can run concurrently after manifest validation.

### 13.4 Reviewer Gates (Human-in-the-Loop)

1. Gate A (post `gap-report`):
   - Reviewer confirms whether missing categories require manual sample addition.
2. Gate B (post first `run`):
   - Reviewer inspects selected outputs for semantic completeness and formatting quality.
3. Gate C (before phase sign-off):
   - Reviewer confirms all acceptance criteria in Section 10 are satisfied.

### 13.5 Failure and Retry Policy

1. Per-file hard failures must not abort the full batch.
2. `SA-5` and `SA-6` support bounded retries (default: 2).
3. All terminal failures are appended to `errors.json` with:
   - `sample_id`, `stage`, `error_type`, `message`, `retry_count`, `timestamp`.
4. `SA-8` must mark run status:
   - `success` if no terminal failures.
   - `partial_success` if at least one file succeeded and at least one failed.
   - `failed` if all files failed or pre-run validation failed.

### 13.6 Ownership and Deliverables by Wave

1. Wave 1 (Foundation)
   - Agents: `SA-0`, `SA-1`, `SA-2`, `SA-3`.
   - Deliverables: inventory report, manifest validation, gap report.

2. Wave 2 (Extraction Core)
   - Agents: `SA-4`, `SA-5`, `SA-6`.
   - Deliverables: per-file `result.md`, `metadata.json`, `vision_prompts.json`.

3. Wave 3 (Validation and Reporting)
   - Agents: `SA-7`, `SA-8`.
   - Deliverables: `quality_flags.json`, `run_summary.json`, `coverage_report.json`, `errors.json`.

### 13.7 Definition of Done for Sub-Agent Plan

This sub-agent execution plan is considered operational when:

1. Each mode (`inventory`, `gap-report`, `run`) can be mapped to a deterministic agent flow.
2. Every agent has explicit input/output contracts.
3. Human reviewer gates are placed at the exact points where policy decisions are needed.
4. Failure semantics are standardized for downstream backend integration.
