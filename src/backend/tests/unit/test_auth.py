from collections.abc import AsyncIterator
from typing import Any
from uuid import uuid4

import pytest

# Patch the shared Redis client used by email_verification to an in-memory
# fakeredis-style stub BEFORE importing the app, so the auth routes hit the
# stub and never touch a real Redis server. We build a minimal AsyncKV shim
# rather than pull in the `fakeredis` dependency.
import app.services.email_verification as ev_mod
from app.core.auth import create_access_token, hash_password, verify_password
from app.db.session import get_session
from app.main import app
from app.models import User


class _AsyncRedisStub:
    def __init__(self) -> None:
        self.store: dict[str, tuple[str, int | None]] = {}
        self.set_calls: list[dict[str, Any]] = []

    def from_url(self, *_a: Any, **_kw: Any) -> "_AsyncRedisStub":
        return self

    async def set(self, key: str, value: str, ex: int | None = None, nx: bool = False) -> bool:
        if nx and key in self.store:
            return False
        self.store[key] = (value, ex)
        self.set_calls.append({"key": key, "value": value, "ex": ex, "nx": nx})
        return True

    async def get(self, key: str) -> str | None:
        entry = self.store.get(key)
        return entry[0] if entry is not None else None

    async def delete(self, key: str) -> int:
        return 1 if self.store.pop(key, None) is not None else 0

    async def aclose(self) -> None:
        return None


_STUB = _AsyncRedisStub()


@pytest.fixture(autouse=True)
def _redis_stub() -> None:
    _STUB.store.clear()
    _STUB.set_calls.clear()


# Swap the shared get_redis() used inside email_verification for our stub.
ev_mod.get_redis = lambda: _STUB  # type: ignore[assignment]


# ---------------------------------------------------------------------------
# DB session stub (mirrors the existing FakeSession pattern in this file).
# ---------------------------------------------------------------------------


class FakeSession:
    def __init__(self, user: User | None) -> None:
        self.user = user
        self.committed = False

    async def scalar(self, statement) -> User | None:
        try:
            params = statement.compile().params
            email_val = next((v for k, v in params.items() if k.startswith("email")), None)
            if email_val is not None:
                if self.user and email_val == self.user.email:
                    return self.user
                return None
        except Exception:
            pass
        return self.user

    async def get(self, _model: type, pk: Any) -> User | None:
        if self.user is not None and getattr(self.user, "id", None) == pk:
            return self.user
        return None

    def add(self, instance: Any) -> None:
        # Pretend the INSERT succeeded with the in-memory user object.
        self.user = instance

    async def commit(self) -> None:
        self.committed = True
        if self.user is not None and getattr(self.user, "id", None) is None:
            self.user.id = uuid4()

    async def refresh(self, instance: Any) -> None:
        if getattr(instance, "id", None) is None:
            instance.id = uuid4()


def make_user(role: str = "student", is_email_verified: bool = True) -> User:
    return User(
        id=uuid4(),
        email=f"{role}@example.test",
        hashed_password=hash_password("password123"),
        role=role,
        full_name=f"{role.title()} User",
        is_email_verified=is_email_verified,
    )


def override_session(user: User | None):
    async def dependency() -> AsyncIterator[FakeSession]:
        yield FakeSession(user)

    return dependency


@pytest.mark.asyncio
async def test_password_hash_verifies() -> None:
    password_hash = hash_password("password123")

    assert verify_password("password123", password_hash)
    assert not verify_password("wrong-password", password_hash)


@pytest.mark.asyncio
async def test_me_requires_token() -> None:
    from httpx import ASGITransport, AsyncClient

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/auth/me")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_returns_current_user_with_valid_token() -> None:
    from httpx import ASGITransport, AsyncClient

    user = make_user()
    app.dependency_overrides[get_session] = override_session(user)
    token = create_access_token(user)

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["id"] == str(user.id)
    assert response.json()["role"] == "student"
    assert response.json()["is_email_verified"] is True


