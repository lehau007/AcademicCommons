from __future__ import annotations

import difflib
import json
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.llm.providers import ChatMessage, LLMUnavailable
from app.llm.router import LLMRouter
from app.models.enums import Difficulty, DocumentStatus, QuestionType
from app.models.tables import Course, Document, DocumentSummary, MockTestItem
from app.schemas.mock_test import (
    DifficultyDistribution,
    MockTestCitation,
    MockTestGenerateResponse,
    MockTestQuestion,
)
from app.services.retrieval_service import RetrievalService

_PLAN_SYSTEM = (
    "You are a test design expert. Given a list of topics and a difficulty distribution, "
    "create a test plan as JSON. All questions must strictly be multiple choice questions (mcq). "
    'Output ONLY valid JSON: {"plan": [{"topic": "...", "question_count": N, "difficulty": "easy|medium|hard", '
    '"question_types": ["mcq"]}]} '
    "The sum of question_count across all plan items MUST equal the requested total number of questions."
)

_PLAN_SCHEMA = {
    "type": "object",
    "properties": {
        "plan": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string"},
                    "question_count": {"type": "integer"},
                    "difficulty": {"type": "string", "enum": ["easy", "medium", "hard"]},
                    "question_types": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["topic", "question_count", "difficulty", "question_types"],
            },
        },
    },
    "required": ["plan"],
}

_QUESTION_SYSTEM = (
    "You are an academic question generator. Generate multiple choice questions (mcq) based ONLY on "
    "the provided document excerpts. "
    'Output ONLY valid JSON with this structure: {"questions": [...]}. '
    "Each item must represent a multiple choice question with exactly 4 options (A, B, C, D) "
    "and have the following format: "
    '{"question_text": "...", "question_type": "mcq", "difficulty": "easy|medium|hard", '
    '"topic": "...", "options": [{"key": "A", "text": "..."}, {"key": "B", "text": "..."}, '
    '{"key": "C", "text": "..."}, {"key": "D", "text": "..."}], '
    '"correct_answer": "A|B|C|D", "explanation": "...", "used_chunk_ids": ["uuid1", ...]} '
    "CRITICAL: Only generate questions that test substantive subject-matter knowledge — "
    "concepts, definitions, syntax, algorithms, reasoning, and worked examples from the course. "
    "NEVER generate questions about non-academic document metadata or slide furniture, including: "
    "cover pages, titles, and lecture/version numbers; institutional branding, names, or "
    "acronyms (such as 'SOICT', 'HUST', 'FIT', 'SAMI'); course names or course codes; "
    "contact information such as websites, URLs, emails, phone numbers, or addresses "
    "(e.g. 'What is the university's website?'); author, instructor, or copyright details; "
    "dates, semesters, or table-of-contents/agenda listings; and anniversary or celebratory "
    "trivia (e.g. how many years an institution has existed). If an excerpt contains only such "
    "material, skip it and produce no question from it. "
    "Distractors (wrong options) must be plausible: related to the topic and not obviously wrong. "
    "Every question MUST include a non-empty explanation (2-3 sentences) that states why the "
    "correct option is right and, where helpful, why the main distractor is wrong. "
    "The explanation must be grounded in the excerpts cited in used_chunk_ids. "
    "If the excerpts do not contain enough substantive material for the requested number of "
    "questions, generate fewer questions instead of inventing content. "
    "Generate ALL questions in a single, consistent language matching the dominant language "
    "of the provided excerpts; if the excerpts are mixed or the dominant language is unclear, "
    "default to Vietnamese. Do not mix languages within one test."
)

