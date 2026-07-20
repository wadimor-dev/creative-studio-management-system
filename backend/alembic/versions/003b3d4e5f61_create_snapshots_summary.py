"""003b create snapshots and daily summary

Revision ID: 003b3d4e5f61
Revises: 003c3d4e5f60
Create Date: 2026-07-19 12:15:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '003b3d4e5f61'
down_revision: Union[str, Sequence[str], None] = '003c3d4e5f60'
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
    if not _table_exists('showroom_storage_snapshots'):
        op.create_table('showroom_storage_snapshots',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('storage_location_id', sa.Integer(), nullable=False),
            sa.Column('product_id', sa.Integer(), nullable=False),
            sa.Column('sample_type', sa.String(length=50), nullable=True),
            sa.Column('quantity', sa.Integer(), nullable=False, server_default='0'),
            sa.Column('snapshot_type', sa.String(length=30), nullable=False, server_default='NIGHTLY'),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            sa.ForeignKeyConstraint(['storage_location_id'], ['showroom_storage_locations.id']),
            sa.ForeignKeyConstraint(['product_id'], ['products.id']),
        )
        op.create_index('ix_showroom_storage_snapshots_id', 'showroom_storage_snapshots', ['id'], unique=False)
        op.create_index('ix_showroom_storage_snapshots_storage_location_id', 'showroom_storage_snapshots', ['storage_location_id'], unique=False)
        op.create_index('ix_showroom_storage_snapshots_product_id', 'showroom_storage_snapshots', ['product_id'], unique=False)

    if not _table_exists('showroom_daily_storage_summary'):
        op.create_table('showroom_daily_storage_summary',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('summary_date', sa.Date(), nullable=False),
            sa.Column('total_items', sa.Integer(), nullable=False, server_default='0'),
            sa.Column('total_products', sa.Integer(), nullable=False, server_default='0'),
            sa.Column('total_locations', sa.Integer(), nullable=False, server_default='0'),
            sa.Column('total_movements', sa.Integer(), nullable=False, server_default='0'),
            sa.Column('incoming', sa.Integer(), nullable=False, server_default='0'),
            sa.Column('outgoing', sa.Integer(), nullable=False, server_default='0'),
            sa.Column('capacity_used_pct', sa.Integer(), nullable=False, server_default='0'),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id'),
        )
        op.create_index('ix_showroom_daily_storage_summary_id', 'showroom_daily_storage_summary', ['id'], unique=False)
        op.create_index('ix_showroom_daily_storage_summary_summary_date', 'showroom_daily_storage_summary', ['summary_date'], unique=False)


def downgrade() -> None:
    if _table_exists('showroom_daily_storage_summary'):
        op.drop_index('ix_showroom_daily_storage_summary_summary_date', 'showroom_daily_storage_summary')
        op.drop_index('ix_showroom_daily_storage_summary_id', 'showroom_daily_storage_summary')
        op.drop_table('showroom_daily_storage_summary')
    if _table_exists('showroom_storage_snapshots'):
        op.drop_index('ix_showroom_storage_snapshots_product_id', 'showroom_storage_snapshots')
        op.drop_index('ix_showroom_storage_snapshots_storage_location_id', 'showroom_storage_snapshots')
        op.drop_index('ix_showroom_storage_snapshots_id', 'showroom_storage_snapshots')
        op.drop_table('showroom_storage_snapshots')
