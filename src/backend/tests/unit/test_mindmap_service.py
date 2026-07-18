from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.services.mindmap_service import _parse_concept_graph


def test_parse_concept_graph_valid_json() -> None:
    text = (
        '{"nodes": [{"id": "n1", "label": "AI", "topic": "tech"}],'
        ' "edges": [{"source": "n1", "target": "n2", "relation": "related"}]}'
    )
    result = _parse_concept_graph(text)
    assert len(result["nodes"]) == 1
    assert result["nodes"][0]["label"] == "AI"


def test_parse_concept_graph_json_in_prose() -> None:
    text = 'Here is the graph: {"nodes": [], "edges": []} — as requested.'
    result = _parse_concept_graph(text)
    assert result["nodes"] == []
    assert result["edges"] == []


def test_parse_concept_graph_invalid_returns_empty() -> None:
    result = _parse_concept_graph("not json at all")
    assert result == {"nodes": [], "edges": []}


def test_parse_concept_graph_missing_keys_returns_empty() -> None:
    result = _parse_concept_graph('{"wrong_key": []}')
    assert result["nodes"] == []
    assert result["edges"] == []


def test_parse_concept_graph_drops_dangling_edges() -> None:
    text = (
        '{"nodes": [{"id": "n1", "label": "AI", "topic": "t"}, {"id": "n2", "label": "ML", "topic": "t"}],'
        ' "edges": [{"source": "n1", "target": "n2", "relation": "includes"},'
        ' {"source": "n1", "target": "n99", "relation": "broken"},'
        ' {"source": "n0", "target": "n2", "relation": "broken"}]}'
    )
    result = _parse_concept_graph(text)
    assert len(result["nodes"]) == 2
    assert len(result["edges"]) == 1
    assert result["edges"][0]["target"] == "n2"


@pytest.mark.asyncio
async def test_generate_via_llm_uses_structured_output() -> None:
    from app.services.mindmap_service import _generate_via_llm

    course = MagicMock(code="IT3160E", name="AI Course", topic_summary=None)
    summary = MagicMock(overall_summary="Search algorithms and heuristics.")
    mock_router = AsyncMock()
    mock_router.chat = AsyncMock(return_value=MagicMock(content='{"nodes": [], "edges": []}'))

    result = await _generate_via_llm(AsyncMock(), course, [summary], mock_router)

    assert result == {"nodes": [], "edges": []}
    assert mock_router.chat.call_args.kwargs["schema"] is not None


@pytest.mark.asyncio
async def test_mindmap_no_indexed_docs_returns_empty_graph() -> None:
    from app.services.mindmap_service import get_or_generate_mindmap

    mock_session = AsyncMock()
    course = MagicMock(id=uuid4(), code="IT3160E", name="AI Course", topic_summary=None, is_active=True)
    mock_session.scalar = AsyncMock(return_value=course)
    mock_session.execute = AsyncMock(return_value=MagicMock(scalars=MagicMock(return_value=iter([]))))

    def execute_side_effect(stmt: object, *args: object, **kwargs: object) -> MagicMock:
        result = MagicMock()
        result.__iter__ = lambda self: iter([])
        result.scalars = MagicMock(return_value=iter([]))
        return result

    mock_session.execute = AsyncMock(side_effect=execute_side_effect)
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    mock_session.add = MagicMock()

    mock_router = AsyncMock()

    result = await get_or_generate_mindmap(
        session=mock_session,
        course_code="IT3160E",
        force_regen=True,
        llm_router=mock_router,
    )

    assert result.concept_graph["nodes"] == []
    assert result.concept_graph["edges"] == []
    mock_router.chat.assert_not_called()


@pytest.mark.asyncio
async def test_mindmap_uses_cache_when_not_force_regen() -> None:
    from datetime import UTC, datetime

    from app.services.mindmap_service import get_or_generate_mindmap

    cached_graph = {"nodes": [{"id": "n1", "label": "Cached", "topic": "t"}], "edges": []}
    cached_artifact = MagicMock(
        concept_graph=cached_graph,
        is_cached=True,
        generated_at=datetime.now(UTC),
    )

    mock_session = AsyncMock()
    course = MagicMock(id=uuid4(), code="IT3160E")

    call_count = 0

    def scalar_side(stmt: object) -> object:
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return course
        return cached_artifact

    mock_session.scalar = AsyncMock(side_effect=scalar_side)
    mock_router = AsyncMock()

    result = await get_or_generate_mindmap(
        session=mock_session,
        course_code="IT3160E",
        force_regen=False,
        llm_router=mock_router,
    )

    assert result.is_cached is True
    assert result.concept_graph["nodes"][0]["label"] == "Cached"
    mock_router.chat.assert_not_called()
