"""Structured JSON logging for the application."""

import json
import logging
import os
from datetime import UTC, datetime
from logging.handlers import RotatingFileHandler


class JsonFormatter(logging.Formatter):
    """Formats log records as single-line JSON objects."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, object] = {
            "timestamp": datetime.fromtimestamp(record.created, tz=UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        if record.stack_info:
            payload["stack_info"] = self.formatStack(record.stack_info)
        return json.dumps(payload, ensure_ascii=False)


def configure_logging(
    level: str = "INFO",
    *,
    error_log_file: str | None = None,
    error_log_max_bytes: int = 5_000_000,
    error_log_backup_count: int = 3,
) -> None:
    """Install the JSON formatter on the root logger.

    When ``error_log_file`` is set, also attach a rotating ERROR-level file
    handler so failures are captured to disk (no need to exec into the
    container). Pass ``None`` (e.g. in production) to keep stdout-only and avoid
    filling the disk. Rotation bounds the file size even when enabled.
    """
    formatter = JsonFormatter()
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    root = logging.getLogger()
    # Remove any existing handlers to avoid duplicate output.
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(getattr(logging, level.upper(), logging.INFO))

    if error_log_file:
        # A logging misconfiguration (unwritable path, read-only FS) must never
        # crash startup — fall back to stdout-only and record why.
        try:
            directory = os.path.dirname(error_log_file)
            if directory:
                os.makedirs(directory, exist_ok=True)
            file_handler = RotatingFileHandler(
                error_log_file,
                maxBytes=error_log_max_bytes,
                backupCount=error_log_backup_count,
                encoding="utf-8",
            )
            file_handler.setLevel(logging.ERROR)
            file_handler.setFormatter(formatter)
            root.addHandler(file_handler)
        except OSError as exc:
            root.warning("error log file disabled (%s): %s", error_log_file, exc)

    # Quieten noisy third-party loggers.
    logging.getLogger("uvicorn.access").propagate = False
    logging.getLogger("uvicorn.error").propagate = True
