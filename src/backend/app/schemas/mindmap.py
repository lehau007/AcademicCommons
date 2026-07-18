from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class MindmapGenerateResponse(BaseModel):
    course_code: str
    is_cached: bool
    concept_graph: dict[str, list[dict[str, str]]]
    generated_at: datetime


__all__ = ["MindmapGenerateResponse"]
