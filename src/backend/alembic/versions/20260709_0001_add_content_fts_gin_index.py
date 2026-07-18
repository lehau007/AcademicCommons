"""add GIN full-text index on document_chunks.content for hybrid (BM25) retrieval

Revision ID: 20260709_0001
Revises: 20260707_0001
Create Date: 2026-07-09

Hybrid retrieval fuses dense (pgvector) with a BM25-style lexical branch that runs
``to_tsvector('simple', content)`` over document_chunks. Without this index every query
recomputes the tsvector per row (sequential scan). The expression index covers all existing
chunks at creation time and every future chunk automatically on INSERT — no reprocessing,
no ingest change. 'simple' config matches the query side (mixed Vietnamese + English corpus,
no stemming/stopwords).
"""

from __future__ import annotations

from collections.abc import Sequence

from alembic import op

revision: str = "20260709_0001"
down_revision: str | None = "20260707_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_chunk_content_fts
          ON document_chunks USING gin (to_tsvector('simple', content))
        """
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS idx_chunk_content_fts")
