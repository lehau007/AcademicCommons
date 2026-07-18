# AI Tutor Ablation Study Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a 2×2 (retrieval × pipeline) ablation of the AI tutor on a hard, difficulty-tagged question set, with production prompt fixes, a traditional-RAG endpoint, and an OpenRouter-free judge flow.

**Architecture:** Phase A is pure code (subagent-parallelizable, unit-tested): production prompt edits, a `/tutor/query-classic` endpoint, ablation-harness changes (NVIDIA-rerank parity + a `--pipeline` axis), a judge prompt-pack builder, a results validator, and a 2×2 comparison. Phase B is runtime execution against the local docker stack (corpus enrichment + reindex, hard-dataset authoring, 4-config generation, external-agent judging, aggregation).

**Tech Stack:** Python 3.11 / FastAPI / SQLAlchemy async / pytest (asyncio_mode=auto), NVIDIA NIM (embed + rerank), OpenCode(`minimax-m3`) + Groq for generation, docker compose (`graduationthesis-*`).

## Global Constraints

- **No OpenRouter anywhere in the eval path.** OpenRouter key is expired. Generation uses OpenCode/Groq; rerank/embed use NVIDIA; judging uses the external prompt-pack.
- **Generation providers:** OpenCode (`minimax-m3`) + Groq only.
- **Do not regress** `tutor_service` token budgets (`_ANSWER_MAX_TOKENS=8192`, `_DECISION_MAX_TOKENS=4096`), the `<think>` strip logic, the identity rules, the DECISION/ANSWER contract, `_AGENT_DECISION_SCHEMA`, or the `used_doc_ids` block.
- **No frontend changes.** The new endpoint is backend-only, not linked in the UI.
- **No re-ingestion / re-OCR.** Graph/table retrievability comes from targeted DB chunk edits + `reindex-embeddings` only.
- **Historical 50-question results are not re-run or merged.** All ablation artifacts live under `evaluation/ai_tutor_evaluation/hard/`.
- Test framework: `pytest` from `src/backend/` (`asyncio_mode = "auto"`, `testpaths = ["tests"]`). Match the mock style in `tests/unit/test_tutor_service.py` (`AsyncMock`/`MagicMock`).
- Backend is a baked docker image: prompt/endpoint changes require `docker compose build api && docker compose up -d api` to take effect at runtime (see memory `project-backend-docker-baked-image`).

---

## Phase A — Code (unit-tested, subagent-parallelizable)

### Task 1: Production prompt — no outside knowledge + query optimization

**Files:**
- Modify: `src/backend/app/services/tutor_service.py` (`_TUTOR_SYSTEM_PROMPT_TEMPLATE` ~L93-110, `_FINAL_ANSWER_INSTRUCTION` ~L142-150)
- Test: `src/backend/tests/unit/test_tutor_prompt_rules.py`

**Interfaces:**
- Consumes: nothing.
- Produces: no new symbols; `_TUTOR_SYSTEM_PROMPT_TEMPLATE` and `_FINAL_ANSWER_INSTRUCTION` keep the same names/types (module-level `str`). `_TUTOR_SYSTEM_PROMPT_TEMPLATE` must still `.format(course_code=, course_name=, topic_summary=)` cleanly (literal braces stay doubled `{{ }}`).

- [ ] **Step 1: Write the failing test**

```python
# src/backend/tests/unit/test_tutor_prompt_rules.py
from __future__ import annotations

from app.services.tutor_service import (
    _FINAL_ANSWER_INSTRUCTION,
    _TUTOR_SYSTEM_PROMPT_TEMPLATE,
)


def test_template_still_formats_with_placeholders() -> None:
    rendered = _TUTOR_SYSTEM_PROMPT_TEMPLATE.format(
        course_code="IT3160E", course_name="Intro to AI", topic_summary="agents, search"
    )
    assert "IT3160E" in rendered


def test_forbids_outside_knowledge_with_greeting_exception() -> None:
    t = _TUTOR_SYSTEM_PROMPT_TEMPLATE.lower()
    assert "only the retrieved context" in t
    assert "general" in t and "knowledge" in t  # forbids general knowledge
    assert "greeting" in t  # explicit exception
    assert "general" in _FINAL_ANSWER_INSTRUCTION.lower()


def test_query_optimization_rule_with_example() -> None:
    t = _TUTOR_SYSTEM_PROMPT_TEMPLATE
    assert "rewrite" in t.lower()  # instruction to rewrite the query
    assert "Optimized query" in t  # the worked example is present
    # the example still parses as a format-safe template (no odd single braces)
    _ = t.format(course_code="X", course_name="Y", topic_summary="Z")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd src/backend && python -m pytest tests/unit/test_tutor_prompt_rules.py -v`
Expected: FAIL (`only the retrieved context` / `Optimized query` not found).

- [ ] **Step 3: Edit the template — strengthen no-knowledge rule + add query-optimization rule**

In `_TUTOR_SYSTEM_PROMPT_TEMPLATE`, replace this exact block:

```
- If a question spans multiple distinct topics (e.g. "I need information about I/O and
```
...keep it, but INSERT a new rule immediately BEFORE that multi-topic bullet, right after the first `- For questions about course content ...` bullet. Insert:

```
- Before retrieving, REWRITE the student's raw question into a focused retrieval query:
  expand abbreviations, add the key domain terms, and strip conversational filler. Retrieve
  with the rewritten query, not the raw sentence.
  Example — student: "ê giải thích giúp t cái bảng so sánh BFS với DFS trong slide đi".
  Optimized query: "so sánh BFS và DFS: độ phức tạp thời gian, bộ nhớ, tính đầy đủ, tối ưu".
  Decision turn: {{"thought": "Rewrite to a focused query about the BFS vs DFS comparison table.", "action": "call_tool", "tool_name": "rag_retrieval_api_tool", "arguments": {{"query": "so sánh BFS và DFS: độ phức tạp thời gian, bộ nhớ, tính đầy đủ, tối ưu", "namespaces": ["knowledge"]}}}}
```

