from __future__ import annotations

import json
import logging
from typing import cast
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.llm.router import LLMRouter, build_llm_router
from app.models import Course
from app.schemas.courses import CourseCreate, CourseSeedUpdate, CourseUpdate

logger = logging.getLogger(__name__)


def _get_llm() -> LLMRouter:
    return build_llm_router(get_settings())


async def list_courses(session: AsyncSession, is_active: bool | None = True) -> list[Course]:
    stmt = select(Course)
    if is_active is not None:
        stmt = stmt.where(Course.is_active.is_(is_active))
    result = await session.scalars(stmt)
    return list(result.all())


async def get_course_by_code(session: AsyncSession, code: str) -> Course | None:
    return cast(Course | None, await session.scalar(select(Course).where(Course.code == code)))


async def get_course_by_id(session: AsyncSession, course_id: UUID) -> Course | None:
    return cast(Course | None, await session.scalar(select(Course).where(Course.id == course_id)))


async def create_course(session: AsyncSession, data: CourseCreate) -> Course:
    course = Course(
        code=data.code,
        name=data.name,
        description=data.description,
        topic_summary=data.topic_summary,
        short_description=data.short_description,
        review_sla_hours=data.review_sla_hours,
    )
    session.add(course)
    await session.commit()
    await session.refresh(course)
    return course


async def update_course(session: AsyncSession, course: Course, data: CourseUpdate) -> Course:
    update_data = data.model_dump(exclude_none=True)
    for field, value in update_data.items():
        setattr(course, field, value)
    await session.commit()
    await session.refresh(course)
    return course


async def update_course_seed(session: AsyncSession, course: Course, data: CourseSeedUpdate) -> Course:
    course.topic_summary = data.topic_summary
    course.short_description = data.short_description
    await session.commit()
    await session.refresh(course)
    await regen_topic_tags(session, course)
    return course


async def regen_topic_tags(session: AsyncSession, course: Course) -> list[str]:
    if not course.topic_summary:
        return []

    try:
        llm = _get_llm()
        result = await llm.chat(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Extract key topic tags from the course summary. "
                        "Return a JSON array of 5-10 short tags."
                    ),
                },
                {"role": "user", "content": course.topic_summary},
            ],
            schema={"type": "array", "items": {"type": "string"}},
            flow="topic_tags",
        )
        parsed = json.loads(result.content) if isinstance(result.content, str) else result.content
        tags = [str(tag) for tag in parsed] if isinstance(parsed, list) else []
    except Exception:
        logger.warning("LLM topic tag generation failed for course %s; keeping existing tags", course.code)
        return list(course.topic_tags)

    course.topic_tags = tags
    await session.commit()
    await session.refresh(course)
    return tags


async def set_course_sla(session: AsyncSession, course: Course, sla_hours: int) -> Course:
    course.review_sla_hours = sla_hours
    await session.commit()
    await session.refresh(course)
    return course
