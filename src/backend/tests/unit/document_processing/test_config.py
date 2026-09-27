from __future__ import annotations

from app.config import Settings
from app.services.document_processing.config import DocumentProcessingConfig


def test_settings_defaults_target_gemini_3_models_on_global() -> None:
    settings = Settings(_env_file=None)

    assert settings.vertex_genai_location == "global"
    assert settings.vertex_chat_model == "gemini-3.8-flash"
    assert settings.vertex_chat_thinking_level == "low"
    assert settings.ocr_vision_model == "gemini-3.5-flash-lite"
    assert settings.ocr_vision_thinking_level == "minimal"
    assert settings.ocr_vision_fallback_model == "gemini-3.8-flash"
    assert settings.ocr_vision_fallback_thinking_level == "low"
    assert settings.document_processing_max_concurrency == 16
    assert settings.document_processing_global_concurrency == 32
    assert settings.document_processing_request_timeout_seconds == 60.0


def test_from_settings_maps_v4_fields_and_blank_thinking_to_none() -> None:
    settings = Settings(
        _env_file=None,
        llm_provider_order="vertex,gemini",
        vertex_genai_location="global",
        ocr_vision_model="lite-x",
        ocr_vision_thinking_level="",
        ocr_vision_fallback_model="flash-y",
        ocr_vision_fallback_thinking_level="low",
        document_processing_max_concurrency=7,
        document_processing_global_concurrency=9,
        document_processing_request_timeout_seconds=12.5,
    )

    config = DocumentProcessingConfig.from_settings(settings)

    assert config.provider_order == ("vertex", "gemini")
    assert config.vertex_genai_location == "global"
    assert config.ocr_vision_model == "lite-x"
    assert config.ocr_vision_thinking_level is None
    assert config.ocr_vision_fallback_model == "flash-y"
    assert config.ocr_vision_fallback_thinking_level == "low"
    assert config.max_concurrency == 7
    assert config.global_concurrency == 9
    assert config.request_timeout_seconds == 12.5
    assert config.max_output_tokens == 8192


def test_pymupdf4llm_is_installed_with_matching_version() -> None:
    import fitz  # type: ignore[import-untyped]
    import pymupdf4llm  # type: ignore[import-untyped]

    assert pymupdf4llm.__version__ == "1.27.2.3"
    assert fitz.VersionBind == "1.27.2.3"