Then REPLACE this exact bullet:

```
- If the retrieved context does not contain the answer, say so explicitly in your final
  answer. Do not invent information.
```

with:

```
- Answer using ONLY the retrieved context. You MUST NOT fall back to general, outside, or
  pre-trained knowledge to fill gaps. If the gathered context does not contain the answer,
  state explicitly that the course materials do not cover it — do not answer from general
  knowledge, and do not invent information. Exception: ordinary greetings, small-talk, and
  meta-questions about the conversation itself may be answered normally without retrieval.
```

- [ ] **Step 4: Edit `_FINAL_ANSWER_INSTRUCTION`**

Replace the substring:

```
If the gathered context does not contain the answer, say so explicitly instead of inventing information.
```

with:

```
If the gathered context does not contain the answer, say so explicitly — do not use general or outside knowledge to fill the gap, and do not invent information.
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `cd src/backend && python -m pytest tests/unit/test_tutor_prompt_rules.py -v`
Expected: 3 passed.

- [ ] **Step 6: Commit**

```bash
git add src/backend/app/services/tutor_service.py src/backend/tests/unit/test_tutor_prompt_rules.py
git commit -m "feat(tutor): forbid outside-knowledge fallback + query-optimization rule in agent prompt"
```

---

### Task 2: `POST /tutor/query-classic` endpoint (traditional single-shot)

**Files:**
- Modify: `src/backend/app/api/v1/tutor.py` (add import of `tutor_query`; add route after `/query`)
- Test: `src/backend/tests/unit/test_tutor_classic_route.py`

**Interfaces:**
- Consumes: `tutor_query(session, course_code, question, include_exercise, llm_router, retrieval_service, settings) -> TutorQueryResponse` (existing, `tutor_service.py:168`); `TutorQueryRequest` (has `course_code`, `question`, `include_exercise: bool = False`).
- Produces: async route `query_tutor_classic(request, session, current_user) -> TutorQueryResponse` registered at `POST /tutor/query-classic`.

- [ ] **Step 1: Write the failing test**

```python
# src/backend/tests/unit/test_tutor_classic_route.py
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

import app.api.v1.tutor as tutor_route
from app.schemas.tutor import TutorQueryRequest, TutorQueryResponse


