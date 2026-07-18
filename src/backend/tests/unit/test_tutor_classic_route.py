from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

import app.api.v1.tutor as tutor_route
from app.schemas.tutor import TutorQueryRequest, TutorQueryResponse


async def test_query_classic_calls_single_shot_tutor_query(monkeypatch) -> None:
    fake = TutorQueryResponse(answer="single-shot answer", citations=[])
    mock_tutor_query = AsyncMock(return_value=fake)
    monkeypatch.setattr(tutor_route, "tutor_query", mock_tutor_query)
    monkeypatch.setattr(tutor_route, "build_llm_router", lambda s: MagicMock())
    monkeypatch.setattr(tutor_route, "get_retrieval_service", lambda s: MagicMock())

    req = TutorQueryRequest(course_code="IT3160E", question="What is A* search?")
    session = MagicMock()
    session.commit = AsyncMock()
    user = MagicMock()

    resp = await tutor_route.query_tutor_classic(req, session, user)

    assert resp.answer == "single-shot answer"
    kwargs = mock_tutor_query.await_args.kwargs
    assert kwargs["course_code"] == "IT3160E"
    assert kwargs["question"] == "What is A* search?"
    assert kwargs["include_exercise"] is False
