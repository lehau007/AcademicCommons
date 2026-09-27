"""Build the vision provider list from DocumentProcessingConfig.provider_order."""

from __future__ import annotations

from typing import Literal

from app.services.document_processing.config import DocumentProcessingConfig
from app.services.document_processing.metrics import LlmCallRecorder
from app.services.document_processing.progress import ProgressEmitter
from app.services.document_processing.providers.azure import AzureOpenAIVisionProvider
from app.services.document_processing.providers.base import VisionLanguageProvider
from app.services.document_processing.providers.bedrock import BedrockVisionProvider
from app.services.document_processing.providers.gemini import GeminiVisionProvider
from app.services.document_processing.providers.opencode import OpenCodeVisionProvider
from app.services.document_processing.providers.openrouter import OpenRouterVisionProvider
from app.services.document_processing.providers.vertex import VertexVisionProvider


def build_vision_providers(
    config: DocumentProcessingConfig,
    *,
    recorder: LlmCallRecorder,
    emitter: ProgressEmitter,
    purpose: Literal["ocr", "viewer"] = "ocr",
) -> list[VisionLanguageProvider]:
    """``vertex`` expands to two instances: flash-lite then flash for OCR, reversed for the viewer.

    Other providers are added only when their credentials are configured; unknown names are skipped.
    """
    vertex_models = [
        (config.ocr_vision_model, config.ocr_vision_thinking_level),
        (config.ocr_vision_fallback_model, config.ocr_vision_fallback_thinking_level),
    ]
    if purpose == "viewer":
        vertex_models.reverse()

    providers: list[VisionLanguageProvider] = []
    for name in config.provider_order:
        if name == "vertex":
            providers.extend(
                VertexVisionProvider(config, recorder=recorder, emitter=emitter, model=model, thinking_level=level)
                for model, level in vertex_models
            )
        elif name == "bedrock" and config.bedrock_api_key and config.bedrock_model_id:
            providers.append(BedrockVisionProvider(config, recorder=recorder, emitter=emitter))
        elif name == "gemini" and config.gemini_api_key:
            providers.append(GeminiVisionProvider(config, recorder=recorder, emitter=emitter))
        elif name == "azure" and config.azure_api_key:
            providers.append(AzureOpenAIVisionProvider(config, recorder=recorder, emitter=emitter))
        elif name == "opencode" and config.opencode_api_key:
            providers.append(OpenCodeVisionProvider(config, recorder=recorder, emitter=emitter))
        elif name == "openrouter" and config.openrouter_api_key:
            providers.append(OpenRouterVisionProvider(config, recorder=recorder, emitter=emitter))
    return providers
