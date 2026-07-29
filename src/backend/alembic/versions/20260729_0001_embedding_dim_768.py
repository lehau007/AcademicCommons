"""migrate pgvector embedding columns from 1024 to 768 dims (Google Vertex AI text-multilingual-embedding-002)

Revision ID: 20260729_0001
Revises: 20260709_0003
Create Date: 2026-07-29

Switch the default embedder to Vertex AI (text-multilingual-embedding-002, 768 dims).
Destructive: embeddings are nulled; chunk/summary content is preserved. Run
`python -m app.cli reindex-embeddings` to regenerate embeddings with Vertex AI.
"""

from __future__ import annotations

from alembic import op

revision = "20260729_0001"
down_revision = "20260709_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("DROP INDEX IF EXISTS idx_chunk_embedding_hnsw;")
    op.execute("DROP INDEX IF EXISTS idx_summary_embedding_hnsw;")

    op.execute("ALTER TABLE document_chunks ALTER COLUMN embedding TYPE vector(768) USING NULL;")
    op.execute("ALTER TABLE document_summaries ALTER COLUMN summary_embedding TYPE vector(768) USING NULL;")

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
