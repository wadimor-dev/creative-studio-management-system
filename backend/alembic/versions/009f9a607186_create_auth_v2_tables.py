"""009 create auth v2 tables (permissions, role_permissions, user_roles, user_sessions)

Revision ID: 009f9a607186
Revises: 008f8a607185
Create Date: 2026-07-21 22:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

revision: str = '009f9a607186'
down_revision: Union[str, Sequence[str], None] = '008f8a607185'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _table_exists(name: str) -> bool:
    conn = op.get_bind()
    r = conn.execute(sa.text(
        "SELECT COUNT(*) FROM information_schema.tables "
        "WHERE table_schema = DATABASE() AND table_name = :t"
    ), {"t": name})
    return r.scalar() > 0


def _column_exists(table: str, column: str) -> bool:
    conn = op.get_bind()
    r = conn.execute(sa.text(
        "SELECT COUNT(*) FROM information_schema.columns "
        "WHERE table_schema = DATABASE() AND table_name = :t AND column_name = :c"
    ), {"t": table, "c": column})
    return r.scalar() > 0


def upgrade() -> None:
    # 1. Add is_system column to roles
    if not _column_exists('roles', 'is_system'):
        op.add_column('roles', sa.Column('is_system', sa.Boolean(), nullable=False, server_default=sa.text('1')))
        # Mark existing roles (ADMIN, STAFF, MANAGER, CREATIVE) as system
        op.execute("UPDATE roles SET is_system = 1 WHERE name IN ('ADMIN', 'STAFF', 'MANAGER', 'CREATIVE')")

    # 2. Create permissions table
    if not _table_exists('permissions'):
        op.create_table('permissions',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('code', sa.String(length=100), nullable=False),
            sa.Column('name', sa.String(length=200), nullable=False),
            sa.Column('module', sa.String(length=50), nullable=True),
            sa.Column('description', sa.Text(), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
            sa.PrimaryKeyConstraint('id'),
            mysql_engine='InnoDB',
            mysql_charset='utf8mb4',
        )
        op.create_index('ix_permissions_id', 'permissions', ['id'])
        op.create_index('ix_permissions_code', 'permissions', ['code'], unique=True)
        op.create_index('ix_permissions_module', 'permissions', ['module'])

    # 3. Create role_permissions table
    if not _table_exists('role_permissions'):
        op.create_table('role_permissions',
            sa.Column('role_id', sa.Integer(), sa.ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True),
            sa.Column('permission_id', sa.Integer(), sa.ForeignKey('permissions.id', ondelete='CASCADE'), primary_key=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
            mysql_engine='InnoDB',
            mysql_charset='utf8mb4',
        )

    # 4. Create user_roles table
    if not _table_exists('user_roles'):
        op.create_table('user_roles',
            sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
            sa.Column('role_id', sa.Integer(), sa.ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
            mysql_engine='InnoDB',
            mysql_charset='utf8mb4',
        )

        # Migrate existing users.role_id to user_roles
        if _column_exists('users', 'role_id'):
            op.execute("""
                INSERT IGNORE INTO user_roles (user_id, role_id)
                SELECT id, role_id FROM users WHERE role_id IS NOT NULL
            """)

    # 5. Drop role_id from users (after migrating data)
    if _column_exists('users', 'role_id'):
        op.drop_constraint('users_ibfk_1', 'users', type_='foreignkey')
        op.drop_column('users', 'role_id')

    # 6. Create user_sessions table
    if not _table_exists('user_sessions'):
        op.create_table('user_sessions',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
            sa.Column('refresh_token_hash', sa.String(length=255), nullable=False),
            sa.Column('device', sa.String(length=100), nullable=True),
            sa.Column('ip_address', sa.String(length=45), nullable=True),
            sa.Column('user_agent', sa.Text(), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
            sa.Column('expired_at', sa.DateTime(timezone=True), nullable=False),
            sa.Column('last_used_at', sa.DateTime(timezone=True), nullable=True),
            sa.Column('revoked_at', sa.DateTime(timezone=True), nullable=True),
            sa.Column('is_revoked', sa.Boolean(), server_default=sa.text('0')),
            sa.PrimaryKeyConstraint('id'),
            mysql_engine='InnoDB',
            mysql_charset='utf8mb4',
        )
        op.create_index('ix_user_sessions_id', 'user_sessions', ['id'])
        op.create_index('ix_user_sessions_user_id', 'user_sessions', ['user_id'])


def downgrade() -> None:
    # Drop tables in reverse order
    if _table_exists('user_sessions'):
        op.drop_index('ix_user_sessions_user_id', 'user_sessions')
        op.drop_index('ix_user_sessions_id', 'user_sessions')
        op.drop_table('user_sessions')

    # Restore role_id column
    if not _column_exists('users', 'role_id'):
        op.add_column('users', sa.Column('role_id', sa.Integer(), sa.ForeignKey('roles.id'), nullable=True))
        # Restore data from user_roles (first role only)
        op.execute("""
            UPDATE users u
            JOIN user_roles ur ON u.id = ur.user_id
            SET u.role_id = ur.role_id
        """)

    if _table_exists('user_roles'):
        op.drop_table('user_roles')

    if _table_exists('role_permissions'):
        op.drop_table('role_permissions')

    if _table_exists('permissions'):
        op.drop_index('ix_permissions_module', 'permissions')
        op.drop_index('ix_permissions_code', 'permissions')
        op.drop_index('ix_permissions_id', 'permissions')
        op.drop_table('permissions')

    if _column_exists('roles', 'is_system'):
        op.drop_column('roles', 'is_system')
