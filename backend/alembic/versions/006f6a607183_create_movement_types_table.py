"""006f create movement_types table + seed data

Revision ID: 006f6a607183
Revises: 005e5f607182
Create Date: 2026-07-21 14:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '006f6a607183'
down_revision: Union[str, Sequence[str], None] = '005e5f607182'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _table_exists(name: str) -> bool:
    conn = op.get_bind()
    r = conn.execute(sa.text(
        "SELECT COUNT(*) FROM information_schema.tables "
        "WHERE table_schema = DATABASE() AND table_name = :t"
    ), {"t": name})
    return r.scalar() > 0


_data = [
    ("HANDOVER", "Handover", "IN"),
    ("SHOWROOM_IN", "Showroom In", "IN"),
    ("RETURN", "Return", "IN"),
    ("RESTOCK", "Restock", "IN"),
    ("TRANSFER_IN", "Transfer In", "IN"),
    ("MAINTENANCE_RETURN", "Maintenance Return", "IN"),
    ("ADJUSTMENT", "Adjustment", "IN"),
    ("SHOWROOM_OUT", "Showroom Out", "OUT"),
    ("BORROW", "Borrow", "OUT"),
    ("TRANSFER_OUT", "Transfer Out", "OUT"),
    ("RELEASE", "Release", "OUT"),
    ("RELEASE_REJECT", "Release Reject", "OUT"),
    ("MAINTENANCE_OUT", "Maintenance Out", "OUT"),
    ("RETIRED", "Retired", "OUT"),
    ("SCRAP", "Scrap", "OUT"),
    ("TRANSFER", "Transfer", "OUT"),
]


def upgrade() -> None:
    conn = op.get_bind()
    if not _table_exists('showroom_movement_types'):
        op.create_table('showroom_movement_types',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('code', sa.String(length=50), nullable=False),
            sa.Column('name', sa.String(length=100), nullable=False),
            sa.Column('direction', sa.String(length=10), nullable=False),
            sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id'),
        )
        op.create_index('ix_showroom_movement_types_id', 'showroom_movement_types', ['id'], unique=False)
        op.create_index('ix_showroom_movement_types_code', 'showroom_movement_types', ['code'], unique=True)

    # seed data
    for code, name, direction in _data:
        r = conn.execute(sa.text(
            "SELECT COUNT(*) FROM showroom_movement_types WHERE code = :c"
        ), {"c": code})
        if r.scalar() == 0:
            op.execute(
                sa.text(
                    "INSERT INTO showroom_movement_types (code, name, direction, is_active) "
                    "VALUES (:code, :name, :direction, 1)"
                ).bindparams(code=code, name=name, direction=direction)
            )


def downgrade() -> None:
    if _table_exists('showroom_movement_types'):
        op.drop_index('ix_showroom_movement_types_code', 'showroom_movement_types')
        op.drop_index('ix_showroom_movement_types_id', 'showroom_movement_types')
        op.drop_table('showroom_movement_types')
