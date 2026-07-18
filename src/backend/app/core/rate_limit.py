from __future__ import annotations

import time
from collections import defaultdict, deque
from collections.abc import Awaitable
from typing import cast

from fastapi import Request
from redis.exceptions import RedisError
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse, Response
from starlette.types import ASGIApp

from app.config import get_settings
from app.core.redis import get_redis

_WINDOW_SECONDS = 60.0
_WINDOW_MS = 60_000

# Atomic sliding-window log over a sorted set. Members scored by timestamp (ms);
# expired entries are trimmed, then the current count is checked against the
# limit before admitting the request. Running it as a single Lua call keeps the
# check-and-insert atomic across concurrent workers and instances.
#   KEYS[1] = bucket key
#   ARGV = now_ms, window_ms, limit, unique_member
# Returns {rejected(0|1), retry_after_seconds}.
_SLIDING_WINDOW_LUA = """
local key = KEYS[1]
local now = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local limit = tonumber(ARGV[3])
redis.call('ZREMRANGEBYSCORE', key, 0, now - window)
local count = redis.call('ZCARD', key)
if count >= limit then
  local oldest = redis.call('ZRANGE', key, 0, 0, 'WITHSCORES')
  local retry = math.ceil(window / 1000)
  if oldest[2] then
    retry = math.ceil((tonumber(oldest[2]) + window - now) / 1000)
  end
  if retry < 1 then retry = 1 end
  return {1, retry}
end
redis.call('ZADD', key, now, ARGV[4])
redis.call('PEXPIRE', key, window)
return {0, 0}
"""


class _MemoryWindow:
    """Per-process sliding-window counter. Correct only for a single instance."""

    def __init__(self) -> None:
        self._hits: dict[str, deque[float]] = defaultdict(deque)

    async def hit(self, key: str, limit: int) -> tuple[bool, int]:
        now = time.monotonic()
        hits = self._hits[key]
        while hits and now - hits[0] > _WINDOW_SECONDS:
            hits.popleft()
        if len(hits) >= limit:
            retry_after = int(_WINDOW_SECONDS - (now - hits[0])) + 1
            return False, retry_after
        hits.append(now)
        return True, 0


class _RedisWindow:
    """Sliding-window counter shared across instances via Redis.

    Fails open on Redis errors: a Redis outage must not turn every request into
    a 500 — the infra-level limiter (nginx ``limit_req``) remains as a backstop.
    """

    def __init__(self) -> None:
        self._member_seq = 0

    async def hit(self, key: str, limit: int) -> tuple[bool, int]:
        now_ms = int(time.time() * 1000)
        # Unique member so simultaneous hits in the same millisecond don't collide.
        self._member_seq += 1
        member = f"{now_ms}-{self._member_seq}"
        try:
            # ARGV are passed as strings (redis coerces them); Lua tonumber() reads
            # them back. The script returns a two-element list [rejected, retry].
            # redis-py's async eval is typed as returning str|Awaitable[str]; cast
            # to the real awaitable-of-list shape.
            result = await cast(
                "Awaitable[list[int]]",
                get_redis().eval(
                    _SLIDING_WINDOW_LUA, 1, key, str(now_ms), str(_WINDOW_MS), str(limit), member
                ),
            )
        except RedisError:
            return True, 0
        rejected, retry_after = result
        return not rejected, int(retry_after)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Per-IP sliding-window rate limit, with a stricter bucket for the login endpoint.

    Backend is chosen by ``settings.rate_limit_backend`` (``memory`` or
    ``redis``). ``redis`` shares state across containers behind a load balancer;
    ``memory`` is per-process and suits single-instance deployments. Either way
    this complements (does not replace) an infrastructure-level limit such as
    nginx ``limit_req`` when one is added in front.
    """

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)
        backend = get_settings().rate_limit_backend.strip().lower()
        self._window = _RedisWindow() if backend == "redis" else _MemoryWindow()

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        settings = get_settings()
        if not settings.rate_limit_enabled:
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        is_login = request.url.path == f"{settings.api_v1_prefix}/auth/login"
        if is_login:
            limit = settings.rate_limit_login_per_minute
            key = f"rl:{client_ip}:login"
        else:
            limit = settings.rate_limit_per_minute
            key = f"rl:{client_ip}"

        allowed, retry_after = await self._window.hit(key, limit)
        if not allowed:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests"},
                headers={"Retry-After": str(retry_after)},
            )
        return await call_next(request)
