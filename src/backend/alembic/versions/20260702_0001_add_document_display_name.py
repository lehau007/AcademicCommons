"""add display_name to documents

Revision ID: 20260702_0001
Revises: 20260623_0001
Create Date: 2026-07-02

Persists the custom display name students enter at upload time (previously
collected in the UI but discarded); falls back to original_filename when null.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260702_0001"
down_revision: str | None = "20260623_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("documents", sa.Column("display_name", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("documents", "display_name")
