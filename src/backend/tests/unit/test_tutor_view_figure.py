from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.config import get_settings
from app.models.enums import DocumentStatus, DocumentTier
from app.schemas.tutor import CitationResponse
from app.services import tutor_service
from app.services.tutor_service import (
    _AGENT_DECISION_SCHEMA,
    _VALID_TOOL_NAMES,
    _argument_keys,
    _excerpt,
    _execute_tool,
    _postprocess_answer,
)


def _chunk(document_id, content: str) -> SimpleNamespace:  # type: ignore[no-untyped-def]
    return SimpleNamespace(
        id=uuid4(), document_id=document_id, document_tier=DocumentTier.OFFICIAL, subtype="lecture_slides",
        section_title="Weighted graphs", page_number=13, chunk_order=4, content=content,
    )


def _setup(  # type: ignore[no-untyped-def]
    monkeypatch: pytest.MonkeyPatch, *, doc_status=DocumentStatus.INDEXED, same_course=True, chunk=None
):
    course = MagicMock()
    course.id = uuid4()
    doc = MagicMock()
    doc.id = uuid4()
    doc.course_id = course.id if same_course else uuid4()
    doc.status = doc_status
    session = MagicMock()
    session.scalar = AsyncMock(side_effect=[doc, chunk])  # the document, then the chunk holding the figure
    session.execute = AsyncMock(return_value=[(doc.id, "graph_presentation.pdf")])
    storage = MagicMock()
    storage.get_object = AsyncMock(return_value=b"png-bytes")
    monkeypatch.setattr(tutor_service, "get_storage", lambda: storage)
    viewer = MagicMock()
    viewer.ask = AsyncMock(return_value="The matrix row 1 is 0 3 0 5 0 0.")
    monkeypatch.setattr(tutor_service, "_figure_viewer", lambda: viewer)
    return course, doc, session, storage, viewer


async def _run(  # type: ignore[no-untyped-def]
    course, session, asset: str, document_ids=None, citations=None, chunk_to_doc_id=None
) -> str:
    return await _execute_tool(
        session=session, course=course, settings=get_settings(), retrieval_service=MagicMock(),
        tool_name="view_figure_api_tool", tool_args={"asset": asset, "question": "What is row 1?"},
        question="raw q", citations=[] if citations is None else citations,
        chunk_to_doc_id={} if chunk_to_doc_id is None else chunk_to_doc_id, document_ids=document_ids,
    )


@pytest.mark.asyncio
async def test_view_figure_loads_image_and_asks_viewer(monkeypatch: pytest.MonkeyPatch) -> None:
    course, doc, session, storage, viewer = _setup(monkeypatch)
    asset = f"asset://{doc.id}/p013-f1.png"

    out = await _run(course, session, asset)

    storage.get_object.assert_awaited_once_with(f"documents/{doc.course_id}/{doc.id}/assets/p013-f1.png")
    viewer.ask.assert_awaited_once_with(b"png-bytes", "What is row 1?")
    assert out.startswith(f"Figure analysis ({asset}):")
    assert "0 3 0 5 0 0" in out


@pytest.mark.parametrize("asset", ["asset://not-a-uuid/p001-f1.png", "../raw/x.pdf", "asset://{doc}/../raw/x.pdf"])
@pytest.mark.asyncio
async def test_view_figure_rejects_malformed_refs(monkeypatch: pytest.MonkeyPatch, asset: str) -> None:
    course, doc, session, storage, _ = _setup(monkeypatch)

    out = await _run(course, session, asset.replace("{doc}", str(doc.id)))

    assert out.startswith("Invalid asset reference")
    storage.get_object.assert_not_awaited()


@pytest.mark.parametrize(
    ("status", "same_course"), [(DocumentStatus.NEEDS_REVIEW, True), (DocumentStatus.INDEXED, False)]
)
@pytest.mark.asyncio
async def test_view_figure_refuses_other_course_or_unindexed(monkeypatch, status, same_course) -> None:  # type: ignore[no-untyped-def]
    course, doc, session, storage, _ = _setup(monkeypatch, doc_status=status, same_course=same_course)
    citations: list[CitationResponse] = []

    out = await _run(course, session, f"asset://{doc.id}/p001-f1.png", citations=citations)

    assert out == "This figure is not available in the current course materials."
    storage.get_object.assert_not_awaited()
    assert citations == []


@pytest.mark.asyncio
async def test_view_figure_respects_document_filter(monkeypatch: pytest.MonkeyPatch) -> None:
    course, doc, session, storage, _ = _setup(monkeypatch)

    out = await _run(course, session, f"asset://{doc.id}/p001-f1.png", document_ids=[uuid4()])

    assert out == "This figure is not available in the current course materials."


def test_tool_is_registered_in_schema_and_valid_names() -> None:
    assert "view_figure_api_tool" in _VALID_TOOL_NAMES
    assert "view_figure_api_tool" in _AGENT_DECISION_SCHEMA["properties"]["tool_name"]["enum"]
    args = _AGENT_DECISION_SCHEMA["properties"]["arguments"]["properties"]
    assert {"asset", "question"} <= set(args)


