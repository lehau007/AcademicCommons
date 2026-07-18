from __future__ import annotations

import asyncio

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.llm.embeddings import EmbeddingService
from app.models import DocumentSummary
from app.models.tables import DocumentChunk


async def reindex_embeddings(
    session: AsyncSession,
    embedding_service: EmbeddingService,
    *,
    batch_size: int = 50,
) -> tuple[int, int]:
    """Re-encode all chunk contents and summary texts with the active embedder.

    Required after switching embedding tiers or migrating the vector column
    dimension — stored vectors from another model are unusable. Returns
    (chunks_updated, summaries_updated). Caller commits.
    """
    chunk_rows = (await session.execute(select(DocumentChunk.id, DocumentChunk.content))).all()
    chunks_updated = 0
    for start in range(0, len(chunk_rows), batch_size):
        batch = chunk_rows[start : start + batch_size]
        vectors = await asyncio.to_thread(
            embedding_service.encode, [row.content for row in batch], "passage"
        )
        for row, vector in zip(batch, vectors, strict=True):
            await session.execute(
                update(DocumentChunk).where(DocumentChunk.id == row.id).values(embedding=vector)
            )
        chunks_updated += len(batch)

    summary_rows = (
        await session.execute(select(DocumentSummary.id, DocumentSummary.overall_summary))
    ).all()
    summaries_updated = 0
    for start in range(0, len(summary_rows), batch_size):
        batch = summary_rows[start : start + batch_size]
        vectors = await asyncio.to_thread(
            embedding_service.encode, [row.overall_summary for row in batch], "passage"
        )
        for row, vector in zip(batch, vectors, strict=True):
            await session.execute(
                update(DocumentSummary)
                .where(DocumentSummary.id == row.id)
                .values(summary_embedding=vector)
            )
        summaries_updated += len(batch)

    return chunks_updated, summaries_updated


__all__ = ["reindex_embeddings"]
