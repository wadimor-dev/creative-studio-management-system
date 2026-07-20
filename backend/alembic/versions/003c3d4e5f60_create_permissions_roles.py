"""003 create permissions, roles, snapshots, daily summary

Revision ID: 003c3d4e5f60
Revises: 002b2c3d4e5f
Create Date: 2026-07-19 12:10:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '003c3d4e5f60'
down_revision: Union[str, Sequence[str], None] = '002b2c3d4e5f'
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
    if not _table_exists('showroom_permissions'):
        op.create_table('showroom_permissions',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('code', sa.String(length=50), nullable=False),
            sa.Column('name', sa.String(length=100), nullable=False),
            sa.Column('description', sa.String(length=255), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id'),
        )
        op.create_index('ix_showroom_permissions_id', 'showroom_permissions', ['id'], unique=False)
        op.create_index('ix_showroom_permissions_code', 'showroom_permissions', ['code'], unique=True)

    if not _table_exists('showroom_roles'):
        op.create_table('showroom_roles',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('code', sa.String(length=50), nullable=False),
            sa.Column('name', sa.String(length=100), nullable=False),
            sa.Column('description', sa.String(length=255), nullable=True),
            sa.Column('is_system', sa.Integer(), nullable=False, server_default='0'),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id'),
        )
        op.create_index('ix_showroom_roles_id', 'showroom_roles', ['id'], unique=False)
        op.create_index('ix_showroom_roles_code', 'showroom_roles', ['code'], unique=True)

    if not _table_exists('showroom_role_permissions'):
        op.create_table('showroom_role_permissions',
            sa.Column('role_id', sa.Integer(), nullable=False),
            sa.Column('permission_id', sa.Integer(), nullable=False),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('role_id', 'permission_id'),
            sa.ForeignKeyConstraint(['role_id'], ['showroom_roles.id']),
            sa.ForeignKeyConstraint(['permission_id'], ['showroom_permissions.id']),
        )

    if not _table_exists('showroom_user_roles'):
        op.create_table('showroom_user_roles',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.Column('role_id', sa.Integer(), nullable=False),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            sa.ForeignKeyConstraint(['user_id'], ['users.id']),
            sa.ForeignKeyConstraint(['role_id'], ['showroom_roles.id']),
        )
        op.create_index('ix_showroom_user_roles_id', 'showroom_user_roles', ['id'], unique=False)
        op.create_index('ix_showroom_user_roles_user_id', 'showroom_user_roles', ['user_id'], unique=False)
        op.create_index('ix_showroom_user_roles_role_id', 'showroom_user_roles', ['role_id'], unique=False)


def downgrade() -> None:
    if _table_exists('showroom_user_roles'):
        op.drop_index('ix_showroom_user_roles_role_id', 'showroom_user_roles')
        op.drop_index('ix_showroom_user_roles_user_id', 'showroom_user_roles')
        op.drop_index('ix_showroom_user_roles_id', 'showroom_user_roles')
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
