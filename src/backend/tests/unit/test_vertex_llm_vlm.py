import io
import PIL.Image
import pytest
from unittest.mock import MagicMock, patch
from app.llm.providers import VertexGeminiProvider, ChatMessage
from app.services.document_processing.config import DocumentProcessingConfig
from app.services.document_processing.metrics import LlmCallRecorder
from app.services.document_processing.progress import ProgressEmitter
from app.services.document_processing.providers.vertex import VertexVisionProvider


def _make_dummy_image_bytes() -> bytes:
    img = PIL.Image.new("RGB", (10, 10), color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


@pytest.mark.asyncio
async def test_vertex_gemini_provider_chat_and_client_construction():
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "Hello from Vertex Gemini"
    mock_response.usage_metadata = MagicMock(prompt_token_count=10, candidates_token_count=5)
    mock_client.models.generate_content.return_value = mock_response

    provider = VertexGeminiProvider(
        project_id="test-proj",
        location="us-central1",
        model="gemini-1.5-flash",
        client=mock_client,
    )
    result = await provider.chat([ChatMessage(role="user", content="Hi")])
    assert result.content == "Hello from Vertex Gemini"
    assert result.provider == "vertex"
    assert result.tokens_in == 10
    assert result.tokens_out == 5

    # Check config passed to generate_content defaults max_output_tokens to 16384
    mock_client.models.generate_content.assert_called_once()
    _, kwargs = mock_client.models.generate_content.call_args
    assert kwargs["config"].max_output_tokens == 16384


@pytest.mark.asyncio
async def test_vertex_gemini_provider_stream():
    mock_client = MagicMock()
    mock_chunk1 = MagicMock(text="Hello ", usage_metadata=None)
    mock_chunk2 = MagicMock(text="world", usage_metadata=MagicMock(prompt_token_count=5, candidates_token_count=2))
    mock_client.models.generate_content_stream.return_value = [mock_chunk1, mock_chunk2]

    provider = VertexGeminiProvider(
        project_id="test-proj",
        location="us-central1",
        model="gemini-1.5-flash",
        client=mock_client,
    )
    chunks = []
    async for chunk in provider.stream([ChatMessage(role="user", content="Hi")]):
        chunks.append(chunk)

    assert len(chunks) == 3
    assert chunks[0].text == "Hello "
    assert chunks[1].text == "world"
    assert chunks[2].done is True
    assert chunks[2].result.content == "Hello world"
    assert chunks[2].result.tokens_in == 5
    assert chunks[2].result.tokens_out == 2


@pytest.mark.asyncio
async def test_vertex_gemini_provider_init_with_vertexai_flag():
    with patch("app.llm.providers.get_vertex_credentials_and_project") as mock_auth, \
         patch("app.llm.providers.genai.Client") as mock_genai_client:
        mock_auth.return_value = (MagicMock(), "resolved-proj")
        provider = VertexGeminiProvider(project_id=None, location="us-east1", model="gemini-1.5-flash")
        
        mock_genai_client.assert_called_once()
        _, kwargs = mock_genai_client.call_args
        assert kwargs["vertexai"] is True
        assert kwargs["project"] == "resolved-proj"
        assert kwargs["location"] == "us-east1"


def test_vertex_vision_provider_complete_passes_16384_max_tokens():
    mock_recorder = MagicMock(spec=LlmCallRecorder)
    mock_emitter = MagicMock(spec=ProgressEmitter)
    config = DocumentProcessingConfig(
        vertex_project_id="test-proj",
        normalization_max_output_tokens=16384,
    )

    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "# Normalized Markdown Header"
    mock_response.usage_metadata = MagicMock(prompt_token_count=100, candidates_token_count=200)
    mock_client.models.generate_content.return_value = mock_response

    with patch("app.services.document_processing.providers.vertex.genai.Client", return_value=mock_client):
        provider = VertexVisionProvider(
            config=config,
            recorder=mock_recorder,
            emitter=mock_emitter,
        )
        response = provider.complete("Normalize this text", images=[_make_dummy_image_bytes()], operation="normalize")

        assert response.status == "success"
        assert response.text == "# Normalized Markdown Header"
        assert response.provider == "vertex"

        mock_client.models.generate_content.assert_called_once()
        _, kwargs = mock_client.models.generate_content.call_args
        assert kwargs["config"].max_output_tokens == 16384
        assert kwargs["config"].temperature == 0.3
