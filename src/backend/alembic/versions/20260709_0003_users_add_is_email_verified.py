"""users.is_email_verified for Resend email verification flow

Revision ID: 20260709_0003
Revises: 20260709_0002
Create Date: 2026-07-09

Adds a permanent boolean flag on `users` recording whether the user has
confirmed ownership of their email address. The ephemeral verification token
itself lives in Redis (TTL-managed) and is intentionally NOT stored in the
database — see app/services/email_verification.py. Existing seeded accounts
(admin/reviewer/student demo users) are flipped to verified so the operator
running `make seed` does not need to verify them by email afterwards.
"""

from __future__ import annotations

from alembic import op

revision = "20260709_0003"
down_revision = "20260709_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS is_email_verified BOOLEAN NOT NULL DEFAULT FALSE;"
    )
    # Pre-verify the seeded demo accounts so the operator can log in immediately
    # after running `make seed` (these are operator-controlled mailboxes already).
    op.execute(
        """
        UPDATE users
        SET is_email_verified = TRUE
        WHERE email IN (
            'admin@soict.hust.edu.vn',
            'reviewer.linhnt@soict.hust.edu.vn',
            'reviewer.ducpv@soict.hust.edu.vn',
            'student.anhnv@sis.hust.edu.vn',
            'student.huylt@sis.hust.edu.vn',
            'student.maiptt@sis.hust.edu.vn'
        );
        """
    )


def downgrade() -> None:
    op.execute("ALTER TABLE users DROP COLUMN IF EXISTS is_email_verified;")