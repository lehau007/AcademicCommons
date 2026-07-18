from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.core.auth import get_current_user, require_role
from app.db.session import get_session
from app.llm.router import build_llm_router
from app.models import User
from app.schemas.mindmap import MindmapGenerateResponse
from app.services.mindmap_service import get_or_generate_mindmap

router = APIRouter(prefix="/courses", tags=["mindmap"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]
AdminOrReviewerDep = Annotated[User, Depends(require_role("admin", "reviewer"))]


@router.get("/{course_code}/mindmap", response_model=MindmapGenerateResponse)
async def get_mindmap(
    course_code: str,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> MindmapGenerateResponse:
    try:
        return await get_or_generate_mindmap(
            session=session,
            course_code=course_code,
            force_regen=False,
            llm_router=build_llm_router(get_settings()),
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/{course_code}/mindmap/generate", response_model=MindmapGenerateResponse)
async def generate_mindmap(
    course_code: str,
    session: SessionDep,
    current_user: AdminOrReviewerDep,
) -> MindmapGenerateResponse:
    try:
        return await get_or_generate_mindmap(
            session=session,
            course_code=course_code,
            force_regen=True,
            llm_router=build_llm_router(get_settings()),
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
