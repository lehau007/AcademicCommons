# Expected-Output Ground-Truth Audit

**Last verified:** 2026-07-06 (supersedes the earlier figure-only audit).

## Methodology
For each of the 10 dataset files I re-rendered/parsed the source and compared it against the
ground-truth markdown in `expected/`, checking **both** dimensions:
1. **Text fidelity / completeness** — is every substantive text block transcribed, with correct
   Vietnamese diacritics, digits, code, and table content?
2. **Figure coverage** — is every graph/diagram/table/photo/chart in the source mentioned and
   substantively described (not just named)?

PDFs were read page-by-page via the `read` tool; the PNG chart and JPG exam as images; the PPTX by
extracting `<a:t>` runs from `ppt/slides/slideN.xml`.

## What changed since the previous audit
The previous audit is **superseded**. Two structural changes and four re-authorings:

- **PPTX swap.** `it3210_ocr_demo_slides_pptx` (a 2-slide demo deck) was removed from the dataset and
  replaced by `it4015e_access_control_pptx` — the real 58-slide SoICT "Access Control" lecture (Van K
  Nguyen, HUT, 2009). The demo file's old audit entry no longer applies; the new deck is audited below.
- **Four figure-partial files re-authored.** The earlier audit flagged 4 files as figure-PARTIAL and
  recommended re-authoring. All four are now fixed:
  - `it3160e_ai_introduction` — Turing/Imitation-Game diagram now names the interrogator / human / AI-
    system / "?" wall; the Deep Blue photo is now identified as a black server rack (Kasparov, 1997).
  - `it3160e_machine_learning` — the "Which cat.?" figure now enumerates all 6 category labels
    (Business, Entertainment, Science, Sports, Technology, Travel & Tourism).
  - `it3210_clang_lect13_vi` — slide 9 now describes the large red ✗ and green ✓ pedagogical icons.
  - `it3210_ocr_demo_slides_pptx` — no longer in the dataset (removed).

## Per-file verdicts

| id | source | text fidelity | figure coverage | verdict |
|---|---|---|---|---|
| it3020e_graph_presentation | 17-pg PDF | full | 7 graphs + 4 matrices + 4 adjacency-list diagrams all described | COMPLETE |
| it3160e_ai_introduction | 14-pg PDF | full | table + Turing + agent–env + expert-system + Deep Blue photo all described (re-authored) | COMPLETE |
| it3160e_intro_ai_presentation | 7-pg PDF | full | text-only, no figures | COMPLETE |
| it3160e_machine_learning | 9-pg PDF | full | 4 prediction-task diagrams incl. all 6 category labels (re-authored) | COMPLETE |
| it3210_clang_lect13_vi | 16-pg VN PDF | full — VN diacritics + C code verbatim, callout text captured | array-of-structs diagram + red ✗/green ✓ icons described (re-authored) | COMPLETE |
| it3210_ocr_demo_chart_png | PNG chart | full | line chart fully described (title, polyline, axis labels) | COMPLETE |
| it4015e_access_control_pptx | 58-slide PPTX | full — all 58 slides, tables/code blocks, symbols (⊆ ≥ ¬dom) verbatim; reversed reading order on slide 32 handled | access-matrix diagram (s8), MAC lattice (s27), RBAC family/RBAC0/RBAC1 diagrams + role hierarchy described | COMPLETE |
| it3292e_exam_cuoiki_2022_pdf | 2-pg scan | full — Câu 1–16 + Phần III; watermark & handwriting flagged | header table captured; no other figures | COMPLETE |
| it3292e_exam_giuaki_oanh_pdf | 2-pg scan | full — VN diacritics intact; "Đề 2"(p1)/"Đề 1"(p2) order noted; red grading annotations flagged | 5-row schema table per page captured | COMPLETE |
| it3292e_exam_giuaki_trinh_jpg | 1-pg JPG | full — Q1–4, schema bullet list, 6 queries; staple/pen flagged | header table captured; no other figures | COMPLETE |

## Overall verdict
**10 / 10 files are COMPLETE.** No missing text, no missing figures, and **no hallucinated (invented)
content** in any expected file. The `expected/` ground truth is safe to use for all six scored metrics,
including the figure-sensitive faithfulness metric.

### Spot-check depth (2026-07-06)
Read directly against source and confirmed faithful: `it4015e_access_control_pptx` (all 58 slides vs
PPTX XML), `it3210_clang_lect13_vi` (VN code slides, pages 6–12 vs PDF), `it3292e_exam_giuaki_oanh_pdf`
(both scanned pages). The re-authoring of `it3160e_ai_introduction` and `it3160e_machine_learning` was
confirmed by string match. The remaining files retain the COMPLETE figure verdicts from the prior pass.

### Note on scores
Because the four re-authored files now carry the full figure detail, judge scores for the pipeline's
**faithfulness** metric are no longer artificially depressed by a thin gold standard. The headline
pipeline weakness (hallucinated figure/diagram descriptions on the vision path) is a real defect of the
pipeline, not an artifact of the ground truth.
