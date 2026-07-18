from __future__ import annotations

import pytest


@pytest.mark.skip(reason="requires db")
async def test_create_course_valid() -> None:
    pass


@pytest.mark.skip(reason="requires db")
async def test_create_course_invalid_sla() -> None:
    pass


@pytest.mark.skip(reason="requires db")
async def test_list_courses() -> None:
    pass


@pytest.mark.skip(reason="requires db")
async def test_update_course() -> None:
    pass


@pytest.mark.skip(reason="requires db")
async def test_assign_reviewer_student_rejected() -> None:
    pass


@pytest.mark.skip(reason="requires db")
async def test_assign_reviewer_valid() -> None:
    pass


@pytest.mark.skip(reason="requires db")
async def test_unassign_reviewer() -> None:
    pass


@pytest.mark.skip(reason="requires db")
async def test_regen_topic_tags() -> None:
    pass
