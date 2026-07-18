# Chunk Page Number Propagation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Carry the source page/slide number from the document extractor through the processing pipeline into `document_chunks.page_number`, so tutor citations can display the page a chunk came from (for documents indexed from now on).

**Architecture:** Extractor blocks already carry `page` (PDF) / `slide` (PPTX). The normalizer batches blocks per page/slide, so at normalize time we know which line ranges of the output markdown belong to which page. We compute a compact `page_map` (`[(line_start, page), ...]`) there, persist it as a small sidecar JSON in S3 next to the markdown (the markdown content itself is never touched), and at index time the chunker looks up each **section's** starting line in that map and stamps every chunk in the section with that page. Attribution is section-level: robust and near-exact because normalized docs emit one `##` heading per slide / logical page region.

**Tech Stack:** Python 3.11, FastAPI worker, SQLAlchemy async, boto3/MinIO storage, pytest.

## Global Constraints

- **No DB migration.** `document_chunks.page_number` (nullable integer) already exists — this plan only starts populating it.
- **Never mutate markdown content.** Page data travels as out-of-band metadata (a sidecar object), so embeddings and stored markdown stay byte-for-byte identical to today.
- **Backward compatible.** A missing `page_map` sidecar (old documents, `custom_runner` path, non-paginated sources) must yield `page_number = NULL`, never an error.
- **Alignment invariant:** `page_map` line indices are counted against the exact markdown string the chunker parses. The normalizer's joined output must have **no leading blank line** so the chunker's leading `.strip()` cannot shift line numbers. Every task that touches line counting is guarded by a test pinning this.
- **Granularity:** PPTX = exact (one batch per slide). PDF = the batch's **starting** page (a batch may span pages), so ±1 page is acceptable and expected.

---

### Task 1: `build_page_map` helper + `normalize()` returns the map

**Files:**
- Modify: `src/backend/app/services/document_processing/normalization.py`
- Modify: `src/backend/app/services/document_processing/pipeline.py:178` (the `normalize` call site)
- Test: `src/backend/tests/unit/test_page_map.py` (create)

**Interfaces:**
- Produces: `build_page_map(outputs: list[str], pages: list[int | None]) -> list[tuple[int, int]]` — a free function in `normalization.py`. `outputs[i]` is the normalized markdown for batch `i`; `pages[i]` is its starting page/slide (or `None` if unknown). Returns sorted `(line_start, page)` boundaries into `"\n\n".join(outputs)`, collapsing consecutive equal pages and carrying the last known page forward over `None`.
- Produces: `DocumentNormalizer.normalize(...) -> tuple[str, list[dict[str, object]], list[tuple[int, int]]]` — now a **3-tuple** `(markdown, trace, page_map)`.

- [ ] **Step 1: Write the failing test for `build_page_map`**

```python
# src/backend/tests/unit/test_page_map.py
from __future__ import annotations

from app.services.document_processing.normalization import build_page_map


def test_build_page_map_line_offsets_match_joined_output() -> None:
    # Two single-line batches on pages 1 and 5.
    outputs = ["# Slide one\ncontent A", "# Slide five\ncontent B"]
    pages = [1, 5]
    page_map = build_page_map(outputs, pages)
    # batch 0 starts at line 0; batch 1 starts after 2 lines + 1 blank separator = line 3.
    assert page_map == [(0, 1), (3, 5)]
    joined = "\n\n".join(outputs)
    # Line 3 of the joined string is indeed the start of batch 1.
    assert joined.split("\n")[3] == "# Slide five"


def test_build_page_map_collapses_repeats_and_carries_none() -> None:
    outputs = ["a", "b", "c", "d"]
    pages = [2, 2, None, 7]  # page 2 repeats; None carries 2 forward; then 7.
    page_map = build_page_map(outputs, pages)
    assert page_map == [(0, 2), (6, 7)]


def test_build_page_map_empty() -> None:
    assert build_page_map([], []) == []
```

- [ ] **Step 2: Run it to verify it fails**

Run: `cd src/backend && python -m pytest tests/unit/test_page_map.py -v`
Expected: FAIL with `ImportError: cannot import name 'build_page_map'`

- [ ] **Step 3: Implement `build_page_map`**

