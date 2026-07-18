from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

from sqlalchemy.sql.dml import Update

from app.llm.embeddings import DeterministicEmbeddingService
from app.services.reindex_service import reindex_embeddings


class _FakeResult:
    def __init__(self, rows: list) -> None:
        self._rows = rows

    def all(self) -> list:
        return self._rows


class _FakeSession:
    def __init__(self, chunk_rows: list, summary_rows: list) -> None:
        self._selects = [_FakeResult(chunk_rows), _FakeResult(summary_rows)]
        self.update_count = 0

    async def execute(self, stmt, *args, **kwargs):
        if isinstance(stmt, Update):
            self.update_count += 1
            return _FakeResult([])
        return self._selects.pop(0)


async def test_reindex_updates_all_chunks_and_summaries() -> None:
    chunk_rows = [SimpleNamespace(id=uuid4(), content=f"chunk {i}") for i in range(3)]
    summary_rows = [SimpleNamespace(id=uuid4(), overall_summary="summary text")]
    session = _FakeSession(chunk_rows, summary_rows)

    chunks, summaries = await reindex_embeddings(
        session, DeterministicEmbeddingService(1536), batch_size=2
    )

    assert (chunks, summaries) == (3, 1)
    assert session.update_count == 4


async def test_reindex_empty_database_is_noop() -> None:
    session = _FakeSession([], [])
    assert await reindex_embeddings(session, DeterministicEmbeddingService(1536)) == (0, 0)
    assert session.update_count == 0
