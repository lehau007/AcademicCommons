from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID, uuid5

import bcrypt
from sqlalchemy import select, text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Course, CourseReviewerAssignment, User

SEED_NAMESPACE = UUID("73bc8d82-7f28-4b9c-bf45-d6fca9e3f4be")
DEFAULT_SEED_PASSWORD = "changeme123"


@dataclass(frozen=True)
class SeedPayloads:
    courses: list[dict[str, Any]]
    users: list[dict[str, Any]]
    reviewer_assignments: list[dict[str, Any]]


@dataclass(frozen=True)
class SeedResult:
    courses: int
    users: int
    reviewer_assignments: int


def seed_data_dir() -> Path:
    parents = list(Path(__file__).resolve().parents)
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "data" / "seed"
        if candidate.exists():
            return candidate
    if len(parents) > 4:
        return parents[4] / "data" / "seed"
    return Path.cwd() / "data" / "seed"


def seed_uuid(external_id: str) -> UUID:
    return uuid5(SEED_NAMESPACE, external_id)


def load_seed_payloads(seed_dir: Path | None = None) -> SeedPayloads:
    base = seed_dir or seed_data_dir()
    return SeedPayloads(
        courses=_load_json_list(base / "courses.json"),
        users=_load_json_list(base / "users.json"),
        reviewer_assignments=_load_json_list(base / "reviewer_assignments.json"),
    )


async def seed_database(session: AsyncSession, seed_dir: Path | None = None) -> SeedResult:
    payloads = load_seed_payloads(seed_dir)

    await _upsert_courses(session, payloads.courses)
    await _upsert_users(session, payloads.users)
    await _upsert_reviewer_assignments(session, payloads.reviewer_assignments)
    await session.commit()

    return SeedResult(
        courses=len(payloads.courses),
        users=len(payloads.users),
        reviewer_assignments=len(payloads.reviewer_assignments),
    )


def _tags_from_summary(text: str | None) -> list[str]:
    if not text:
        return []
    sep = ";" if ";" in text else ","
    parts = text.split(sep)
    return [p.strip() for p in parts if p.strip()][:10]


def normalize_course(raw: dict[str, Any]) -> dict[str, Any]:
    code = _required_str(raw, "course_code")
    description = raw.get("description") or raw.get("decription")
    topic_summary = raw.get("topic_summary")
    topic_tags = raw.get("topic_tags") or _tags_from_summary(topic_summary) or _tags_from_summary(description)
    return {
        "code": code,
        "name": _required_str(raw, "name"),
        "description": description,
        "topic_summary": topic_summary,
        "short_description": raw.get("short_description"),
        "topic_tags": topic_tags,
        "is_active": raw.get("is_active", True),
    }


def normalize_user(raw: dict[str, Any], password_hash: str) -> dict[str, Any]:
    external_id = _required_str(raw, "user_id")
    return {
        "id": seed_uuid(external_id),
        "email": _required_str(raw, "email"),
        "hashed_password": password_hash,
        "role": _required_str(raw, "role"),
        "full_name": raw.get("full_name"),
        "is_active": raw.get("is_active", True),
        # Operator-controlled demo mailboxes; skip the email-verification round-trip.
        "is_email_verified": True,
    }


def hash_seed_password(password: str = DEFAULT_SEED_PASSWORD) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


async def _upsert_courses(session: AsyncSession, raw_courses: list[dict[str, Any]]) -> None:
    for raw_course in raw_courses:
        values = normalize_course(raw_course)
        statement = insert(Course).values(**values)
        await session.execute(
            statement.on_conflict_do_update(
                index_elements=[Course.code],
                set_={
                    "name": statement.excluded.name,
                    "description": statement.excluded.description,
                    "topic_summary": statement.excluded.topic_summary,
                    "short_description": statement.excluded.short_description,
                    "topic_tags": statement.excluded.topic_tags,
                    "is_active": statement.excluded.is_active,
                    "updated_at": datetime.now().astimezone(),
                },
            )
        )


async def _upsert_users(session: AsyncSession, raw_users: list[dict[str, Any]]) -> None:
    password_hash = hash_seed_password()
    for raw_user in raw_users:
        values = normalize_user(raw_user, password_hash)
        statement = insert(User).values(**values)
        await session.execute(
            statement.on_conflict_do_update(
                index_elements=[User.email],
                set_={
                    "role": statement.excluded.role,
                    "full_name": statement.excluded.full_name,
                    "is_active": statement.excluded.is_active,
                    "is_email_verified": True,
                    "updated_at": datetime.now().astimezone(),
                },
            )
        )


async def _upsert_reviewer_assignments(
    session: AsyncSession,
    raw_assignments: list[dict[str, Any]],
) -> None:
    course_ids = await _course_ids_by_code(session)
    user_roles = await _user_roles_by_id(session)

    for raw_assignment in raw_assignments:
        user_id = seed_uuid(_required_str(raw_assignment, "user_id"))
        course_code = _required_str(raw_assignment, "course_code")
        assigned_by = seed_uuid(_required_str(raw_assignment, "assigned_by"))
        course_id = course_ids.get(course_code)
        if course_id is None:
            raise ValueError(f"Reviewer assignment references unknown course_code={course_code!r}")
        if user_roles.get(user_id) != "reviewer":
            raise ValueError(f"Reviewer assignment user_id={user_id!s} must reference a reviewer")
        if user_roles.get(assigned_by) != "admin":
            raise ValueError(f"Reviewer assignment assigned_by={assigned_by!s} must reference an admin")

        assigned_at = datetime.fromisoformat(_required_str(raw_assignment, "assigned_at"))
        is_active = bool(raw_assignment.get("is_active", True))
        values = {
            "user_id": user_id,
            "course_id": course_id,
            "assigned_by": assigned_by,
            "assigned_at": assigned_at,
            "is_active": is_active,
        }
        statement = insert(CourseReviewerAssignment).values(**values)
        await session.execute(
            statement.on_conflict_do_update(
                index_elements=[
                    CourseReviewerAssignment.user_id,
                    CourseReviewerAssignment.course_id,
                ],
                index_where=text("is_active = TRUE"),
                set_={
                    "assigned_by": statement.excluded.assigned_by,
                    "assigned_at": statement.excluded.assigned_at,
                    "is_active": statement.excluded.is_active,
                    "unassigned_at": None,
                },
            )
        )


async def _course_ids_by_code(session: AsyncSession) -> dict[str, UUID]:
    rows = await session.execute(select(Course.code, Course.id))
    return {code: course_id for code, course_id in rows}


async def _user_roles_by_id(session: AsyncSession) -> dict[UUID, str]:
    rows = await session.execute(select(User.id, User.role))
    return {user_id: role for user_id, role in rows}


def _load_json_list(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"{path} must contain a JSON array")
    if not all(isinstance(item, dict) for item in data):
        raise ValueError(f"{path} must contain only JSON objects")
    return data


def _required_str(raw: dict[str, Any], key: str) -> str:
    value = raw.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"Missing required seed field: {key}")
    return value
