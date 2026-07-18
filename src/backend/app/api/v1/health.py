from fastapi import APIRouter

from app.services.health import collect_health

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict[str, str | dict[str, str]]:
    return await collect_health()

