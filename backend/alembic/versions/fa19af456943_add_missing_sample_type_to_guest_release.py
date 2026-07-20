"""add missing sample_type to guest release

Revision ID: fa19af456943
Revises: b1c2d3e4f5a6
Create Date: 2026-07-18 21:34:36.460426

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fa19af456943'
down_revision: Union[str, Sequence[str], None] = 'b1c2d3e4f5a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "showroom_guest_releases",
        sa.Column(
            "sample_type",
            sa.String(length=50),
            nullable=True
        )
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
