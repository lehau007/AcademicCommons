from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CommunityVote, ContributionScore, Course, Document, User
from app.models.enums import DocumentStatus


async def cast_vote(session: AsyncSession, document_id: UUID, vote: str | None, user: User) -> CommunityVote:
    """UPSERT vote. vote must be 'up', 'down', or None (retract)."""
    if vote is not None and vote not in ("up", "down"):
        raise HTTPException(status_code=422, detail="vote must be 'up', 'down', or null")

    doc = await session.scalar(select(Document).where(Document.id == document_id))
    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found")
    if doc.status != DocumentStatus.INDEXED:
        raise HTTPException(status_code=409, detail="Can only vote on INDEXED documents")

    existing = await session.scalar(
        select(CommunityVote).where(
            CommunityVote.user_id == user.id,
            CommunityVote.document_id == document_id,
        )
    )
    if existing is None:
        cv = CommunityVote(user_id=user.id, document_id=document_id, vote=vote)
        session.add(cv)
    else:
        existing.vote = vote
        from datetime import UTC, datetime
        existing.voted_at = datetime.now(UTC)
        cv = existing

    await session.commit()
    await session.refresh(cv)
    return cv


async def get_vote_summary(session: AsyncSession, document_id: UUID, user: User) -> dict[str, Any]:
    """Aggregate up/down counts for a document plus the current user's own vote."""
    doc = await session.scalar(select(Document).where(Document.id == document_id))
    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found")

    up_count = await session.scalar(
        select(func.count()).select_from(CommunityVote).where(
            CommunityVote.document_id == document_id,
            CommunityVote.vote == "up",
        )
    )
    down_count = await session.scalar(
        select(func.count()).select_from(CommunityVote).where(
            CommunityVote.document_id == document_id,
            CommunityVote.vote == "down",
        )
    )
    my_vote = await session.scalar(
        select(CommunityVote.vote).where(
            CommunityVote.user_id == user.id,
            CommunityVote.document_id == document_id,
        )
    )
    return {
        "document_id": document_id,
        "up_count": up_count or 0,
        "down_count": down_count or 0,
        "my_vote": my_vote,
    }


async def get_course_leaderboard(session: AsyncSession, course_code: str, limit: int = 20) -> list[dict[str, Any]]:
    """Get top contributors for a course."""
    course = await session.scalar(select(Course).where(Course.code == course_code))
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    scores = await session.scalars(
        select(ContributionScore)
        .where(ContributionScore.course_id == course.id)
        .order_by(ContributionScore.points.desc())
        .limit(limit)
    )
    results = []
    for i, score in enumerate(scores.all(), 1):
        user = await session.scalar(select(User).where(User.id == score.user_id))
        if user:
            results.append({
                "user_id": str(score.user_id),
                "full_name": user.full_name,
                "email": user.email,
                "points": score.points,
                "rank": i,
            })
    return results


async def get_global_leaderboard(session: AsyncSession, limit: int = 20) -> list[dict[str, Any]]:
    """Get top contributors globally."""
    stmt = (
        select(ContributionScore.user_id, func.sum(ContributionScore.points).label("total_points"))
        .group_by(ContributionScore.user_id)
        .order_by(func.sum(ContributionScore.points).desc())
        .limit(limit)
    )
    rows = (await session.execute(stmt)).all()
    results = []
    for i, row in enumerate(rows, 1):
        user = await session.scalar(select(User).where(User.id == row.user_id))
        if user:
            results.append({
                "user_id": str(row.user_id),
                "full_name": user.full_name,
                "email": user.email,
                "points": float(row.total_points),
                "rank": i,
            })
    return results


async def get_my_contribution_score(session: AsyncSession, user: User) -> dict[str, Any]:
    """Get the current user's scores per course and global rank."""
    scores = await session.scalars(
        select(ContributionScore).where(ContributionScore.user_id == user.id)
    )
    course_scores = []
    total = 0.0
    for score in scores.all():
        course = await session.scalar(select(Course).where(Course.id == score.course_id))
        if course:
            # Compute rank dynamically: count users with more points in this course
            rank_ahead = await session.scalar(
                select(func.count()).select_from(ContributionScore).where(
                    ContributionScore.course_id == score.course_id,
                    ContributionScore.points > score.points,
                )
            )
            course_rank = (rank_ahead or 0) + 1
            course_scores.append({
                "course_id": str(score.course_id),
                "course_code": course.code,
                "points": score.points,
                "rank": course_rank,
            })
            total += score.points

    stmt = (
        select(ContributionScore.user_id, func.sum(ContributionScore.points).label("total"))
        .group_by(ContributionScore.user_id)
        .order_by(func.sum(ContributionScore.points).desc())
    )
    rows = (await session.execute(stmt)).all()
    global_rank = None
    for i, row in enumerate(rows, 1):
        if row.user_id == user.id:
            global_rank = i
            break

    return {
        "user_id": str(user.id),
        "courses": course_scores,
        "global_rank": global_rank,
        "total_points": total,
    }


async def award_contribution_points(
    session: AsyncSession,
    user_id: UUID,
    course_id: UUID,
    contribution_type: str,
    relevance_score: float,
) -> None:
    """Award points when document becomes INDEXED."""
    base_points = {
        "summary_note": 10.0,
        "review_note": 8.0,
        "past_exam": 7.0,
        "solved_exercise": 7.0,
    }
    base = base_points.get(contribution_type, 5.0)
    points = base * (relevance_score / 10.0)

    existing = await session.scalar(
        select(ContributionScore).where(
            ContributionScore.user_id == user_id,
            ContributionScore.course_id == course_id,
        )
    )
    if existing is None:
        cs = ContributionScore(user_id=user_id, course_id=course_id, points=points)
        session.add(cs)
    else:
        existing.points += points
        from datetime import UTC, datetime
        existing.last_updated = datetime.now(UTC)
    await session.flush()
