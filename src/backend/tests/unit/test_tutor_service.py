from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.llm.providers import LLMUnavailable
from app.models.enums import DocumentTier
from app.schemas.tutor import TutorQueryRequest
from app.services.retrieval_service import RetrievedChunk
from app.services.tutor_service import (
    _extract_used_chunk_ids,
    _is_non_answer_output,
    _postprocess_answer,
    _strip_json_suffix,
)


def test_is_non_answer_output_bare_arrays() -> None:
    # The exact leaked outputs observed in the ablation (used_doc_ids / namespaces arrays).
    assert _is_non_answer_output('["knowledge"]')
    assert _is_non_answer_output(
        '["789b2a7d-059f-4511-8e1d-84c9e3da61f3", "05b2b027-8faf-4bd7-9663-47f319deeb15"]'
    )


def test_is_non_answer_output_metadata_dict() -> None:
    assert _is_non_answer_output('{"used_doc_ids": ["x"]}')
    assert _is_non_answer_output('```json\n{"used_doc_ids": ["x"]}\n```')


def test_is_non_answer_output_prose_is_a_real_answer() -> None:
    assert not _is_non_answer_output("# Trả lời\nBảng student gồm các cột student_id, ...")
    assert not _is_non_answer_output("The answer is 42.")
    # prose that merely embeds a JSON code block is still a real answer
    assert not _is_non_answer_output('Config:\n```json\n{"a": 1}\n```\nDone.')


def test_postprocess_blanks_bare_array_to_fallback() -> None:
    clean, _ = _postprocess_answer('["knowledge"]', [], {})
    assert "chưa rõ" in clean  # the friendly empty-answer fallback


def _make_chunk(text: str = "test content") -> RetrievedChunk:
    return RetrievedChunk(
        id=uuid4(),
        document_id=uuid4(),
        content=text,
        document_tier=DocumentTier.COMMUNITY,
        subtype=None,
        section_title=None,
        page_number=None,
        chunk_order=1,
        cosine_sim=0.9,
        final_score=0.9,
    )


def test_tutor_query_request_document_ids_defaults_to_none() -> None:
    request = TutorQueryRequest(course_code="IT3160E", question="What is AI?")
    assert request.document_ids is None


def test_tutor_query_request_accepts_document_ids() -> None:
    doc_id = uuid4()
    request = TutorQueryRequest(course_code="IT3160E", question="What is AI?", document_ids=[doc_id])
    assert request.document_ids == [doc_id]


def test_extract_used_chunk_ids_valid() -> None:
    chunk = _make_chunk()
    text = f'Some answer here. {{"used_chunk_ids": ["{chunk.id}"]}}'
    result = _extract_used_chunk_ids(text, {chunk.id})
    assert chunk.id in result


def test_extract_used_chunk_ids_invalid_uuid_filtered() -> None:
    chunk = _make_chunk()
    text = '{"used_chunk_ids": ["not-a-uuid", "also-invalid"]}'
    result = _extract_used_chunk_ids(text, {chunk.id})
    assert chunk.id in result


def test_extract_used_chunk_ids_not_in_valid_set_filtered() -> None:
    chunk = _make_chunk()
    fake_id = uuid4()
    text = f'{{"used_chunk_ids": ["{fake_id}"]}}'
    result = _extract_used_chunk_ids(text, {chunk.id})
    assert fake_id not in result
    assert chunk.id in result


def test_extract_used_chunk_ids_malformed_json_returns_all() -> None:
    chunk = _make_chunk()
    text = 'Some answer with no valid json'
    result = _extract_used_chunk_ids(text, {chunk.id})
    assert chunk.id in result


def test_strip_json_suffix_removes_chunk_ids_json() -> None:
    text = 'Here is the answer. {"used_chunk_ids": ["abc"]}'
    result = _strip_json_suffix(text)
    assert "used_chunk_ids" not in result
    assert "Here is the answer." in result


def test_strip_json_suffix_no_json_unchanged() -> None:
    text = "Just an answer with no JSON."
    result = _strip_json_suffix(text)
    assert result == text