Add to `src/backend/app/services/document_processing/normalization.py` (module level, near the top after imports):

```python
def build_page_map(outputs: list[str], pages: list[int | None]) -> list[tuple[int, int]]:
    """Map line offsets in ``"\\n\\n".join(outputs)`` to their source page/slide.

    Each output segment starts one blank separator line after the previous one
    (the ``"\\n\\n"`` join), so ``line_cursor`` accounts for that gap. ``None``
    pages carry the last known page forward; consecutive equal pages collapse
    to a single boundary. Line indices are 0-based into the joined string.
    """
    page_map: list[tuple[int, int]] = []
    line_cursor = 0
    last_page = 1
    for idx, text in enumerate(outputs):
        if idx > 0:
            line_cursor += 1  # blank line inserted by the "\n\n" join
        page = pages[idx] if idx < len(pages) and pages[idx] is not None else last_page
        if not page_map or page_map[-1][1] != page:
            page_map.append((line_cursor, page))
        last_page = page
        line_cursor += text.count("\n") + 1
    return page_map
```

- [ ] **Step 4: Run it to verify it passes**

Run: `cd src/backend && python -m pytest tests/unit/test_page_map.py -v`
Expected: PASS (3 tests)

- [ ] **Step 5: Write the failing test for `normalize()` returning a page_map**

Append to `src/backend/tests/unit/test_page_map.py`:

```python
from app.services.document_processing.config import DocumentProcessingConfig
from app.services.document_processing.normalization import DocumentNormalizer


def _normalizer_vision_off() -> DocumentNormalizer:
    # enable_real_vision False -> passthrough mode, no provider calls.
    config = DocumentProcessingConfig(enable_real_vision=False)
    return DocumentNormalizer(config, provider_chain=None)  # chain unused in passthrough


def test_normalize_returns_page_map_passthrough() -> None:
    normalizer = _normalizer_vision_off()
    blocks = [
        {"kind": "text", "page": 1, "content": "Alpha on page one."},
        {"kind": "text", "page": 4, "content": "Beta on page four."},
    ]
    markdown, trace, page_map = normalizer.normalize(blocks, doc_type="document")
    assert not markdown.startswith("\n")  # alignment invariant: no leading blank line
    assert page_map[0] == (0, 1)
    assert any(page == 4 for _, page in page_map)
```

Note: verify `DocumentProcessingConfig` accepts `enable_real_vision` as a kwarg; if its constructor differs, build it the way `test_ocr_worker.py` / `config.py` construct it and only set `enable_real_vision=False`. If `batch_blocks` merges these two blocks into one batch (char budget), split them onto separate pages far enough apart or lower the budget in the config so each block is its own batch — the test must exercise two page boundaries.

- [ ] **Step 6: Run it to verify it fails**

Run: `cd src/backend && python -m pytest tests/unit/test_page_map.py::test_normalize_returns_page_map_passthrough -v`
Expected: FAIL — `normalize` returns a 2-tuple, so the 3-way unpack raises `ValueError: not enough values to unpack`.

- [ ] **Step 7: Thread pages through `normalize()`**

In `src/backend/app/services/document_processing/normalization.py`, inside `normalize()`, track the page for every appended output and return the map. Replace the body from the `outputs`/`trace` init through the return:

```python
        outputs: list[str] = []
        output_pages: list[int | None] = []
        trace: list[dict[str, object]] = []

        for i, batch in enumerate(batches):
            combined = "\n\n".join(str(b.get("content", "")) for b in batch)
            page_range = [b.get("page") or b.get("slide") for b in batch if b.get("page") or b.get("slide")]
            batch_page = page_range[0] if page_range else None
            trace_entry: dict[str, object] = {
                "batch_index": i,
                "block_count": len(batch),
                "input_chars": len(combined),
                "page_or_slide_range": [page_range[0], page_range[-1]] if page_range else None,
            }

            if not combined.strip():
                trace_entry["mode"] = "skipped_empty"
                trace.append(trace_entry)
                continue

            if not real_vision:
                outputs.append(combined)
                output_pages.append(batch_page)
                trace_entry["mode"] = "passthrough_vision_disabled"
                trace_entry["output_chars"] = len(combined)
                trace.append(trace_entry)
                continue

            prompt = self._build_normalization_prompt(combined, doc_type)
            output, err = self._chain.text(prompt, operation="normalization")
            if err is not None:
                outputs.append(combined)
                output_pages.append(batch_page)
                trace_entry["mode"] = "llm_fallback_to_input"
                trace_entry["output_chars"] = len(combined)
                trace_entry["error"] = err
            else:
                outputs.append(output)
                output_pages.append(batch_page)
                trace_entry["mode"] = "llm"
                trace_entry["output_chars"] = len(output)
            trace.append(trace_entry)

        page_map = build_page_map(outputs, output_pages)
        return "\n\n".join(outputs), trace, page_map
```

