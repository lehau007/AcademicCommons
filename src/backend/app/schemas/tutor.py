from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel


class TutorQueryRequest(BaseModel):
    course_code: str
    question: str
    include_exercise: bool = False
    session_id: UUID | None = None
    document_ids: list[UUID] | None = None


class CitationResponse(BaseModel):
    chunk_id: UUID
    document_title: str | None
    document_tier: str
    document_subtype: str | None
    section_title: str | None
    page_number: int | None
    chunk_order: int | None
    excerpt: str


class TutorQueryResponse(BaseModel):
    answer: str
    citations: list[CitationResponse]
    session_id: UUID | None = None


class TutorSummarizeRequest(BaseModel):
    course_code: str


class TutorSummarizeResponse(BaseModel):
    course_id: UUID
    summary_markdown: str
    citations: list[dict[str, Any]]

    model_config = {"from_attributes": True}


class DocumentSummaryResponse(BaseModel):
    document_id: UUID
    topic: str | None
    concepts: list[str]
    overall_summary: str | None
    ocr_quality: str | None
    language: str | None

    model_config = {"from_attributes": True}


from datetime import datetime
from app.models.enums import ChatRole


class ChatMessageRead(BaseModel):
    id: UUID
    session_id: UUID
    role: ChatRole
    content: str
    citations: list[dict[str, Any]]
    created_at: datetime

    model_config = {"from_attributes": True}


class ChatSessionRead(BaseModel):
    id: UUID
    user_id: UUID
    course_id: UUID
    course_code: str | None = None
    summary: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


__all__ = [
    "CitationResponse",
    "TutorQueryRequest",
    "TutorQueryResponse",
    "TutorSummarizeRequest",
    "TutorSummarizeResponse",
    "DocumentSummaryResponse",
    "ChatMessageRead",
    "ChatSessionRead",
]
