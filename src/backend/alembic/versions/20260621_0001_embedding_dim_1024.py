"""migrate pgvector embedding columns from 384 to 1024 dims (NVIDIA nv-embedqa-e5-v5)

Revision ID: 20260621_0001
Revises: 96479eebe1bf
Create Date: 2026-06-21

No real embedding data exists yet, so the dimension change is destructive: the
HNSW indexes are dropped and the column types are altered in place.
"""

from __future__ import annotations

from alembic import op

revision = "20260621_0001"
down_revision = "96479eebe1bf"
branch_labels = None
depends_on = None


def upgrade() -> None:
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


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS idx_chunk_embedding_hnsw;")
    op.execute("DROP INDEX IF EXISTS idx_summary_embedding_hnsw;")

    op.execute("ALTER TABLE document_chunks ALTER COLUMN embedding TYPE vector(384) USING NULL;")
    op.execute("ALTER TABLE document_summaries ALTER COLUMN summary_embedding TYPE vector(384) USING NULL;")

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
