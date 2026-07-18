from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.enums import ContributionType, MaterialType


class DocumentUploadOfficialRequest(BaseModel):
    course_code: str
    material_type: MaterialType


class DocumentUploadCommunityRequest(BaseModel):
    course_code: str
    contribution_type: ContributionType
    topic_tags: list[str] = Field(default_factory=list)


class DocumentDeleteRequest(BaseModel):
    reason: str = Field(min_length=3, max_length=1000)


class DocumentUploadResponse(BaseModel):
    document_id: UUID
    status: str
    sla_deadline: datetime | None


class DocumentRead(BaseModel):
    id: UUID
    course_id: UUID
    uploader_id: UUID
    document_tier: str
    material_type: str | None
    contribution_type: str | None
    topic_tags: list[str]
    status: str
    version: int
    is_active_version: bool
    original_filename: str
    display_name: str | None = None
    file_format: str
    storage_raw_path: str | None
    storage_md_path: str | None
    no_reviewer_flag: bool
    sla_breached: bool
    permanently_failed: bool
    sla_deadline: datetime | None
    uploaded_at: datetime
    updated_at: datetime
    review_reason: str | None = None
    course_code: str | None = None
    reviewer_note: str | None = None
    # Actionable suggestion for FAILED documents (student listing)
    failure_hint: str | None = None
    # Populated only by the management listing (from the latest evaluation report)
    ai_recommendation: str | None = None
    ai_overall_score: float | None = None  # 0-100

    model_config = {"from_attributes": True}


class DocumentListRead(BaseModel):
    items: list[DocumentRead]
    total: int


class SignedUrlResponse(BaseModel):
    url: str
    expires_in_seconds: int = 900