async def test_query_classic_calls_single_shot_tutor_query(monkeypatch) -> None:
    fake = TutorQueryResponse(answer="single-shot answer", citations=[])
    mock_tutor_query = AsyncMock(return_value=fake)
    monkeypatch.setattr(tutor_route, "tutor_query", mock_tutor_query)
    monkeypatch.setattr(tutor_route, "build_llm_router", lambda s: MagicMock())
    monkeypatch.setattr(tutor_route, "get_retrieval_service", lambda s: MagicMock())

    req = TutorQueryRequest(course_code="IT3160E", question="What is A* search?")
    session = MagicMock()
    session.commit = AsyncMock()
    user = MagicMock()

    resp = await tutor_route.query_tutor_classic(req, session, user)

    assert resp.answer == "single-shot answer"
    kwargs = mock_tutor_query.await_args.kwargs
    assert kwargs["course_code"] == "IT3160E"
    assert kwargs["question"] == "What is A* search?"
    assert kwargs["include_exercise"] is False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd src/backend && python -m pytest tests/unit/test_tutor_classic_route.py -v`
Expected: FAIL (`module 'app.api.v1.tutor' has no attribute 'tutor_query'` or `query_tutor_classic`).

- [ ] **Step 3: Add the import**

In `src/backend/app/api/v1/tutor.py`, extend the existing `from app.services.tutor_service import (...)` block to also import `tutor_query`:

```python
from app.services.tutor_service import (
    stream_tutor_agent_loop,
    tutor_course_summary,
    tutor_query,
    tutor_query_agent_loop,
)
```

- [ ] **Step 4: Add the route** (place immediately after the `/query` route, before `_sse`)

```python
@router.post("/query-classic", response_model=TutorQueryResponse)
async def query_tutor_classic(
    request: TutorQueryRequest,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> TutorQueryResponse:
    """Traditional single-shot RAG (retrieve once -> generate). Ablation baseline;
    intentionally NOT wired into the frontend."""
    settings = get_settings()
    res = await tutor_query(
        session=session,
        course_code=request.course_code,
        question=request.question,
        include_exercise=request.include_exercise,
        llm_router=build_llm_router(settings),
        retrieval_service=get_retrieval_service(settings),
        settings=settings,
    )
    await session.commit()
    return res
```

- [ ] **Step 5: Run test to verify it passes**

Run: `cd src/backend && python -m pytest tests/unit/test_tutor_classic_route.py -v`
Expected: 1 passed.

- [ ] **Step 6: Commit**

```bash
git add src/backend/app/api/v1/tutor.py src/backend/tests/unit/test_tutor_classic_route.py
git commit -m "feat(tutor): add POST /tutor/query-classic single-shot endpoint (backend-only)"
```

---

### Task 3: Ablation rerank parity — reuse production `_rerank` (NVIDIA, no OpenRouter)

**Files:**
- Modify: `evaluation/ai_tutor_evaluation/scripts/ablation_retrieval.py` (imports + `_rerank` method + `_search` reranked branch)
- Test: `evaluation/ai_tutor_evaluation/scripts/test_ablation_retrieval.py`

**Interfaces:**
- Consumes: `app.services.retrieval_service._rerank(query, candidates, query_vec, settings, k) -> list[RetrievedChunk]` (existing, `retrieval_service.py:136`). It is the authoritative path: with an OpenRouter key it uses OpenRouter, otherwise NVIDIA rerank, otherwise local MMR. Since the key is absent it uses NVIDIA/MMR — exactly what production does now.
- Produces: `AblationRetrieval` unchanged public surface (`search`, `MODES`, `calls`). No more direct `OpenRouterRerank` construction.

- [ ] **Step 1: Write the failing test** (asserts the module no longer hardcodes OpenRouter and delegates to production `_rerank`)

```python
# evaluation/ai_tutor_evaluation/scripts/test_ablation_retrieval.py
from __future__ import annotations

import ast
from pathlib import Path

SRC = Path(__file__).with_name("ablation_retrieval.py").read_text()


def test_no_hardcoded_openrouter_rerank() -> None:
    assert "OpenRouterRerank(" not in SRC


def test_delegates_to_production_rerank() -> None:
    # imports and calls retrieval_service._rerank so rerank behaviour == production
    assert "_rerank" in SRC
    tree = ast.parse(SRC)
    imported = {
        n.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module == "app.services.retrieval_service"
        for n in node.names
    }
    assert "_rerank" in imported
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd evaluation/ai_tutor_evaluation/scripts && python -m pytest test_ablation_retrieval.py -v`
Expected: FAIL (`OpenRouterRerank(` still present; `_rerank` not imported).

- [ ] **Step 3: Update imports** — add `_rerank` to the `from app.services.retrieval_service import (...)` block:

```python
from app.services.retrieval_service import (
    RetrievedChunk,
    _fetch_bm25,
    _fetch_candidates,
    _fetch_net_votes,
    _is_outline_chunk,
    _rerank,
    _row_to_chunk,
    build_embedding_service,
    rrf_fuse,
)
```

- [ ] **Step 4: Replace the `_rerank` method call in `_search`**

In `_search`, the reranked branch currently reads:

```python
        do_rerank = self._mode in {"dense_rerank", "bm25_rerank"}
        if do_rerank:
            ranked = await asyncio.to_thread(self._rerank, query, candidates, k)
            rerank_floor = getattr(settings, "tutor_rerank_threshold", 0.0)
            if rerank_floor > 0.0 and any(c.rerank_score is not None for c in ranked):
                ranked = [c for c in ranked if (c.rerank_score or 0.0) >= rerank_floor]
        else:
            ranked = candidates  # keep RRF order; rerank_score stays None
```

Change the `self._rerank(query, candidates, k)` call to the production function (it needs `query_vec`):

```python
        do_rerank = self._mode in {"dense_rerank", "bm25_rerank"}
        if do_rerank:
            ranked = await asyncio.to_thread(_rerank, query, candidates, query_vec, settings, k)
            rerank_floor = getattr(settings, "tutor_rerank_threshold", 0.0)
            if rerank_floor > 0.0 and any(c.rerank_score is not None for c in ranked):
                ranked = [c for c in ranked if (c.rerank_score or 0.0) >= rerank_floor]
        else:
            ranked = candidates  # keep RRF order; rerank_score stays None
```

- [ ] **Step 5: Delete the now-unused `_rerank` method and stale export**

Remove the entire `def _rerank(self, query, candidates, k): ...` method (the one building `OpenRouterRerank`). Update the module footer `__all__` to drop nothing new but keep `["AblationRetrieval", "rrf_fuse", "_fetch_bm25"]` as-is.

- [ ] **Step 6: Run tests to verify they pass**

Run: `cd evaluation/ai_tutor_evaluation/scripts && python -m pytest test_ablation_retrieval.py -v`
Expected: 2 passed.

- [ ] **Step 7: Commit**

```bash
git add evaluation/ai_tutor_evaluation/scripts/ablation_retrieval.py evaluation/ai_tutor_evaluation/scripts/test_ablation_retrieval.py
git commit -m "fix(ablation): reuse production NVIDIA rerank instead of hardcoded OpenRouter"
```

---

### Task 4: `run_ablation.py` — add `--pipeline {agentic,traditional}` axis

**Files:**
- Modify: `evaluation/ai_tutor_evaluation/scripts/run_ablation.py`
- Test: `evaluation/ai_tutor_evaluation/scripts/test_run_ablation_dispatch.py`

**Interfaces:**
- Consumes: `tutor_query_agent_loop(...)` and `tutor_query(session, course_code, question, include_exercise, llm_router, retrieval_service, settings) -> TutorQueryResponse`.
- Produces: pure helper `default_out_dir(pipeline: str, mode: str) -> str` returning `f"hard/actual_{pipeline}_{_MODE_SHORT[mode]}"` where `_MODE_SHORT = {"dense_rerank": "dense", "hybrid_norerank": "hybrid", "bm25_rerank": "bm25"}`; CLI now requires `--pipeline`.

- [ ] **Step 1: Write the failing test** (pure helper — no DB/app-loop needed)

```python
# evaluation/ai_tutor_evaluation/scripts/test_run_ablation_dispatch.py
from __future__ import annotations

import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "run_ablation", Path(__file__).with_name("run_ablation.py")
)


def _load():
    mod = importlib.util.module_from_spec(_spec)
    # run_ablation imports app.*; only load if importable, else skip via ImportError
    _spec.loader.exec_module(mod)
    return mod


def test_default_out_dir_naming() -> None:
    try:
        mod = _load()
    except ModuleNotFoundError:
        import pytest
        pytest.skip("app.* not importable outside container")
    assert mod.default_out_dir("agentic", "dense_rerank") == "hard/actual_agentic_dense"
    assert mod.default_out_dir("traditional", "hybrid_norerank") == "hard/actual_traditional_hybrid"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd evaluation/ai_tutor_evaluation/scripts && python -m pytest test_run_ablation_dispatch.py -v`
Expected: FAIL (`module 'run_ablation' has no attribute 'default_out_dir'`) — or SKIP if `app.*` unavailable locally (then verify inside the container in Step 6).

- [ ] **Step 3: Add the helper + pipeline arg + traditional branch**

Add near the top (after imports):

```python
_MODE_SHORT = {"dense_rerank": "dense", "hybrid_norerank": "hybrid", "bm25_rerank": "bm25"}


def default_out_dir(pipeline: str, mode: str) -> str:
    return f"hard/actual_{pipeline}_{_MODE_SHORT[mode]}"
```

Add to `run_one`'s signature a `pipeline: str` param and branch the generation call. Replace the current single `res = await tutor_query_agent_loop(...)` with:

```python
            if pipeline == "agentic":
                res = await tutor_query_agent_loop(
                    session=db,
                    session_id=chat_session.id,
                    question=q["question"],
                    llm_router=build_llm_router(settings),
                    retrieval_service=recorder,
                    settings=settings,
                )
            else:  # traditional single-shot
                res = await tutor_query(
                    session=db,
                    course_code=q["course_code"],
                    question=q["question"],
                    include_exercise=False,
                    llm_router=build_llm_router(settings),
                    retrieval_service=recorder,
                    settings=settings,
                )
```

Import `tutor_query` alongside `tutor_query_agent_loop`:

```python
from app.services.tutor_service import tutor_query, tutor_query_agent_loop
```

Add `"ablation_mode"` sibling key `"pipeline": pipeline` to the output dict.

- [ ] **Step 4: Wire the CLI arg**

In `main()`, add:

```python
    parser.add_argument("--pipeline", required=True, choices=["agentic", "traditional"])
```

Change the `--out` argument to optional with a computed default:

```python
    parser.add_argument("--out", default=None)
    ...
    out_dir = Path(args.out or default_out_dir(args.pipeline, args.mode))
```

Thread `args.pipeline` into `run_one(q, args.mode, args.pipeline, out_dir, sem)` (update `run_one` signature order accordingly: `run_one(q, mode, pipeline, out_dir, sem)`).

- [ ] **Step 5: Run test / verify**

Run: `cd evaluation/ai_tutor_evaluation/scripts && python -m pytest test_run_ablation_dispatch.py -v`
Expected: PASS or SKIP. If SKIP, verify argparse inside the container in Phase B (`python run_ablation.py --help` shows `--pipeline`).

- [ ] **Step 6: Commit**

```bash
git add evaluation/ai_tutor_evaluation/scripts/run_ablation.py evaluation/ai_tutor_evaluation/scripts/test_run_ablation_dispatch.py
git commit -m "feat(ablation): add --pipeline {agentic,traditional} axis to run_ablation"
```

---

### Task 5: Judge prompt-pack builder (`build_judge_pack.py`)

**Files:**
- Create: `evaluation/ai_tutor_evaluation/scripts/build_judge_pack.py`
- Test: `evaluation/ai_tutor_evaluation/scripts/test_build_judge_pack.py`

**Interfaces:**
- Consumes: an `actual_<config>/` dir of `<qid>.json` (each with `question`, `answer`, `citations`, `retrieval_calls[].chunks[].content`), `dataset/questions_hard.json` (`qid`, `ground_truth`), `metrics/rubric.md`.
- Produces: `build_pack(actual_dir: Path, questions: list[dict], rubric_text: str, out_dir: Path, config: str) -> int` writing `out_dir/INSTRUCTIONS.md`, `out_dir/rubric.md`, `out_dir/schema.json`, `out_dir/<qid>.md`; returns the number of `<qid>.md` bundles written. CLI: `--actual`, `--questions`, `--rubric`, `--out`, `--config`.

- [ ] **Step 1: Write the failing test**

```python
# evaluation/ai_tutor_evaluation/scripts/test_build_judge_pack.py
from __future__ import annotations

import json
from pathlib import Path

import importlib.util

_spec = importlib.util.spec_from_file_location(
    "build_judge_pack", Path(__file__).with_name("build_judge_pack.py")
)
bjp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bjp)


