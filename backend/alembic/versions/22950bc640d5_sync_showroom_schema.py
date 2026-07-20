"""sync showroom schema

Revision ID: 22950bc640d5
Revises: fa19af456943
Create Date: 2026-07-18 21:41:49.233932

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '22950bc640d5'
down_revision: Union[str, Sequence[str], None] = 'fa19af456943'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


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
    # ─── showroom_borrowings: status ENUM → String ───
    if _col_is_enum('showroom_borrowings', 'status'):
        op.execute("ALTER TABLE showroom_borrowings MODIFY status VARCHAR(20) NOT NULL DEFAULT 'BORROWED'")

    # ─── showroom_borrowings: drop approved_by + approved_at ───
    if _col_exists('showroom_borrowings', 'approved_by'):
        _drop_fk_by_column('showroom_borrowings', 'approved_by', 'users')
        op.drop_column('showroom_borrowings', 'approved_by')

    if _col_exists('showroom_borrowings', 'approved_at'):
        op.drop_column('showroom_borrowings', 'approved_at')

    # ─── showroom_maintenance: status ENUM → String ───
    if _col_is_enum('showroom_maintenance', 'status'):
        op.execute("ALTER TABLE showroom_maintenance MODIFY status VARCHAR(20) NOT NULL DEFAULT 'PENDING'")

    # ─── showroom_master_data: drop unique constraint ───
    if _constraint_exists('showroom_master_data', 'uix_master_data_type_value'):
        op.drop_constraint('uix_master_data_type_value', 'showroom_master_data', type_='unique')

    # ─── showroom_movements: expand Enum values (ENUM → String) ───
    if _col_is_enum('showroom_movements', 'movement_type'):
        op.execute("ALTER TABLE showroom_movements MODIFY movement_type VARCHAR(50) NOT NULL")

    # ─── showroom_opname_sessions: status ENUM → String ───
    if _col_is_enum('showroom_opname_sessions', 'status'):
        op.execute("ALTER TABLE showroom_opname_sessions MODIFY status VARCHAR(20) NOT NULL DEFAULT 'draft'")

    # ─── showroom_reservations: status ENUM → String ───
    if _col_is_enum('showroom_reservations', 'status'):
        op.execute("ALTER TABLE showroom_reservations MODIFY status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE'")

    # ─── showroom_restock_requests ───
    if not _col_exists('showroom_restock_requests', 'sample_type'):
        op.add_column('showroom_restock_requests', sa.Column('sample_type', sa.String(length=50), nullable=True))

    op.execute("ALTER TABLE showroom_restock_requests MODIFY minimum_quantity INT NULL")
    op.execute("ALTER TABLE showroom_restock_requests MODIFY current_quantity INT NULL")

    if _col_is_enum('showroom_restock_requests', 'status'):
        op.execute("ALTER TABLE showroom_restock_requests MODIFY status VARCHAR(20) NOT NULL DEFAULT 'PENDING'")

    # ─── showroom_sample_stocks: replace unique constraint ───
    if _constraint_exists('showroom_sample_stocks', 'uix_showroom_stock_product_location'):
        if not _index_exists('showroom_sample_stocks', 'ix_showroom_sample_stocks_product_id'):
            op.create_index('ix_showroom_sample_stocks_product_id', 'showroom_sample_stocks', ['product_id'], unique=False)
        if not _index_exists('showroom_sample_stocks', 'ix_showroom_sample_stocks_location_id'):
            op.create_index('ix_showroom_sample_stocks_location_id', 'showroom_sample_stocks', ['location_id'], unique=False)
        op.drop_constraint('uix_showroom_stock_product_location', 'showroom_sample_stocks', type_='unique')

    if not _constraint_exists('showroom_sample_stocks', 'uix_showroom_stock_product_location_type'):
        op.create_unique_constraint('uix_showroom_stock_product_location_type', 'showroom_sample_stocks', ['product_id', 'location_id', 'sample_type'])


def downgrade() -> None:
    op.drop_constraint('uix_showroom_stock_product_location_type', 'showroom_sample_stocks', type_='unique')
    op.create_index('uix_showroom_stock_product_location', 'showroom_sample_stocks', ['product_id', 'location_id'], unique=True)
    op.execute("ALTER TABLE showroom_restock_requests MODIFY minimum_quantity INT NOT NULL")
    op.execute("ALTER TABLE showroom_restock_requests MODIFY current_quantity INT NOT NULL")
    op.drop_column('showroom_restock_requests', 'sample_type')
    op.create_index('uix_master_data_type_value', 'showroom_master_data', ['type', 'value'], unique=True)
    op.add_column('showroom_borrowings', sa.Column('approved_at', sa.DateTime(), nullable=True))
    op.add_column('showroom_borrowings', sa.Column('approved_by', sa.Integer(), nullable=True))
    op.create_foreign_key('showroom_borrowings_ibfk_1', 'showroom_borrowings', 'users', ['approved_by'], ['id'])
