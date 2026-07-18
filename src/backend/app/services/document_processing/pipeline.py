"""Document processing pipeline orchestrator.

Single-document, in-memory API that replaces the experiment's manifest-driven,
artifact-on-disk ``run_mode``. The OCR worker calls :meth:`process_document` and gets
markdown + metrics back directly — no temp manifest, no artifact round-trip.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

from app.config import Settings
from app.services.document_processing.classification import VisualClassifier
from app.services.document_processing.config import DocumentProcessingConfig
from app.services.document_processing.extractors.base import build_extractor
from app.services.document_processing.metrics import LlmCallRecorder
from app.services.document_processing.models import DocumentProcessingResult
from app.services.document_processing.normalization import Normalizer
from app.services.document_processing.progress import ProgressEmitter
from app.services.document_processing.providers.azure import AzureOpenAIVisionProvider
from app.services.document_processing.providers.base import VisionLanguageProvider
from app.services.document_processing.providers.bedrock import BedrockVisionProvider
from app.services.document_processing.providers.chain import ProviderChain
from app.services.document_processing.providers.gemini import GeminiVisionProvider
from app.services.document_processing.providers.groq import GroqVisionProvider
from app.services.document_processing.providers.opencode import OpenCodeVisionProvider
from app.services.document_processing.providers.openrouter import OpenRouterVisionProvider
from app.services.document_processing.routing import RouteDecider
from app.services.document_processing.validation import OutputValidator


class DocumentProcessingPipeline:
    def __init__(
        self,
        config: DocumentProcessingConfig,
        *,
        progress_callback: Callable[[dict[str, Any]], None] | None = None,
    ) -> None:
        self._config = config
        self._recorder = LlmCallRecorder(config.input_cost_per_1m, config.output_cost_per_1m)
        self._emitter = ProgressEmitter(progress_callback)
        self._chain = ProviderChain(
            self._build_providers(),
            recorder=self._recorder,
            emitter=self._emitter,
            enable_real_vision=config.enable_real_vision,
        )
        self._classifier = VisualClassifier(config, provider_chain=self._chain)
        self._router = RouteDecider()
        self._normalizer = Normalizer(config, provider_chain=self._chain)
        self._validator = OutputValidator()

    def _build_providers(self) -> list[VisionLanguageProvider]:
        """Build the provider chain in ``config.provider_order`` (== llm_provider_order).

        Both vision and text dispatch iterate this list in order, so ordering here drives
        both paths. A provider is only added when its required credentials (and model,
        where required) are present; unknown names are skipped.
        """
        cfg = self._config

        def _bedrock() -> VisionLanguageProvider | None:
            if cfg.bedrock_api_key and cfg.bedrock_model_id:
                return BedrockVisionProvider(cfg, recorder=self._recorder, emitter=self._emitter)
            return None

        def _gemini() -> VisionLanguageProvider | None:
            if cfg.gemini_api_key:
                return GeminiVisionProvider(cfg, recorder=self._recorder, emitter=self._emitter)
            return None

        def _groq() -> VisionLanguageProvider | None:
            if cfg.groq_api_key:
                return GroqVisionProvider(cfg, recorder=self._recorder, emitter=self._emitter)
            return None

        def _azure() -> VisionLanguageProvider | None:
            if cfg.azure_api_key:
                return AzureOpenAIVisionProvider(cfg, recorder=self._recorder, emitter=self._emitter)
            return None

        def _opencode() -> VisionLanguageProvider | None:
            if cfg.opencode_api_key:
                return OpenCodeVisionProvider(cfg, recorder=self._recorder, emitter=self._emitter)
            return None

        def _openrouter() -> VisionLanguageProvider | None:
            if cfg.openrouter_api_key:
                return OpenRouterVisionProvider(cfg, recorder=self._recorder, emitter=self._emitter)
            return None

        builders: dict[str, Callable[[], VisionLanguageProvider | None]] = {
            "bedrock": _bedrock,
            "gemini": _gemini,
            "groq": _groq,
            "azure": _azure,
            "opencode": _opencode,
            "openrouter": _openrouter,
        }

        providers: list[VisionLanguageProvider] = []
        for name in cfg.provider_order:
            builder = builders.get(name)
            if builder is None:
                continue
            provider = builder()
            if provider is not None:
                providers.append(provider)
        return providers

    def process_document(
        self,
        input_path: Path,
        *,
        document_id: str,
        expected_route: str | None = None,
    ) -> DocumentProcessingResult:
        """Route -> extract -> canonicalize -> normalize a single document, in memory.

        Mirrors one iteration of the experiment's ``run_mode`` per-sample loop, minus the
        on-disk artifact writes. Returns markdown + diagnostics (metrics, progress, trace).
        """
        self._emitter.emit("sample_start", sample_id=document_id, input_path=str(input_path))

        # Route.
        self._emitter.emit("route_start", sample_id=document_id)
        decision = self._router.decide(input_path)
        route, route_evidence = decision.route, decision.evidence
        self._emitter.emit("route_end", sample_id=document_id, route=route, route_evidence=route_evidence)

        # Extract.
        self._emitter.emit("extraction_start", sample_id=document_id, suffix=input_path.suffix.lower())
        extractor = build_extractor(
            input_path,
            self._config,
            provider_chain=self._chain,
            classifier=self._classifier,
            emitter=self._emitter,
        )
        extraction = extractor.extract(input_path)
        blocks, prompts, visual_trace = extraction.blocks, extraction.prompts, extraction.visual_trace
        self._emitter.emit(
            "extraction_end",
            sample_id=document_id,
            block_count=len(blocks),
            prompt_count=len(prompts),
            visual_count=len(visual_trace),
        )

        # Canonicalize structured blocks (mutates block content) + collect validators.
        validators = self._validator.canonicalize_structured_blocks(blocks)

        # Merge raw markdown AFTER canonicalization (matches run_mode ordering).
        raw_markdown = self._normalizer.merge_blocks_to_markdown(document_id, input_path.name, blocks)
        quality_flags = self._validator.assemble_quality_flags(
            route=route,
            expected_route=expected_route,
            validators=validators,
            raw_markdown=raw_markdown,
        )

        # Determine doc_type and normalize.
        ext = input_path.suffix.lower()
        if ext == ".pptx":
            doc_type = "pptx"
        elif ext == ".pdf":
            doc_type = str(route_evidence.get("inferred_type", "document"))
        else:
            doc_type = "document"

        cleaned_blocks = self._normalizer.rule_based_cleanup(blocks)
        self._emitter.emit(
            "normalization_start", sample_id=document_id, doc_type=doc_type, block_count=len(cleaned_blocks)
        )
        normalized_md, normalization_trace, page_map = self._normalizer.normalize(cleaned_blocks, doc_type)
        self._emitter.emit(
            "normalization_end",
            sample_id=document_id,
            batch_count=len(normalization_trace),
            normalized_chars=len(normalized_md),
        )
        self._emitter.emit("sample_end", sample_id=document_id, status="success")

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


def build_document_processing_pipeline(
    settings: Settings,
    *,
    progress_callback: Callable[[dict[str, Any]], None] | None = None,
) -> DocumentProcessingPipeline:
    return DocumentProcessingPipeline(
        DocumentProcessingConfig.from_settings(settings),
        progress_callback=progress_callback,
    )
