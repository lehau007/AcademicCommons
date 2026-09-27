from __future__ import annotations

from app.services.document_processing.metrics import LlmCallRecorder


def test_summary_groups_tokens_by_model_and_counts_operations() -> None:
    recorder = LlmCallRecorder()
    recorder.record("ocr", "vertex", "lite", "success", 10, prompt_tokens=100, completion_tokens=20)
    recorder.record("figure", "vertex", "lite", "success", 10, prompt_tokens=50, completion_tokens=5)
    recorder.record("ocr", "vertex", "flash", "error", 10, error="timeout")

    summary = recorder.summary()

    assert summary["by_model"]["lite"] == {"calls": 2, "failed_calls": 0, "prompt_tokens": 150, "completion_tokens": 25}
    assert summary["by_model"]["flash"] == {"calls": 1, "failed_calls": 1, "prompt_tokens": 0, "completion_tokens": 0}
    assert summary["by_operation"] == {"ocr": 2, "figure": 1}
