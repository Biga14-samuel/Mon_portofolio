"""create items table

Revision ID: 0001_create_items
Revises:
Create Date: 2026-07-20 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001_create_items"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    item_type = sa.Enum("parcours", "competence", "realisation", name="item_type", create_type=False)
    item_type.create(op.get_bind(), checkfirst=True)
    op.create_table(
        "items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("type", item_type, nullable=False),
        sa.Column("category", sa.String(length=80), nullable=False, server_default="General"),
        sa.Column("title", sa.String(length=140), nullable=False),
        sa.Column("subtitle", sa.String(length=180), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_items_id"), "items", ["id"], unique=False)
    op.create_index(op.f("ix_items_category"), "items", ["category"], unique=False)
    op.create_index(op.f("ix_items_type"), "items", ["type"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_items_type"), table_name="items")
    op.drop_index(op.f("ix_items_category"), table_name="items")
    op.drop_index(op.f("ix_items_id"), table_name="items")
    op.drop_table("items")
    sa.Enum(name="item_type").drop(op.get_bind(), checkfirst=True)