@pytest.mark.asyncio
async def test_tutor_query_no_indexed_docs() -> None:
    from app.config import get_settings
    from app.services.tutor_service import tutor_query

    mock_session = AsyncMock()
    mock_session.scalar = AsyncMock(return_value=MagicMock(id=uuid4(), code="IT3160E", is_active=True))

    mock_retrieval = AsyncMock()
    mock_retrieval.search = AsyncMock(return_value=[])

    mock_router = AsyncMock()

    result = await tutor_query(
        session=mock_session,
        course_code="IT3160E",
        question="What is AI?",
        include_exercise=False,
        llm_router=mock_router,
        retrieval_service=mock_retrieval,
        settings=get_settings(),
    )

    assert "Không có tài liệu" in result.answer
    assert result.citations == []
    mock_router.chat.assert_not_called()


@pytest.mark.asyncio
async def test_tutor_query_llm_unavailable_returns_graceful() -> None:
    from app.config import get_settings
    from app.services.tutor_service import tutor_query

    chunk = _make_chunk("some lecture content about AI")
    mock_session = AsyncMock()
    mock_session.scalar = AsyncMock(return_value=MagicMock(id=uuid4(), code="IT3160E", is_active=True))
    mock_session.execute = AsyncMock(return_value=MagicMock(scalars=MagicMock(return_value=[])))

    mock_retrieval = AsyncMock()
    mock_retrieval.search = AsyncMock(return_value=[chunk])

    mock_router = AsyncMock()
    mock_router.chat = AsyncMock(side_effect=LLMUnavailable("all providers down"))

    result = await tutor_query(
        session=mock_session,
        course_code="IT3160E",
        question="What is AI?",
        include_exercise=False,
        llm_router=mock_router,
        retrieval_service=mock_retrieval,
        settings=get_settings(),
    )

    assert "unavailable" in result.answer.lower()
    assert result.citations == []


def test_parse_decision_tool_call() -> None:
    from app.services.tutor_service import _parse_decision

    text = (
        '{"thought": "need course documents", "action": "call_tool", '
        '"tool_name": "rag_retrieval_api_tool", "arguments": {"query": "quorum"}}'
    )
    decision = _parse_decision(text)
    assert decision is not None
    assert decision["action"] == "call_tool"
    assert decision["tool_name"] == "rag_retrieval_api_tool"
    assert decision["arguments"] == {"query": "quorum"}


def test_parse_decision_final_answer() -> None:
    from app.services.tutor_service import _parse_decision

    decision = _parse_decision('{"thought": "enough info", "action": "final_answer"}')
    assert decision is not None
    assert decision["action"] == "final_answer"


def test_parse_decision_json_wrapped_in_prose() -> None:
    from app.services.tutor_service import _parse_decision

    text = (
        'Let me look that up. {"thought": "search", "action": "call_tool", '
        '"tool_name": "rag_retrieval_api_tool", "arguments": {}}'
    )
    decision = _parse_decision(text)
    assert decision is not None
    assert decision["action"] == "call_tool"


def test_parse_decision_plain_text_returns_none() -> None:
    from app.services.tutor_service import _parse_decision

    assert _parse_decision("AI is a broad field of computer science.") is None


def test_parse_decision_minimax_invoke_with_ragged_params() -> None:
    from app.services.tutor_service import _parse_decision

    text = (
        "Bạn ơi, mình cần tra cứu tài liệu môn học để có thể tóm tắt chính xác "
        "cho bạn nhé! Để mình xem qua.]<]minimax[>[ "
        "]<]minimax[>[<invoke name=\"course_wide_summary_cache_tool\">"
        "]<]minimax[>[<invoke name=\"rag_retrieval_api_tool\">]<]minimax[>["
        "<query\">tổng quan môn học IT3020E Toán rời rạc nội dung chính\"]"
        "<]minimax[>[<namespaces\">[\"knowledge\"]\"}]<]minimax[>["
    )
    decision = _parse_decision(text)
    assert decision is not None
    assert decision["action"] == "call_tool"
    # Only the first <invoke> per turn is consumed.
    assert decision["tool_name"] == "course_wide_summary_cache_tool"
    assert decision["arguments"] == {}
    assert "tra cứu" in decision["thought"]


