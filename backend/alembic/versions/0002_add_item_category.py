"""add item category

Revision ID: 0002_add_item_category
Revises: 0001_create_items
Create Date: 2026-07-21 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0002_add_item_category"
down_revision: str | None = "0001_create_items"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("items", sa.Column("category", sa.String(length=80), nullable=False, server_default="General"))
    op.create_index(op.f("ix_items_category"), "items", ["category"], unique=False)
    op.alter_column("items", "category", server_default=None)


def downgrade() -> None:
    op.drop_index(op.f("ix_items_category"), table_name="items")
    op.drop_column("items", "category")
