"""add content json

Revision ID: 0005_add_content_json
Revises: 0004_admin_rich_items_and_tags
Create Date: 2026-07-21 14:26:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0005_add_content_json'
down_revision: Union[str, None] = '0004_admin_rich_items_and_tags'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('items', sa.Column('content', sa.JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column('items', 'content')
