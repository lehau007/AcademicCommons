"""Answers a tutor question about one figure image with a vision model (3.8-flash first)."""

from __future__ import annotations

import asyncio
import dataclasses
from typing import Any

from app.config import Settings
from app.services.document_processing.config import DocumentProcessingConfig
from app.services.document_processing.metrics import LlmCallRecorder
from app.services.document_processing.progress import ProgressEmitter
from app.services.document_processing.providers.chain import ProviderChain
from app.services.document_processing.providers.factory import build_vision_providers

VIEW_PROMPT = """You help a tutor answer a student's question about a figure from the course material.
Answer using ONLY what is visible in the image. Transcribe relevant labels, values and text exactly.
If the image does not show the answer, say so briefly.
Question: {question}"""


class _DiscardingRecorder(LlmCallRecorder):
    """The viewer lives for the whole API process; per-call records would grow without bound."""

    def record(self, *args: Any, **kwargs: Any) -> None:
        return None


class _DiscardingEmitter(ProgressEmitter):
    def emit(self, event: str, **fields: Any) -> None:
        return None


class FigureViewer:
    def __init__(self, settings: Settings) -> None:
        # The viewer always calls the model, even where OCR vision is disabled (local dev).
        config = dataclasses.replace(DocumentProcessingConfig.from_settings(settings), enable_real_vision=True)
        recorder, emitter = _DiscardingRecorder(), _DiscardingEmitter()
        self._chain = ProviderChain(
            build_vision_providers(config, recorder=recorder, emitter=emitter, purpose="viewer"),
            recorder=recorder,
            emitter=emitter,
            enable_real_vision=True,
            global_concurrency=config.global_concurrency,
        )

    async def ask(self, image: bytes, question: str) -> str:
        return await asyncio.to_thread(
            self._chain.vision,
            VIEW_PROMPT.format(question=question[:500]),
            image,
            max_output_tokens=1024,
            operation="figure_view",
        )
