"""004 add version and storage_location_id to sample stocks

Revision ID: 004d4e5f6071
Revises: 003b3d4e5f61
Create Date: 2026-07-19 12:20:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '004d4e5f6071'
down_revision: Union[str, Sequence[str], None] = '003b3d4e5f61'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _col_exists(table: str, col: str) -> bool:
    conn = op.get_bind()
    r = conn.execute(sa.text(
        "SELECT COUNT(*) FROM information_schema.columns "
        "WHERE table_schema = DATABASE() AND table_name = :t AND column_name = :c"
    ), {"t": table, "c": col})
    return r.scalar() > 0


def _index_exists(table: str, name: str) -> bool:
    conn = op.get_bind()
    r = conn.execute(sa.text(
        "SELECT COUNT(*) FROM information_schema.statistics "
        "WHERE table_schema = DATABASE() AND table_name = :t AND index_name = :c"
    ), {"t": table, "c": name})
    return r.scalar() > 0


def upgrade() -> None:
    if not _col_exists('showroom_sample_stocks', 'storage_location_id'):
        op.add_column('showroom_sample_stocks', sa.Column('storage_location_id', sa.Integer(), nullable=True))
        if not _index_exists('showroom_sample_stocks', 'ix_showroom_sample_stocks_storage_location_id'):
            op.create_index('ix_showroom_sample_stocks_storage_location_id', 'showroom_sample_stocks', ['storage_location_id'], unique=False)
        op.create_foreign_key(
            'fk_stock_storage_loc',
            'showroom_sample_stocks',
            'showroom_storage_locations',
            ['storage_location_id'],
            ['id'],
        )

    if not _col_exists('showroom_sample_stocks', 'version'):
        op.add_column('showroom_sample_stocks', sa.Column('version', sa.Integer(), nullable=False, server_default='1'))


def downgrade() -> None:
    if _col_exists('showroom_sample_stocks', 'version'):
        op.drop_column('showroom_sample_stocks', 'version')
    if _col_exists('showroom_sample_stocks', 'storage_location_id'):
        op.drop_constraint('fk_stock_storage_loc', 'showroom_sample_stocks', type_='foreignkey')
        if _index_exists('showroom_sample_stocks', 'ix_showroom_sample_stocks_storage_location_id'):
            op.drop_index('ix_showroom_sample_stocks_storage_location_id', 'showroom_sample_stocks')
        op.drop_column('showroom_sample_stocks', 'storage_location_id')
