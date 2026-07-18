from __future__ import annotations

from datetime import UTC, datetime
from types import SimpleNamespace
from uuid import uuid4

import app.services.document_summary_service as summary_module
from app.llm import DeterministicEmbeddingService
from app.models import DocumentSummary
from app.services.document_summary_service import summarize_markdown, upsert_document_summary


class FakeSummarySession:
    def __init__(self, existing: DocumentSummary | None = None) -> None:
        self.existing = existing
        self.added: list[object] = []
        self.flush_count = 0

    async def scalar(self, query) -> DocumentSummary | None:
        return self.existing

    def add(self, item: object) -> None:
        self.added.append(item)

    async def flush(self) -> None:
        self.flush_count += 1


def test_summarize_markdown_returns_schema_shaped_payload() -> None:
    markdown = """
# Distributed Systems

Distributed systems coordinate multiple nodes to provide resilient services.

## Replication

Replication improves availability and helps tolerate node failures.

## Consensus

Consensus protocols coordinate leaders, followers, and quorums for safety.
"""

    payload = summarize_markdown(markdown)
    as_json = payload.model_dump(mode="json")

    assert as_json["schema_version"] == "1.0"
    assert as_json["topic"] == "Distributed Systems"
    assert as_json["language"] == "en"
    assert as_json["ocr_quality"] == "high"
    assert len(as_json["section_summaries"]) == 3
    assert as_json["section_summaries"][0]["page_range"] == [1, 1]
    assert "Replication" in as_json["concepts"]
    assert "Consensus" in as_json["overall_summary"]


async def test_upsert_document_summary_creates_summary_with_1024d_embedding() -> None:
    session = FakeSummarySession()
    document_id = uuid4()
    now = datetime(2026, 6, 3, 9, 0, tzinfo=UTC)

    summary, payload = await upsert_document_summary(
        session,
        document_id=document_id,
        markdown_text="# Topic\n\nThis document explains fault tolerance and replication strategies.",
        embedding_service=DeterministicEmbeddingService(),
        now=now,
    )

    assert summary.document_id == document_id
    assert summary.schema_version == "1.0"
    assert summary.topic == payload.topic
    assert len(summary.summary_embedding or []) == 1024
    assert summary.created_at == now
    assert summary.updated_at == now
    assert session.flush_count == 1
    assert session.added[-1] is summary


def test_default_embedding_service_follows_retrieval_tier(monkeypatch) -> None:
    fake_settings = SimpleNamespace(
        openrouter_api_key=None,
        nvidia_api_key=None,
        embedding_dim=1536,
    )
    monkeypatch.setattr("app.config.get_settings", lambda: fake_settings)

    service = summary_module.build_embedding_service()

    assert isinstance(service, DeterministicEmbeddingService)
    assert service.dimension == 1536


async def test_upsert_document_summary_updates_existing_row_in_place() -> None:
    existing = DocumentSummary(document_id=uuid4(), topic="Old Topic", overall_summary="Old summary")
    session = FakeSummarySession(existing=existing)
    now = datetime(2026, 6, 3, 10, 0, tzinfo=UTC)

    summary, _ = await upsert_document_summary(
        session,
        document_id=existing.document_id,
        markdown_text="# New Topic\n\nThis updated text covers machine learning pipelines and embeddings.",
        embedding_service=DeterministicEmbeddingService(),
        now=now,
    )

    assert summary is existing
    assert summary.topic == "New Topic"
    assert summary.overall_summary is not None
    assert len(summary.summary_embedding or []) == 1024
    assert summary.updated_at == now
    assert session.flush_count == 1
