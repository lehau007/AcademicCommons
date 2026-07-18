from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import require_role
from app.db.session import get_session
from app.models import User
from app.schemas.reviewers import ReviewerAssignmentCreate, ReviewerAssignmentRead
from app.services.course_service import get_course_by_code
from app.services.reviewer_service import (
    assign_reviewer,
    list_active_assignments,
    unassign_reviewer,
)

router = APIRouter(prefix="/courses", tags=["reviewers"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]
AdminDep = Annotated[User, Depends(require_role("admin"))]


async def _resolve_course_id(course_code: str, session: SessionDep) -> UUID:
    course = await get_course_by_code(session, course_code)
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course.id


@router.get("/{course_code}/reviewers", response_model=list[ReviewerAssignmentRead])
async def list_reviewers(
    course_code: str,
    session: SessionDep,
    _: AdminDep,
) -> list[ReviewerAssignmentRead]:
    course_id = await _resolve_course_id(course_code, session)
    assignments = await list_active_assignments(session, course_id)
    return [ReviewerAssignmentRead.model_validate(a) for a in assignments]


@router.post(
    "/{course_code}/reviewers",
    response_model=ReviewerAssignmentRead,
    status_code=status.HTTP_201_CREATED,
)
async def assign_reviewer_endpoint(
    course_code: str,
    payload: ReviewerAssignmentCreate,
    session: SessionDep,
    admin: AdminDep,
) -> ReviewerAssignmentRead:
    course_id = await _resolve_course_id(course_code, session)
    assignment = await assign_reviewer(session, course_id, payload.user_id, admin.id)
    return ReviewerAssignmentRead.model_validate(assignment)


@router.delete("/{course_code}/reviewers/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unassign_reviewer_endpoint(
    course_code: str,
    user_id: UUID,
    session: SessionDep,
    _: AdminDep,
) -> None:
    course_id = await _resolve_course_id(course_code, session)
    await unassign_reviewer(session, course_id, user_id)
