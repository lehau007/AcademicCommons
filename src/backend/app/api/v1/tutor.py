from __future__ import annotations

import json
import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import get_settings
from app.core.auth import get_current_user
from app.db.session import AsyncSessionLocal, get_session
from app.llm.router import build_llm_router
from app.models import ChatMessage, ChatSession, Course, DocumentSummary, User
from app.schemas.tutor import (
    ChatMessageRead,
    ChatSessionRead,
    DocumentSummaryResponse,
    TutorQueryRequest,
    TutorQueryResponse,
    TutorSummarizeRequest,
    TutorSummarizeResponse,
)
from app.services.retrieval_service import get_retrieval_service
from app.services.tutor_service import (
    stream_tutor_agent_loop,
    tutor_course_summary,
    tutor_query,
    tutor_query_agent_loop,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tutor", tags=["tutor"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]


@router.post("/query", response_model=TutorQueryResponse)
async def query_tutor(
    request: TutorQueryRequest,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> TutorQueryResponse:
    settings = get_settings()

    if request.session_id is not None:
        chat_session = await session.scalar(
            select(ChatSession).where(ChatSession.id == request.session_id)
        )
        if not chat_session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat session not found",
            )
    else:
        course = await session.scalar(
            select(Course).where(Course.code == request.course_code, Course.is_active.is_(True))
        )
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Active course not found",
            )
        chat_session = ChatSession(
            user_id=current_user.id,
            course_id=course.id,
            summary=None,
        )
        session.add(chat_session)
        await session.flush()

    res = await tutor_query_agent_loop(
        session=session,
        session_id=chat_session.id,
        question=request.question,
        llm_router=build_llm_router(settings),
        retrieval_service=get_retrieval_service(settings),
        settings=settings,
        document_ids=request.document_ids,
    )
    res.session_id = chat_session.id
    await session.commit()
    return res


@router.post("/query-classic", response_model=TutorQueryResponse)
async def query_tutor_classic(
    request: TutorQueryRequest,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> TutorQueryResponse:
    """Traditional single-shot RAG (retrieve once -> generate). Ablation baseline;
    intentionally NOT wired into the frontend."""
    settings = get_settings()
    res = await tutor_query(
        session=session,
        course_code=request.course_code,
        question=request.question,
        include_exercise=request.include_exercise,
        llm_router=build_llm_router(settings),
        retrieval_service=get_retrieval_service(settings),
        settings=settings,
    )
    await session.commit()
    return res


def _sse(event: dict) -> str:
    return f"data: {json.dumps(event, ensure_ascii=False)}\n\n"


@router.post("/query/stream")
async def query_tutor_stream(
    request: TutorQueryRequest,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> StreamingResponse:
    settings = get_settings()

    if request.session_id is not None:
        chat_session = await session.scalar(
            select(ChatSession).where(ChatSession.id == request.session_id)
        )
        if not chat_session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat session not found")
    else:
        course = await session.scalar(
            select(Course).where(Course.code == request.course_code, Course.is_active.is_(True))
        )
        if not course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Active course not found")
        chat_session = ChatSession(user_id=current_user.id, course_id=course.id, summary=None)
        session.add(chat_session)
        await session.flush()

    session_id = chat_session.id
    # Persist the (possibly new) chat session now: the request-scoped `session`
    # is torn down by FastAPI the moment this endpoint returns the
    # StreamingResponse — i.e. before the generator body below is consumed.
    await session.commit()

    async def event_stream():
        yield _sse({"type": "session", "session_id": str(session_id)})
        # Open a session whose lifetime matches the stream, so the DB connection
        # is not closed out from under the agent loop mid-stream.
        async with AsyncSessionLocal() as stream_session:
            try:
                async for event in stream_tutor_agent_loop(
                    session=stream_session,
                    session_id=session_id,
                    question=request.question,
                    llm_router=build_llm_router(settings),
                    retrieval_service=get_retrieval_service(settings),
                    settings=settings,
                    document_ids=request.document_ids,
                ):
                    yield _sse(event)
                await stream_session.commit()
            except Exception as exc:  # noqa: BLE001 - surfaced to the client as an SSE error event
                logger.exception("tutor stream failed session_id=%s", session_id)
                await stream_session.rollback()
                yield _sse({"type": "error", "message": str(exc)})

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.get("/summary/{doc_id}", response_model=DocumentSummaryResponse)
async def get_document_summary(
    doc_id: UUID,
    session: SessionDep,
    _: CurrentUserDep,
) -> DocumentSummaryResponse:
    doc_summary = await session.scalar(
        select(DocumentSummary).where(DocumentSummary.document_id == doc_id)
    )
    if doc_summary is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document summary not found for this document ID",
        )
    return DocumentSummaryResponse.model_validate(doc_summary)


@router.post("/summarize", response_model=TutorSummarizeResponse)
async def summarize_course(
    request: TutorSummarizeRequest,
    session: SessionDep,
    _: CurrentUserDep,
) -> TutorSummarizeResponse:
    settings = get_settings()
    course = await session.scalar(
        select(Course).where(Course.code == request.course_code, Course.is_active.is_(True))
    )
    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Active course not found",
        )

    summary_cache = await tutor_course_summary(
        session=session,
        course_id=course.id,
        llm_router=build_llm_router(settings),
    )
    await session.commit()
    return TutorSummarizeResponse.model_validate(summary_cache)


@router.get("/sessions", response_model=list[ChatSessionRead])
async def list_chat_sessions(
    session: SessionDep,
    current_user: CurrentUserDep,
    course_code: str | None = None,
) -> list[ChatSessionRead]:
    query = (
        select(ChatSession)
        .where(ChatSession.user_id == current_user.id)
        .options(selectinload(ChatSession.course))
        .order_by(ChatSession.updated_at.desc())
    )
    if course_code:
        query = query.join(ChatSession.course).where(Course.code == course_code)

    result = await session.execute(query)
    sessions = result.scalars().all()

    return [
        ChatSessionRead(
            id=s.id,
            user_id=s.user_id,
            course_id=s.course_id,
            course_code=s.course.code if s.course else None,
            summary=s.summary,
            created_at=s.created_at,
            updated_at=s.updated_at,
        )
        for s in sessions
    ]


@router.get("/sessions/{session_id}/messages", response_model=list[ChatMessageRead])
async def get_session_messages(
    session_id: UUID,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> list[ChatMessageRead]:
    chat_session = await session.scalar(
        select(ChatSession).where(
            ChatSession.id == session_id,
            ChatSession.user_id == current_user.id,
        )
    )
    if not chat_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found",
        )

    query = (
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at.asc())
    )
    result = await session.execute(query)
    messages = result.scalars().all()

    return [
        ChatMessageRead(
            id=m.id,
            session_id=m.session_id,
            role=m.role,
            content=m.content,
            citations=m.citations,
            created_at=m.created_at,
        )
        for m in messages
    ]


@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat_session(
    session_id: UUID,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> None:
    chat_session = await session.scalar(
        select(ChatSession).where(
            ChatSession.id == session_id,
            ChatSession.user_id == current_user.id,
        )
    )
    if not chat_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found",
        )

    await session.delete(chat_session)
    await session.commit()