_QUESTIONS_SCHEMA = {
    "type": "object",
    "properties": {
        "questions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "question_text": {"type": "string"},
                    "question_type": {"type": "string", "enum": ["mcq"]},
                    "difficulty": {"type": "string", "enum": ["easy", "medium", "hard"]},
                    "topic": {"type": "string"},
                    "options": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "key": {"type": "string"},
                                "text": {"type": "string"},
                            },
                            "required": ["key", "text"],
                        },
                    },
                    "correct_answer": {"type": "string"},
                    "explanation": {"type": "string"},
                    "used_chunk_ids": {"type": "array", "items": {"type": "string"}},
                },
                "required": [
                    "question_text",
                    "question_type",
                    "difficulty",
                    "topic",
                    "options",
                    "correct_answer",
                    "explanation",
                    "used_chunk_ids",
                ],
            },
        },
    },
    "required": ["questions"],
}


async def generate_mock_test(
    session: AsyncSession,
    course_code: str,
    total_questions: int,
    difficulty_distribution: DifficultyDistribution,
    llm_router: LLMRouter,
    retrieval_service: RetrievalService,
) -> MockTestGenerateResponse:
    course = await session.scalar(select(Course).where(Course.code == course_code, Course.is_active.is_(True)))
    if course is None:
        raise ValueError(f"Course '{course_code}' not found")

    topics = await _collect_topics(session, course)
    if not topics:
        return MockTestGenerateResponse(course_code=course_code, total_questions=0, questions=[])

    plan = await _generate_plan(topics, total_questions, difficulty_distribution, llm_router)
    if not plan:
        return MockTestGenerateResponse(course_code=course_code, total_questions=0, questions=[])

    test_run_id = uuid4()
    all_raw_questions: list[Any] = []

    for plan_item in plan:
        topic = str(plan_item.get("topic", ""))
        count = int(plan_item.get("question_count", 1))
        difficulty = str(plan_item.get("difficulty", "medium"))

        chunks = await retrieval_service.search(
            session, course.id, topic, namespaces=["knowledge", "exercise"], k=8
        )
        if not chunks:
            continue

        chunk_content_map = {chunk.id: chunk.content for chunk in chunks}
        chunk_id_set = {chunk.id for chunk in chunks}
        context = "\n\n---\n\n".join(f"[chunk_id={chunk.id}]\n{chunk.content}" for chunk in chunks)

        try:
            raw = await _generate_questions_for_topic(
                topic=topic,
                count=count,
                difficulty=difficulty,
                question_types=["mcq"],
                context=context,
                valid_chunk_ids=chunk_id_set,
                chunk_content_map=chunk_content_map,
                llm_router=llm_router,
            )
            all_raw_questions.extend(raw)
        except LLMUnavailable:
            continue

    deduped = _dedup_questions(all_raw_questions)

    db_items: list[MockTestItem] = []
    for q in deduped:
        used_ids: list[UUID] = [uid for uid in q.get("used_chunk_ids", []) if isinstance(uid, UUID)]
        citations_data = [
            {"chunk_id": str(uid), "excerpt": str(q.get("_chunk_content_map", {}).get(uid, ""))[:200]}
            for uid in used_ids
        ]
        item = MockTestItem(
            test_run_id=test_run_id,
            course_id=course.id,
            question_text=str(q.get("question_text", "")),
            question_type=_safe_question_type(str(q.get("question_type", "mcq"))),
            difficulty=_safe_difficulty(str(q.get("difficulty", "medium"))),
            topic=str(q.get("topic", "")) or None,
            options=list(q.get("options", [])),
            correct_answer=str(q.get("correct_answer", "")),
            explanation=str(q.get("explanation", "")) or None,
            citations=citations_data,
        )
        session.add(item)
        db_items.append(item)

    if db_items:
        await session.flush()

    questions: list[MockTestQuestion] = []
    for item in db_items:
        await session.refresh(item)
        citations = [
            MockTestCitation(
                chunk_id=UUID(str(c["chunk_id"])),
                excerpt=str(c.get("excerpt", ""))[:200],
            )
            for c in (item.citations or [])
            if c.get("chunk_id")
        ]
        questions.append(
            MockTestQuestion(
                id=item.id,
                test_run_id=test_run_id,
                question_text=item.question_text,
                question_type=item.question_type.value,
                difficulty=item.difficulty.value,
                topic=item.topic,
                options=item.options,
                correct_answer=item.correct_answer,
                explanation=item.explanation,
                citations=citations,
            )
        )

    await session.commit()
    return MockTestGenerateResponse(
        course_code=course_code,
        total_questions=len(questions),
        test_run_id=test_run_id,
        questions=questions,
    )


