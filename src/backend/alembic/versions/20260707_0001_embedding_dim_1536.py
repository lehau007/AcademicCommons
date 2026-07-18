"""migrate pgvector embedding columns from 1024 to 1536 dims (openai/text-embedding-3-small)

Revision ID: 20260707_0001
Revises: 20260702_0001
Create Date: 2026-07-07

Destructive: embeddings are nulled (vectors from the old model are unusable in
the new space anyway). Run `python -m app.cli reindex-embeddings` afterwards.
"""

from __future__ import annotations

from alembic import op

revision = "20260707_0001"
down_revision = "20260702_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("DROP INDEX IF EXISTS idx_chunk_embedding_hnsw;")
    op.execute("DROP INDEX IF EXISTS idx_summary_embedding_hnsw;")

    op.execute("ALTER TABLE document_chunks ALTER COLUMN embedding TYPE vector(1536) USING NULL;")
    op.execute("ALTER TABLE document_summaries ALTER COLUMN summary_embedding TYPE vector(1536) USING NULL;")

    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_chunk_embedding_hnsw
            ON document_chunks USING hnsw (embedding vector_cosine_ops)
            WITH (m = 16, ef_construction = 64);
        """
    )
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_summary_embedding_hnsw
            ON document_summaries USING hnsw (summary_embedding vector_cosine_ops)
            WITH (m = 16, ef_construction = 64);
        """
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS idx_chunk_embedding_hnsw;")
    op.execute("DROP INDEX IF EXISTS idx_summary_embedding_hnsw;")

    op.execute("ALTER TABLE document_chunks ALTER COLUMN embedding TYPE vector(1024) USING NULL;")
    op.execute("ALTER TABLE document_summaries ALTER COLUMN summary_embedding TYPE vector(1024) USING NULL;")

    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_chunk_embedding_hnsw
            ON document_chunks USING hnsw (embedding vector_cosine_ops)
            WITH (m = 16, ef_construction = 64);
        """
    )
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_summary_embedding_hnsw
            ON document_summaries USING hnsw (summary_embedding vector_cosine_ops)
            WITH (m = 16, ef_construction = 64);
        """
    )
