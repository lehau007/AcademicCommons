from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CourseRead(BaseModel):
    id: UUID
    code: str
    name: str
    description: str | None
    topic_summary: str | None
    short_description: str | None
    topic_tags: list[str]
    review_sla_hours: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CourseCreate(BaseModel):
    code: str = Field(max_length=20)
    name: str
    description: str | None = None
    topic_summary: str | None = None
    short_description: str | None = None
    review_sla_hours: int = Field(default=48, ge=24, le=72)


class CourseUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    topic_summary: str | None = None
    short_description: str | None = None
    review_sla_hours: int | None = Field(default=None, ge=24, le=72)


class CourseSeedUpdate(BaseModel):
    topic_summary: str
    short_description: str | None = None


class TopicTagsRead(BaseModel):
    tags: list[str]
