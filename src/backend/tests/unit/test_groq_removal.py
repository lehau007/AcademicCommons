import pytest
from app.config import get_settings
from app.services.document_processing.config import DocumentProcessingConfig


def test_groq_removal_settings():
    settings = get_settings()
    assert not hasattr(settings, "groq_api_key"), "settings should not have groq_api_key"
    assert "groq" not in settings.llm_provider_order, "groq should not be in llm_provider_order"


def test_normalization_max_output_tokens_config():
    settings = get_settings()
    config = DocumentProcessingConfig.from_settings(settings)
    assert hasattr(config, "normalization_max_output_tokens"), "config should have normalization_max_output_tokens"
    assert config.normalization_max_output_tokens == 16384
