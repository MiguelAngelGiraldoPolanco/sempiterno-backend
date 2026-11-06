"""populate_sale_date_from_create_at

Revision ID: 9f9e732d2832
Revises: b407bdd79bc0
Create Date: 2026-11-06 15:03:57.911429

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9f9e732d2832"
down_revision: str | None = "b407bdd79bc0"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("""
        UPDATE ticket
        SET sale_date = create_at
        WHERE sale_date IS NULL
    """)


def downgrade() -> None:
    op.execute("""
        UPDATE ticket
        SET sale_date = NULL
    """)
