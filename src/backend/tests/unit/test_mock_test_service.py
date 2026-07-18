from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.models.enums import QuestionType
from app.schemas.mock_test import DifficultyDistribution
from app.services.mock_test_service import (
    _parse_plan,
    _parse_questions,
    _safe_question_type,
    generate_mock_test,
    get_mock_test_by_run_id,
    get_recent_mock_test,
)


def test_safe_question_type_always_forces_multiple_choice() -> None:
    assert _safe_question_type("short_answer") == QuestionType.MULTIPLE_CHOICE
    assert _safe_question_type("true_false") == QuestionType.MULTIPLE_CHOICE
    assert _safe_question_type("mcq") == QuestionType.MULTIPLE_CHOICE
    assert _safe_question_type("random_text") == QuestionType.MULTIPLE_CHOICE


def test_parse_plan_valid() -> None:
    text = (
        'Some prefix text {"plan": [{"topic": "sorting", "question_count": 3, '
        '"difficulty": "medium", "question_types": ["mcq"]}]} suffix'
    )
    plan = _parse_plan(text)
    assert len(plan) == 1
    assert plan[0]["topic"] == "sorting"
    assert plan[0]["question_count"] == 3


def test_parse_plan_invalid() -> None:
    text = 'invalid json'
    plan = _parse_plan(text)
    assert plan == []


def test_parse_questions_valid() -> None:
    text = '[{"question_text": "What is bubble sort?", "question_type": "mcq"}]'
    questions = _parse_questions(text)
    assert len(questions) == 1
    assert questions[0]["question_text"] == "What is bubble sort?"


def test_parse_questions_object_form() -> None:
    text = '{"questions": [{"question_text": "What is a hash table?", "question_type": "mcq"}]}'
    questions = _parse_questions(text)
    assert len(questions) == 1
    assert questions[0]["question_text"] == "What is a hash table?"


@pytest.mark.asyncio
async def test_generate_plan_uses_structured_output_and_total_constraint() -> None:
    from app.services.mock_test_service import _generate_plan

    mock_router = AsyncMock()
    mock_router.chat = AsyncMock(return_value=MagicMock(content='{"plan": []}'))

    await _generate_plan(["Hashing"], 5, DifficultyDistribution(easy=1, medium=3, hard=1), mock_router)

    kwargs = mock_router.chat.call_args.kwargs
    assert kwargs["schema"] is not None
    user_msg = mock_router.chat.call_args.args[0][1]["content"]
    assert "exactly 5" in user_msg


@pytest.mark.asyncio
async def test_question_missing_chunk_ids_yields_empty_citations() -> None:
    from app.services.mock_test_service import _generate_questions_for_topic

    cid = uuid4()
    mock_router = AsyncMock()
    mock_router.chat = AsyncMock(
        return_value=MagicMock(
            content='{"questions": [{"question_text": "Q?", "question_type": "mcq", "used_chunk_ids": []}]}'
        )
    )

    raw = await _generate_questions_for_topic(
        topic="t",
        count=1,
        difficulty="medium",
        question_types=["mcq"],
        context="ctx",
        valid_chunk_ids={cid},
        chunk_content_map={cid: "content"},
        llm_router=mock_router,
    )

    assert raw[0]["used_chunk_ids"] == []
    assert mock_router.chat.call_args.kwargs["schema"] is not None


@pytest.mark.asyncio
async def test_generate_mock_test_forces_mcq() -> None:
    mock_course = MagicMock()
    mock_course.id = uuid4()
    mock_course.code = "IT3160E"
    mock_course.topic_summary = "Algorithm design and analysis"

    mock_session = AsyncMock()
    mock_session.add = MagicMock()
    mock_session.scalar = AsyncMock(return_value=mock_course)
    
    async def mock_refresh_fn(item):
        if not getattr(item, "id", None):
            item.id = uuid4()
    mock_session.refresh = mock_refresh_fn
    
    # Mocking topics collect
    mock_execute_result = MagicMock()
    mock_execute_result.__iter__ = MagicMock(return_value=iter([]))
    mock_session.execute = AsyncMock(return_value=mock_execute_result)

    mock_llm_res_plan = MagicMock()
    mock_llm_res_plan.content = (
        '{"plan": [{"topic": "Hashing", "question_count": 2, '
        '"difficulty": "medium", "question_types": ["mcq"]}]}'
    )
    
    mock_llm_res_question = MagicMock()
    mock_llm_res_question.content = (
        '[{"question_text": "Sample MCQ?", "question_type": "mcq", "difficulty": "medium", '
        '"topic": "Hashing", "options": [{"key": "A", "text": "Yes"}], "correct_answer": "A", '
        '"explanation": "Correct option is A", "used_chunk_ids": []}]'
    )

    mock_router = AsyncMock()
    # First call is for plan, second call is for question generation
    mock_router.chat = AsyncMock(side_effect=[mock_llm_res_plan, mock_llm_res_question])

    mock_retrieval = AsyncMock()
    mock_retrieval.search = AsyncMock(return_value=[MagicMock(id=uuid4(), content="hashed tables content")])

    dist = DifficultyDistribution(easy=0, medium=2, hard=0)
    result = await generate_mock_test(
        session=mock_session,
        course_code="IT3160E",
        total_questions=2,
        difficulty_distribution=dist,
        llm_router=mock_router,
        retrieval_service=mock_retrieval,
    )

    assert result.course_code == "IT3160E"
    assert result.total_questions == 1
    assert result.questions[0].question_type == QuestionType.MULTIPLE_CHOICE.value


@pytest.mark.asyncio
async def test_unknown_course_raises_value_error() -> None:
    # Non-existent course must surface as a ValueError (→ 404 at the API layer),
    # matching the Mindmap API, not a 200 with an empty list.
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=None)
    dist = DifficultyDistribution(easy=0, medium=1, hard=0)

    with pytest.raises(ValueError, match="not found"):
        await generate_mock_test(
            session=session,
            course_code="NOPE",
            total_questions=1,
            difficulty_distribution=dist,
            llm_router=AsyncMock(),
            retrieval_service=AsyncMock(),
        )
    with pytest.raises(ValueError, match="not found"):
        await get_recent_mock_test(session=session, course_code="NOPE")
    with pytest.raises(ValueError, match="not found"):
        await get_mock_test_by_run_id(session=session, course_code="NOPE", test_run_id=uuid4())
