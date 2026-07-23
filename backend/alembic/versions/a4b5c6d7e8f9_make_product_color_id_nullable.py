"""Make product color_id nullable

Revision ID: a4b5c6d7e8f9
Revises: 4f70ca5e63bc
Create Date: 2026-07-23 13:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4b5c6d7e8f9'
down_revision: Union[str, Sequence[str], None] = '4f70ca5e63bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('products', 'color_id',
                    existing_type=sa.Integer(),
                    nullable=True,
                    existing_nullable=False)


def downgrade() -> None:
    op.alter_column('products', 'color_id',
                    existing_type=sa.Integer(),
                    nullable=False,
                    existing_nullable=True)
