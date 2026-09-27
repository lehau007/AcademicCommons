import io
import PIL.Image
import pytest
from unittest.mock import MagicMock, patch
from google.genai import types as genai_types
from app.llm.providers import VertexGeminiProvider, ChatMessage
from app.services.document_processing.config import DocumentProcessingConfig
from app.services.document_processing.metrics import LlmCallRecorder
from app.services.document_processing.progress import ProgressEmitter
from app.services.document_processing.providers.vertex import VertexVisionProvider

VERTEX_VISION = "app.services.document_processing.providers.vertex"


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
    mock_response.usage_metadata = MagicMock(prompt_token_count=10, candidates_token_count=5, thoughts_token_count=0)
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
    mock_chunk2 = MagicMock(
        text="world",
        usage_metadata=MagicMock(prompt_token_count=5, candidates_token_count=2, thoughts_token_count=0),
    )
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


def _vision_response(text: str, *, prompt: int = 100, out: int = 20, thoughts: int = 5) -> MagicMock:
    response = MagicMock()
    response.text = text
    response.usage_metadata = MagicMock(
        prompt_token_count=prompt, candidates_token_count=out, thoughts_token_count=thoughts
    )
    return response


def _make_vision_provider(mock_client: MagicMock, recorder: LlmCallRecorder, **kwargs):  # type: ignore[no-untyped-def]
    config = DocumentProcessingConfig(
        vertex_project_id="test-proj", vertex_genai_location="global", request_timeout_seconds=45
    )
    return VertexVisionProvider(config, recorder=recorder, emitter=ProgressEmitter(), **kwargs)


def test_vertex_vision_provider_uses_global_location_model_thinking_and_schema() -> None:
    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = _vision_response("# Page")
    recorder = LlmCallRecorder()
    with patch(f"{VERTEX_VISION}.get_vertex_credentials_and_project", return_value=(MagicMock(), "resolved")), \
         patch(f"{VERTEX_VISION}.genai.Client", return_value=mock_client) as ctor:
        provider = _make_vision_provider(
            mock_client, recorder, model="gemini-3.5-flash-lite", thinking_level="minimal"
        )
        response = provider.complete(
            "OCR this",
            images=[_make_dummy_image_bytes()],
            operation="ocr",
            response_schema={"type": "OBJECT"},
            max_output_tokens=777,
        )

    assert response.ok and response.text == "# Page"
    assert provider.model == "gemini-3.5-flash-lite"
    _, ctor_kwargs = ctor.call_args
    assert ctor_kwargs["location"] == "global"
    assert ctor_kwargs["project"] == "test-proj"
    _, kwargs = mock_client.models.generate_content.call_args
    assert kwargs["model"] == "gemini-3.5-flash-lite"
    config = kwargs["config"]
    assert config.max_output_tokens == 777
    assert config.thinking_config.thinking_level == genai_types.ThinkingLevel.MINIMAL
    assert config.response_mime_type == "application/json"
    assert kwargs["contents"][0].inline_data.mime_type == "image/png"
    assert kwargs["contents"][-1] == "OCR this"
    assert recorder.summary()["by_model"]["gemini-3.5-flash-lite"]["completion_tokens"] == 25


def test_vertex_vision_provider_without_thinking_level_sends_no_thinking_config() -> None:
    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = _vision_response("ok")
    with patch(f"{VERTEX_VISION}.get_vertex_credentials_and_project", return_value=(MagicMock(), "p")), \
         patch(f"{VERTEX_VISION}.genai.Client", return_value=mock_client):
        provider = _make_vision_provider(mock_client, LlmCallRecorder(), model="m")
        provider.complete("text only")

    _, kwargs = mock_client.models.generate_content.call_args
    assert kwargs["config"].thinking_config is None
    assert kwargs["config"].max_output_tokens == 8192


def test_vertex_vision_provider_builds_one_client_under_concurrent_first_use() -> None:
    import threading
    import time
    from concurrent.futures import ThreadPoolExecutor

    calls: list[int] = []
    barrier = threading.Barrier(16)

    def _slow_client(**kwargs: object) -> MagicMock:
        calls.append(1)
        time.sleep(0.05)  # widen the race window
        return MagicMock()

    def _first_use(provider: VertexVisionProvider) -> object:
        barrier.wait()
        return provider._get_client()

    with patch(f"{VERTEX_VISION}.get_vertex_credentials_and_project", return_value=(MagicMock(), "p")), \
         patch(f"{VERTEX_VISION}.genai.Client", side_effect=_slow_client):
        provider = _make_vision_provider(MagicMock(), LlmCallRecorder(), model="m")
        with ThreadPoolExecutor(max_workers=16) as pool:
            clients = list(pool.map(_first_use, [provider] * 16))

    assert len(calls) == 1
    assert all(client is clients[0] for client in clients)


def test_vertex_vision_provider_empty_text_is_error_so_chain_falls_back() -> None:
    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = _vision_response("")
    with patch(f"{VERTEX_VISION}.get_vertex_credentials_and_project", return_value=(MagicMock(), "p")), \
         patch(f"{VERTEX_VISION}.genai.Client", return_value=mock_client):
        provider = _make_vision_provider(mock_client, LlmCallRecorder(), model="m", thinking_level="low")
        response = provider.complete("x")

    assert response.ok is False
    assert "empty" in (response.error or "")


@pytest.mark.asyncio
async def test_vertex_gemini_provider_applies_thinking_level_and_counts_thoughts() -> None:
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "ok"
    mock_response.usage_metadata = MagicMock(prompt_token_count=10, candidates_token_count=5, thoughts_token_count=7)
    mock_client.models.generate_content.return_value = mock_response
    provider = VertexGeminiProvider(
        project_id="p", location="global", model="gemini-3.8-flash", thinking_level="low", client=mock_client
    )

    result = await provider.chat([ChatMessage(role="user", content="Hi")])

    _, kwargs = mock_client.models.generate_content.call_args
    assert kwargs["config"].thinking_config.thinking_level == genai_types.ThinkingLevel.LOW
    assert result.tokens_out == 12


@pytest.mark.asyncio
async def test_vertex_gemini_provider_stream_applies_thinking_level() -> None:
    mock_client = MagicMock()
    usage = MagicMock(prompt_token_count=5, candidates_token_count=2, thoughts_token_count=3)
    mock_client.models.generate_content_stream.return_value = [MagicMock(text="Hi", usage_metadata=usage)]
    provider = VertexGeminiProvider(
        project_id="p", location="global", model="m", thinking_level="low", client=mock_client
    )

    chunks = [chunk async for chunk in provider.stream([ChatMessage(role="user", content="Hi")])]

    _, kwargs = mock_client.models.generate_content_stream.call_args
    assert kwargs["config"].thinking_config.thinking_level == genai_types.ThinkingLevel.LOW
    assert chunks[-1].result.tokens_out == 5


def test_build_llm_router_uses_genai_location_chat_model_and_thinking(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.config import Settings
    from app.llm import router as router_module

    captured: dict[str, object] = {}

    class _FakeVertex:
        provider_name = "vertex"

        def __init__(self, **kwargs: object) -> None:
            captured.update(kwargs)
            self.model = kwargs["model"]

    monkeypatch.setattr(router_module, "VertexGeminiProvider", _FakeVertex)
    settings = Settings(_env_file=None, llm_provider_order="vertex", vertex_project_id="proj")

    router = router_module.build_llm_router(settings)

    assert len(router.providers) == 1
    assert captured == {
        "model": "gemini-3.8-flash",
        "location": "global",
        "project_id": "proj",
        "thinking_level": "low",
    }