def test_build_pack_emits_bundles_and_meta(tmp_path: Path) -> None:
    actual = tmp_path / "actual"
    actual.mkdir()
    (actual / "q1.json").write_text(json.dumps({
        "qid": "q1", "question": "What is A*?", "answer": "A* uses f=g+h.",
        "citations": [], "retrieval_calls": [
            {"query": "A* search", "chunks": [{"content": "A* expands lowest f=g+h."}]}
        ],
    }))
    questions = [{"qid": "q1", "ground_truth": "A* selects the node with lowest f=g+h."}]
    out = tmp_path / "pack"
    n = bjp.build_pack(actual, questions, "RUBRIC-TEXT", out, "agentic_dense")

    assert n == 1
    assert (out / "INSTRUCTIONS.md").exists()
    assert (out / "schema.json").exists()
    assert "RUBRIC-TEXT" in (out / "rubric.md").read_text()
    bundle = (out / "q1.md").read_text()
    assert "What is A*?" in bundle
    assert "A* selects the node with lowest f=g+h." in bundle  # ground truth
    assert "A* expands lowest f=g+h." in bundle  # retrieved context
    assert "A* uses f=g+h." in bundle  # tutor answer
    # schema lists the six metrics
    schema = json.loads((out / "schema.json").read_text())
    for m in ["faithfulness", "answer_relevancy", "answer_correctness",
              "context_precision", "context_recall", "citation_accuracy"]:
        assert m in json.dumps(schema)


