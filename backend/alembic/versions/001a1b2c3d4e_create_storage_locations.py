"""001 create showroom storage locations

Revision ID: 001a1b2c3d4e
Revises: a3b4c5d6e7f8
Create Date: 2026-07-19 12:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '001a1b2c3d4e'
down_revision: Union[str, Sequence[str], None] = 'a3b4c5d6e7f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _table_exists(name: str) -> bool:
    conn = op.get_bind()
    r = conn.execute(sa.text(
        "SELECT COUNT(*) FROM information_schema.tables "
        "WHERE table_schema = DATABASE() AND table_name = :t"
    ), {"t": name})
    return r.scalar() > 0


def upgrade() -> None:
    if _table_exists('showroom_storage_locations'):
        return

    op.create_table('showroom_storage_locations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('parent_id', sa.Integer(), nullable=True),
        sa.Column('location_id', sa.Integer(), nullable=False),
        sa.Column('storage_type', sa.String(length=50), nullable=False, server_default='shelf'),
        sa.Column('capacity_qty', sa.Integer(), nullable=True),
        sa.Column('capacity_unit', sa.String(length=20), nullable=True, server_default='PCS'),
        sa.Column('capacity_note', sa.String(length=255), nullable=True),
        sa.Column('used_capacity', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('path', sa.String(length=500), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_showroom_storage_locations_id', 'showroom_storage_locations', ['id'], unique=False)
    op.create_index('ix_showroom_storage_locations_code', 'showroom_storage_locations', ['code'], unique=True)
    op.create_index('ix_showroom_storage_locations_parent_id', 'showroom_storage_locations', ['parent_id'], unique=False)
    op.create_index('ix_showroom_storage_locations_location_id', 'showroom_storage_locations', ['location_id'], unique=False)
    op.create_foreign_key(
        'fk_storage_loc_parent',
        'showroom_storage_locations',
        'showroom_storage_locations',
        ['parent_id'],
        ['id'],
    )
    op.create_foreign_key(
        'fk_storage_loc_location',
        'showroom_storage_locations',
        'showroom_locations',
        ['location_id'],
        ['id'],
    )


def downgrade() -> None:
    if not _table_exists('showroom_storage_locations'):
        return
    op.drop_constraint('fk_storage_loc_parent', 'showroom_storage_locations', type_='foreignkey')
    op.drop_constraint('fk_storage_loc_location', 'showroom_storage_locations', type_='foreignkey')
    op.drop_index('ix_showroom_storage_locations_location_id', 'showroom_storage_locations')
    op.drop_index('ix_showroom_storage_locations_parent_id', 'showroom_storage_locations')
    op.drop_index('ix_showroom_storage_locations_code', 'showroom_storage_locations')
    op.drop_index('ix_showroom_storage_locations_id', 'showroom_storage_locations')
    op.drop_table('showroom_storage_locations')
