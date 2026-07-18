"""PDF extractor. Ports experiment ``extract_pdf_text`` (lines ~940-1132)."""

from __future__ import annotations

import hashlib
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app.services.document_processing.classification import VisualClassifier
from app.services.document_processing.extractors.base import Extractor
from app.services.document_processing.models import ExtractionResult
from app.services.document_processing.routing import RouteDecider


@dataclass
class _PageRenderTask:
    page_index: int
    image_bytes: bytes
    prompt_text: str


@dataclass
class _ImageTask:
    page_index: int
    image_index: int
    image_bytes: bytes
    image_hash: str
    position_hint: str
    page_text: str
    repeat_count: int
    is_decorative_repeat: bool


class PdfExtractor(Extractor):
    def extract(self, path: Path) -> ExtractionResult:
        blocks: list[dict[str, Any]] = []
        prompts: list[dict[str, Any]] = []
        visual_trace: list[dict[str, Any]] = []

        try:
            import fitz  # type: ignore[import-untyped]  # PyMuPDF
        except Exception as exc:
            return ExtractionResult(
                blocks=blocks,
                prompts=[{"kind": "error", "message": f"PyMuPDF unavailable: {exc}"}],
                visual_trace=visual_trace,
            )

        enable_real_vision = self._config.enable_real_vision
        inferred_type, _ = RouteDecider().classify_pdf_type(path)
        max_workers = max(1, self._config.vision_max_workers)

        doc = fitz.open(path)
        page_count = len(doc)

        if inferred_type in ("scanned_pdf", "slide_pdf"):
            blocks, prompts = self._extract_rendered_pages(
                doc, page_count, inferred_type, enable_real_vision, max_workers
            )
            doc.close()
            return ExtractionResult(blocks=blocks, prompts=prompts, visual_trace=visual_trace)

        # Pre-pass: images repeating across many pages are almost certainly decorative
        # (logos, banners, page borders). Hash-based detection avoids a VLM call entirely.
        image_hash_pages: dict[str, set[int]] = {}
        for page_index, page in enumerate(doc):
            for img_info in page.get_images(full=True):
                xref = img_info[0]
                try:
                    base = doc.extract_image(xref)
                    h = hashlib.sha256(base["image"]).hexdigest()
                    image_hash_pages.setdefault(h, set()).add(page_index)
                except Exception:
                    continue
        repeat_threshold = max(2, int(page_count * 0.3)) if page_count else 2
        decorative_repeat_hashes = {
            h for h, pages in image_hash_pages.items() if len(pages) >= repeat_threshold
        }

        # Pass 1 (no network calls): extract text layer, enumerate embedded images.
        page_text_by_idx: dict[int, str] = {}
        image_blocks_by_page: dict[int, list[dict[str, Any]]] = {}
        image_tasks: list[_ImageTask] = []

        for page_index, page in enumerate(doc):
            text = (page.get_text("text") or "").strip()
            page_text_by_idx[page_index] = text
            page_height = page.rect.height if page.rect else None

            for image_idx, img_info in enumerate(page.get_images(full=True)):
                xref = img_info[0]
                if not enable_real_vision:
                    prompts.append({
                        "kind": "vision_prompt",
                        "page": page_index + 1,
                        "image_index": image_idx,
                        "instruction": "Describe diagram/table/formula and convert to markdown text.",
                    })
                    image_blocks_by_page.setdefault(page_index, []).append({
                        "kind": "vision_placeholder",
                        "page": page_index + 1,
                        "content": "[VISION_PLACEHOLDER] Describe visual element on this page.",
                    })
                    continue

                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_hash = hashlib.sha256(image_bytes).hexdigest()
                try:
                    rects = page.get_image_rects(xref)
                    rect = rects[0] if rects else None
                except Exception:
                    rect = None
                position_hint = self._classifier.position_hint(
                    rect.y0 if rect else None,
                    rect.y1 if rect else None,
                    page_height,
                )

                image_tasks.append(
                    _ImageTask(
                        page_index=page_index,
                        image_index=image_idx,
                        image_bytes=image_bytes,
                        image_hash=image_hash,
                        position_hint=position_hint,
                        page_text=text,
                        repeat_count=len(image_hash_pages.get(image_hash, set())),
                        is_decorative_repeat=image_hash in decorative_repeat_hashes,
                    )
                )

        # Pass 2 (network calls, parallelized): classify + extract each embedded image.
        def _run_task(task: _ImageTask) -> dict[str, Any]:
            page_index = task.page_index
            if task.is_decorative_repeat:
                classification = self._classifier.make_classification(
                    "decorative", "none", 1.0, "repeated_across_pages", task.position_hint
                )
            else:
                classification = self._classifier.classify(
                    task.image_bytes, surrounding_text=task.page_text, position_hint=task.position_hint
                )

            trace_entry: dict[str, Any] = {
                "source": "page",
                "page": page_index + 1,
                "image_index": task.image_index,
                "image_hash_prefix": task.image_hash[:16],
                "repeat_count": task.repeat_count,
                "position_hint": task.position_hint,
                "classification": classification,
                "action_taken": classification["action"],
            }

            if classification["action"] == "skip":
                return {
                    "trace_entry": trace_entry,
                    "prompt": {
                        "kind": "vision_skipped_decorative",
                        "page": page_index + 1,
                        "image_index": task.image_index,
                        "position_hint": task.position_hint,
                        "repeat_count": task.repeat_count,
                        "reason": classification["reason"],
                    },
                    "block": None,
                }

            if classification["action"] == "minimal_tag":
                return {
                    "trace_entry": trace_entry,
                    "prompt": {
                        "kind": "vision_minimal_tag",
                        "page": page_index + 1,
                        "image_index": task.image_index,
                        "position_hint": task.position_hint,
                        "classification": classification,
                    },
                    "block": {
                        "kind": "text",
                        "page": page_index + 1,
                        "image_index": task.image_index,
                        "content": f"[Visual: decorative element, page {page_index + 1}]",
                    },
                }

            # action == "extract"
            prompt_text = VisualClassifier.specialized_prompt(classification["label"], context=task.page_text)
            content = self._chain.vision(prompt_text, task.image_bytes)
            return {
                "trace_entry": trace_entry,
                "prompt": {
                    "kind": "vision_prompt",
                    "page": page_index + 1,
                    "image_index": task.image_index,
                    "category": classification["label"],
                    "position_hint": task.position_hint,
                    "instruction": prompt_text,
                },
                "block": {
                    "kind": "text",
                    "page": page_index + 1,
                    "image_index": task.image_index,
                    "content": f"\n### Visual Element (Page {page_index + 1}, Image {task.image_index})\n{content}\n",
                },
            }

        if image_tasks:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                for task, result in zip(image_tasks, executor.map(_run_task, image_tasks), strict=True):
                    visual_trace.append(result["trace_entry"])
                    prompts.append(result["prompt"])
                    if result["block"] is not None:
                        image_blocks_by_page.setdefault(task.page_index, []).append(result["block"])

        for page_index in range(page_count):
            text = page_text_by_idx.get(page_index, "")
            if text:
                blocks.append({"kind": "text", "page": page_index + 1, "content": text})
            blocks.extend(image_blocks_by_page.get(page_index, []))

        doc.close()
        return ExtractionResult(blocks=blocks, prompts=prompts, visual_trace=visual_trace)

    def _extract_rendered_pages(
        self,
        doc: Any,
        page_count: int,
        inferred_type: str,
        enable_real_vision: bool,
        max_workers: int,
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Scanned/slide PDFs: each page is rendered whole and OCR'd via one vision call.

        Pages are fully independent, so rendering + vision calls are parallelized the
        same way as embedded-image extraction.
        """
        import fitz  # type: ignore[import-untyped]

        blocks: list[dict[str, Any]] = []
        prompts: list[dict[str, Any]] = []

        if not enable_real_vision:
            for page_index in range(page_count):
                blocks.append({
                    "kind": "vision_placeholder",
                    "page": page_index + 1,
                    "content": "[VISION_PLACEHOLDER] OCR output pending for scanned page.",
                })
                prompts.append({
                    "kind": "vision_prompt",
                    "page": page_index + 1,
                    "instruction": "Perform OCR on this scanned page.",
                })
            return blocks, prompts

        if inferred_type == "slide_pdf":
            prompt_text = (
                "This is a lecture slide page. Extract its content as Markdown:\n"
                "- The slide title (large text at top) → ## heading\n"
                "- Bullet points → - list items\n"
                "- Any table → Markdown table\n"
                "- Any formula or equation → LaTeX inside $...$\n"
                "- Any diagram/graph/memory layout/flowchart → draw/represent it visually using a Markdown table (e.g. for variables/states/transitions) or a text-based ASCII diagram (using boxes [+---+] and arrows [-->] inside a preformatted ``` block). Underneath this visual representation, add [Diagram: ...] explaining in 1-2 sentences the concept/process the diagram illustrates and why it matters — not a restatement of which boxes connect to which\n"  # noqa: E501
                "Keep the original language of the slide; do not translate.\n"
                "Output only the Markdown content, no commentary."
            )
        else:
            prompt_text = (
                "This is a scanned mixed-layout page. Extract ALL of its content as clean Markdown, "
                "in approximate reading order:\n"
                "- Body text → paragraphs\n"
                "- Table-like regions → Markdown tables\n"
                "- Graph/diagram regions → a text-based ASCII diagram (using boxes [+---+] and arrows [-->] inside a preformatted ``` block), with [Diagram: ...] underneath explaining in 1-2 sentences the concept/process it illustrates and why it matters — not a restatement of which boxes connect to which\n"  # noqa: E501
                "- Handwritten annotations → blockquotes prefixed with [Handwritten]\n"
                "Keep the original language of the document; do not translate.\n"
                "Output only the Markdown content, no commentary."
            )

        page_tasks: list[_PageRenderTask] = []
        for page_index, page in enumerate(doc):
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            page_tasks.append(
                _PageRenderTask(page_index=page_index, image_bytes=pix.tobytes("png"), prompt_text=prompt_text)
            )

        def _run_task(task: _PageRenderTask) -> dict[str, Any]:
            content = self._chain.vision(task.prompt_text, task.image_bytes)
            return {
                "block": {
                    "kind": "text",
                    "page": task.page_index + 1,
                    "content": content,
                    "ocr_strategy": "region_based",
                },
                "prompt": {
                    "kind": "vision_ocr",
                    "page": task.page_index + 1,
                    "instruction": task.prompt_text,
                    "ocr_strategy": "region_based",
                },
            }

        results_by_page: dict[int, dict[str, Any]] = {}
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for task, result in zip(page_tasks, executor.map(_run_task, page_tasks), strict=True):
                results_by_page[task.page_index] = result

        for page_index in range(page_count):
            result = results_by_page[page_index]
            blocks.append(result["block"])
            prompts.append(result["prompt"])

        return blocks, prompts
