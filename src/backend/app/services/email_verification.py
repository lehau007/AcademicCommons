"""Ephemeral email-verification tokens stored in Redis.

Each issued token maps ``token -> user_id`` with a TTL
(``settings.email_verification_ttl_minutes``, default 60). Verification
atomically reads-then-deletes the token (one-shot use). A short
resend-cooldown key per user_id rate-limits ``/auth/resend-verification``
(default 60s).

Why Redis and not a DB table: tokens are short-lived OTPs — Redis' native TTL
handles expiry with zero cleanup. The only persistent state is the
``users.is_email_verified`` boolean column (see migration
``20260709_0003_users_add_is_email_verified``).
"""

from __future__ import annotations

import logging
import secrets
from typing import Final
from uuid import UUID

from redis.exceptions import RedisError

from app.config import get_settings
from app.core.redis import get_redis

logger = logging.getLogger(__name__)
settings = get_settings()

_TOKEN_PREFIX: Final[str] = "email_verify:"
_RESEND_COOLDOWN_PREFIX: Final[str] = "email_verify:cooldown:"


async def create_token(user_id: UUID) -> str:
    """Issue a single-use token for ``user_id`` and store it in Redis.

    Existing tokens for the same user are not invalidated — the newest one
    shadows earlier ones. After TTL expiry the entry disappears on its own.
    """
    token = secrets.token_urlsafe(32)
    try:
        await get_redis().set(
            f"{_TOKEN_PREFIX}{token}",
            str(user_id),
            ex=settings.email_verification_ttl_minutes * 60,
        )
    except RedisError as exc:
        logger.error("redis.create_token_failed user=%s err=%s", user_id, exc)
        raise
    return token


async def consume_token(token: str) -> UUID | None:
    """Return the user_id bound to ``token`` and delete it, or None if missing/expired.

    Single-shot: a token consumed here can never be replayed, even before its TTL.
    """
    try:
        client = get_redis()
        key = f"{_TOKEN_PREFIX}{token}"
        user_id_raw = await client.get(key)
        if user_id_raw is None:
            return None
        await client.delete(key)
        return UUID(user_id_raw)
    except RedisError as exc:
        logger.error("redis.consume_token_failed err=%s", exc)
        return None
    except (ValueError, TypeError):
        return None


async def set_resend_cooldown(user_id: UUID) -> bool:
    """Start the per-user resend cooldown. Returns False if a cooldown is already active."""
    try:
        ok = await get_redis().set(
            f"{_RESEND_COOLDOWN_PREFIX}{user_id}",
            "1",
            ex=settings.email_verification_resend_cooldown_seconds,
            nx=True,
        )
        return bool(ok)
    except RedisError as exc:
        logger.error("redis.set_cooldown_failed user=%s err=%s", user_id, exc)
        # Fail-open on Redis outage: resumes sending rather than blocking users.
        return True