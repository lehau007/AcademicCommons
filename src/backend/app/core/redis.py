"""Process-wide Redis client backed by a single connection pool.

Rationale: opening ``Redis.from_url(...)`` per call (and closing it in a
``finally``) forces a fresh TCP/SSL handshake every time and churns ephemeral
ports under load. A shared :class:`~redis.asyncio.ConnectionPool` lets all
callers (email verification, rate limiting, ...) borrow and return connections
instead. The client is created lazily on first use and closed once at app
shutdown via :func:`close_redis` (wired into the FastAPI lifespan).
"""

from __future__ import annotations

from redis.asyncio import ConnectionPool, Redis

from app.config import get_settings

_pool: ConnectionPool | None = None
_client: Redis | None = None


def get_redis() -> Redis:
    """Return the shared Redis client, creating the pool on first call."""
    global _pool, _client
    if _client is None:
        settings = get_settings()
        _pool = ConnectionPool.from_url(settings.redis_url, decode_responses=True)
        _client = Redis(connection_pool=_pool)
    return _client


async def close_redis() -> None:
    """Close the shared client and pool. Safe to call when never initialised."""
    global _pool, _client
    if _client is not None:
        await _client.aclose()
        _client = None
    if _pool is not None:
        await _pool.aclose()
        _pool = None