async def get_mock_test_by_run_id(
    session: AsyncSession,
    course_code: str,
    test_run_id: UUID,
) -> MockTestGenerateResponse:
    course = await session.scalar(select(Course).where(Course.code == course_code))
    if course is None:
        raise ValueError(f"Course '{course_code}' not found")

    rows = await session.execute(
        select(MockTestItem).where(
            MockTestItem.course_id == course.id,
            MockTestItem.test_run_id == test_run_id,
        )
    )
    items = list(rows.scalars())
    questions = _items_to_questions(items, test_run_id)
    return MockTestGenerateResponse(
        course_code=course_code,
        total_questions=len(questions),
        test_run_id=test_run_id,
        questions=questions,
    )


async def get_recent_mock_test(
    session: AsyncSession,
    course_code: str,
    limit: int = 10,
) -> MockTestGenerateResponse:
    course = await session.scalar(select(Course).where(Course.code == course_code))
    if course is None:
        raise ValueError(f"Course '{course_code}' not found")

    rows = await session.execute(
        select(MockTestItem)
        .where(MockTestItem.course_id == course.id)
        .order_by(MockTestItem.generated_at.desc())
        .limit(limit)
    )
    items = list(rows.scalars())
    run_id = items[0].test_run_id if items else None
    questions = _items_to_questions(items, run_id)
    return MockTestGenerateResponse(course_code=course_code, total_questions=len(questions), questions=questions)


def _items_to_questions(items: list[MockTestItem], test_run_id: UUID | None) -> list[MockTestQuestion]:
    return [
        MockTestQuestion(
            id=item.id,
            test_run_id=item.test_run_id,
            question_text=item.question_text,
            question_type=item.question_type.value,
            difficulty=item.difficulty.value,
            topic=item.topic,
            options=item.options,
            correct_answer=item.correct_answer,
            explanation=item.explanation,
            citations=[
                MockTestCitation(chunk_id=UUID(str(c["chunk_id"])), excerpt=str(c.get("excerpt", ""))[:200])
                for c in (item.citations or [])
                if c.get("chunk_id")
            ],
        )
        for item in items
    ]


async def _collect_topics(session: AsyncSession, course: Course) -> list[str]:
    indexed_ids_result = await session.execute(
        select(Document.id).where(Document.course_id == course.id, Document.status == DocumentStatus.INDEXED)
    )
    indexed_ids = [row[0] for row in indexed_ids_result]

    topics: list[str] = []
    if indexed_ids:
        summary_rows = await session.execute(
            select(DocumentSummary).where(DocumentSummary.document_id.in_(indexed_ids))
        )
        for summary in summary_rows.scalars():
            if summary.topic:
                topics.append(summary.topic)
            topics.extend(str(c) for c in (summary.concepts or []))

    if course.topic_summary:
        topics.append(course.topic_summary[:100])

    seen: set[str] = set()
    deduped: list[str] = []
    for t in topics:
        if t not in seen:
            seen.add(t)
            deduped.append(t)
    return deduped[:20]


async def _generate_plan(
    topics: list[str],
    total_questions: int,
    dist: DifficultyDistribution,
    llm_router: LLMRouter,
) -> list[Any]:
    topic_list = "\n".join(f"- {t}" for t in topics[:15])
    user_msg = (
        f"Topics:\n{topic_list}\n\n"
        f"Generate a test plan for {total_questions} questions with this difficulty distribution:\n"
        f"Easy: {dist.easy}, Medium: {dist.medium}, Hard: {dist.hard}\n"
        "Distribute questions across topics. Each plan item must have question_count >= 1. "
        f"The question_count values of all plan items must sum to exactly {total_questions}."
    )
    messages: list[ChatMessage] = [
        {"role": "system", "content": _PLAN_SYSTEM},
        {"role": "user", "content": user_msg},
    ]
    result = await llm_router.chat(messages, schema=_PLAN_SCHEMA, max_tokens=4096, flow="mock_test")
    return _parse_plan(result.content)