def test_parse_decision_minimax_invoke_first_with_params() -> None:
    from app.services.tutor_service import _parse_decision

    text = (
        "I will look up the relevant documents."
        "<invoke name=\"rag_retrieval_api_tool\">"
        "<query\">what is quorum consensus?\"]"
        "<namespaces\">[\"knowledge\"]"
    )
    decision = _parse_decision(text)
    assert decision is not None
    assert decision["action"] == "call_tool"
    assert decision["tool_name"] == "rag_retrieval_api_tool"
    assert decision["arguments"] == {"query": "what is quorum consensus?", "namespaces": ["knowledge"]}


def test_parse_decision_minimax_unknown_tool_returns_none() -> None:
    from app.services.tutor_service import _parse_decision

    assert _parse_decision('<invoke name="not_a_real_tool">') is None


def test_answer_max_tokens_budget_is_raised() -> None:
    """The final ANSWER turn token budget must leave headroom for reasoning-
    capable providers (e.g. minimax-m3 emits a `...` block that counts
    against ``max_tokens``). 8192 gives ~4k headroom beyond the previous
    4096 cap so the visible Markdown answer is not truncated mid-sentence."""
    from app.services.tutor_service import _ANSWER_MAX_TOKENS

    assert _ANSWER_MAX_TOKENS >= 8192


def test_postprocess_answer_without_ids_returns_no_citations() -> None:
    from app.schemas.tutor import CitationResponse
    from app.services.tutor_service import _postprocess_answer

    citation = CitationResponse(
        chunk_id=uuid4(),
        document_title="doc.pdf",
        document_tier=DocumentTier.COMMUNITY.value,
        document_subtype=None,
        section_title=None,
        page_number=None,
        chunk_order=1,
        excerpt="excerpt",
    )
    answer_clean, filtered = _postprocess_answer("Answer with no trailing id JSON.", [citation], {})
    assert answer_clean == "Answer with no trailing id JSON."
    assert filtered == []


def test_postprocess_answer_json_only_answer_falls_back_to_friendly_message() -> None:
    from app.schemas.tutor import CitationResponse
    from app.services.tutor_service import _postprocess_answer

    doc_id = uuid4()
    chunk_id = uuid4()
    citation = CitationResponse(
        chunk_id=chunk_id,
        document_title="doc.pdf",
        document_tier=DocumentTier.COMMUNITY.value,
        document_subtype=None,
        section_title=None,
        page_number=None,
        chunk_order=1,
        excerpt="excerpt",
    )
    # The model answered with ONLY the trailing id-JSON — nothing before it.
    answer = f'{{"used_doc_ids": ["{doc_id}"]}}'

    answer_clean, filtered = _postprocess_answer(answer, [citation], {chunk_id: doc_id})

    assert answer_clean == "Xin lỗi, mình chưa rõ câu trả lời — bạn hỏi lại giúp mình nhé?"
    assert filtered == [citation]


@pytest.mark.asyncio
async def test_tutor_query_agent_loop_direct_answer() -> None:
    from app.config import get_settings
    from app.services.tutor_service import tutor_query_agent_loop

    session_id = uuid4()
    course_id = uuid4()
    mock_chat_session = MagicMock()
    mock_chat_session.id = session_id
    mock_chat_session.course_id = course_id
    mock_chat_session.summary = "previous discussion about sorting"

    mock_course = MagicMock()
    mock_course.id = course_id
    mock_course.code = "IT3160E"
    mock_course.name = "Introduction to AI"
    mock_course.topic_summary = "AI fundamentals"

    mock_session = AsyncMock()
    mock_session.add = MagicMock()
    # Define a helper function to mock different scalar return values
    async def mock_scalar_fn(stmt):
        stmt_str = str(stmt).lower()
        if "chat_sessions" in stmt_str:
            return mock_chat_session
        if "courses" in stmt_str:
            return mock_course
        if "count" in stmt_str:
            return 2
        return None

    mock_session.scalar = mock_scalar_fn

    mock_scalars_result = MagicMock()
    mock_scalars_result.all = MagicMock(return_value=[])
    mock_session.scalars = AsyncMock(return_value=mock_scalars_result)

    mock_retrieval = AsyncMock()
    mock_retrieval.search = AsyncMock(return_value=[])

    mock_llm_res = MagicMock()
    mock_llm_res.content = "Artificial intelligence is broad."
    mock_router = AsyncMock()
    mock_router.chat = AsyncMock(return_value=mock_llm_res)

    result = await tutor_query_agent_loop(
        session=mock_session,
        session_id=session_id,
        question="What is AI?",
        llm_router=mock_router,
        retrieval_service=mock_retrieval,
        settings=get_settings(),
    )

    assert "broad" in result.answer
    assert result.citations == []


