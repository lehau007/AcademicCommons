from __future__ import annotations

from datetime import datetime
from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user, require_role
from app.db.session import get_session
from app.models import Course, CourseSummaryCache, User
from app.models.enums import DocumentStatus, DocumentTier
from app.schemas.courses import (
    CourseCreate,
    CourseRead,
    CourseSeedUpdate,
    CourseUpdate,
    TopicTagsRead,
)
from app.schemas.documents import DocumentListRead, DocumentRead
from app.services.course_service import (
    create_course,
    get_course_by_code,
    list_courses,
    regen_topic_tags,
    set_course_sla,
    update_course,
    update_course_seed,
)
from app.services.document_service import get_document_list

router = APIRouter(prefix="/courses", tags=["courses"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]
AdminDep = Annotated[User, Depends(require_role("admin"))]


class SlaUpdate(BaseModel):
    sla_hours: int = Field(ge=24, le=72)


async def get_course_or_404(code: str, session: SessionDep) -> Course:
    course = await get_course_by_code(session, code)
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course


@router.get("", response_model=list[CourseRead])
async def list_courses_endpoint(
    session: SessionDep,
    _: CurrentUserDep,
    is_active: bool | None = True,
) -> list[CourseRead]:
    courses = await list_courses(session, is_active=is_active)
    return [CourseRead.model_validate(c) for c in courses]


@router.get("/{course_code}", response_model=CourseRead)
async def get_course_endpoint(
    course_code: str,
    session: SessionDep,
    _: CurrentUserDep,
) -> CourseRead:
    course = await get_course_or_404(course_code, session)
    return CourseRead.model_validate(course)


@router.post("", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
async def create_course_endpoint(
    payload: CourseCreate,
    session: SessionDep,
    _: AdminDep,
) -> CourseRead:
    course = await create_course(session, payload)
    return CourseRead.model_validate(course)


@router.put("/{course_code}", response_model=CourseRead)
async def update_course_endpoint(
    course_code: str,
    payload: CourseUpdate,
    session: SessionDep,
    _: AdminDep,
) -> CourseRead:
    course = await get_course_or_404(course_code, session)
    course = await update_course(session, course, payload)
    return CourseRead.model_validate(course)


@router.put("/{course_code}/seed", response_model=CourseRead)
async def update_course_seed_endpoint(
    course_code: str,
    payload: CourseSeedUpdate,
    session: SessionDep,
    _: AdminDep,
) -> CourseRead:
    course = await get_course_or_404(course_code, session)
    course = await update_course_seed(session, course, payload)
    return CourseRead.model_validate(course)


@router.put("/{course_code}/sla", response_model=CourseRead)
async def set_sla_endpoint(
    course_code: str,
    payload: SlaUpdate,
    session: SessionDep,
    _: AdminDep,
) -> CourseRead:
    course = await get_course_or_404(course_code, session)
    course = await set_course_sla(session, course, payload.sla_hours)
    return CourseRead.model_validate(course)


@router.get("/{course_code}/documents", response_model=DocumentListRead)
async def list_course_documents(
    course_code: str,
    session: SessionDep,
    user: CurrentUserDep,
    tier: DocumentTier | None = None,
    status_filter: DocumentStatus | None = None,
    sort: str = "recent",
    subtype: str | None = None,
    topic_tag: str | None = None,
) -> DocumentListRead:
    docs = await get_document_list(
        session, course_code, tier, status_filter, sort, user, subtype=subtype, topic_tag=topic_tag
    )
    return DocumentListRead(items=[DocumentRead.model_validate(d) for d in docs], total=len(docs))


@router.post("/{course_code}/topic-tags/regenerate", response_model=TopicTagsRead)
async def regenerate_topic_tags_endpoint(
    course_code: str,
    session: SessionDep,
    _: AdminDep,
) -> TopicTagsRead:
    course = await get_course_or_404(course_code, session)
    tags = await regen_topic_tags(session, course)
    return TopicTagsRead(tags=tags)


class CourseSummaryRead(BaseModel):
    course_id: UUID
    summary_markdown: str
    citations: list[dict[str, Any]]
    generated_at: datetime

    model_config = {"from_attributes": True}


@router.get("/{course_id}/summary", response_model=CourseSummaryRead)
async def get_course_summary_endpoint(
    course_id: UUID,
    session: SessionDep,
    _: CurrentUserDep,
) -> CourseSummaryRead:
    summary_cache = await session.scalar(
        select(CourseSummaryCache).where(CourseSummaryCache.course_id == course_id)
    )
    if summary_cache is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course summary cache not found for this course",
        )
    return CourseSummaryRead.model_validate(summary_cache)
