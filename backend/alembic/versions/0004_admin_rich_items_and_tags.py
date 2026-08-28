"""add rich item admin fields and tags

Revision ID: 0004_admin_rich_items_and_tags
Revises: 0003_add_item_featured
Create Date: 2026-07-21 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0004_admin_rich_items_and_tags"
down_revision: str | None = "0003_add_item_featured"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _upgrade_items_columns() -> None:
    op.add_column("items", sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("items", sa.Column("github_url", sa.String(length=500), nullable=True))
    op.add_column("items", sa.Column("demo_url", sa.String(length=500), nullable=True))
    op.add_column("items", sa.Column("image_url", sa.String(length=500), nullable=True))
    op.create_index(op.f("ix_items_display_order"), "items", ["display_order"], unique=False)
    op.alter_column("items", "display_order", server_default=None)


def _upgrade_tags_table() -> None:
    op.create_table(
        "tags",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("type", sa.String(length=20), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("type", "name", name="uq_tags_type_name"),
    )
    op.create_index(op.f("ix_tags_id"), "tags", ["id"], unique=False)
    op.create_index(op.f("ix_tags_name"), "tags", ["name"], unique=False)
    op.create_index(op.f("ix_tags_type"), "tags", ["type"], unique=False)


def _seed_initial_tags() -> None:
    tags_table = sa.table(
        "tags",
        sa.column("type", sa.String),
        sa.column("name", sa.String),
    )
    op.bulk_insert(
        tags_table,
        [
            {"type": "parcours", "name": "Cursus"},
            {"type": "parcours", "name": "Diplôme"},
            {"type": "parcours", "name": "Certification"},
            {"type": "parcours", "name": "Formation"},
            {"type": "parcours", "name": "Stage"},
            {"type": "parcours", "name": "Expérience professionnelle"},
            {"type": "competence", "name": "Détection"},
            {"type": "competence", "name": "Threat Intel"},
            {"type": "competence", "name": "Incident Response"},
            {"type": "competence", "name": "Sécurité / Cybersécurité"},
            {"type": "competence", "name": "Administration réseau"},
            {"type": "competence", "name": "Administration système"},
            {"type": "competence", "name": "Systèmes"},
            {"type": "competence", "name": "Réseau"},
            {"type": "competence", "name": "Dev / Scripting"},
            {"type": "competence", "name": "DB"},
            {"type": "competence", "name": "Méthodologie / Gestion de projet"},
            {"type": "competence", "name": "Base de données"},
            {"type": "competence", "name": "Compétences transversales"},
            {"type": "competence", "name": "Infographie"},
            {"type": "competence", "name": "Programmation web"},
            {"type": "competence", "name": "Automatisation / Scripting"},
            {"type": "competence", "name": "Cloud / Virtualisation"},
            {"type": "competence", "name": "Maintenance"},
            {"type": "realisation", "name": "Réseau sécurité"},
            {"type": "realisation", "name": "Cybersécurité"},
            {"type": "realisation", "name": "Fibre optique"},
            {"type": "realisation", "name": "Maintenance"},
            {"type": "realisation", "name": "Conception"},
            {"type": "realisation", "name": "Administration système"},
            {"type": "realisation", "name": "Programmation web"},
            {"type": "realisation", "name": "Base de données"},
        ],
    )


def upgrade() -> None:
    _upgrade_items_columns()
    _upgrade_tags_table()
    _seed_initial_tags()


def downgrade() -> None:
    op.drop_index(op.f("ix_tags_type"), table_name="tags")
    op.drop_index(op.f("ix_tags_name"), table_name="tags")
    op.drop_index(op.f("ix_tags_id"), table_name="tags")
    op.drop_table("tags")
    op.drop_index(op.f("ix_items_display_order"), table_name="items")
    op.drop_column("items", "image_url")
    op.drop_column("items", "demo_url")
    op.drop_column("items", "github_url")
    op.drop_column("items", "display_order")
