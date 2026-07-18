"""Normalization: rule-based cleanup + LLM-based markdown normalization + block merge.

Ports experiment ``rule_based_cleanup`` / ``batch_blocks_for_normalization`` /
``_call_normalization_llm`` / ``llm_based_normalization`` / ``merge_blocks_to_markdown``
(lines ~795-936, 1309-1332).
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

from app.services.document_processing.config import DocumentProcessingConfig
from app.services.document_processing.models import Block
from app.services.document_processing.providers.chain import ProviderChain


def build_page_map(outputs: list[str], pages: list[int | None]) -> list[tuple[int, int]]:
    """Map line offsets in ``"\\n\\n".join(outputs)`` to their source page/slide.

    Each output segment starts one blank separator line after the previous one
    (the ``"\\n\\n"`` join), so ``line_cursor`` accounts for that gap. ``None``
    pages carry the last known page forward; consecutive equal pages collapse
    to a single boundary. Line indices are 0-based into the joined string.
    A batch whose page is unknown AND no prior batch established a page stays
    unmapped — returning ``[]`` for an all-``None`` input, never a fabricated
    page number (non-paginated sources must yield ``page_number = NULL``).
    """
    page_map: list[tuple[int, int]] = []
    line_cursor = 0
    last_page: int | None = None
    for idx, text in enumerate(outputs):
        if idx > 0:
            line_cursor += 1  # blank line inserted by the "\n\n" join
        page = pages[idx] if idx < len(pages) and pages[idx] is not None else last_page
        if page is not None and (not page_map or page_map[-1][1] != page):
            page_map.append((line_cursor, page))
        if page is not None:
            last_page = page
        line_cursor += text.count("\n") + 1
    return page_map


def _strip_outer_fence(text: str) -> str:
    """Strip a code fence only when it wraps the ENTIRE block (e.g. a model
    accidentally wrapping its whole response in ```json ... ```).

    Fences that appear inside the content — e.g. the ASCII-diagram code blocks
    the vision-OCR prompts intentionally ask for — must be left untouched, or
    the diagram loses its monospace formatting and gets word-wrapped as prose.
    """
    stripped = text.strip()
    if not stripped.startswith("```") or not stripped.endswith("```"):
        return text
    lines = stripped.split("\n")
    if len(lines) < 2 or lines[-1].strip() != "```":
        return text
    inner = lines[1:-1]
    if any(line.strip() == "```" for line in inner):
        # More than one fence pair (or a fence + our own closer) — ambiguous,
        # leave as-is rather than risk eating an intentional diagram fence.
        return text
    return "\n".join(inner)


class Normalizer:
    def __init__(self, config: DocumentProcessingConfig, *, provider_chain: ProviderChain) -> None:
        self._config = config
        self._chain = provider_chain

    def rule_based_cleanup(self, blocks: list[Block]) -> list[Block]:
        cleaned = []
        for b in blocks:
            if b["kind"] == "text":
                text = b.get("content", "")
                text = text.replace("Here's a description", "").replace("Here is the table", "")
                text = _strip_outer_fence(text)
                if "image_url" in text:
                    text = text.replace("image_url", "")
                b_new = dict(b)
                b_new["content"] = text
                cleaned.append(b_new)
            else:
                cleaned.append(b)
        return cleaned

    def batch_blocks(self, blocks: list[Block], char_budget: int | None = None) -> list[list[Block]]:
        """Batches blocks for normalization (defaults to config budget).

        A new batch starts when adding the next block would exceed the budget.
        Slides are grouped together to reduce sequential LLM calls.
        """
        if char_budget is None:
            char_budget = self._config.normalize_char_budget
        char_budget = min(char_budget, 50000)

        batches: list[list[Block]] = []
        current: list[Block] = []
        current_len = 0

        for b in blocks:
            if b.get("kind") not in ("text", "vision_placeholder"):
                continue
            content = str(b.get("content", ""))

            over_budget = current and (current_len + len(content) > char_budget)

            if current and over_budget:
                batches.append(current)
                current = []
                current_len = 0

            current.append(b)
            current_len += len(content)

        if current:
            batches.append(current)
        return batches

    def normalize(
        self, blocks: list[Block], doc_type: str = "document"
    ) -> tuple[str, list[dict[str, object]], list[tuple[int, int]]]:
        """Returns (normalized_markdown, per_batch_trace, page_map). Mirrors ``llm_based_normalization``."""
        batches = self.batch_blocks(blocks)
        if not batches:
            return "[EMPTY_OUTPUT]", [], []

        real_vision = self._config.enable_real_vision

        # Per-batch context, in input order. batch_page/trace_entry are cheap to
        # precompute; the expensive part is the per-batch normalization LLM call.
        contexts: list[tuple[str, int | None, dict[str, object]]] = []
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
            contexts.append((combined, batch_page, trace_entry))

        # Run the normalization LLM call for every non-empty batch concurrently.
        # The calls are independent and I/O-bound (provider HTTP), so a bounded
        # thread pool turns what was N sequential LLM round-trips into ~N/workers,
        # which is the difference between finishing under the OCR job timeout and
        # being cancelled/retried forever on large documents. Order is preserved
        # by keying results on the batch index. A hard per-batch deadline caps a
        # stalled provider call so one slow batch can't sink the whole document.
        results: dict[int, tuple[str | None, str | None]] = {}
        if real_vision:
            llm_indices = [i for i, (combined, _p, _t) in enumerate(contexts) if combined.strip()]
            if llm_indices:
                deadline = self._config.request_timeout_seconds * 6
                max_workers = max(1, min(self._config.normalize_max_workers, len(llm_indices)))
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    futures = {
                        i: executor.submit(
                            self._chain.text,
                            self._build_normalization_prompt(contexts[i][0], doc_type),
                            operation="normalization",
                        )
                        for i in llm_indices
                    }
                    for i, future in futures.items():
                        try:
                            results[i] = future.result(timeout=deadline)
                        except Exception as exc:  # noqa: BLE001 - degrade to raw input on any failure
                            results[i] = (None, f"{type(exc).__name__}: {exc}")

        outputs: list[str] = []
        output_pages: list[int | None] = []
        trace: list[dict[str, object]] = []

        for i, (combined, batch_page, trace_entry) in enumerate(contexts):
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

            output, err = results[i]
            if err is not None or output is None:
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

        joined = "\n\n".join(outputs)
        # Alignment invariant: page_map's line offsets are counted against this
        # exact joined string, but downstream chunking counts against its
        # .strip()'d form. If the join starts with a blank line, .strip() would
        # shift every offset — degrade to no page attribution rather than risk
        # silently wrong page numbers (never guess; NULL is always safe).
        page_map = build_page_map(outputs, output_pages) if not joined.startswith("\n") else []
        return joined, trace, page_map

    @staticmethod
    def _build_normalization_prompt(combined: str, doc_type: str) -> str:
        """Slide-vs-document prompt construction ported from experiment lines 856-875."""
        if doc_type in ("slide_pdf", "pptx"):
            return (
                "The following is text extracted from lecture slides. Reformat it as clean Markdown:\n"
                "- The first short line of each segment is the slide title → ## heading\n"
                "- Format bullet points with -\n"
                "- Remove standalone page numbers (a lone digit on its own line)\n"
                "- Remove navigation headers repeated across slides (e.g. repeated table-of-contents lines)\n"
                "- If formula characters are garbled or fragmented, replace with [Formula: brief description]\n"
                "- Preserve tables as Markdown tables\n"
                "- Leave any ```...``` fenced code block (e.g. ASCII diagrams) exactly as-is, byte-for-byte; "
                "never reflow, reformat, or merge lines inside a fence\n"
                "- Keep any existing [Table: ...], [Chart: ...] or [Diagram: ...] summary line verbatim on its own line\n"
                "- For any Markdown table or fenced ASCII diagram that does NOT already have such a summary "
                "line directly above it, ADD one from the content: a single line in the document's language "
                "identifying what it is and, in one sentence, what it shows — [Table: ...] above a table, "
                "[Diagram: ...] above a diagram. Never add a second summary when one is already present\n"
                "- Keep the original language of the text; do not translate\n"
                "Output ONLY the cleaned Markdown. Do not explain your choices, restate or "
                "quote these instructions, or include any reasoning or commentary about the "
                "task — emit the result and nothing else.\n"
                "One ## section per slide.\n\n" + combined
            )
        return (
            "Normalize the following extracted document text into clean, coherent Markdown:\n"
            "- Identify headings and use # / ## notation\n"
            "- Reconstruct table-like data as Markdown tables\n"
            "- Merge paragraph fragments broken across lines\n"
            "- Remove page headers/footers (repeated titles, standalone page numbers)\n"
            "- Preserve exact meaning, formulas, and structured data\n"
            "- Leave any ```...``` fenced code block (e.g. ASCII diagrams) exactly as-is, byte-for-byte; "
            "never reflow, reformat, or merge lines inside a fence\n"
            "- Keep any existing [Table: ...], [Chart: ...] or [Diagram: ...] summary line verbatim on its own line\n"
            "- For any Markdown table or fenced ASCII diagram that does NOT already have such a summary "
            "line directly above it, ADD one from the content: a single line in the document's language "
            "identifying what it is and, in one sentence, what it shows — [Table: ...] above a table, "
            "[Diagram: ...] above a diagram. Never add a second summary when one is already present\n"
            "- Keep the original language of the text; do not translate\n"
            "Output ONLY the normalized Markdown. Do not explain your choices, restate or "
            "quote these instructions, or include any reasoning or commentary about the "
            "task — emit the result and nothing else.\n\n" + combined
        )

    def merge_blocks_to_markdown(self, sample_id: str, source_rel_path: str, blocks: list[Block]) -> str:
        """Mirrors experiment ``merge_blocks_to_markdown``."""
        lines = [f"# OCR Result: {sample_id}", "", f"Source: `{source_rel_path}`", ""]
        for block in blocks:
            if block["kind"] == "text":
                location = block.get("page") or block.get("slide") or "?"
                lines.append(f"## Segment {location}")
                lines.append("")
                lines.append(block.get("content", "").strip())
                lines.append("")
            elif block["kind"] == "vision_placeholder":
                location = block.get("page") or block.get("slide") or "?"
                lines.append(f"> Vision segment {location}: {block.get('content', '')}")
                lines.append("")

        content = "\n".join(lines).strip()
        if not content:
            return "# OCR Result\n\n[EMPTY_OUTPUT]"
        return content + "\n"
