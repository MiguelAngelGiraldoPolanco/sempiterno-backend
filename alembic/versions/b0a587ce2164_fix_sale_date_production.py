"""fix_sale_date_production

Revision ID: b0a587ce2164
Revises: 9f9e732d2832
Create Date: 2026-11-06 15:18:53.387253

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b0a587ce2164"
down_revision: str | None = "9f9e732d2832"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    inspector = sa.inspect(op.get_bind())

    columns = [column["name"] for column in inspector.get_columns("ticket")]

    if "sale_date" not in columns:
        op.add_column("ticket", sa.Column("sale_date", sa.DateTime(), nullable=True))

    op.execute("""
        UPDATE ticket
        SET sale_date = create_at
        WHERE sale_date IS NULL
    """)


def downgrade() -> None:
    pass
