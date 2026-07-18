from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Course, CourseReviewerAssignment, User


async def list_active_assignments(
    session: AsyncSession, course_id: UUID
) -> list[CourseReviewerAssignment]:
    result = await session.scalars(
        select(CourseReviewerAssignment)
        .where(
            CourseReviewerAssignment.course_id == course_id,
            CourseReviewerAssignment.is_active.is_(True),
        )
        .options(selectinload(CourseReviewerAssignment.reviewer))
    )
    return list(result.all())


async def assign_reviewer(
    session: AsyncSession, course_id: UUID, user_id: UUID, assigned_by: UUID
) -> CourseReviewerAssignment:
    user = await session.scalar(select(User).where(User.id == user_id))
    if user is None or user.role != "reviewer":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not exist or is not a reviewer",
        )

    course = await session.scalar(select(Course).where(Course.id == course_id))
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    existing = await session.scalar(
        select(CourseReviewerAssignment).where(
            CourseReviewerAssignment.course_id == course_id,
            CourseReviewerAssignment.user_id == user_id,
            CourseReviewerAssignment.is_active.is_(True),
        )
    )
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Reviewer is already assigned to this course",
        )

    assignment = CourseReviewerAssignment(
        course_id=course_id,
        user_id=user_id,
        assigned_by=assigned_by,
        is_active=True,
        assigned_at=datetime.now(UTC),
    )
    session.add(assignment)
    await session.commit()
    await session.refresh(assignment)

    # Load reviewer relationship for schema serialization.
    await session.refresh(assignment, ["reviewer"])
    return assignment


async def unassign_reviewer(session: AsyncSession, course_id: UUID, user_id: UUID) -> None:
    assignment = await session.scalar(
        select(CourseReviewerAssignment).where(
            CourseReviewerAssignment.course_id == course_id,
            CourseReviewerAssignment.user_id == user_id,
            CourseReviewerAssignment.is_active.is_(True),
        )
    )
    if assignment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Active reviewer assignment not found",
        )

    assignment.is_active = False
    assignment.unassigned_at = datetime.now(UTC)
    await session.commit()
