"""Image extractor. Ports experiment ``extract_image_text`` (lines ~1278-1309)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from app.services.document_processing.classification import VisualClassifier
from app.services.document_processing.extractors.base import Extractor
from app.services.document_processing.models import ExtractionResult


class ImageExtractor(Extractor):
    def extract(self, path: Path) -> ExtractionResult:
        visual_trace: list[dict[str, Any]] = []
        enable_real_vision = self._config.enable_real_vision

        blocks: list[dict[str, Any]]
        prompts: list[dict[str, Any]]
        if enable_real_vision:
            with open(path, "rb") as f:
                image_bytes = f.read()
            classification = self._classifier.classify(image_bytes)
            visual_trace.append({
                "source": "image_file",
                "file": path.name,
                "classification": classification,
                "action_taken": classification["action"],
            })
            prompt_text = (
                VisualClassifier.specialized_prompt(classification["label"])
                + " Also perform OCR on any text."
            )
            content = self._chain.vision(prompt_text, image_bytes)
            blocks = [{"kind": "text", "content": content}]
            prompts = [{"kind": "vision_ocr", "instruction": prompt_text, "image_path": path.name}]
        else:
            prompt_text = "Perform OCR and describe any table/formula/diagram in markdown format."
            prompts = [{"kind": "vision_prompt", "instruction": prompt_text, "image_path": path.name}]
            blocks = [{"kind": "vision_placeholder", "content": "[VISION_PLACEHOLDER] OCR output pending from vision model."}]  # noqa: E501

        return ExtractionResult(blocks=blocks, prompts=prompts, visual_trace=visual_trace)
