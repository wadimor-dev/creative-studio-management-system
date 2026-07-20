"""showroom v2 defensive sync

Revision ID: f7a8b9c0d1e2
Revises: 22950bc640d5
Create Date: 2026-07-18 23:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'f7a8b9c0d1e2'
down_revision: Union[str, Sequence[str], None] = '22950bc640d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _table_exists(name: str) -> bool:
    conn = op.get_bind()
    r = conn.execute(sa.text(
        "SELECT COUNT(*) FROM information_schema.tables "
        "WHERE table_schema = DATABASE() AND table_name = :t"
    ), {"t": name})
    return r.scalar() > 0


def _col_exists(table: str, col: str) -> bool:
    conn = op.get_bind()
    r = conn.execute(sa.text(
        "SELECT COUNT(*) FROM information_schema.columns "
        "WHERE table_schema = DATABASE() AND table_name = :t AND column_name = :c"
    ), {"t": table, "c": col})
    return r.scalar() > 0


def _col_is_enum(table: str, col: str) -> bool:
    conn = op.get_bind()
    r = conn.execute(sa.text(
        "SELECT COUNT(*) FROM information_schema.columns "
        "WHERE table_schema = DATABASE() AND table_name = :t "
        "AND column_name = :c AND data_type = 'enum'"
    ), {"t": table, "c": col})
    return r.scalar() > 0


def _constraint_exists(table: str, name: str) -> bool:
    conn = op.get_bind()
    r = conn.execute(sa.text(
        "SELECT COUNT(*) FROM information_schema.table_constraints "
        "WHERE table_schema = DATABASE() AND table_name = :t AND constraint_name = :c"
    ), {"t": table, "c": name})
    return r.scalar() > 0


def _index_exists(table: str, name: str) -> bool:
    conn = op.get_bind()
    r = conn.execute(sa.text(
        "SELECT COUNT(*) FROM information_schema.statistics "
        "WHERE table_schema = DATABASE() AND table_name = :t AND index_name = :c"
    ), {"t": table, "c": name})
    return r.scalar() > 0


def _drop_fk_by_column(table: str, col: str, ref_table: str):
    conn = op.get_bind()
    r = conn.execute(sa.text(
        "SELECT constraint_name FROM information_schema.key_column_usage "
        "WHERE table_schema = DATABASE() AND table_name = :t "
        "AND column_name = :c AND referenced_table_name = :r LIMIT 1"
    ), {"t": table, "c": col, "r": ref_table})
    row = r.fetchone()
    if row:
        op.execute(f"ALTER TABLE `{table}` DROP FOREIGN KEY `{row[0]}`")


def upgrade() -> None:
    # ═══════════════════════════════════════════════════════════
    # showroom_master_data
    # ═══════════════════════════════════════════════════════════
    if not _table_exists('showroom_master_data'):
        op.create_table('showroom_master_data',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('type', sa.String(length=50), nullable=False),
            sa.Column('name', sa.String(length=100), nullable=False),
            sa.Column('value', sa.String(length=100), nullable=False),
            sa.Column('description', sa.String(length=255), nullable=True),
            sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
            sa.Column('sort_order', sa.Integer(), nullable=False, server_default='0'),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id'),
        )
        op.create_index(op.f('ix_showroom_master_data_id'), 'showroom_master_data', ['id'], unique=False)
        op.create_index(op.f('ix_showroom_master_data_type'), 'showroom_master_data', ['type'], unique=False)

    if _constraint_exists('showroom_master_data', 'uix_master_data_type_value'):
        op.drop_constraint('uix_master_data_type_value', 'showroom_master_data', type_='unique')

    # ═══════════════════════════════════════════════════════════
    # showroom_sample_stocks
    # ═══════════════════════════════════════════════════════════
    if not _col_exists('showroom_sample_stocks', 'sample_type'):
        op.add_column('showroom_sample_stocks', sa.Column('sample_type', sa.String(length=50), nullable=True))

    if _constraint_exists('showroom_sample_stocks', 'uix_showroom_stock_product_location'):
        if not _index_exists('showroom_sample_stocks', 'ix_showroom_sample_stocks_product_id'):
            op.create_index('ix_showroom_sample_stocks_product_id', 'showroom_sample_stocks', ['product_id'], unique=False)
        if not _index_exists('showroom_sample_stocks', 'ix_showroom_sample_stocks_location_id'):
            op.create_index('ix_showroom_sample_stocks_location_id', 'showroom_sample_stocks', ['location_id'], unique=False)
        op.drop_constraint('uix_showroom_stock_product_location', 'showroom_sample_stocks', type_='unique')

    if not _constraint_exists('showroom_sample_stocks', 'uix_showroom_stock_product_location_type'):
        op.create_unique_constraint(
            'uix_showroom_stock_product_location_type',
            'showroom_sample_stocks',
            ['product_id', 'location_id', 'sample_type'],
        )

    # Ensure FK indexes exist (required by MySQL InnoDB)
    if not _index_exists('showroom_sample_stocks', 'ix_showroom_sample_stocks_product_id'):
        op.create_index('ix_showroom_sample_stocks_product_id', 'showroom_sample_stocks', ['product_id'], unique=False)
    if not _index_exists('showroom_sample_stocks', 'ix_showroom_sample_stocks_location_id'):
        op.create_index('ix_showroom_sample_stocks_location_id', 'showroom_sample_stocks', ['location_id'], unique=False)

    # ═══════════════════════════════════════════════════════════
    # showroom_movements
    # ═══════════════════════════════════════════════════════════
    if not _col_exists('showroom_movements', 'sample_type'):
        op.add_column('showroom_movements', sa.Column('sample_type', sa.String(length=50), nullable=True))

    if _col_is_enum('showroom_movements', 'movement_type'):
        op.execute("ALTER TABLE showroom_movements MODIFY movement_type VARCHAR(50) NOT NULL")

    # ═══════════════════════════════════════════════════════════
    # showroom_guest_releases
    # ═══════════════════════════════════════════════════════════
    if not _col_exists('showroom_guest_releases', 'status'):
        op.add_column('showroom_guest_releases', sa.Column('status', sa.String(length=20), nullable=False, server_default='DRAFT'))

    if not _col_exists('showroom_guest_releases', 'location_id'):
        op.add_column('showroom_guest_releases', sa.Column('location_id', sa.Integer(), nullable=True))
        op.create_foreign_key('fk_guest_release_location', 'showroom_guest_releases', 'showroom_locations', ['location_id'], ['id'])

    if not _col_exists('showroom_guest_releases', 'rejected_by'):
        op.add_column('showroom_guest_releases', sa.Column('rejected_by', sa.Integer(), nullable=True))
        op.create_foreign_key('fk_guest_release_rejected_by', 'showroom_guest_releases', 'users', ['rejected_by'], ['id'])

    if not _col_exists('showroom_guest_releases', 'rejected_at'):
        op.add_column('showroom_guest_releases', sa.Column('rejected_at', sa.DateTime(), nullable=True))

    if not _col_exists('showroom_guest_releases', 'sample_type'):
        op.add_column('showroom_guest_releases', sa.Column('sample_type', sa.String(length=50), nullable=True))

    # ═══════════════════════════════════════════════════════════
    # showroom_borrowings
    # ═══════════════════════════════════════════════════════════
    if not _col_exists('showroom_borrowings', 'sample_type'):
        op.add_column('showroom_borrowings', sa.Column('sample_type', sa.String(length=50), nullable=True))

    if not _col_exists('showroom_borrowings', 'borrowed_at'):
        op.add_column('showroom_borrowings', sa.Column('borrowed_at', sa.DateTime(), nullable=True))

    if _col_exists('showroom_borrowings', 'approved_by'):
        _drop_fk_by_column('showroom_borrowings', 'approved_by', 'users')
        op.drop_column('showroom_borrowings', 'approved_by')

    if _col_exists('showroom_borrowings', 'approved_at'):
        op.drop_column('showroom_borrowings', 'approved_at')

    if _col_is_enum('showroom_borrowings', 'status'):
        op.execute("ALTER TABLE showroom_borrowings MODIFY status VARCHAR(20) NOT NULL DEFAULT 'BORROWED'")

    # ═══════════════════════════════════════════════════════════
    # showroom_restock_requests
    # ═══════════════════════════════════════════════════════════
    if not _col_exists('showroom_restock_requests', 'source'):
        op.add_column('showroom_restock_requests', sa.Column('source', sa.String(length=20), nullable=False, server_default='auto'))

    if not _col_exists('showroom_restock_requests', 'sample_type'):
        op.add_column('showroom_restock_requests', sa.Column('sample_type', sa.String(length=50), nullable=True))

    op.execute("ALTER TABLE showroom_restock_requests MODIFY minimum_quantity INT NULL")
    op.execute("ALTER TABLE showroom_restock_requests MODIFY current_quantity INT NULL")

    if _col_is_enum('showroom_restock_requests', 'status'):
        op.execute("ALTER TABLE showroom_restock_requests MODIFY status VARCHAR(20) NOT NULL DEFAULT 'PENDING'")

    # ═══════════════════════════════════════════════════════════
    # showroom_maintenance
    # ═══════════════════════════════════════════════════════════
    if not _col_exists('showroom_maintenance', 'sample_type'):
        op.add_column('showroom_maintenance', sa.Column('sample_type', sa.String(length=50), nullable=True))

    if _col_is_enum('showroom_maintenance', 'maintenance_type'):
        op.execute("ALTER TABLE showroom_maintenance MODIFY maintenance_type VARCHAR(50) NOT NULL")

    if _col_is_enum('showroom_maintenance', 'status'):
        op.execute("ALTER TABLE showroom_maintenance MODIFY status VARCHAR(20) NOT NULL DEFAULT 'PENDING'")

    # ═══════════════════════════════════════════════════════════
    # showroom_opname_sessions
    # ═══════════════════════════════════════════════════════════
    if _col_is_enum('showroom_opname_sessions', 'status'):
        op.execute("ALTER TABLE showroom_opname_sessions MODIFY status VARCHAR(20) NOT NULL DEFAULT 'draft'")

    # ═══════════════════════════════════════════════════════════
    # showroom_reservations
    # ═══════════════════════════════════════════════════════════
    if _col_is_enum('showroom_reservations', 'status'):
        op.execute("ALTER TABLE showroom_reservations MODIFY status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE'")


def downgrade() -> None:
    # This migration is idempotent and handles multiple partial DB states.
    # Downgrade is not safely reversible without knowing the exact starting state.
    pass
