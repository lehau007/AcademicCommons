from __future__ import annotations

import logging

import pytest

from app.llm.observability import log_event


def test_log_event_emits_stable_metadata(caplog: pytest.LogCaptureFixture) -> None:
    logger = logging.getLogger("test.model_observability")
    with caplog.at_level(logging.INFO, logger=logger.name):
        log_event(
            logger,
            "llm_call_start",
            provider="vertex",
            model="gemini-2.5-flash",
            flow="tutor",
            schema_enabled=True,
        )

    assert caplog.messages == [
        "event=llm_call_start flow=tutor model=gemini-2.5-flash "
        "provider=vertex schema_enabled=true"
    ]


def test_log_event_redacts_payload_values_without_raising(caplog) -> None:
    logger = logging.getLogger("test.model_observability")
    with caplog.at_level(logging.INFO, logger=logger.name):
        log_event(logger, "unsafe", prompt={"content": "secret"})

    combined = "\n".join(caplog.messages)
    assert "prompt=<redacted>" in combined
    assert "secret" not in combined