@pytest.mark.asyncio
async def test_tutor_query_agent_loop_final_answer_decision_then_answer_call() -> None:
    from app.config import get_settings
    from app.services.tutor_service import tutor_query_agent_loop

    session_id = uuid4()
    course_id = uuid4()
    mock_chat_session = MagicMock()
    mock_chat_session.id = session_id
    mock_chat_session.course_id = course_id
    mock_chat_session.summary = "previous discussion about sorting"

    mock_course = MagicMock()
    mock_course.id = course_id
    mock_course.code = "IT3160E"
    mock_course.name = "Introduction to AI"
    mock_course.topic_summary = "AI fundamentals"

    mock_session = AsyncMock()
    mock_session.add = MagicMock()

    async def mock_scalar_fn(stmt):
        stmt_str = str(stmt).lower()
        if "chat_sessions" in stmt_str:
            return mock_chat_session
        if "courses" in stmt_str:
            return mock_course
        if "count" in stmt_str:
            return 2
        return None

    mock_session.scalar = mock_scalar_fn

    mock_scalars_result = MagicMock()
    mock_scalars_result.all = MagicMock(return_value=[])
    mock_session.scalars = AsyncMock(return_value=mock_scalars_result)

    mock_retrieval = AsyncMock()
    mock_retrieval.search = AsyncMock(return_value=[])

    decision_res = MagicMock(content='{"thought": "I can answer from context", "action": "final_answer"}')
    answer_res = MagicMock(content="AI là một lĩnh vực rộng của khoa học máy tính.")
    mock_router = AsyncMock()
    mock_router.chat = AsyncMock(side_effect=[decision_res, answer_res])

    result = await tutor_query_agent_loop(
        session=mock_session,
        session_id=session_id,
        question="AI là gì?",
        llm_router=mock_router,
        retrieval_service=mock_retrieval,
        settings=get_settings(),
    )

    assert "lĩnh vực rộng" in result.answer
    assert '"thought"' not in result.answer
    assert mock_router.chat.await_count == 2
    # Decision phase must run with structured output enforced.
    first_call = mock_router.chat.call_args_list[0]
    assert first_call.kwargs["schema"] is not None
    # The rolling summary must be injected as a user message, not a mid-history system message.
    first_messages = first_call.args[0]
    summary_msgs = [m for m in first_messages if "previous conversation" in m["content"]]
    assert summary_msgs and all(m["role"] == "user" for m in summary_msgs)
    # The final-answer call must not enforce the decision schema.
    second_call = mock_router.chat.call_args_list[1]
    assert second_call.kwargs.get("schema") is None


@pytest.mark.asyncio
async def test_execute_tool_rag_retrieval_passes_document_ids_through() -> None:
    from app.config import get_settings
    from app.services.tutor_service import _execute_tool

    course_id = uuid4()
    mock_course = MagicMock()
    mock_course.id = course_id

    mock_session = AsyncMock()
    mock_session.execute = AsyncMock(return_value=MagicMock(__iter__=lambda self: iter([])))

    doc_ids = [uuid4(), uuid4()]
    mock_retrieval = AsyncMock()
    mock_retrieval.search = AsyncMock(return_value=[])

    await _execute_tool(
        session=mock_session,
        course=mock_course,
        settings=get_settings(),
        retrieval_service=mock_retrieval,
        tool_name="rag_retrieval_api_tool",
        tool_args={"query": "what is AI?", "namespaces": ["knowledge"]},
        question="What is AI?",
        citations=[],
        chunk_to_doc_id={},
        document_ids=doc_ids,
    )

    mock_retrieval.search.assert_awaited_once()
    _, kwargs = mock_retrieval.search.call_args
    assert kwargs["document_ids"] == doc_ids


