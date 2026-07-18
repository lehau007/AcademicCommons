from __future__ import annotations

from app.services.document_processing.providers.base import (
    ProviderResponse,
    VisionLanguageProvider,
)

from .conftest import make_chain


class _FakeProvider(VisionLanguageProvider):
    def __init__(self, name: str, *, status: str, text: str = "") -> None:
        self.provider_name = name
        self._status = status
        self._text = text
        self.calls = 0

    def complete(
        self,
        prompt: str,
        *,
        images: list[bytes] | None = None,
        operation: str = "text",
    ) -> ProviderResponse:
        self.calls += 1
        return ProviderResponse(
            text=self._text,
            provider=self.provider_name,
            model="fake-model",
            status=self._status,
            latency_ms=1,
            error=None if self._status == "success" else "boom",
        )


def test_vision_falls_back_to_succeeding_provider() -> None:
    failing = _FakeProvider("p1", status="error")
    succeeding = _FakeProvider("p2", status="success", text="VISION_OK")
    chain = make_chain([failing, succeeding], enable_real_vision=True)

    assert chain.vision("prompt") == "VISION_OK"
    assert failing.calls == 1
    assert succeeding.calls == 1


def test_text_returns_success_text_and_no_error() -> None:
    failing = _FakeProvider("p1", status="error")
    succeeding = _FakeProvider("p2", status="success", text="TEXT_OK")
    chain = make_chain([failing, succeeding], enable_real_vision=True)

    text, err = chain.text("prompt")
    assert text == "TEXT_OK"
    assert err is None


def test_text_all_failing_returns_prompt_and_error() -> None:
    failing = _FakeProvider("p1", status="error")
    chain = make_chain([failing], enable_real_vision=True)

    text, err = chain.text("the prompt")
    assert text == "the prompt"
    assert err == "boom"


def test_vision_disabled_returns_placeholder_without_calling_providers() -> None:
    provider = _FakeProvider("p1", status="success", text="should not be used")
    chain = make_chain([provider], enable_real_vision=False)

    result = chain.vision("prompt", b"img")
    assert result.startswith("[VISION_PLACEHOLDER]")
    assert provider.calls == 0
