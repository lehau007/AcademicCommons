from __future__ import annotations

from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from app.llm.providers import ProviderResult
from app.models import Course
from app.services.course_service import regen_topic_tags, set_course_sla


def make_course(topic_summary: str | None = None) -> Course:
    course = Course(
        id=uuid4(),
        code="IT3040",
        name="Test Course",
        topic_summary=topic_summary,
        topic_tags=[],
        review_sla_hours=48,
    )
    return course


def make_provider_result(content: str) -> ProviderResult:
    return ProviderResult(
        content=content,
        tokens_in=10,
        tokens_out=10,
        latency_ms=100,
        cost_usd=0.0,
        provider="mock",
        model="mock-model",
    )


@pytest.mark.asyncio
async def test_regen_topic_tags_returns_empty_when_no_summary() -> None:
    session = AsyncMock()
    course = make_course(topic_summary=None)

    tags = await regen_topic_tags(session, course)

    assert tags == []
    # LLM must not be called when there is no summary.
    session.commit.assert_not_called()


@pytest.mark.asyncio
async def test_regen_topic_tags_calls_llm_and_saves_tags() -> None:
    session = AsyncMock()
    course = make_course(topic_summary="Introduction to algorithms and data structures")

    expected_tags = ["algorithms", "data structures", "sorting", "graphs", "complexity"]
    mock_result = make_provider_result('["algorithms", "data structures", "sorting", "graphs", "complexity"]')

    mock_llm = AsyncMock()
    mock_llm.chat = AsyncMock(return_value=mock_result)

    with patch("app.services.course_service._get_llm", return_value=mock_llm):
        tags = await regen_topic_tags(session, course)

    assert tags == expected_tags
    assert course.topic_tags == expected_tags
    session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_regen_topic_tags_returns_existing_on_llm_failure() -> None:
    session = AsyncMock()
    existing_tags = ["oop", "design patterns"]
    course = make_course(topic_summary="Object-oriented design")
    course.topic_tags = existing_tags

    mock_llm = AsyncMock()
    mock_llm.chat = AsyncMock(side_effect=RuntimeError("LLM unavailable"))

    with patch("app.services.course_service._get_llm", return_value=mock_llm):
        tags = await regen_topic_tags(session, course)

    assert tags == existing_tags
    # Commit must not be called when LLM fails.
    session.commit.assert_not_called()


@pytest.mark.asyncio
async def test_set_course_sla_updates_and_commits() -> None:
    session = AsyncMock()
    course = make_course()
    course.review_sla_hours = 48

    await set_course_sla(session, course, 72)

    assert course.review_sla_hours == 72
    session.commit.assert_called_once()
    session.refresh.assert_called_once_with(course)
