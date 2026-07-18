from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.config import Settings
from app.core import rate_limit as rate_limit_module
from app.core.rate_limit import RateLimitMiddleware


def _make_settings(**overrides: object) -> Settings:
    return Settings(_env_file=None, **overrides)


def _client(settings: Settings, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setattr(rate_limit_module, "get_settings", lambda: settings)
    app = FastAPI()
    app.add_middleware(RateLimitMiddleware)

    @app.get("/ping")
    async def ping() -> dict[str, bool]:
        return {"ok": True}

    @app.post("/api/v1/auth/login")
    async def login() -> dict[str, bool]:
        return {"ok": True}

    return TestClient(app)


def test_global_limit_returns_429_with_retry_after(monkeypatch: pytest.MonkeyPatch) -> None:
    client = _client(_make_settings(rate_limit_per_minute=3), monkeypatch)
    for _ in range(3):
        assert client.get("/ping").status_code == 200
    res = client.get("/ping")
    assert res.status_code == 429
    assert int(res.headers["Retry-After"]) >= 1


def test_login_has_stricter_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    settings = _make_settings(rate_limit_per_minute=100, rate_limit_login_per_minute=2)
    client = _client(settings, monkeypatch)
    for _ in range(2):
        assert client.post("/api/v1/auth/login").status_code == 200
    assert client.post("/api/v1/auth/login").status_code == 429
    # Login throttling must not consume the global bucket for other routes.
    assert client.get("/ping").status_code == 200


def test_disabled_flag_bypasses_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    settings = _make_settings(rate_limit_enabled=False, rate_limit_per_minute=1)
    client = _client(settings, monkeypatch)
    for _ in range(5):
        assert client.get("/ping").status_code == 200


class _FakeRedis:
    """Minimal async stand-in whose ``eval`` emulates the sliding-window Lua.

    Real atomicity/expiry is exercised by the integration suite against a live
    Redis; here we only need the same admit/reject + retry-after contract to
    verify the middleware wiring for the ``redis`` backend.
    """

    def __init__(self) -> None:
        self._zsets: dict[str, list[float]] = {}

    async def eval(self, _script: str, _numkeys: int, key: str, *args: object) -> list[int]:
        now, window, limit = int(args[0]), int(args[1]), int(args[2])
        scores = [s for s in self._zsets.get(key, []) if s > now - window]
        if len(scores) >= limit:
            retry = max(1, -(-(int(scores[0]) + window - now) // 1000))  # ceil ms->s
            self._zsets[key] = scores
            return [1, retry]
        scores.append(now)
        self._zsets[key] = scores
        return [0, 0]


def test_redis_backend_limits_via_shared_store(monkeypatch: pytest.MonkeyPatch) -> None:
    settings = _make_settings(rate_limit_backend="redis", rate_limit_per_minute=2)
    monkeypatch.setattr(rate_limit_module, "get_settings", lambda: settings)
    fake = _FakeRedis()
    monkeypatch.setattr(rate_limit_module, "get_redis", lambda: fake)

    app = FastAPI()
    app.add_middleware(RateLimitMiddleware)

    @app.get("/ping")
    async def ping() -> dict[str, bool]:
        return {"ok": True}

    client = TestClient(app)
    assert client.get("/ping").status_code == 200
    assert client.get("/ping").status_code == 200
    res = client.get("/ping")
    assert res.status_code == 429
    assert int(res.headers["Retry-After"]) >= 1


def test_redis_backend_fails_open_on_redis_error(monkeypatch: pytest.MonkeyPatch) -> None:
    from redis.exceptions import RedisError

    settings = _make_settings(rate_limit_backend="redis", rate_limit_per_minute=1)
    monkeypatch.setattr(rate_limit_module, "get_settings", lambda: settings)

    class _BrokenRedis:
        async def eval(self, *_a: object, **_kw: object) -> list[int]:
            raise RedisError("down")

    monkeypatch.setattr(rate_limit_module, "get_redis", lambda: _BrokenRedis())

    app = FastAPI()
    app.add_middleware(RateLimitMiddleware)

    @app.get("/ping")
    async def ping() -> dict[str, bool]:
        return {"ok": True}

    client = TestClient(app)
    # Redis unavailable → fail open, requests still served (infra limiter is the backstop).
    for _ in range(5):
        assert client.get("/ping").status_code == 200


def test_cors_origins_list_parses_comma_separated() -> None:
    settings = _make_settings(cors_origins="https://kb.example.com, http://localhost:3000 ,")
    assert settings.cors_origins_list == ["https://kb.example.com", "http://localhost:3000"]


def test_429_still_carries_cors_headers(monkeypatch: pytest.MonkeyPatch) -> None:
    from app import main as main_module

    settings = _make_settings(rate_limit_per_minute=1)
    monkeypatch.setattr(main_module, "get_settings", lambda: settings)
    monkeypatch.setattr(rate_limit_module, "get_settings", lambda: settings)
    client = TestClient(main_module.create_app())

    origin = {"Origin": "http://localhost:3000"}
    assert client.get("/health", headers=origin).status_code == 200
    res = client.get("/health", headers=origin)
    assert res.status_code == 429
    assert res.headers.get("access-control-allow-origin") == "http://localhost:3000"


def test_cors_origins_setting_controls_allowed_origin(monkeypatch: pytest.MonkeyPatch) -> None:
    from app import main as main_module

    settings = _make_settings(cors_origins="https://kb.example.com")
    monkeypatch.setattr(main_module, "get_settings", lambda: settings)
    monkeypatch.setattr(rate_limit_module, "get_settings", lambda: settings)
    client = TestClient(main_module.create_app())

    res = client.get("/health", headers={"Origin": "https://kb.example.com"})
    assert res.headers.get("access-control-allow-origin") == "https://kb.example.com"
    res = client.get("/health", headers={"Origin": "http://localhost:3000"})
    assert res.headers.get("access-control-allow-origin") is None
