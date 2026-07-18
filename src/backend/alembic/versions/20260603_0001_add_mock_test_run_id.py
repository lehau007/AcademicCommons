"""add test_run_id to mock_test_items

Revision ID: 20260603_0001
Revises: 20260602_0001
Create Date: 2026-06-03
"""

from __future__ import annotations

import sqlalchemy as sa

from alembic import op

revision = "20260603_0001"
down_revision = "20260602_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("mock_test_items", sa.Column("test_run_id", sa.dialects.postgresql.UUID(as_uuid=True), nullable=True))
    op.create_index("idx_mock_test_run", "mock_test_items", ["test_run_id"])


def downgrade() -> None:
    op.drop_index("idx_mock_test_run", table_name="mock_test_items")
    op.drop_column("mock_test_items", "test_run_id")
