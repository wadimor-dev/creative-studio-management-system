"""008f drop showroom permissions/roles/user_roles tables

Revision ID: 008f8a607185
Revises: 007f7a607184
Create Date: 2026-07-21 16:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '008f8a607185'
down_revision: Union[str, Sequence[str], None] = '007f7a607184'
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
    if _table_exists('showroom_user_roles'):
        op.drop_table('showroom_user_roles')
    if _table_exists('showroom_role_permissions'):
        op.drop_table('showroom_role_permissions')
    if _table_exists('showroom_roles'):
        op.drop_index('ix_showroom_roles_code', 'showroom_roles')
        op.drop_index('ix_showroom_roles_id', 'showroom_roles')
        op.drop_table('showroom_roles')
    if _table_exists('showroom_permissions'):
        op.drop_index('ix_showroom_permissions_code', 'showroom_permissions')
        op.drop_index('ix_showroom_permissions_id', 'showroom_permissions')
        op.drop_table('showroom_permissions')


def downgrade() -> None:
    pass
