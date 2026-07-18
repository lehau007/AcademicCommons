from fastapi import APIRouter

from app.api.v1.admin import router as admin_router
from app.api.v1.auth import router as auth_router
from app.api.v1.courses import router as courses_router
from app.api.v1.documents import router as documents_router
from app.api.v1.health import router as health_router
from app.api.v1.mindmap import router as mindmap_router
from app.api.v1.mock_test import router as mock_test_router
from app.api.v1.notifications import router as notifications_router
from app.api.v1.rag import router as rag_router
from app.api.v1.review import router as review_router
from app.api.v1.reviewers import router as reviewers_router
from app.api.v1.tutor import router as tutor_router
from app.api.v1.vote import router as vote_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(health_router)
api_router.include_router(courses_router)
api_router.include_router(reviewers_router)
api_router.include_router(documents_router)
api_router.include_router(review_router)
api_router.include_router(vote_router)
api_router.include_router(admin_router)
api_router.include_router(tutor_router)
api_router.include_router(mindmap_router)
api_router.include_router(mock_test_router)
api_router.include_router(notifications_router)
api_router.include_router(rag_router)
