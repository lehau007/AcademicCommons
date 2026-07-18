from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel


class VoteRequest(BaseModel):
    vote: str | None  # "up", "down", or null to retract


class VoteSummaryResponse(BaseModel):
    document_id: UUID
    up_count: int
    down_count: int
    my_vote: str | None


class LeaderboardEntry(BaseModel):
    user_id: UUID
    full_name: str | None
    email: str
    points: float
    rank: int

    model_config = {"from_attributes": True}


class ContributionScoreResponse(BaseModel):
    user_id: UUID
    courses: list[dict[str, Any]]  # [{course_id, course_code, points, rank}]
    global_rank: int | None
    total_points: float
