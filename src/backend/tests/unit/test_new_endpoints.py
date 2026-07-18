from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4, UUID
from typing import Any, AsyncIterator
from unittest.mock import MagicMock
import pytest
from httpx import ASGITransport, AsyncClient

from app.core.auth import create_access_token, hash_password
from app.db.session import get_session
from app.main import app
from app.models import ChatMessage, ChatSession, Course, EvaluationReport, ReviewDecision, User
from app.models.enums import ChatRole


class FakeDBSession:
    def __init__(self, user: User | None = None, scalar_value: Any = None, scalars_value: list[Any] = None) -> None:
        self.user = user
        self.scalar_value = scalar_value
        self.scalars_value = scalars_value or []
        self.added: list[Any] = []
        self.deleted: list[Any] = []
        self.committed = False

    async def scalar(self, statement) -> Any:
        stmt_str = str(statement).lower()
        if "users" in stmt_str and "where users.id =" in stmt_str and self.user:
            return self.user
        return self.scalar_value

    async def execute(self, statement) -> Any:
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = self.scalars_value
        
        mock_res = MagicMock()
        mock_res.scalars.return_value = mock_scalars
        return mock_res

    def add(self, item: Any) -> None:
        self.added.append(item)

    async def delete(self, item: Any) -> None:
        self.deleted.append(item)

    async def commit(self) -> None:
        self.committed = True

    async def refresh(self, item: Any) -> None:
        pass


def make_user(role: str = "student") -> User:
    return User(
        id=uuid4(),
        email=f"{role}_{uuid4().hex[:4]}@example.test",
        hashed_password=hash_password("password123"),
        role=role,
        full_name=f"{role.title()} User",
        is_active=True,
    )


def override_session_helper(session: FakeDBSession):
    async def dependency() -> AsyncIterator[FakeDBSession]:
        yield session
    return dependency


