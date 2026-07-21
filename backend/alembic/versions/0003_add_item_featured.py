"""add item featured flag

Revision ID: 0003_add_item_featured
Revises: 0002_add_item_category
Create Date: 2026-07-21 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0003_add_item_featured"
down_revision: str | None = "0002_add_item_category"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("items", sa.Column("featured", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.create_index(op.f("ix_items_featured"), "items", ["featured"], unique=False)
    op.alter_column("items", "featured", server_default=None)


def downgrade() -> None:
    op.drop_index(op.f("ix_items_featured"), table_name="items")
    op.drop_column("items", "featured")
