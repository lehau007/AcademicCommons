from __future__ import annotations

import json
from datetime import UTC, datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.llm.providers import ChatMessage, LLMUnavailable
from app.llm.router import LLMRouter
from app.models.enums import DocumentStatus, DocumentTier, RagNamespace
from app.models.tables import Course, Document, DocumentChunk, DocumentSummary, MindmapArtifact
from app.schemas.mindmap import MindmapGenerateResponse

_EMPTY_GRAPH: dict[str, list[dict[str, str]]] = {"nodes": [], "edges": []}

_SYSTEM_PROMPT = (
    "You are an academic knowledge graph builder. "
    "Given a list of document summaries for a course, generate a concept map as JSON. "
    'Output ONLY valid JSON with this structure: {"nodes": [{"id": "...", "label": "...", "topic": "..."}], '
    '"edges": [{"source": "...", "target": "...", "relation": "..."}]} '
    "Generate between 10 and 25 nodes covering the most important concepts. "
    "Every edge's source and target MUST exactly match the id of a node in nodes. "
    "Write node labels, topics, and edge relations in the same language as the document summaries; "
    "do not translate."
)

_MINDMAP_SCHEMA = {
    "type": "object",
    "properties": {
        "nodes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "label": {"type": "string"},
                    "topic": {"type": "string"},
                },
                "required": ["id", "label", "topic"],
            },
        },
        "edges": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "source": {"type": "string"},
                    "target": {"type": "string"},
                    "relation": {"type": "string"},
                },
                "required": ["source", "target", "relation"],
            },
        },
    },
    "required": ["nodes", "edges"],
}


async def get_or_generate_mindmap(
    session: AsyncSession,
    course_code: str,
    force_regen: bool,
    llm_router: LLMRouter,
) -> MindmapGenerateResponse:
    course = await session.scalar(select(Course).where(Course.code == course_code, Course.is_active.is_(True)))
    if course is None:
        raise ValueError(f"Course '{course_code}' not found")

    if not force_regen:
        cached = await session.scalar(
            select(MindmapArtifact)
            .where(MindmapArtifact.course_id == course.id, MindmapArtifact.is_cached.is_(True))
            .order_by(MindmapArtifact.generated_at.desc())
        )
        if cached is not None:
            return MindmapGenerateResponse(
                course_code=course_code,
                is_cached=True,
                concept_graph=cached.concept_graph,
                generated_at=cached.generated_at,
            )

    # Load only summaries for official documents (Tier 1) that have at least one knowledge-namespace chunk.
    # Community summaries and exercise/exam documents are excluded from the concept map.
    knowledge_doc_ids_result = await session.execute(
        select(DocumentChunk.document_id)
        .join(Document, Document.id == DocumentChunk.document_id)
        .where(
            Document.course_id == course.id,
            Document.status == DocumentStatus.INDEXED,
            Document.document_tier == DocumentTier.OFFICIAL,
            DocumentChunk.rag_namespace == RagNamespace.KNOWLEDGE,
        )
        .distinct()
    )
    knowledge_ids = [row[0] for row in knowledge_doc_ids_result]

    summaries: list[DocumentSummary] = []
    if knowledge_ids:
        summary_rows = await session.execute(
            select(DocumentSummary).where(DocumentSummary.document_id.in_(knowledge_ids))
        )
        summaries = list(summary_rows.scalars())

    if not summaries:
        concept_graph = _EMPTY_GRAPH
    else:
        concept_graph = await _generate_via_llm(session, course, summaries, llm_router)

    await session.execute(
        update(MindmapArtifact)
        .where(MindmapArtifact.course_id == course.id)
        .values(is_cached=False)
    )

    artifact = MindmapArtifact(
        course_id=course.id,
        concept_graph=concept_graph,
        is_cached=True,
        generated_at=datetime.now(UTC),
    )
    session.add(artifact)
    await session.commit()
    await session.refresh(artifact)

    return MindmapGenerateResponse(
        course_code=course_code,
        is_cached=False,
        concept_graph=concept_graph,
        generated_at=artifact.generated_at,
    )


async def _generate_via_llm(
    session: AsyncSession,
    course: Course,
    summaries: list[DocumentSummary],
    llm_router: LLMRouter,
) -> dict[str, list[dict[str, str]]]:
    summary_texts = []
    for s in summaries:
        if s.overall_summary:
            summary_texts.append(f"- {s.overall_summary[:500]}")

    course_context = f"Course: {course.code} — {course.name}"
    if course.topic_summary:
        course_context += f"\nTopic summary: {course.topic_summary[:300]}"

    user_message = (
        f"{course_context}\n\n"
        f"Document summaries ({len(summary_texts)} documents):\n"
        + "\n".join(summary_texts[:20])
    )

    messages: list[ChatMessage] = [
        {"role": "system", "content": _SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    try:
        result = await llm_router.chat(messages, schema=_MINDMAP_SCHEMA, max_tokens=4096, flow="mindmap")
        return _parse_concept_graph(result.content)
    except LLMUnavailable:
        return _EMPTY_GRAPH


def _parse_concept_graph(text: str) -> dict[str, list[dict[str, str]]]:
    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        if start == -1 or end == 0:
            return _EMPTY_GRAPH
        payload = json.loads(text[start:end])
        nodes = payload.get("nodes", [])
        edges = payload.get("edges", [])
        if not isinstance(nodes, list) or not isinstance(edges, list):
            return _EMPTY_GRAPH
        node_ids = {n.get("id") for n in nodes if isinstance(n, dict)}
        edges = [
            e for e in edges
            if isinstance(e, dict) and e.get("source") in node_ids and e.get("target") in node_ids
        ]
        return {"nodes": nodes, "edges": edges}
    except (json.JSONDecodeError, ValueError):
        return _EMPTY_GRAPH


__all__ = ["get_or_generate_mindmap"]
