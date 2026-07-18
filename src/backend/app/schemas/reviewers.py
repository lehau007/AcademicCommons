from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, model_validator


class ReviewerAssignmentRead(BaseModel):
    id: UUID
    course_id: UUID
    user_id: UUID
    reviewer_email: str | None = None
    is_active: bool
    assigned_at: datetime
    unassigned_at: datetime | None

    model_config = {"from_attributes": True}

    @model_validator(mode="before")
    @classmethod
    def extract_reviewer_email(cls, data: Any) -> Any:
        # When constructing from an ORM object, pull email off the loaded relationship.
        if hasattr(data, "reviewer") and data.reviewer is not None:
            # Return a dict so we can inject reviewer_email without modifying the ORM model.
            return {
                "id": data.id,
                "course_id": data.course_id,
                "user_id": data.user_id,
                "reviewer_email": data.reviewer.email,
                "is_active": data.is_active,
                "assigned_at": data.assigned_at,
                "unassigned_at": data.unassigned_at,
            }
        return data


class ReviewerAssignmentCreate(BaseModel):
    user_id: UUID
