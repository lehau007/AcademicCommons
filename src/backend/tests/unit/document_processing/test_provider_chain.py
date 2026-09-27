from __future__ import annotations

import threading
import time
from typing import Any

from app.services.document_processing.providers.base import (
    ProviderResponse,
    VisionLanguageProvider,
    sniff_image_mime,
)

from .conftest import make_chain


class _FakeProvider(VisionLanguageProvider):
    def __init__(self, name: str, *, status: str = "success", text: str = "", raises: bool = False) -> None:
        self.provider_name = name
        self._status = status
        self._text = text
        self._raises = raises
        self.calls: list[dict[str, Any]] = []

    def complete(
        self,
        prompt: str,
        *,
        images: list[bytes] | None = None,
        operation: str = "text",
        **kwargs: Any,
    ) -> ProviderResponse:
        self.calls.append({"prompt": prompt, "images": images, "operation": operation, **kwargs})
        if self._raises:
            raise RuntimeError("sdk exploded")
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
    succeeding = _FakeProvider("p2", text="VISION_OK")
    chain = make_chain([failing, succeeding], enable_real_vision=True)

    assert chain.vision("prompt") == "VISION_OK"
    assert len(failing.calls) == 1
    assert len(succeeding.calls) == 1


def test_vision_forwards_schema_budget_operation_and_wraps_single_image() -> None:
    provider = _FakeProvider("p1", text="{}")
    chain = make_chain([provider], enable_real_vision=True)

    chain.vision("prompt", b"img", response_schema={"type": "OBJECT"}, max_output_tokens=321, operation="figure")

    call = provider.calls[0]
    assert call["images"] == [b"img"]
    assert call["response_schema"] == {"type": "OBJECT"}
    assert call["max_output_tokens"] == 321
    assert call["operation"] == "figure"


def test_vision_omits_unset_kwargs_for_legacy_providers() -> None:
    provider = _FakeProvider("p1", text="ok")
    chain = make_chain([provider], enable_real_vision=True)

    chain.vision("prompt")

    assert "response_schema" not in provider.calls[0]
    assert "max_output_tokens" not in provider.calls[0]


def test_vision_treats_provider_exception_as_failure_and_falls_back() -> None:
    chain = make_chain([_FakeProvider("p1", raises=True), _FakeProvider("p2", text="OK")], enable_real_vision=True)

    assert chain.vision("prompt") == "OK"


def test_vision_all_failing_returns_error_marker() -> None:
    chain = make_chain([_FakeProvider("p1", status="error")], enable_real_vision=True)

    assert chain.vision("prompt").startswith("[VISION_ERROR]")


def test_vision_disabled_returns_placeholder_without_calls() -> None:
    provider = _FakeProvider("p1", text="x")
    chain = make_chain([provider], enable_real_vision=False)

    assert chain.vision("prompt").startswith("[VISION_PLACEHOLDER]")
    assert provider.calls == []
    assert chain.enabled is False


def test_global_limit_caps_concurrent_calls_across_chains() -> None:
    lock = threading.Lock()
    state = {"active": 0, "peak": 0}

    class _Counting(_FakeProvider):
        def complete(self, prompt: str, **kwargs: Any) -> ProviderResponse:  # type: ignore[override]
            with lock:
                state["active"] += 1
                state["peak"] = max(state["peak"], state["active"])
            time.sleep(0.05)
            with lock:
                state["active"] -= 1
            return super().complete(prompt, **kwargs)

    chains = [make_chain([_Counting("p", text="ok")], enable_real_vision=True, global_concurrency=2) for _ in range(3)]
    threads = [threading.Thread(target=chain.vision, args=("p",)) for chain in chains for _ in range(3)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert state["peak"] <= 2


def test_sniff_image_mime() -> None:
    assert sniff_image_mime(b"\x89PNG\r\n\x1a\nrest") == "image/png"
    assert sniff_image_mime(b"\xff\xd8\xff\xe0rest") == "image/jpeg"
    assert sniff_image_mime(b"GIF89a") == "image/gif"
    assert sniff_image_mime(b"unknown") == "image/png"