@pytest.mark.asyncio
async def test_list_chat_sessions() -> None:
    student = make_user("student")
    course = Course(id=uuid4(), code="CS101", name="Intro to CS", review_sla_hours=48)
    session_obj = ChatSession(
        id=uuid4(),
        user_id=student.id,
        course_id=course.id,
        summary="A summary",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    session_obj.course = course
    
    fake_db = FakeDBSession(user=student, scalars_value=[session_obj])
    app.dependency_overrides[get_session] = override_session_helper(fake_db)
    token = create_access_token(student)
    
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/tutor/sessions", headers={"Authorization": f"Bearer {token}"})
    finally:
        app.dependency_overrides.clear()
        
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == str(session_obj.id)
    assert data[0]["course_code"] == "CS101"


@pytest.mark.asyncio
async def test_get_session_messages() -> None:
    student = make_user("student")
    session_id = uuid4()
    chat_session = ChatSession(
        id=session_id,
        user_id=student.id,
        course_id=uuid4(),
        summary="Summary",
    )
    
    message = ChatMessage(
        id=uuid4(),
        session_id=session_id,
        role=ChatRole.USER,
        content="Hello Tutor",
        citations=[],
        created_at=datetime.now(timezone.utc),
    )
    
    class CustomFakeSession(FakeDBSession):
        async def scalar(self, statement) -> Any:
            stmt_str = str(statement).lower()
            if "users" in stmt_str and self.user:
                return self.user
            if "chat_sessions" in stmt_str:
                return chat_session
            return None
            
    fake_db = CustomFakeSession(user=student, scalars_value=[message])
    app.dependency_overrides[get_session] = override_session_helper(fake_db)
    token = create_access_token(student)
    
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get(
                f"/api/v1/tutor/sessions/{session_id}/messages",
                headers={"Authorization": f"Bearer {token}"}
            )
    finally:
        app.dependency_overrides.clear()
        
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == str(message.id)
    assert data[0]["content"] == "Hello Tutor"


@pytest.mark.asyncio
async def test_delete_chat_session() -> None:
    student = make_user("student")
    session_id = uuid4()
    chat_session = ChatSession(
        id=session_id,
        user_id=student.id,
        course_id=uuid4(),
        summary="Summary",
    )
    
    class CustomFakeSession(FakeDBSession):
        async def scalar(self, statement) -> Any:
            stmt_str = str(statement).lower()
            if "users" in stmt_str and self.user:
                return self.user
            if "chat_sessions" in stmt_str:
                return chat_session
            return None
            
    fake_db = CustomFakeSession(user=student)
    app.dependency_overrides[get_session] = override_session_helper(fake_db)
    token = create_access_token(student)
    
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.delete(
                f"/api/v1/tutor/sessions/{session_id}",
                headers={"Authorization": f"Bearer {token}"}
            )
    finally:
        app.dependency_overrides.clear()
        
    assert response.status_code == 204
    assert chat_session in fake_db.deleted
    assert fake_db.committed


@pytest.mark.asyncio
async def test_admin_list_users() -> None:
    admin = make_user("admin")
    student = make_user("student")
    
    fake_db = FakeDBSession(user=admin, scalars_value=[admin, student])
    app.dependency_overrides[get_session] = override_session_helper(fake_db)
    token = create_access_token(admin)
    
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/admin/users", headers={"Authorization": f"Bearer {token}"})
    finally:
        app.dependency_overrides.clear()
        
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    emails = [u["email"] for u in data]
    assert admin.email in emails
    assert student.email in emails


class _AdminUpdateUserFakeSession(FakeDBSession):
    """Distinguishes the auth lookup (filters on is_active) from the
    endpoint's own target-user lookup (no is_active filter) so a self-update
    test can supply a different target user than the authenticated admin."""

    def __init__(self, admin: User, target: User) -> None:
        super().__init__(user=admin)
        self._target = target

    async def scalar(self, statement) -> Any:
        stmt_str = str(statement).lower()
        if "users" in stmt_str and "is_active is true" in stmt_str:
            return self.user
        if "users" in stmt_str and "where users.id =" in stmt_str:
            return self._target
        return self.scalar_value


@pytest.mark.asyncio
async def test_admin_update_user_role_success() -> None:
    admin = make_user("admin")
    student = make_user("student")
    fake_db = _AdminUpdateUserFakeSession(admin, student)
    app.dependency_overrides[get_session] = override_session_helper(fake_db)
    token = create_access_token(admin)

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.patch(
                f"/api/v1/admin/users/{student.id}",
                json={"role": "reviewer"},
                headers={"Authorization": f"Bearer {token}"},
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["role"] == "reviewer"
    assert student.role == "reviewer"
    assert fake_db.committed


@pytest.mark.asyncio
async def test_admin_deactivate_user_success() -> None:
    admin = make_user("admin")
    student = make_user("student")
    fake_db = _AdminUpdateUserFakeSession(admin, student)
    app.dependency_overrides[get_session] = override_session_helper(fake_db)
    token = create_access_token(admin)

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.patch(
                f"/api/v1/admin/users/{student.id}",
                json={"is_active": False},
                headers={"Authorization": f"Bearer {token}"},
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["is_active"] is False
    assert student.is_active is False


@pytest.mark.asyncio
async def test_admin_cannot_demote_self() -> None:
    admin = make_user("admin")
    fake_db = _AdminUpdateUserFakeSession(admin, admin)
    app.dependency_overrides[get_session] = override_session_helper(fake_db)
    token = create_access_token(admin)

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.patch(
                f"/api/v1/admin/users/{admin.id}",
                json={"role": "student"},
                headers={"Authorization": f"Bearer {token}"},
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 400
    assert admin.role == "admin"


@pytest.mark.asyncio
async def test_admin_cannot_deactivate_self() -> None:
    admin = make_user("admin")
    fake_db = _AdminUpdateUserFakeSession(admin, admin)
    app.dependency_overrides[get_session] = override_session_helper(fake_db)
    token = create_access_token(admin)

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.patch(
                f"/api/v1/admin/users/{admin.id}",
                json={"is_active": False},
                headers={"Authorization": f"Bearer {token}"},
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 400
    assert admin.is_active is True


@pytest.mark.asyncio
async def test_admin_update_user_not_found() -> None:
    admin = make_user("admin")

    class _NotFoundFakeSession(FakeDBSession):
        async def scalar(self, statement) -> Any:
            stmt_str = str(statement).lower()
            if "users" in stmt_str and "is_active is true" in stmt_str:
                return self.user
            return None

    fake_db = _NotFoundFakeSession(user=admin)
    app.dependency_overrides[get_session] = override_session_helper(fake_db)
    token = create_access_token(admin)

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.patch(
                f"/api/v1/admin/users/{uuid4()}",
                json={"role": "reviewer"},
                headers={"Authorization": f"Bearer {token}"},
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_admin_update_user_requires_admin_role() -> None:
    student = make_user("student")
    fake_db = FakeDBSession(user=student)
    app.dependency_overrides[get_session] = override_session_helper(fake_db)
    token = create_access_token(student)

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.patch(
                f"/api/v1/admin/users/{uuid4()}",
                json={"role": "reviewer"},
                headers={"Authorization": f"Bearer {token}"},
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_reviewer_analytics() -> None:
    reviewer = make_user("reviewer")
    course = Course(id=uuid4(), code="IT3040", name="Math", review_sla_hours=36)
    
    from datetime import datetime, UTC, timedelta
    decided_time = datetime.now(UTC) + timedelta(hours=36)
    report = EvaluationReport(
        id=uuid4(),
        final_recommendation="APPROVE",
    )
    decision1 = ReviewDecision(
        id=uuid4(),
        decision="APPROVE",
        evaluation_report=report,
        decided_at=decided_time,
    )
    
    class CustomFakeSession(FakeDBSession):
        async def scalar(self, statement) -> Any:
            stmt_str = str(statement).lower()
            if "users" in stmt_str and self.user:
                return self.user
            return None
            
        async def execute(self, statement) -> Any:
            stmt_str = str(statement).lower()
            mock_scalars = MagicMock()
            mock_res = MagicMock()
            
            if "courses" in stmt_str and "review_decision" in stmt_str:
                from app.models import Document
                doc = Document(id=uuid4(), course_id=course.id, sla_deadline=decided_time)
                mock_res.all.return_value = [(decision1, report, doc, course)]
            elif "courses" in stmt_str:
                mock_scalars.all.return_value = [course]
            elif "review_decision" in stmt_str:
                mock_scalars.all.return_value = [decision1]
            else:
                mock_scalars.all.return_value = []
                mock_res.all.return_value = []
            
            mock_res.scalars.return_value = mock_scalars
            return mock_res
            
    fake_db = CustomFakeSession(user=reviewer)
    app.dependency_overrides[get_session] = override_session_helper(fake_db)
    token = create_access_token(reviewer)
    
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/review/analytics", headers={"Authorization": f"Bearer {token}"})
    finally:
        app.dependency_overrides.clear()
        
    assert response.status_code == 200
    data = response.json()
    assert data["average_sla_hours_per_course"]["IT3040"] == 36.0
    assert data["ai_agreement_rate"] == 1.0
    assert data["ai_override_rate"] == 0.0


@pytest.mark.asyncio
async def test_upload_community_document_rejects_missing_consent() -> None:
    student = make_user("student")
    fake_db = FakeDBSession(user=student)
    app.dependency_overrides[get_session] = override_session_helper(fake_db)
    token = create_access_token(student)

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/documents/community",
                headers={"Authorization": f"Bearer {token}"},
                data={
                    "course_code": "IT3160E",
                    "contribution_type": "summary_note",
                    "topic_tags": "[]",
                    # shared_rights_confirmed intentionally omitted
                },
                files={"file": ("note.pdf", b"%PDF-1.4 test", "application/pdf")},
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_upload_community_document_rejects_false_consent() -> None:
    student = make_user("student")
    fake_db = FakeDBSession(user=student)
    app.dependency_overrides[get_session] = override_session_helper(fake_db)
    token = create_access_token(student)

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/documents/community",
                headers={"Authorization": f"Bearer {token}"},
                data={
                    "course_code": "IT3160E",
                    "contribution_type": "summary_note",
                    "topic_tags": "[]",
                    "shared_rights_confirmed": "false",
                },
                files={"file": ("note.pdf", b"%PDF-1.4 test", "application/pdf")},
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 422