@pytest.mark.asyncio
async def test_register_creates_unverified_user_and_stores_token() -> None:
    from httpx import ASGITransport, AsyncClient

    # Pre-existing user query must return None (no email collision).
    app.dependency_overrides[get_session] = override_session(None)

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/auth/register",
                json={
                    "email": "new@example.test",
                    "password": "password123",
                    "role": "student",
                    "full_name": "New Student",
                },
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "new@example.test"
    assert data["role"] == "student"
    assert data["is_email_verified"] is False

    # The register flow must have created a Redis-backed token for verification.
    token_keys = [key for key in _STUB.store if key.startswith("email_verify:")]
    assert len(token_keys) == 1
    # And the token should map to a user id value.
    user_id_value = _STUB.store[token_keys[0]][0]
    assert user_id_value is not None and len(user_id_value) > 0


@pytest.mark.asyncio
async def test_login_blocked_when_email_not_verified() -> None:
    from httpx import ASGITransport, AsyncClient

    user = make_user(is_email_verified=False)
    app.dependency_overrides[get_session] = override_session(user)

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/auth/login",
                json={"email": user.email, "password": "password123"},
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 403
    assert response.json()["detail"] == "email_not_verified"


@pytest.mark.asyncio
async def test_verify_email_redeems_token_and_marks_verified() -> None:
    from httpx import ASGITransport, AsyncClient

    user = make_user(is_email_verified=False)
    # Seed a Redis-backed token bound to this user.
    token = await ev_mod.create_token(user.id)
    _STUB.store[f"email_verify:{token}"] = (str(user.id), None)

    user.is_email_verified = False
    app.dependency_overrides[get_session] = override_session(user)

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/api/v1/auth/verify-email", params={"token": token})
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["verified"] is True
    assert response.json()["user"]["is_email_verified"] is True
    # Single-shot: the consumed token must have been removed.
    assert f"email_verify:{token}" not in _STUB.store


@pytest.mark.asyncio
async def test_verify_email_rejects_invalid_token() -> None:
    from httpx import ASGITransport, AsyncClient

    app.dependency_overrides[get_session] = override_session(None)

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/api/v1/auth/verify-email", params={"token": "never-issued"})
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_resend_verification_does_not_leak_email_exists() -> None:
    from httpx import ASGITransport, AsyncClient

    # No user with this email — must still return ok=true (no enumeration signal).
    app.dependency_overrides[get_session] = override_session(None)

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/auth/resend-verification",
                json={"email": "nobody@example.test"},
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["ok"] is True
    # No token should have been written for a non-existent user.
    token_keys = [key for key in _STUB.store if key.startswith("email_verify:")]
    assert token_keys == []


@pytest.mark.asyncio
async def test_resend_verification_enforces_cooldown() -> None:
    from httpx import ASGITransport, AsyncClient

    user = make_user(is_email_verified=False)
    app.dependency_overrides[get_session] = override_session(user)

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            first = await client.post(
                "/api/v1/auth/resend-verification",
                json={"email": user.email},
            )
            second = await client.post(
                "/api/v1/auth/resend-verification",
                json={"email": user.email},
            )
    finally:
        app.dependency_overrides.clear()

    assert first.status_code == 200
    assert second.status_code == 200  # ok regardless of cooldown

    # The cooldown NX means exactly one token+cooldown entry should exist.
    token_keys = [
        key for key in _STUB.store if key.startswith("email_verify:") and "cooldown:" not in key
    ]
    assert len(token_keys) == 1
    cooldown_keys = [key for key in _STUB.store if "cooldown:" in key]
    assert len(cooldown_keys) == 1


@pytest.mark.asyncio
async def test_invalid_token_returns_401() -> None:
    from httpx import ASGITransport, AsyncClient

    app.dependency_overrides[get_session] = override_session(make_user())

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/auth/me", headers={"Authorization": "Bearer bad-token"})
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 401