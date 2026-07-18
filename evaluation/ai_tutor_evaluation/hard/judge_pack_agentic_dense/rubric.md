# AI Tutor Evaluation — Metrics Rubric

Each judge call scores **one metric for one question**. It receives:

- The **question** and the human-verified **ground-truth answer** (`dataset/questions.json`).
- `actual/<qid>.json` — the tutor's output:
  - `answer` — the tutor's final markdown answer.
  - `citations` — the chunks the tutor cited (chunk id, document, snippet).
  - `retrieved_chunks` — **all** chunks the retrieval step returned (id, score, text),
    whether cited or not.
- The definition + anchors of the **one metric** being scored (below).

Return **strict JSON only** (no prose outside the JSON):

```json
{ "score": 1, "justification": "", "evidence": [] }
```

- `score` — integer 1–5.
- `justification` — 1–2 sentences.
- `evidence` — short quoted strings from the answer / chunks / ground truth supporting the
  score. **Required for any score below 5.**

## Scale anchors (apply to every metric)

- **5 — Excellent:** essentially perfect; no meaningful defect.
- **4 — Good:** minor issues that don't affect a student's understanding.
- **3 — Acceptable:** noticeable issues but the core is usable.
- **2 — Poor:** significant error/omission; partially unusable.
- **1 — Failing:** metric essentially not met.

Judge substance, not style. Do not reward or penalize length, formatting, or tone unless the
metric explicitly concerns it. The tutor may legitimately include correct information beyond
the ground truth — only the metric being scored decides whether that matters.

## Metrics

### 1. Faithfulness (`faithfulness`)
Does the answer contain **only** claims grounded in the retrieved chunks?
- Decompose the answer into factual claims; check each against `retrieved_chunks`.
- 5 = every claim supported; 3 = a few peripheral claims unsupported; 1 = core claims invented.
- General-knowledge glue (definitions of common words, arithmetic) does not count as a claim.
- Evidence: quote each **unsupported claim** verbatim.

### 2. Answer Relevancy (`answer_relevancy`)
Does the answer address the question actually asked?
- 5 = directly and completely on-topic; 3 = answers a related but shifted question, or buries
  the answer in off-topic material; 1 = does not answer the question.
- Ignore correctness here — a wrong but on-topic answer can still score 5.
- Evidence: quote the off-topic/evasive part.

### 3. Answer Correctness (`answer_correctness`)
Is the answer factually consistent with the **ground-truth answer**?
- 5 = covers all key facts of the ground truth, no contradictions; 3 = misses some key facts
  or has a minor error; 1 = contradicts the ground truth on the main point.
- Extra correct detail beyond the ground truth is not a defect.
- Evidence: quote the missing/contradicting fact from the ground truth vs the answer.

### 4. Context Precision (`context_precision`)
What fraction of `retrieved_chunks` is relevant to the question?
- 5 = nearly all chunks relevant; 3 = roughly half are noise; 1 = retrieval mostly noise.
- A chunk is "relevant" if it could plausibly help answer this question.
- Evidence: cite the ids/first words of irrelevant chunks.

### 5. Context Recall (`context_recall`)
Do the retrieved chunks contain the information needed to produce the **ground-truth answer**?
- 5 = every key fact of the ground truth appears in some retrieved chunk; 3 = about half;
  1 = the needed content was not retrieved at all.
- This scores **retrieval**, not the answer. If `retrieved_chunks` is empty, score 1.
- Evidence: quote ground-truth facts that appear in no retrieved chunk.

### 6. Citation Accuracy (`citation_accuracy`)
Do the citations point to chunks that actually support the statements they are attached to?
- 5 = every citation supports its statement; 3 = some citations point to loosely related
  chunks; 1 = citations point to unrelated content, or answer makes sourced-sounding claims
  with no citations at all.
- If the answer has no citations AND makes no claims needing them (e.g. a refusal), score 5
  and note "N/A — no citations needed".
- Evidence: pair the cited statement with the actual content of the cited chunk.

## Required merged output — `results/<qid>.json`

The judge script merges the 6 per-metric calls into:

```json
{
  "qid": "<qid>",
  "course_code": "",
  "judge_model": "",
  "scores": {
    "faithfulness":      { "score": 1, "justification": "", "evidence": [] },
    "answer_relevancy":  { "score": 1, "justification": "", "evidence": [] },
    "answer_correctness":{ "score": 1, "justification": "", "evidence": [] },
    "context_precision": { "score": 1, "justification": "", "evidence": [] },
    "context_recall":    { "score": 1, "justification": "", "evidence": [] },
    "citation_accuracy": { "score": 1, "justification": "", "evidence": [] }
  }
}
```

A metric whose call failed after retries is recorded as `null` and excluded from aggregation.