def test_instructions_name_the_output_dir(tmp_path: Path) -> None:
    out = tmp_path / "pack"
    bjp.build_pack(tmp_path / "empty", [], "R", out, "traditional_hybrid")
    assert "results_traditional_hybrid" in (out / "INSTRUCTIONS.md").read_text()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd evaluation/ai_tutor_evaluation/scripts && python -m pytest test_build_judge_pack.py -v`
Expected: FAIL (module/file not found).

- [ ] **Step 3: Implement `build_judge_pack.py`**

```python
"""Build an OpenRouter-free judge prompt-pack for one ablation config.

The RAGAS judge used to call OpenRouter; that key is expired. Instead, this emits a
self-contained folder an external agentic coding tool (opencode / gemini-cli / Claude) reads
to produce results_<config>/<qid>.json (the six-metric schema aggregate.py already consumes).

    python build_judge_pack.py --actual ../hard/actual_agentic_dense \
        --questions ../dataset/questions_hard.json --rubric ../metrics/rubric.md \
        --out ../hard/judge_pack_agentic_dense --config agentic_dense
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

METRICS = [
    "faithfulness", "answer_relevancy", "answer_correctness",
    "context_precision", "context_recall", "citation_accuracy",
]

_SCHEMA = {
    "type": "object",
    "properties": {
        "qid": {"type": "string"},
        "scores": {
            "type": "object",
            "properties": {
                m: {
                    "type": "object",
                    "properties": {
                        "score": {"type": "integer", "minimum": 1, "maximum": 5},
                        "reason": {"type": "string"},
                    },
                    "required": ["score", "reason"],
                }
                for m in METRICS
            },
            "required": METRICS,
        },
    },
    "required": ["qid", "scores"],
}


def _bundle_md(actual: dict, ground_truth: str) -> str:
    ctx_blocks = []
    seen = set()
    for call in actual.get("retrieval_calls", []):
        for ch in call.get("chunks", []):
            c = ch.get("content", "")
            if c and c not in seen:
                seen.add(c)
                ctx_blocks.append(f"- {c}")
    ctx = "\n".join(ctx_blocks) if ctx_blocks else "(no chunks retrieved)"
    cites = json.dumps(actual.get("citations", []), ensure_ascii=False, indent=2)
    return (
        f"# {actual.get('qid')}\n\n"
        f"## Question\n{actual.get('question', '')}\n\n"
        f"## Ground truth\n{ground_truth}\n\n"
        f"## Retrieved context (what the tutor saw)\n{ctx}\n\n"
        f"## Tutor answer\n{actual.get('answer', '')}\n\n"
        f"## Citations\n```json\n{cites}\n```\n"
    )


def _instructions_md(config: str) -> str:
    return (
        f"# Judge instructions — config `{config}`\n\n"
        "You are an impartial RAGAS-style grader. For EACH `<qid>.md` bundle in this folder:\n"
        "1. Read `rubric.md` for the six metrics and their 1–5 anchors.\n"
        "2. Score the tutor answer against the ground truth and the retrieved context.\n"
        f"3. Write `../results_{config}/<qid>.json` matching `schema.json` exactly: a `qid`\n"
        "   and a `scores` object with all six metrics, each `{\"score\": 1-5, \"reason\": \"...\"}`.\n\n"
        "Rules: score only from the bundle; never invent facts; if the answer says the\n"
        "materials do not cover the question AND the ground truth is absent from the retrieved\n"
        "context, that is faithful (do not penalise faithfulness). Output valid JSON only.\n"
    )


def build_pack(actual_dir: Path, questions: list[dict], rubric_text: str,
               out_dir: Path, config: str) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "INSTRUCTIONS.md").write_text(_instructions_md(config), encoding="utf-8")
    (out_dir / "rubric.md").write_text(rubric_text, encoding="utf-8")
    (out_dir / "schema.json").write_text(json.dumps(_SCHEMA, indent=2), encoding="utf-8")
    gt = {q["qid"]: q.get("ground_truth", "") for q in questions}
    n = 0
    for p in sorted(actual_dir.glob("*.json")):
        if p.name.startswith("_"):
            continue
        actual = json.loads(p.read_text())
        qid = actual.get("qid", p.stem)
        (out_dir / f"{qid}.md").write_text(_bundle_md(actual, gt.get(qid, "")), encoding="utf-8")
        n += 1
    return n


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--actual", required=True)
    ap.add_argument("--questions", required=True)
    ap.add_argument("--rubric", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    questions = json.loads(Path(args.questions).read_text())
    rubric = Path(args.rubric).read_text()
    n = build_pack(Path(args.actual), questions, rubric, Path(args.out), args.config)
    print(f"wrote {n} bundles to {args.out}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd evaluation/ai_tutor_evaluation/scripts && python -m pytest test_build_judge_pack.py -v`
Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add evaluation/ai_tutor_evaluation/scripts/build_judge_pack.py evaluation/ai_tutor_evaluation/scripts/test_build_judge_pack.py
git commit -m "feat(eval): OpenRouter-free judge prompt-pack builder"
```

---

### Task 6: Results validator (`validate_results.py`)

**Files:**
- Create: `evaluation/ai_tutor_evaluation/scripts/validate_results.py`
- Test: `evaluation/ai_tutor_evaluation/scripts/test_validate_results.py`

**Interfaces:**
- Consumes: a `results_<config>/` dir of `<qid>.json` produced by the external judge; a set of expected qids.
- Produces: `validate(results_dir: Path, expected_qids: set[str]) -> dict` returning `{"missing_qids": [...], "invalid": [{"qid":..., "problem":...}], "ok": int}`. CLI prints a report and exits non-zero if anything is missing/invalid.

- [ ] **Step 1: Write the failing test**

```python
# evaluation/ai_tutor_evaluation/scripts/test_validate_results.py
from __future__ import annotations

import json
from pathlib import Path

import importlib.util

_spec = importlib.util.spec_from_file_location(
    "validate_results", Path(__file__).with_name("validate_results.py")
)
vr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(vr)

_GOOD = {"qid": "q1", "scores": {m: {"score": 4, "reason": "ok"} for m in vr.METRICS}}


def test_valid_results_pass(tmp_path: Path) -> None:
    (tmp_path / "q1.json").write_text(json.dumps(_GOOD))
    report = vr.validate(tmp_path, {"q1"})
    assert report["missing_qids"] == []
    assert report["invalid"] == []
    assert report["ok"] == 1


def test_detects_missing_and_invalid(tmp_path: Path) -> None:
    bad = {"qid": "q2", "scores": {"faithfulness": {"score": 9, "reason": "x"}}}
    (tmp_path / "q2.json").write_text(json.dumps(bad))
    report = vr.validate(tmp_path, {"q1", "q2"})
    assert "q1" in report["missing_qids"]
    assert any(item["qid"] == "q2" for item in report["invalid"])  # missing metrics + out-of-range
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd evaluation/ai_tutor_evaluation/scripts && python -m pytest test_validate_results.py -v`
Expected: FAIL (module not found).

- [ ] **Step 3: Implement `validate_results.py`**

```python
"""Validate externally-judged results before aggregation (replaces the automated judge's trust).

    python validate_results.py --results ../hard/results_agentic_dense \
        --questions ../dataset/questions_hard.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

METRICS = [
    "faithfulness", "answer_relevancy", "answer_correctness",
    "context_precision", "context_recall", "citation_accuracy",
]


def validate(results_dir: Path, expected_qids: set[str]) -> dict:
    found: set[str] = set()
    invalid: list[dict] = []
    for p in sorted(results_dir.glob("*.json")):
        if p.name in {"summary.json"} or p.name.startswith("_"):
            continue
        try:
            r = json.loads(p.read_text())
        except json.JSONDecodeError as exc:
            invalid.append({"qid": p.stem, "problem": f"bad json: {exc}"})
            continue
        qid = r.get("qid", p.stem)
        found.add(qid)
        scores = r.get("scores")
        if not isinstance(scores, dict):
            invalid.append({"qid": qid, "problem": "missing scores object"})
            continue
        problems = []
        for m in METRICS:
            cell = scores.get(m)
            if not isinstance(cell, dict) or "score" not in cell:
                problems.append(f"missing metric {m}")
                continue
            s = cell["score"]
            if not isinstance(s, int) or not (1 <= s <= 5):
                problems.append(f"{m} score out of range: {s!r}")
        if problems:
            invalid.append({"qid": qid, "problem": "; ".join(problems)})
    return {
        "missing_qids": sorted(expected_qids - found),
        "invalid": invalid,
        "ok": len(found) - len({i["qid"] for i in invalid}),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", required=True)
    ap.add_argument("--questions", required=True)
    args = ap.parse_args()
    qids = {q["qid"] for q in json.loads(Path(args.questions).read_text())}
    report = validate(Path(args.results), qids)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if report["missing_qids"] or report["invalid"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd evaluation/ai_tutor_evaluation/scripts && python -m pytest test_validate_results.py -v`
Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add evaluation/ai_tutor_evaluation/scripts/validate_results.py evaluation/ai_tutor_evaluation/scripts/test_validate_results.py
git commit -m "feat(eval): results validator for externally-judged ablation output"
```

---

### Task 7: 2×2 comparison (`compare_ablation_2x2.py`)

**Files:**
- Create: `evaluation/ai_tutor_evaluation/scripts/compare_ablation_2x2.py`
- Test: `evaluation/ai_tutor_evaluation/scripts/test_compare_ablation_2x2.py`

**Interfaces:**
- Consumes: four `hard/results_<config>/` dirs and matching `hard/actual_<config>/` dirs; `dataset/questions_hard.json` with `difficulty_type`.
- Produces: `metric_means(scores: dict) -> dict`, `by_difficulty(scores, qid_to_type) -> dict[str, dict]`, and `render(root: Path) -> str` returning the full markdown report (2×2 grid + per-difficulty breakdown). CLI writes `hard/report.md`.

- [ ] **Step 1: Write the failing test**

```python
# evaluation/ai_tutor_evaluation/scripts/test_compare_ablation_2x2.py
from __future__ import annotations

import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "compare_ablation_2x2", Path(__file__).with_name("compare_ablation_2x2.py")
)
cmp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cmp)


def _scores(val: int) -> dict:
    return {m: {"score": val} for m in cmp.METRICS}


def test_metric_means_and_overall() -> None:
    scores = {"q1": _scores(4), "q2": _scores(2)}
    means = cmp.metric_means(scores)
    assert means["faithfulness"] == 3.0
    assert means["overall"] == 3.0


def test_by_difficulty_groups() -> None:
    scores = {"q1": _scores(5), "q2": _scores(1)}
    qid_to_type = {"q1": "table", "q2": "graph"}
    grouped = cmp.by_difficulty(scores, qid_to_type)
    assert grouped["table"]["overall"] == 5.0
    assert grouped["graph"]["overall"] == 1.0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd evaluation/ai_tutor_evaluation/scripts && python -m pytest test_compare_ablation_2x2.py -v`
Expected: FAIL (module not found).

- [ ] **Step 3: Implement `compare_ablation_2x2.py`**

```python
"""2x2 (retrieval x pipeline) ablation comparison on the hard set.

Reads the four hard/results_<config> dirs, prints per-metric means + overall with deltas vs
agentic_dense, plus a per-difficulty_type breakdown. Writes hard/report.md.

    python compare_ablation_2x2.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HARD = ROOT / "hard"

METRICS = [
    "faithfulness", "answer_relevancy", "answer_correctness",
    "context_precision", "context_recall", "citation_accuracy",
]

# (label, config id) — config id names both results_<id> and actual_<id>
CONFIGS = [
    ("Agentic + Dense (baseline)", "agentic_dense"),
    ("Agentic + Hybrid", "agentic_hybrid"),
    ("Traditional + Dense", "traditional_dense"),
    ("Traditional + Hybrid", "traditional_hybrid"),
]


def load_scores(results_dir: Path) -> dict[str, dict]:
    out = {}
    for p in results_dir.glob("*.json"):
        if p.name == "summary.json" or p.name.startswith("_"):
            continue
        r = json.loads(p.read_text())
        out[r.get("qid", p.stem)] = r["scores"]
    return out


def metric_means(scores: dict[str, dict]) -> dict[str, float]:
    res = {}
    for m in METRICS:
        vals = [s[m]["score"] for s in scores.values() if s.get(m) is not None]
        res[m] = round(sum(vals) / len(vals), 2) if vals else float("nan")
    allv = [s[m]["score"] for s in scores.values() for m in METRICS if s.get(m) is not None]
    res["overall"] = round(sum(allv) / len(allv), 2) if allv else float("nan")
    return res


def by_difficulty(scores: dict[str, dict], qid_to_type: dict[str, str]) -> dict[str, dict]:
    groups: dict[str, dict[str, dict]] = {}
    for qid, s in scores.items():
        groups.setdefault(qid_to_type.get(qid, "unknown"), {})[qid] = s
    return {t: metric_means(g) for t, g in groups.items()}


def render(root: Path) -> str:
    questions = json.loads((root / "dataset" / "questions_hard.json").read_text())
    qid_to_type = {q["qid"]: q.get("difficulty_type", "unknown") for q in questions}
    hard = root / "hard"

    lines: list[str] = ["# AI Tutor Ablation — 2x2 (hard set)\n"]
    cols = METRICS + ["overall"]
    lines.append("## Grid (Δ vs Agentic+Dense)\n")
    lines.append("| Config | n | " + " | ".join(c.replace("_", " ") for c in cols) + " |")
    lines.append("|" + "---|" * (len(cols) + 2))

    baseline = None
    means_by_cfg = {}
    for label, cfg in CONFIGS:
        rdir = hard / f"results_{cfg}"
        if not rdir.exists():
            lines.append(f"| {label} | 0 | " + " | ".join(["—"] * len(cols)) + " |")
            continue
        scores = load_scores(rdir)
        means = metric_means(scores)
        means_by_cfg[cfg] = (scores, means)
        if baseline is None:
            baseline = means
        cells = []
        for m in cols:
            v = means[m]
            if baseline and cfg != CONFIGS[0][1]:
                cells.append(f"{v:.2f} ({v - baseline[m]:+.2f})")
            else:
                cells.append(f"{v:.2f}")
        lines.append(f"| {label} | {len(scores)} | " + " | ".join(cells) + " |")

    lines.append("\n## By difficulty type (overall score)\n")
    types = sorted({t for t in qid_to_type.values()})
    lines.append("| Config | " + " | ".join(types) + " |")
    lines.append("|" + "---|" * (len(types) + 1))
    for label, cfg in CONFIGS:
        if cfg not in means_by_cfg:
            continue
        scores, _ = means_by_cfg[cfg]
        grouped = by_difficulty(scores, qid_to_type)
        cells = [f"{grouped[t]['overall']:.2f}" if t in grouped else "—" for t in types]
        lines.append(f"| {label} | " + " | ".join(cells) + " |")

    lines.append(
        "\n_Judge: external agentic tool (OpenRouter expired). Generation: OpenCode/Groq. "
        "Retrieval: NVIDIA embed + rerank. Historical 50-Q run not included._\n"
    )
    return "\n".join(lines)


def main() -> None:
    report = render(ROOT)
    print(report)
    (HARD).mkdir(parents=True, exist_ok=True)
    (HARD / "report.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd evaluation/ai_tutor_evaluation/scripts && python -m pytest test_compare_ablation_2x2.py -v`
Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add evaluation/ai_tutor_evaluation/scripts/compare_ablation_2x2.py evaluation/ai_tutor_evaluation/scripts/test_compare_ablation_2x2.py
git commit -m "feat(eval): 2x2 ablation comparison with per-difficulty breakdown"
```

---

## Phase B — Runtime execution (local docker stack; inline, sequential)

> These tasks require the running `graduationthesis-*` containers, DB access, and NVIDIA/OpenCode/Groq keys in the api container env. They are not unit-testable; each has an explicit verification command. Run inline (not via subagents) so the operator can react to the live stack and drive the external judge tool.

### Task 8: Corpus inspection + graph/table enrichment + reindex

**Files:**
- Create: `evaluation/ai_tutor_evaluation/scripts/inspect_corpus.py` (read-only DB dump of chunks per course: id, document title, section_title, chunk_order, content preview)
- Create: `evaluation/ai_tutor_evaluation/expected/_hard_enrichment_log.md` (record of every edited chunk)

**Interfaces:**
- Consumes: `app.db.session.AsyncSessionLocal`, the `Chunk`/`DocumentChunk` model (confirm the exact model name via `grep -rn "class .*Chunk" src/backend/app/models/`).
- Produces: a printed/JSON catalogue used to author the dataset; targeted `UPDATE chunk SET content = content || '\n\n' || <light description>` edits applied via a session, logged.

- [ ] **Step 1:** Confirm the chunk model + columns: `grep -rn "class .*Chunk" src/backend/app/models/`. Note the table/model name and the `content`, `section_title`, `document_id`, `namespace` fields.
- [ ] **Step 2:** Write `inspect_corpus.py` to dump, per course_code, every chunk's `id, document title, section_title, chunk_order, content[:300]` to stdout/JSON. Run inside the container:
  `docker cp evaluation/ai_tutor_evaluation graduationthesis-api-1:/tmp/tutor_eval && docker exec graduationthesis-api-1 python /tmp/tutor_eval/scripts/inspect_corpus.py > /tmp/corpus_dump.txt`
- [ ] **Step 3:** From the dump, identify chunks that reference a figure/graph or a table but lack a textual description of its content. Pick the specific figures/tables the hard graph/table questions will target.
- [ ] **Step 4:** For each target chunk, append a 1–2 sentence factual description (what it shows; axes/columns; key values/trend) — **no invented data**. Apply as DB updates inside the container. Record `chunk_id`, before/after snippet in `_hard_enrichment_log.md`.
- [ ] **Step 5:** Reindex: `docker exec graduationthesis-api-1 python -m app.cli reindex-embeddings`.
- [ ] **Step 6: Verify** — a keyword query for an enriched figure/table now returns its chunk:
  run `inspect_corpus.py`-style search or a quick retrieval smoke against the enriched chunk; confirm the chunk id appears in top-k.
- [ ] **Step 7: Commit** the scripts + enrichment log (not DB state):
  `git add evaluation/ai_tutor_evaluation/scripts/inspect_corpus.py evaluation/ai_tutor_evaluation/expected/_hard_enrichment_log.md && git commit -m "chore(eval): corpus inspection + graph/table chunk enrichment log"`

### Task 9: Author `questions_hard.json` + coverage report

**Files:**
- Create: `evaluation/ai_tutor_evaluation/dataset/questions_hard.json`
- Create: `evaluation/ai_tutor_evaluation/expected/_hard_review_report.md`

- [ ] **Step 1:** Author 12–20 questions across `difficulty_type ∈ {graph, table, multi_intent, long_context}`, each `{qid, course_code, question, ground_truth, difficulty_type}`, grounded in the corpus dump from Task 8. Multi-intent questions must have ≥2 distinct sub-questions; long-context ground truths must require ≥3 chunks.
- [ ] **Step 2:** For every qid, record in `_hard_review_report.md` the covering chunk(s)/document(s) and a verdict (covered / partial / impossible). Exclude or explicitly flag impossible ones.
- [ ] **Step 3: Verify** — `python -c "import json; d=json.load(open('evaluation/ai_tutor_evaluation/dataset/questions_hard.json')); assert all(set(q)>= {'qid','course_code','question','ground_truth','difficulty_type'} for q in d); print(len(d),'questions', {q['difficulty_type'] for q in d})"`.
- [ ] **Step 4: Commit** `git add evaluation/ai_tutor_evaluation/dataset/questions_hard.json evaluation/ai_tutor_evaluation/expected/_hard_review_report.md && git commit -m "feat(eval): hard difficulty-tagged dataset + coverage report"`

### Task 10: Rebuild api image + generate the 4 configs

- [ ] **Step 1:** Ensure generation providers: the api container env has `OPENCODE_API_KEY` and/or `GROQ_API_KEY` and `LLM_PROVIDER_ORDER` prefers them (e.g. `groq,opencode`), and `NVIDIA_API_KEY` is set. (Do not print secret values.)
- [ ] **Step 2:** Rebuild so the prompt + endpoint changes are baked: `docker compose build api && docker compose up -d api`. Verify the prompt change is in the image: `docker exec graduationthesis-api-1 grep -c "Optimized query" /app/app/services/tutor_service.py` → `1`.
- [ ] **Step 3:** Copy harness: `docker cp evaluation/ai_tutor_evaluation graduationthesis-api-1:/tmp/tutor_eval`.
- [ ] **Step 4:** Generate all four (resumable; run sequentially to bound load):
```bash
for pipe in agentic traditional; do for mode in dense_rerank hybrid_norerank; do
  docker exec graduationthesis-api-1 python /tmp/tutor_eval/scripts/run_ablation.py \
    --pipeline $pipe --mode $mode --questions /tmp/tutor_eval/dataset/questions_hard.json
done; done
docker cp graduationthesis-api-1:/tmp/tutor_eval/hard evaluation/ai_tutor_evaluation/
```
- [ ] **Step 5: Verify** — each `hard/actual_<config>/` has one `<qid>.json` per hard question, and graph/table qids show the enriched chunk in `retrieval_calls`. Spot-check a no-coverage question: the answer says the materials don't cover it (no general-knowledge fallback).
- [ ] **Step 6: Commit** `git add evaluation/ai_tutor_evaluation/hard && git commit -m "eval: generate 2x2 ablation actuals on hard set"`

### Task 11: Judge (external) + validate + aggregate + report

- [ ] **Step 1:** Build the four judge packs:
```bash
for cfg in agentic_dense agentic_hybrid traditional_dense traditional_hybrid; do
  python evaluation/ai_tutor_evaluation/scripts/build_judge_pack.py \
    --actual evaluation/ai_tutor_evaluation/hard/actual_$cfg \
    --questions evaluation/ai_tutor_evaluation/dataset/questions_hard.json \
    --rubric evaluation/ai_tutor_evaluation/metrics/rubric.md \
    --out evaluation/ai_tutor_evaluation/hard/judge_pack_$cfg --config $cfg
done
```
- [ ] **Step 2:** Operator feeds each `hard/judge_pack_<cfg>/` to an external agentic coding tool (opencode / gemini-cli / Claude), which writes `hard/results_<cfg>/<qid>.json` per the pack's `INSTRUCTIONS.md`.
- [ ] **Step 3:** Validate each config:
```bash
for cfg in agentic_dense agentic_hybrid traditional_dense traditional_hybrid; do
  python evaluation/ai_tutor_evaluation/scripts/validate_results.py \
    --results evaluation/ai_tutor_evaluation/hard/results_$cfg \
    --questions evaluation/ai_tutor_evaluation/dataset/questions_hard.json
done
```
Expected: exit 0 (no missing/invalid). Fix bundles/re-judge any failures.
- [ ] **Step 4:** Render the 2×2 report: `python evaluation/ai_tutor_evaluation/scripts/compare_ablation_2x2.py` → writes `hard/report.md`.
- [ ] **Step 5: Verify** — `hard/report.md` shows 4 config rows with deltas + a per-difficulty_type breakdown, and states the caveats (external judge, OpenCode/Groq generation).
- [ ] **Step 6:** Update `.agents/context/REGISTRY.md` (per CLAUDE.md session rule) with the new ablation scripts/artifacts, then commit:
  `git add evaluation/ai_tutor_evaluation/hard .agents/context/REGISTRY.md && git commit -m "eval: 2x2 ablation judged results + report"`

---

## Self-Review (spec coverage)

- Spec §4 (2×2) → Tasks 4, 10, 7. §5 (prompt) → Task 1. §6 (endpoint) → Task 2. §7 (judge pack + validator) → Tasks 5, 6, 11. §8 (runner + rerank fix) → Tasks 3, 4. §9 (hard dataset) → Task 9. §9.1 (enrichment) → Task 8. §10 (execution order) → Phase B order. §11 (success criteria) → verify steps in Tasks 10–11.
- Type consistency: `METRICS` list identical across Tasks 5/6/7; `default_out_dir`/`_MODE_SHORT` (Task 4) feed the `actual_<config>` / `results_<config>` names consumed by Tasks 5/7/11; config ids (`agentic_dense`, `agentic_hybrid`, `traditional_dense`, `traditional_hybrid`) are used verbatim in Tasks 7, 10, 11.
- No placeholders: all code steps show full code; runtime steps give exact commands + expected output.
