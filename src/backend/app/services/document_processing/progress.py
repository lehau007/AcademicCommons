"""Instance-based progress emitter.

Replaces the experiment's module-level ``_progress_callback`` / ``_progress_records`` /
``_emit_progress`` globals. Wraps an optional callback (e.g. the OCR worker trace) and
records every event so the pipeline can return them in its result.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any


class ProgressEmitter:
    def __init__(self, callback: Callable[[dict[str, Any]], None] | None = None) -> None:
        self._callback = callback
        self._records: list[dict[str, Any]] = []

    def emit(self, event: str, **fields: Any) -> None:
        payload = {"timestamp": datetime.now(UTC).isoformat(), "event": event, **fields}
        self._records.append(payload)
        if self._callback is None:
            return
        try:
            self._callback(payload)
        except Exception:
            # Progress reporting must never break the pipeline.
            pass

    @property
    def records(self) -> list[dict[str, Any]]:
        return list(self._records)
