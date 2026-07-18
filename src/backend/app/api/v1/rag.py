from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.core.auth import get_current_user
from app.db.session import get_session
from app.models import Course, User
from app.services.retrieval_service import get_retrieval_service
from app.services.tutor_service import _load_document_titles

router = APIRouter(prefix="/rag", tags=["rag"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]


class RagRetrieveRequest(BaseModel):
    course_code: str
    query: str
    namespaces: list[str] = ["knowledge"]
    limit: int = 8


class ChunkResponse(BaseModel):
    id: UUID
    document_id: UUID
    document_title: str | None
    document_tier: str
    subtype: str | None
    section_title: str | None
    page_number: int | None
    chunk_order: int
    content: str
    score: float


@router.post("/retrieve", response_model=list[ChunkResponse])
async def retrieve_chunks(
    request: RagRetrieveRequest,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> list[ChunkResponse]:
    course = await session.scalar(
        select(Course).where(Course.code == request.course_code, Course.is_active.is_(True))
    )
    if course is None:
        raise HTTPException(status_code=404, detail=f"Course '{request.course_code}' not found")

    settings = get_settings()
    retrieval_service = get_retrieval_service(settings)

    chunks = await retrieval_service.search(
        session,
        course_id=course.id,
        query=request.query,
        namespaces=request.namespaces,
        k=request.limit,
    )

    doc_ids = list({chunk.document_id for chunk in chunks})
    doc_titles = await _load_document_titles(session, doc_ids)

    return [
        ChunkResponse(
            id=chunk.id,
            document_id=chunk.document_id,
            document_title=doc_titles.get(chunk.document_id),
            document_tier=chunk.document_tier.value,
            subtype=chunk.subtype,
            section_title=chunk.section_title,
            page_number=chunk.page_number,
            chunk_order=chunk.chunk_order,
            content=chunk.content,
            score=chunk.final_score,
        )
        for chunk in chunks
    ]
