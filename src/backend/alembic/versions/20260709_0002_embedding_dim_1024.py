"""migrate pgvector embedding columns from 1536 back to 1024 dims (nvidia/nv-embedqa-e5-v5)

Revision ID: 20260709_0002
Revises: 20260709_0001
Create Date: 2026-07-09

Switch the active embedder back to NVIDIA (nv-embedqa-e5-v5, 1024 dims) because the
OpenRouter key (openai/text-embedding-3-small, 1536 dims) ran out of credit. Destructive:
embeddings are nulled (vectors from the 1536-dim model are unusable in the 1024-dim space
anyway); chunk/summary CONTENT is preserved. Run `python -m app.cli reindex-embeddings`
afterwards to regenerate embeddings with NVIDIA. The BM25 full-text GIN index
(idx_chunk_content_fts, on to_tsvector(content)) is unaffected — it does not touch the
embedding column.
"""

from __future__ import annotations

from alembic import op

revision = "20260709_0002"
down_revision = "20260709_0001"
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
