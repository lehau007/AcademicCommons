from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.core.auth import get_current_user
from app.db.session import get_session
from app.llm.router import build_llm_router
from app.models import User
from app.schemas.mock_test import MockTestGenerateRequest, MockTestGenerateResponse
from app.services.mock_test_service import generate_mock_test, get_mock_test_by_run_id, get_recent_mock_test
from app.services.retrieval_service import get_retrieval_service

router = APIRouter(prefix="/courses", tags=["mocktest"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]


@router.post("/{course_code}/mock-tests/generate", response_model=MockTestGenerateResponse)
async def create_mock_test(
    course_code: str,
    request: MockTestGenerateRequest,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> MockTestGenerateResponse:
    settings = get_settings()
    try:
        return await generate_mock_test(
            session=session,
            course_code=course_code,
            total_questions=request.total_questions,
            difficulty_distribution=request.difficulty_distribution,
            llm_router=build_llm_router(settings),
            retrieval_service=get_retrieval_service(settings),
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/{course_code}/mock-tests/recent", response_model=MockTestGenerateResponse)
async def get_mock_tests_recent(
    course_code: str,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> MockTestGenerateResponse:
    try:
        return await get_recent_mock_test(session=session, course_code=course_code)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/{course_code}/mock-tests/{test_run_id}", response_model=MockTestGenerateResponse)
async def get_mock_test(
    course_code: str,
    test_run_id: UUID,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> MockTestGenerateResponse:
    try:
        return await get_mock_test_by_run_id(
            session=session, course_code=course_code, test_run_id=test_run_id
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