@pytest.mark.asyncio
async def test_tutor_course_summary_generation() -> None:
    from app.services.tutor_service import tutor_course_summary

    course_id = uuid4()
    mock_course = MagicMock()
    mock_course.id = course_id
    mock_course.code = "IT3160E"
    mock_course.name = "Introduction to AI"
    mock_course.topic_summary = "AI fundamentals"

    mock_session = AsyncMock()
    mock_session.add = MagicMock()
    async def mock_scalar_fn(stmt):
        stmt_str = str(stmt).lower()
        if "courses" in stmt_str:
            return mock_course
        if "course_summaries_cache" in stmt_str:
            return None # no cache yet
        return None

    mock_session.scalar = mock_scalar_fn

    # Return some mock document summaries
    mock_summaries_result = MagicMock()
    mock_summaries_result.all = MagicMock(return_value=[])
    mock_session.scalars = AsyncMock(return_value=mock_summaries_result)

    mock_llm_res = MagicMock()
    mock_llm_res.content = "# Comprehensive Summary\nThis is a cache summary. {\"concepts\": []}"
    mock_router = AsyncMock()
    mock_router.chat = AsyncMock(return_value=mock_llm_res)

    result = await tutor_course_summary(
        session=mock_session,
        course_id=course_id,
        llm_router=mock_router,
    )

    assert result.course_id == course_id
    assert "Comprehensive Summary" in result.summary_markdown


@pytest.mark.asyncio
async def test_tutor_query_agent_loop_with_course_summary_citations() -> None:
    import json
    from app.config import get_settings
    from app.services.tutor_service import tutor_query_agent_loop
    from app.models.tables import CourseSummaryCache

    session_id = uuid4()
    course_id = uuid4()
    doc_id = uuid4()

    mock_chat_session = MagicMock()
    mock_chat_session.id = session_id
    mock_chat_session.course_id = course_id
    mock_chat_session.summary = ""

    mock_course = MagicMock()
    mock_course.id = course_id
    mock_course.code = "IT3160E"
    mock_course.name = "Introduction to AI"
    mock_course.topic_summary = "AI fundamentals"

    mock_summary_cache = CourseSummaryCache(
        course_id=course_id,
        summary_markdown="This is the cached course summary.",
        citations=[
            {
                "document_id": str(doc_id),
                "document_title": "AI_syllabus.pdf",
                "document_tier": "official"
            }
        ],
    )

    mock_session = AsyncMock()
    mock_session.add = MagicMock()

    async def mock_scalar_fn(stmt):
        stmt_str = str(stmt).lower()
        if "chat_sessions" in stmt_str:
            return mock_chat_session
        if "courses" in stmt_str:
            return mock_course
        if "course_summaries_cache" in stmt_str:
            return mock_summary_cache
        return None

    mock_session.scalar = mock_scalar_fn

    mock_scalars_result = MagicMock()
    mock_scalars_result.all = MagicMock(return_value=[])
    mock_session.scalars = AsyncMock(return_value=mock_scalars_result)

    mock_retrieval = AsyncMock()

    decision_res = MagicMock(
        content=json.dumps({
            "thought": "I will check the course summary.",
            "action": "call_tool",
            "tool_name": "course_wide_summary_cache_tool",
            "arguments": {}
        })
    )
    final_decision_res = MagicMock(
        content=json.dumps({
            "thought": "I have the summary, I will answer.",
            "action": "final_answer"
        })
    )
    answer_res = MagicMock(
        content="According to the syllabus, we learn AI.\n" + json.dumps({"used_doc_ids": [str(doc_id)]})
    )

    mock_router = AsyncMock()
    mock_router.chat = AsyncMock(side_effect=[decision_res, final_decision_res, answer_res])

    result = await tutor_query_agent_loop(
        session=mock_session,
        session_id=session_id,
        question="What is the syllabus?",
        llm_router=mock_router,
        retrieval_service=mock_retrieval,
        settings=get_settings(),
    )

    assert "According to the syllabus" in result.answer
    assert len(result.citations) == 1
    assert result.citations[0].document_title == "AI_syllabus.pdf"
    assert result.citations[0].chunk_id == doc_id