def _parse_plan(text: str) -> list[Any]:
    # Find the first complete JSON object by matching braces
    start = text.find("{")
    if start == -1:
        return []
    depth = 0
    end = -1
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    if end == -1:
        return []
    try:
        payload = json.loads(text[start:end])
        plan = payload.get("plan", [])
        return plan if isinstance(plan, list) else []
    except (json.JSONDecodeError, ValueError):
        return []


async def _generate_questions_for_topic(
    *,
    topic: str,
    count: int,
    difficulty: str,
    question_types: list[str],
    context: str,
    valid_chunk_ids: set[UUID],
    chunk_content_map: dict[UUID, str],
    llm_router: LLMRouter,
) -> list[Any]:
    q_types_str = " and ".join(question_types) if question_types else "mcq"
    user_msg = (
        f"Context documents:\n{context}\n\n"
        f"Generate {count} {difficulty} {q_types_str} question(s) about: {topic}\n"
        "Use ONLY the provided context. Include used_chunk_ids referencing the chunk_ids above."
    )
    messages: list[ChatMessage] = [
        {"role": "system", "content": _QUESTION_SYSTEM},
        {"role": "user", "content": user_msg},
    ]
    result = await llm_router.chat(messages, schema=_QUESTIONS_SCHEMA, max_tokens=4096, flow="mock_test")
    raw_questions = _parse_questions(result.content)

    for q in raw_questions:
        raw_ids = q.get("used_chunk_ids", [])
        valid_ids: list[UUID] = []
        for rid in raw_ids if isinstance(raw_ids, list) else []:
            try:
                uid = UUID(str(rid))
                if uid in valid_chunk_ids:
                    valid_ids.append(uid)
            except (ValueError, AttributeError):
                pass
        # No fallback to arbitrary chunks: a question without valid ids gets no citations.
        q["used_chunk_ids"] = valid_ids
        # Attach chunk content map so citations can use real excerpts.
        q["_chunk_content_map"] = chunk_content_map

    return raw_questions


def _parse_questions(text: str) -> list[Any]:
    text = text.strip()
    # Object form {"questions": [...]} produced by structured output.
    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        if start != -1 and end > start:
            payload = json.loads(text[start:end])
            if isinstance(payload, dict):
                questions = payload.get("questions")
                if isinstance(questions, list):
                    return questions
    except (json.JSONDecodeError, ValueError):
        pass
    # Bare JSON array fallback.
    try:
        start = text.find("[")
        end = text.rfind("]") + 1
        if start != -1 and end > start:
            result = json.loads(text[start:end])
            return result if isinstance(result, list) else []
    except (json.JSONDecodeError, ValueError):
        pass
    return []


def _dedup_questions(questions: list[Any]) -> list[Any]:
    result: list[Any] = []
    for q in questions:
        text_q = str(q.get("question_text", ""))
        is_dup = any(
            difflib.SequenceMatcher(None, text_q, str(existing.get("question_text", ""))).ratio() > 0.8
            for existing in result
        )
        if not is_dup:
            result.append(q)
    return result


def _safe_question_type(value: str) -> QuestionType:
    return QuestionType.MULTIPLE_CHOICE


def _safe_difficulty(value: str) -> Difficulty:
    mapping: dict[str, Difficulty] = {
        "easy": Difficulty.EASY,
        "medium": Difficulty.MEDIUM,
        "hard": Difficulty.HARD,
    }
    return mapping.get(value.lower(), Difficulty.MEDIUM)


__all__ = ["generate_mock_test", "get_mock_test_by_run_id", "get_recent_mock_test"]
