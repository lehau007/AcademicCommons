from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field


class DifficultyDistribution(BaseModel):
    easy: int = Field(default=3, ge=0)
    medium: int = Field(default=5, ge=0)
    hard: int = Field(default=2, ge=0)


class MockTestGenerateRequest(BaseModel):
    total_questions: int = Field(default=10, ge=1, le=50)
    difficulty_distribution: DifficultyDistribution = Field(default_factory=DifficultyDistribution)


class MockTestCitation(BaseModel):
    chunk_id: UUID
    excerpt: str


class MockTestQuestion(BaseModel):
    id: UUID
    test_run_id: UUID | None
    question_text: str
    question_type: str
    difficulty: str
    topic: str | None
    options: list[dict[str, str]]
    correct_answer: str
    explanation: str | None
    citations: list[MockTestCitation]


class MockTestGenerateResponse(BaseModel):
    course_code: str
    total_questions: int
    test_run_id: UUID | None = None
    questions: list[MockTestQuestion]


__all__ = [
    "DifficultyDistribution",
    "MockTestCitation",
    "MockTestGenerateRequest",
    "MockTestGenerateResponse",
    "MockTestQuestion",
]