Also update the early empty-batches return near the top of `normalize()`:

```python
        if not batches:
            return "[EMPTY_OUTPUT]", [], []
```

- [ ] **Step 8: Update the pipeline call site**

In `src/backend/app/services/document_processing/pipeline.py`, change the `normalize` unpack (around line 178):

```python
        normalized_md, normalization_trace, page_map = self._normalizer.normalize(cleaned_blocks, doc_type)
```

Leave the `DocumentProcessingResult(...)` construction for Task 4; `page_map` is unused locally for now, which is acceptable within this single task's boundary since Task 4 immediately consumes it. (If a linter fails on the unused name, proceed straight into Task 4 before running lint.)

- [ ] **Step 9: Run the tests to verify they pass**

Run: `cd src/backend && python -m pytest tests/unit/test_page_map.py -v`
Expected: PASS (4 tests)

- [ ] **Step 10: Commit**

```bash
git add src/backend/app/services/document_processing/normalization.py \
        src/backend/app/services/document_processing/pipeline.py \
        src/backend/tests/unit/test_page_map.py
git commit -m "feat(pipeline): compute page_map during markdown normalization"
```

---

### Task 2: `parse_markdown_sections` records each section's start line

**Files:**
- Modify: `src/backend/app/workers/chunking.py` (the `Section` dataclass + `parse_markdown_sections`)
- Test: `src/backend/tests/unit/test_chunking.py` (append)

