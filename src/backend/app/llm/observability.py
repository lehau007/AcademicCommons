from __future__ import annotations

import logging

_SCALAR_TYPES = (str, int, float, bool)


def _render(value: object) -> str:
    if value is None:
        return "none"
    if isinstance(value, bool):
        return str(value).lower()
    if not isinstance(value, _SCALAR_TYPES):
        return "<redacted>"
    return str(value).replace("\n", "\\n")


def log_event(
    logger: logging.Logger,
    event: str,
    *,
    level: int = logging.INFO,
    **fields: object,
) -> None:
    parts = [f"event={_render(event)}"]
    parts.extend(f"{key}={_render(fields[key])}" for key in sorted(fields))
    logger.log(level, " ".join(parts))
