"""add location description, image_url and QR support

Revision ID: a3b4c5d6e7f8
Revises: f7a8b9c0d1e2
Create Date: 2026-07-19 10:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'a3b4c5d6e7f8'
down_revision: Union[str, Sequence[str], None] = 'f7a8b9c0d1e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def column_exists(table: str, column: str, bind) -> bool:
    inspector = sa.inspect(bind)
    columns = [c["name"] for c in inspector.get_columns(table)]
    return column in columns


def upgrade() -> None:
    bind = op.get_bind()

    if not column_exists("showroom_locations", "description", bind):
        op.add_column("showroom_locations", sa.Column("description", sa.Text(), nullable=True))

    if not column_exists("showroom_locations", "image_url", bind):
        op.add_column("showroom_locations", sa.Column("image_url", sa.String(length=500), nullable=True))


def downgrade() -> None:
    bind = op.get_bind()

    if column_exists("showroom_locations", "image_url", bind):
        op.drop_column("showroom_locations", "image_url")

    if column_exists("showroom_locations", "description", bind):
        op.drop_column("showroom_locations", "description")
