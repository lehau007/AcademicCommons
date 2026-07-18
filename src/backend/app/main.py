import logging
import time
import uuid
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse, Response

from app.api.v1.health import health
from app.api.v1.router import api_router
from app.config import get_settings
from app.core.logging import configure_logging
from app.core.rate_limit import RateLimitMiddleware
from app.core.redis import close_redis
from app.llm.errors import ProviderError

_log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # The shared Redis client is created lazily on first use; here we just make
    # sure its connection pool is released cleanly on shutdown.
    yield
    await close_redis()


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Propagate or generate an X-Request-ID header; log request method/path/status/latency."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.state.request_id = request_id
        t0 = time.monotonic()
        response: Response = await call_next(request)
        latency_ms = int((time.monotonic() - t0) * 1000)
        response.headers["X-Request-ID"] = request_id
        _log.info(
            "%s %s %d %dms req=%s",
            request.method,
            request.url.path,
            response.status_code,
            latency_ms,
            request_id,
        )
        return response


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(
        error_log_file=(
            settings.error_log_file_path if settings.error_log_file_enabled else None
        ),
        error_log_max_bytes=settings.error_log_file_max_bytes,
        error_log_backup_count=settings.error_log_file_backup_count,
    )
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="Backend API for course-centric academic knowledge management.",
        lifespan=lifespan,
    )
    # Outermost first at runtime: CORS -> RequestID -> RateLimit (429s still get
    # CORS headers and a logged request id).
    app.add_middleware(RateLimitMiddleware)
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router, prefix=settings.api_v1_prefix)
    app.add_api_route("/health", health, methods=["GET"], tags=["health"])

    @app.exception_handler(ProviderError)
    async def provider_error_handler(request: Request, exc: ProviderError) -> JSONResponse:
        # 503 with a handled body (instead of an unhandled 500) keeps CORS headers,
        # so the browser sees the real message rather than "Failed to fetch".
        _log.error("provider failure %s: %s", exc.code, exc, exc_info=exc)
        return JSONResponse(status_code=503, content={"detail": str(exc), "code": exc.code})

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
