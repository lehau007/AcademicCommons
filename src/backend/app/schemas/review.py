from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class ReviewQueueItem(BaseModel):
    document_id: UUID
    filename: str
    course_code: str
    document_tier: str
    status: str
    sla_deadline: datetime | None
    sla_breached: bool
    no_reviewer_flag: bool
    uploaded_at: datetime

    model_config = {"from_attributes": True}


class ReviewDetailResponse(BaseModel):
    document_id: UUID
    course_code: str
    document_tier: str
    status: str
    evaluation_report: dict[str, Any] | None  # raw JSONB from EvaluationReport
    state_logs: list[dict[str, Any]]

    model_config = {"from_attributes": True}


class ReviewDecideRequest(BaseModel):
    decision: str  # APPROVE|REJECT|OVERRIDE_APPROVE|OVERRIDE_REJECT
    final_contribution_type: str | None = None  # ContributionType value
    note: str | None = None


class ReviewDecisionRead(BaseModel):
    id: UUID
    document_id: UUID
    decision: str
    final_contribution_type: str | None
    note: str | None
    decided_at: datetime

    model_config = {"from_attributes": True}


class BatchApproveRequest(BaseModel):
    document_ids: list[UUID] = Field(min_length=1)
    note: str | None = None


class BatchApproveResponse(BaseModel):
    approved: list[UUID]
    count: int


class ReviewAnalyticsResponse(BaseModel):
    average_sla_hours_per_course: dict[str, float]
    sla_threshold_hours_per_course: dict[str, float] = Field(default_factory=dict)
    ai_agreement_rate: float
    ai_override_rate: float
