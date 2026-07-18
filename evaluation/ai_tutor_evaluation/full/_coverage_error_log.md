# Full-set (65Q) coverage gate + actual error-check

Gate run on the **agentic_dense baseline** actuals (65Q) against the current index
(NVIDIA embed+rerank), 2026-07-12. Coverage is probed via the tutor's own retrieval
(`retrieval_calls[].chunks`), not by eye, per spec §2.4.

## Coverage (50 standard + 15 hard)

- **Zero-chunk retrieval:** none. Every one of the 65 questions retrieved context on the
  current index — no ground truth became unreachable after the embedding/corpus changes.
- **Refusal / "not covered" answers:** none genuine. `hard_ai_multi_04` tripped a keyword
  scan (`tài liệu…`) but the answer is a full, grounded two-part response — false positive.

Verdict: **all 50 originals still answerable on the current stack; no questions flagged
as uncovered.** Gate passed.

## Actual generation errors found & fixed

- `discrete_math_06` (agentic_dense): **empty answer** on first generation despite 16 chunks
  retrieved (transient token-budget / `<think>` starvation, cf. minimax-token-budget note).
  **Regenerated with `--only`** → 2144-char grounded answer. Fixed.
- Answer-leak (bare JSON array surfaced as answer): **0** across the baseline (bug-fixed image).
- Generation failures (exceptions): **0**.

## Actual error-check across ALL 4 configs (post-generation)

Scanned every config for answer-leak (bare JSON array), empty/short answers, zero-chunk
retrieval, and refusal phrasing:

| Config | files | answer-leak | empty | zero-chunk | notes |
|---|---|---|---|---|---|
| agentic_dense | 65 | 0 | 0 (1 regenerated) | 0 | clean |
| agentic_hybrid | 65 | 0 | 0 (1 regenerated) | 0 | clean |
| traditional_dense | 65 | 0 | 0 | 0 | see `discrete_math_16` below |
| traditional_hybrid | 65 | 0 | 0 | 0 | clean |

- **Empty answers regenerated:** `discrete_math_06` came back empty under BOTH agentic configs
  on first pass (transient token-budget/`<think>` starvation) despite 16 chunks retrieved;
  regenerated with `--only`, both now ~2.1k-char grounded answers.
- **`traditional_dense/discrete_math_16` ("spanning subgraph")** — NOT an error. The single-shot
  traditional path retrieved on the raw query, which did not surface an explicit definition, so
  the answer honestly states the term is not explicitly defined and explains adjacent concepts.
  This is a legitimate ablation signal (traditional-pipeline mis-retrieval), kept as-is for the
  judge to score — regenerating it would tamper with the result.

Final state: all 4 × 65 = 260 actuals present, 0 empties, 0 answer-leaks, 0 generation failures.