**Interfaces:**
- Consumes: nothing from Task 1 (independent).
- Produces: `Section` dataclass gains `start_line: int` (0-based line index of the section's heading in the stripped markdown; `0` for the implicit "Document Start" section). `parse_markdown_sections(markdown_text: str) -> list[Section]` unchanged signature, now populates `start_line`.

- [ ] **Step 1: Write the failing test**

Append to `src/backend/tests/unit/test_chunking.py`:

```python
from app.workers.chunking import parse_markdown_sections


def test_parse_markdown_sections_records_start_line() -> None:
    md = "Intro line\n\n# First\nbody one\n\n## Second\nbody two"
    sections = parse_markdown_sections(md)
    # Stripped lines: 0="Intro line",1="",2="# First",3="body one",4="",5="## Second",6="body two"
    titles = {s.title: s.start_line for s in sections}
    assert titles["Document Start"] == 0
    assert titles["First"] == 2
    assert titles["Second"] == 5
```

- [ ] **Step 2: Run it to verify it fails**

Run: `cd src/backend && python -m pytest tests/unit/test_chunking.py::test_parse_markdown_sections_records_start_line -v`
Expected: FAIL — `TypeError: __init__() got an unexpected keyword argument 'start_line'` (or `AttributeError: 'Section' object has no attribute 'start_line'`).

- [ ] **Step 3: Add `start_line` and populate it**

In `src/backend/app/workers/chunking.py`, update the `Section` dataclass:

```python
@dataclass
class Section:
    title: str
    body: str
    start_line: int = 0
```

Rewrite `parse_markdown_sections` to track line indices:

```python
def parse_markdown_sections(markdown_text: str) -> list[Section]:
    text = markdown_text.replace("\r\n", "\n").strip()
    if not text:
        return []

    sections: list[Section] = []
    current_title = "Document Start"
    current_lines: list[str] = []
    current_start = 0

    for line_no, line in enumerate(text.split("\n")):
        if re.match(r"^#{1,6}\s+", line):
            body = "\n".join(current_lines).strip()
            if body:
                sections.append(Section(title=current_title, body=body, start_line=current_start))
            current_title = _normalize_heading(line)
            current_lines = []
            current_start = line_no
        else:
            current_lines.append(line)

    final_body = "\n".join(current_lines).strip()
    if final_body:
        sections.append(Section(title=current_title, body=final_body, start_line=current_start))

    return sections
```

- [ ] **Step 4: Run it to verify it passes (and no regressions)**

Run: `cd src/backend && python -m pytest tests/unit/test_chunking.py -v`
Expected: PASS (all existing tests + the new one)

- [ ] **Step 5: Commit**

```bash
git add src/backend/app/workers/chunking.py src/backend/tests/unit/test_chunking.py
git commit -m "feat(chunking): record section start line for page attribution"
```

---

### Task 3: `build_chunks` stamps each chunk with its section's page

**Files:**
- Modify: `src/backend/app/workers/chunking.py` (the `Chunk` dataclass, `build_chunks`, new `_page_for_line` helper, `__all__`)
- Test: `src/backend/tests/unit/test_chunking.py` (append)

**Interfaces:**
- Consumes: `page_map: list[tuple[int, int]]` produced by Task 1's `build_page_map`; `Section.start_line` from Task 2.
- Produces: `Chunk` dataclass gains `page: int | None = None`. `build_chunks(markdown_text: str, encoder: Encoder, page_map: list[tuple[int, int]] | None = None, similarity_threshold: float = 0.55, min_chunk_chars: int = 350, max_chunk_chars: int = 1200) -> list[Chunk]` — new optional `page_map` param; when provided, every chunk carries its section's page.

- [ ] **Step 1: Write the failing test**

Append to `src/backend/tests/unit/test_chunking.py`:

```python
from app.workers.chunking import Chunk


def test_build_chunks_assigns_page_from_page_map() -> None:
    # Section "First" starts at line 0 -> page 1; "Second" starts at line 5 -> page 8.
    md = "# First\nbody one is reasonably long text.\n\n## Second\nbody two is also text here."
    page_map = [(0, 1), (5, 8)]
    chunks = build_chunks(md, DummyEncoder(), page_map=page_map, min_chunk_chars=1)
    assert chunks, "expected at least one chunk per section"
    by_section = {c.section_title: c.page for c in chunks}
    assert by_section["First"] == 1
    assert by_section["Second"] == 8


def test_build_chunks_without_page_map_leaves_page_none() -> None:
    md = "# First\nbody one is reasonably long text."
    chunks = build_chunks(md, DummyEncoder(), min_chunk_chars=1)
    assert chunks
    assert all(c.page is None for c in chunks)
```

Note: confirm line 5 of the stripped `md` is `## Second` (lines: 0=`# First`,1=`body...`,2=``,3=``... adjust the `##` heading's line to match its real index; recompute from `md.strip().split("\n")` if the test fails on the boundary, keeping `page_map` aligned to the actual heading line).

- [ ] **Step 2: Run it to verify it fails**

Run: `cd src/backend && python -m pytest tests/unit/test_chunking.py::test_build_chunks_assigns_page_from_page_map -v`
Expected: FAIL — `TypeError: build_chunks() got an unexpected keyword argument 'page_map'`.

- [ ] **Step 3: Add `page`, the lookup helper, and thread it through `build_chunks`**

In `src/backend/app/workers/chunking.py`, add `import bisect` at the top with the other imports. Update the `Chunk` dataclass:

```python
@dataclass
class Chunk:
    text: str
    section_title: str
    chunk_order: int
    char_count: int
    page: int | None = None
```

Add a module-level helper (near `parse_markdown_sections`):

```python
def _page_for_line(page_map: list[tuple[int, int]], line: int) -> int | None:
    """Return the page whose boundary is at or before ``line`` (bisect)."""
    if not page_map:
        return None
    starts = [start for start, _ in page_map]
    idx = bisect.bisect_right(starts, line) - 1
    if idx < 0:
        return page_map[0][1]
    return page_map[idx][1]
```

Update `build_chunks` — signature and the per-section loop:

```python
def build_chunks(
    markdown_text: str,
    encoder: Encoder,
    page_map: list[tuple[int, int]] | None = None,
    similarity_threshold: float = 0.55,
    min_chunk_chars: int = 350,
    max_chunk_chars: int = 1200,
) -> list[Chunk]:
    sections = parse_markdown_sections(markdown_text)
    chunks: list[Chunk] = []
    chunk_order = 1

    for section in sections:
        paragraphs = _split_paragraphs(section.body)
        if not paragraphs:
            continue

        section_page = _page_for_line(page_map, section.start_line) if page_map else None

        paragraph_embeddings = encoder.encode(paragraphs)
        merged = _chunk_section(
            section=section,
            paragraph_embeddings=paragraph_embeddings,
            similarity_threshold=similarity_threshold,
            min_chunk_chars=min_chunk_chars,
            max_chunk_chars=max_chunk_chars,
        )
        for text, _ in merged:
            chunks.append(
                Chunk(
                    text=text,
                    section_title=section.title,
                    chunk_order=chunk_order,
                    char_count=len(text),
                    page=section_page,
                )
            )
            chunk_order += 1

    return chunks
```

Add `_page_for_line` to `__all__` is not required (private); leave `__all__` as-is.

- [ ] **Step 4: Run the tests to verify they pass**

Run: `cd src/backend && python -m pytest tests/unit/test_chunking.py -v`
Expected: PASS (all)

- [ ] **Step 5: Commit**

```bash
git add src/backend/app/workers/chunking.py src/backend/tests/unit/test_chunking.py
git commit -m "feat(chunking): stamp chunks with source page from page_map"
```

---

### Task 4: Persist the page_map sidecar in S3 during OCR

**Files:**
- Modify: `src/backend/app/services/document_processing/models.py` (`DocumentProcessingResult`)
- Modify: `src/backend/app/services/document_processing/pipeline.py` (populate `page_map`)
- Modify: `src/backend/app/storage/client.py` (new key helper)
- Modify: `src/backend/app/workers/ocr_worker.py` (return + store sidecar)
- Test: `src/backend/tests/unit/test_storage_keys.py` (create)

**Interfaces:**
- Consumes: `page_map` from Task 1 (via `normalize`).
- Produces: `pagemap_document_key(course_id: UUID, document_id: UUID) -> str` in `storage/client.py`. `DocumentProcessingResult.page_map: list[tuple[int, int]]`. `run_document_processing_pipeline(...) -> tuple[str, list[tuple[int, int]]]` (now returns markdown **and** page_map; `custom_runner` path returns `(markdown, [])`).

- [ ] **Step 1: Write the failing test for the key helper**

```python
# src/backend/tests/unit/test_storage_keys.py
from __future__ import annotations

from uuid import UUID

from app.storage.client import markdown_document_key, pagemap_document_key


def test_pagemap_key_sits_next_to_markdown() -> None:
    course = UUID("11111111-1111-1111-1111-111111111111")
    doc = UUID("22222222-2222-2222-2222-222222222222")
    md = markdown_document_key(course, doc)
    pm = pagemap_document_key(course, doc)
    assert pm == md.rsplit("/", 1)[0] + "/pagemap.json"
    assert pm.endswith("pagemap.json")
```

- [ ] **Step 2: Run it to verify it fails**

Run: `cd src/backend && python -m pytest tests/unit/test_storage_keys.py -v`
Expected: FAIL — `ImportError: cannot import name 'pagemap_document_key'`.

- [ ] **Step 3: Add the key helper**

In `src/backend/app/storage/client.py`, after `markdown_document_key`:

```python
def pagemap_document_key(course_id: UUID, document_id: UUID) -> str:
    return f"documents/{course_id}/{document_id}/markdown/pagemap.json"
```

- [ ] **Step 4: Run it to verify it passes**

Run: `cd src/backend && python -m pytest tests/unit/test_storage_keys.py -v`
Expected: PASS

- [ ] **Step 5: Add `page_map` to the result model and populate it**

In `src/backend/app/services/document_processing/models.py`, add a field to `DocumentProcessingResult`:

```python
    page_map: list[tuple[int, int]] = field(default_factory=list)
```

In `src/backend/app/services/document_processing/pipeline.py`, pass it into the constructed result (the `normalized_md, normalization_trace, page_map = ...` unpack from Task 1 already exists):

```python
        return DocumentProcessingResult(
            markdown=normalized_md,
            route=route,
            inferred_type=doc_type,
            blocks=blocks,
            prompts=prompts,
            visual_trace=visual_trace,
            normalization_trace=normalization_trace,
            quality_flags=quality_flags,
            llm_metrics=self._recorder.summary(),
            progress=self._emitter.records,
            page_map=page_map,
        )
```

- [ ] **Step 6: Return page_map from `run_document_processing_pipeline` and store the sidecar**

In `src/backend/app/workers/ocr_worker.py`, change the return of `run_document_processing_pipeline` (last line) to:

```python
    return result.markdown, result.page_map
```

Update its docstring first line to `... and return (markdown, page_map).`

At the call site (around line 208-217), handle both runner paths and store the sidecar. Add `import json` at the top of the file if not already imported, and import the key helper alongside `markdown_document_key`:

```python
from app.storage.client import markdown_document_key, pagemap_document_key
```

Then:

```python
                with trace.step("run_document_processing_pipeline"):
                    if custom_runner is not None:
                        markdown_text = await custom_runner(input_path, document)
                        page_map: list[tuple[int, int]] = []
                    else:
                        markdown_text, page_map = await run_document_processing_pipeline(
                            input_path, document, trace=trace
                        )

            md_key = markdown_document_key(document.course_id, document.id)
            with trace.step("storage_put_markdown", storage_key=md_key, markdown_chars=len(markdown_text)):
                await storage.put_object(md_key, markdown_text.encode("utf-8"), "text/markdown; charset=utf-8")
            document.storage_md_path = md_key
            if page_map:
                pm_key = pagemap_document_key(document.course_id, document.id)
                with trace.step("storage_put_pagemap", storage_key=pm_key, boundary_count=len(page_map)):
                    await storage.put_object(
                        pm_key, json.dumps(page_map).encode("utf-8"), "application/json"
                    )
```

Note: if `test_ocr_worker.py` asserts on the exact return type of `run_document_processing_pipeline` or stubs it, update that stub to return a `(markdown, [])` tuple.

- [ ] **Step 7: Run the storage + OCR worker tests**

Run: `cd src/backend && python -m pytest tests/unit/test_storage_keys.py tests/unit/test_ocr_worker.py -v`
Expected: PASS (fix the `test_ocr_worker.py` stub to the 2-tuple return if it fails on unpacking)

- [ ] **Step 8: Commit**

```bash
git add src/backend/app/services/document_processing/models.py \
        src/backend/app/services/document_processing/pipeline.py \
        src/backend/app/storage/client.py \
        src/backend/app/workers/ocr_worker.py \
        src/backend/tests/unit/test_storage_keys.py
git commit -m "feat(ocr): persist page_map sidecar alongside markdown"
```

---

### Task 5: Index worker reads the sidecar and writes `page_number`

**Files:**
- Modify: `src/backend/app/workers/index_worker.py` (`process_index_job` phase 2, `_finalize_indexed`)
- Test: manual reindex verification (worker path is DB + S3 bound; unit-covered logic lives in Tasks 1–4)

**Interfaces:**
- Consumes: `pagemap_document_key` (Task 4), `build_chunks(..., page_map=...)` (Task 3), `Chunk.page` (Task 3).
- Produces: `DocumentChunk.page_number` populated from `Chunk.page` for newly indexed documents.

- [ ] **Step 1: Load the sidecar in phase 2 and pass it to `build_chunks`**

In `src/backend/app/workers/index_worker.py`, add imports at the top:

```python
import json
from app.storage.client import pagemap_document_key
```

In `process_index_job`, phase 2 (after `markdown_text` is decoded, before `build_chunks`), load the sidecar defensively. Replace the `raw_chunks = await asyncio.to_thread(build_chunks, markdown_text, embedding_service)` block:

```python
        page_map: list[tuple[int, int]] = []
        course_id_val = doc_fields["course_id"]
        if isinstance(course_id_val, UUID):
            pm_key = pagemap_document_key(course_id_val, document_id)
            try:
                pm_bytes = await storage.get_object(pm_key)
                page_map = [(int(s), int(p)) for s, p in json.loads(pm_bytes.decode("utf-8"))]
            except Exception:
                page_map = []  # missing/corrupt sidecar -> page_number stays NULL

        # Embedding/rerank use a blocking HTTP client; run off the event loop so
        # concurrent jobs don't starve asyncpg (which raises MissingGreenlet).
        raw_chunks = await asyncio.to_thread(build_chunks, markdown_text, embedding_service, page_map)
```

Note: `build_chunks`'s third positional parameter is `page_map` (Task 3), so passing it positionally is correct.

- [ ] **Step 2: Write `page_number` in `_finalize_indexed`**

In `_finalize_indexed`, add `page_number=chunk.page` to the `DocumentChunk(...)` construction:

```python
        db_chunks = [
            DocumentChunk(
                document_id=document_id,
                course_id=course_id,
                document_tier=doc_fields["document_tier"],
                subtype=subtype,
                rag_namespace=rag_namespace,
                section_title=chunk.section_title,
                page_number=chunk.page,
                chunk_order=chunk.chunk_order,
                content=chunk.text,
                embedding=embeddings[i] if i < len(embeddings) else None,
            )
            for i, chunk in enumerate(raw_chunks)
        ]
```

- [ ] **Step 3: Verify the full unit suite still passes**

Run: `cd src/backend && python -m pytest tests/unit/test_chunking.py tests/unit/test_page_map.py tests/unit/test_storage_keys.py tests/unit/test_ocr_worker.py tests/unit/test_reindex_service.py -v`
Expected: PASS

- [ ] **Step 4: Manual end-to-end verification (real stack)**

Rebuild the affected images (per project memory, `:8000` and workers are baked), then reindex one PDF and one PPTX document and confirm pages land:

```bash
docker compose build api worker-ocr worker-index && docker compose up -d api worker-ocr worker-index
# Trigger a reindex of a known PDF document via the admin CLI or the reindex endpoint,
# then check the DB:
docker exec graduationthesis-postgres-1 psql -U postgres -d academic_kb -c \
  "SELECT section_title, page_number, chunk_order FROM document_chunks \
   WHERE document_id = '<REINDEXED_DOC_ID>' ORDER BY chunk_order LIMIT 20;"
```

Expected: `page_number` is non-NULL and increases monotonically with `chunk_order`; for a PPTX the values equal the slide numbers. Confirm the sidecar exists:

```bash
docker exec graduationthesis-minio-1 sh -c 'mc ls local/<bucket>/documents/<course_id>/<doc_id>/markdown/ 2>/dev/null' || true
```

Expected: both `output.md` and `pagemap.json` are present.

- [ ] **Step 5: Commit**

```bash
git add src/backend/app/workers/index_worker.py
git commit -m "feat(index): populate document_chunks.page_number from page_map sidecar"
```

---

## Self-Review

**Spec coverage:**
- Extractor page/slide already present → consumed by `normalize` (Task 1). ✓
- Page lost at normalize → `build_page_map` captures it (Task 1). ✓
- Cross-worker boundary (OCR → index) → sidecar JSON persisted (Task 4) and read (Task 5). ✓
- Chunk-to-page attribution → section-level via `start_line` + `_page_for_line` (Tasks 2–3). ✓
- `document_chunks.page_number` populated → `_finalize_indexed` (Task 5). ✓
- No content mutation / no migration / backward compatible → sidecar-only, nullable column, defensive load. ✓

**Type consistency:** `page_map: list[tuple[int, int]]` is used identically in Tasks 1, 3, 4, 5. `build_chunks(markdown_text, encoder, page_map, ...)` param order matches the positional call in Task 5. `Chunk.page` / `Section.start_line` names are consistent across Tasks 2, 3, 5. `run_document_processing_pipeline` 2-tuple return matches its unpack in Task 4.

**Placeholder scan:** No TBD/TODO; every code step shows full code; boundary line numbers in tests carry a recompute note because exact indices depend on the literal string, and the test itself is the guard.

**Known follow-ups (out of scope):** old documents keep `page_number = NULL` until reindexed; the tutor UI already reads `page_number` for citations, so no frontend change is required to display it once populated — verify the citation card renders the page when present.