def test_system_prompt_mentions_figure_lines() -> None:
    assert "view_figure_api_tool(asset: str, question: str)" in tutor_service._TUTOR_SYSTEM_PROMPT_TEMPLATE
    assert "asset://" in tutor_service._FINAL_ANSWER_INSTRUCTION


def test_postprocess_keeps_figure_image_lines() -> None:
    answer = f"Ma trận:\n\n![Weight matrix](asset://{uuid4()}/p013-f1.png)\n\nGiải thích."

    cleaned, _ = _postprocess_answer(answer, [], {})

    assert "![Weight matrix](asset://" in cleaned


@pytest.mark.asyncio
async def test_view_figure_cites_the_chunk_that_contains_the_figure(monkeypatch: pytest.MonkeyPatch) -> None:
    course = MagicMock()
    course.id = uuid4()
    doc_id = uuid4()
    asset = f"asset://{doc_id}/p013-f1.png"
    chunk = _chunk(doc_id, f"![Weight matrix]({asset})\n[Figure: A 6x6 weight matrix of the graph.]")
    _, doc, session, _, _ = _setup(monkeypatch, chunk=chunk)
    doc.id, doc.course_id = doc_id, course.id
    session.execute = AsyncMock(return_value=[(doc_id, "graph_presentation.pdf")])
    citations: list[CitationResponse] = []
    chunk_to_doc_id: dict = {}  # type: ignore[type-arg]

    out = await _run(course, session, asset, citations=citations, chunk_to_doc_id=chunk_to_doc_id)

    assert out.startswith(f"Figure analysis ({asset}):")
    assert out.endswith(f"Source document_id: {doc_id}")
    [citation] = citations
    assert citation.chunk_id == chunk.id
    assert citation.document_title == "graph_presentation.pdf"
    assert (citation.document_tier, citation.document_subtype) == ("official", "lecture_slides")
    assert (citation.section_title, citation.page_number, citation.chunk_order) == ("Weighted graphs", 13, 4)
    assert citation.excerpt == "Weight matrix\n[Figure: A 6x6 weight matrix of the graph.]"
    assert chunk_to_doc_id == {chunk.id: doc_id}
    chunk_query = session.scalar.await_args_list[1].args[0].compile()
    assert asset in chunk_query.params.values() and doc_id in chunk_query.params.values()


@pytest.mark.asyncio
async def test_view_figure_without_a_matching_chunk_adds_no_citation(monkeypatch: pytest.MonkeyPatch) -> None:
    course, doc, session, _, _ = _setup(monkeypatch, chunk=None)
    citations: list[CitationResponse] = []
    chunk_to_doc_id: dict = {}  # type: ignore[type-arg]

    out = await _run(course, session, f"asset://{doc.id}/p001-f1.png", citations=citations,
                     chunk_to_doc_id=chunk_to_doc_id)

    assert out.startswith("Figure analysis (") and out.endswith(f"Source document_id: {doc.id}")
    assert citations == [] and chunk_to_doc_id == {}


def test_view_figure_citation_survives_postprocess_via_used_doc_ids() -> None:
    doc_id, chunk_id = uuid4(), uuid4()
    citation = CitationResponse(
        chunk_id=chunk_id, document_title="g.pdf", document_tier="official", document_subtype=None,
        section_title=None, page_number=13, chunk_order=4, excerpt="Weight matrix",
    )

    _, kept = _postprocess_answer(f'Answer.\n{{"used_doc_ids": ["{doc_id}"]}}', [citation], {chunk_id: doc_id})

    assert kept == [citation]


def test_excerpt_replaces_asset_image_markdown_with_its_caption() -> None:
    text = f"Intro.\n![Weight matrix](asset://{uuid4()}/p013-f1.png)\n[Figure: A matrix.]"

    assert _excerpt(text) == "Intro.\nWeight matrix\n[Figure: A matrix.]"
    assert _excerpt("x" * 500) == "x" * 200


@pytest.mark.asyncio
async def test_rag_citation_excerpt_has_no_raw_asset_link() -> None:
    doc_id = uuid4()
    chunk = _chunk(doc_id, f"![Weight matrix](asset://{doc_id}/p013-f1.png)\n[Figure: A matrix.]")
    retrieval = MagicMock()
    retrieval.search = AsyncMock(return_value=[chunk])
    session = MagicMock()
    session.execute = AsyncMock(return_value=[(doc_id, "graph_presentation.pdf")])
    citations: list[CitationResponse] = []

    await _execute_tool(
        session=session, course=MagicMock(), settings=get_settings(), retrieval_service=retrieval,
        tool_name="rag_retrieval_api_tool", tool_args={"query": "weight matrix"}, question="q",
        citations=citations, chunk_to_doc_id={},
    )

    assert citations[0].excerpt == "Weight matrix\n[Figure: A matrix.]"


def test_view_figure_argument_keys_are_logged_but_not_their_values() -> None:
    keys = _argument_keys({"asset": "asset://secret/p001-f1.png", "question": "SECRET QUESTION", "other": 1})

    assert keys == "asset,question"
