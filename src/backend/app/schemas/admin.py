from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel


class FailedDocumentEntry(BaseModel):
    document_id: UUID
    original_filename: str
    failure_reason: str | None
    raw_failure_output: dict[str, Any] | None = None
    attempt_count: int
    failed_at: datetime | None  # completed_at of job
    job_type: str  # "ocr" | "index" | "eval"


class ReprocessRequest(BaseModel):
    from_state: str  # "PARSING" or "EVALUATING"


class AuditLogEntry(BaseModel):
    id: UUID
    actor_id: UUID
    action_type: str
    target_entity_type: str
    target_entity_id: UUID | None
    from_state: str | None
    to_state: str | None
    reason: str | None
    logged_at: datetime

    model_config = {"from_attributes": True}


class AuditLogPage(BaseModel):
    items: list[AuditLogEntry]
    total: int


class SeedStatusResponse(BaseModel):
    course_code: str
    has_seed: bool  # topic_summary is not None and not empty
    approved_doc_count: int
    is_cold_start: bool  # approved_doc_count < 3
