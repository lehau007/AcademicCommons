"""Configuration for the document processing pipeline.

Replaces the scattered ``os.getenv`` reads and module constants in the experiment
with a single frozen dataclass, built from the backend :class:`~app.config.Settings`.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.config import Settings

# Azure AI Foundry defaults (mirrors the experiment defaults; overridden via Settings).
AZURE_ENDPOINT_DEFAULT = "https://haulv226038-3382-resource.services.ai.azure.com/openai/v1"
AZURE_DEPLOYMENT_DEFAULT = "gpt-4-1-mini-2025-04-14-ft-cd68c6dbd12543298c5eb1ad64af5e4a"
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
GROQ_MODEL_DEFAULT = "meta-llama/llama-4-scout-17b-16e-instruct"
OPENCODE_BASE_URL = "https://opencode.ai/zen/go/v1"
OPENCODE_MODEL_DEFAULT = "minimax-m3"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_MODEL_DEFAULT = "openai/gpt-5.4-mini"


@dataclass(frozen=True)
class DocumentProcessingConfig:
    enable_real_vision: bool = False
    vision_max_workers: int = 6

    # Vision/OCR provider chain order (mirrors settings.llm_provider_order_list).
    provider_order: tuple[str, ...] = ()

    azure_endpoint: str | None = None
    azure_deployment: str | None = None
    azure_api_key: str | None = None

    gemini_api_key: str | None = None
    gemini_model: str = "gemini-3.1-flash-lite"

    groq_api_key: str | None = None
    groq_model: str = GROQ_MODEL_DEFAULT
    groq_base_url: str = GROQ_BASE_URL

    opencode_api_key: str | None = None
    opencode_model: str = OPENCODE_MODEL_DEFAULT
    opencode_base_url: str = OPENCODE_BASE_URL

    openrouter_api_key: str | None = None
    openrouter_model: str = OPENROUTER_MODEL_DEFAULT
    openrouter_base_url: str = OPENROUTER_BASE_URL

    bedrock_api_key: str | None = None
    bedrock_base_url: str | None = None
    bedrock_model_id: str | None = None
    aws_region: str = "us-east-1"

    input_cost_per_1m: float = 0.15
    output_cost_per_1m: float = 0.60
    normalize_char_budget: int = 24000
    normalize_max_workers: int = 4
    request_timeout_seconds: float = 30.0

    @classmethod
    def from_settings(cls, settings: Settings) -> DocumentProcessingConfig:
        return cls(
            enable_real_vision=settings.ocr_enable_real_vision,
            vision_max_workers=settings.ocr_vision_max_workers,
            provider_order=tuple(settings.llm_provider_order_list),
            azure_endpoint=settings.azure_openai_endpoint or AZURE_ENDPOINT_DEFAULT,
            azure_deployment=settings.azure_openai_deployment or AZURE_DEPLOYMENT_DEFAULT,
            azure_api_key=settings.azure_ai_api_key,
            gemini_api_key=settings.gemini_api_key,
            gemini_model=settings.gemini_model,
            groq_api_key=settings.groq_api_key,
            groq_model=settings.groq_model,
            opencode_api_key=settings.opencode_api_key,
            opencode_model=settings.opencode_model,
            opencode_base_url=settings.opencode_base_url,
            openrouter_api_key=settings.openrouter_api_key,
            openrouter_model=settings.openrouter_model,
            openrouter_base_url=settings.openrouter_base_url,
            bedrock_api_key=settings.bedrock_api_key,
            bedrock_base_url=settings.bedrock_base_url,
            bedrock_model_id=settings.bedrock_model_id,
            aws_region=settings.aws_region,
            input_cost_per_1m=settings.azure_openai_input_cost_per_1m,
            output_cost_per_1m=settings.azure_openai_output_cost_per_1m,
            normalize_char_budget=settings.document_processing_normalize_char_budget,
            normalize_max_workers=settings.document_processing_normalize_max_workers,
        )
