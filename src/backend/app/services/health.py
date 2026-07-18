from app.config import Settings, get_settings
from app.db.session import check_database
from app.storage.s3 import check_storage
from app.workers.redis_health import check_redis


def _detect_llm_provider(settings: Settings) -> str:
    if settings.azure_ai_api_key:
        return "azure"
    if settings.gemini_api_key:
        return "gemini"
    if settings.groq_api_key:
        return "groq"
    return "none"


async def collect_health() -> dict[str, str | dict[str, str]]:
    settings = get_settings()
    checks = {
        "db": await check_database(),
        "redis": await check_redis(settings.redis_url),
        "storage": await check_storage(settings),
    }
    status = "ok" if all(value == "ok" for value in checks.values()) else "degraded"
    return {
        "status": status,
        "checks": checks,
        "llm_provider": _detect_llm_provider(settings),
    }
