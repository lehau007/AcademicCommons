from __future__ import annotations

from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user, require_role
from app.db.session import get_session
from app.models import User
from app.schemas.vote import ContributionScoreResponse, VoteRequest, VoteSummaryResponse
from app.services import vote_service

router = APIRouter(tags=["voting"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]
StudentOnlyDep = Annotated[User, Depends(require_role("student"))]


@router.post("/documents/{document_id}/vote", response_model=VoteSummaryResponse)
async def cast_vote(
    document_id: UUID,
    payload: VoteRequest,
    session: SessionDep,
    user: StudentOnlyDep,
) -> VoteSummaryResponse:
    """Cast or retract a vote on an INDEXED document. Students only."""
    await vote_service.cast_vote(session, document_id, payload.vote, user)
    summary = await vote_service.get_vote_summary(session, document_id, user)
    return VoteSummaryResponse(**summary)


@router.get("/documents/{document_id}/vote", response_model=VoteSummaryResponse)
async def get_vote(
    document_id: UUID,
    session: SessionDep,
    user: CurrentUserDep,
) -> VoteSummaryResponse:
    """Get vote tallies for a document plus the requesting user's own vote."""
    summary = await vote_service.get_vote_summary(session, document_id, user)
    return VoteSummaryResponse(**summary)


@router.get("/leaderboard/course/{course_code}", response_model=list[dict[str, Any]])
async def get_course_leaderboard(
    course_code: str,
    session: SessionDep,
    _: CurrentUserDep,
    limit: int = Query(default=20, ge=1, le=100),
) -> list[dict[str, Any]]:
    """Get top contributors for a specific course."""
    return await vote_service.get_course_leaderboard(session, course_code, limit=limit)


@router.get("/leaderboard/global", response_model=list[dict[str, Any]])
async def get_global_leaderboard(
    session: SessionDep,
    _: CurrentUserDep,
    limit: int = Query(default=20, ge=1, le=100),
) -> list[dict[str, Any]]:
    """Get top contributors globally."""
    return await vote_service.get_global_leaderboard(session, limit=limit)


@router.get("/users/me/contribution-score", response_model=ContributionScoreResponse)
async def get_my_contribution_score(
    session: SessionDep,
    user: CurrentUserDep,
) -> ContributionScoreResponse:
    """Get the current user's contribution scores and rankings."""
    data = await vote_service.get_my_contribution_score(session, user)
    return ContributionScoreResponse(**data)
