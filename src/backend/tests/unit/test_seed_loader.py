import bcrypt

from app.services.seed import (
    DEFAULT_SEED_PASSWORD,
    hash_seed_password,
    load_seed_payloads,
    normalize_course,
    normalize_user,
    seed_uuid,
)


def test_loads_expected_seed_counts() -> None:
    payloads = load_seed_payloads()

    assert len(payloads.courses) == 27
    assert len(payloads.users) == 6
    assert len(payloads.reviewer_assignments) == 3


def test_normalizes_course_description_typo() -> None:
    payloads = load_seed_payloads()
    raw_course = next(course for course in payloads.courses if course["course_code"] == "IT3312E")

    course = normalize_course(raw_course)

    assert course["code"] == "IT3312E"
    assert course["description"] == raw_course["decription"]


def test_seed_user_uuid_is_deterministic() -> None:
    assert seed_uuid("admin-001") == seed_uuid("admin-001")
    assert seed_uuid("admin-001") != seed_uuid("reviewer-001")


def test_normalizes_user_with_default_password_hash() -> None:
    password_hash = hash_seed_password()
    user = normalize_user(
        {
            "user_id": "reviewer-001",
            "email": "reviewer.linhnt@soict.hust.edu.vn",
            "full_name": "Reviewer",
            "role": "reviewer",
            "note": "ignored by backend schema",
        },
        password_hash,
    )

    assert user["id"] == seed_uuid("reviewer-001")
    assert user["role"] == "reviewer"
    assert "note" not in user
    assert bcrypt.checkpw(DEFAULT_SEED_PASSWORD.encode("utf-8"), password_hash.encode("utf-8"))
