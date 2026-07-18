"""Shared pytest fixtures and hermetic test environment setup."""

import os

# Force the in-memory rate-limit backend for the test suite, regardless of what
# the developer's local `.env` selects. The `redis` backend borrows a
# process-wide asyncio Redis client (app.core.redis.get_redis) that binds to the
# event loop it was created on; pytest-asyncio spins up a fresh loop per test,
# so a cached middleware holding that client would raise "Event loop is closed"
# on the second test. The memory window is pure-Python and loop-agnostic.
# Tests that specifically exercise the redis backend opt back in explicitly
# (see tests/unit/test_rate_limit.py).
os.environ.setdefault("RATE_LIMIT_BACKEND", "memory")

from app.config import get_settings  # noqa: E402

get_settings.cache_clear()
