"""002 create QR entities and activity logs

Revision ID: 002b2c3d4e5f
Revises: 001a1b2c3d4e
Create Date: 2026-07-19 12:05:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '002b2c3d4e5f'
down_revision: Union[str, Sequence[str], None] = '001a1b2c3d4e'
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
    # QR Entities
    if not _table_exists('showroom_qr_entities'):
        op.create_table('showroom_qr_entities',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('entity_type', sa.String(length=50), nullable=False),
            sa.Column('entity_id', sa.Integer(), nullable=False),
            sa.Column('token', sa.String(length=100), nullable=False),
            sa.Column('label', sa.String(length=100), nullable=True),
            sa.Column('storage_location_id', sa.Integer(), nullable=True),
            sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
            sa.Column('version', sa.Integer(), nullable=False, server_default='1'),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id'),
        )
        op.create_index('ix_showroom_qr_entities_id', 'showroom_qr_entities', ['id'], unique=False)
        op.create_index('ix_showroom_qr_entities_entity_type', 'showroom_qr_entities', ['entity_type'], unique=False)
        op.create_index('ix_showroom_qr_entities_entity_id', 'showroom_qr_entities', ['entity_id'], unique=False)
        op.create_index('ix_showroom_qr_entities_token', 'showroom_qr_entities', ['token'], unique=True)
        op.create_index('ix_showroom_qr_entities_storage_location_id', 'showroom_qr_entities', ['storage_location_id'], unique=False)
        op.create_foreign_key(
            'fk_qr_entity_storage',
            'showroom_qr_entities',
            'showroom_storage_locations',
            ['storage_location_id'],
            ['id'],
        )

    # Activity Logs
    if not _table_exists('showroom_activity_logs'):
        op.create_table('showroom_activity_logs',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('action', sa.String(length=50), nullable=False),
            sa.Column('entity_type', sa.String(length=50), nullable=False),
            sa.Column('entity_id', sa.Integer(), nullable=False),
            sa.Column('actor_id', sa.Integer(), nullable=True),
            sa.Column('actor_type', sa.String(length=20), nullable=False, server_default='USER'),
            sa.Column('request_id', sa.String(length=36), nullable=True),
            sa.Column('idempotency_key', sa.String(length=100), nullable=True),
            sa.Column('detail', sa.Text(), nullable=True),
            sa.Column('old_value', sa.Text(), nullable=True),
            sa.Column('new_value', sa.Text(), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id'),
        )
        op.create_index('ix_showroom_activity_logs_id', 'showroom_activity_logs', ['id'], unique=False)
        op.create_index('ix_showroom_activity_logs_action', 'showroom_activity_logs', ['action'], unique=False)
        op.create_index('ix_showroom_activity_logs_entity_type', 'showroom_activity_logs', ['entity_type'], unique=False)
        op.create_index('ix_showroom_activity_logs_actor_id', 'showroom_activity_logs', ['actor_id'], unique=False)
        op.create_index('ix_showroom_activity_logs_request_id', 'showroom_activity_logs', ['request_id'], unique=False)
        op.create_index('ix_showroom_activity_logs_idempotency_key', 'showroom_activity_logs', ['idempotency_key'], unique=True)
        op.create_foreign_key(
            'fk_activity_log_actor',
            'showroom_activity_logs',
            'users',
            ['actor_id'],
            ['id'],
        )


def downgrade() -> None:
    if _table_exists('showroom_activity_logs'):
        op.drop_constraint('fk_activity_log_actor', 'showroom_activity_logs', type_='foreignkey')
        op.drop_index('ix_showroom_activity_logs_idempotency_key', 'showroom_activity_logs')
        op.drop_index('ix_showroom_activity_logs_request_id', 'showroom_activity_logs')
        op.drop_index('ix_showroom_activity_logs_actor_id', 'showroom_activity_logs')
        op.drop_index('ix_showroom_activity_logs_entity_type', 'showroom_activity_logs')
        op.drop_index('ix_showroom_activity_logs_action', 'showroom_activity_logs')
        op.drop_index('ix_showroom_activity_logs_id', 'showroom_activity_logs')
        op.drop_table('showroom_activity_logs')

    if _table_exists('showroom_qr_entities'):
        op.drop_constraint('fk_qr_entity_storage', 'showroom_qr_entities', type_='foreignkey')
        op.drop_index('ix_showroom_qr_entities_storage_location_id', 'showroom_qr_entities')
        op.drop_index('ix_showroom_qr_entities_token', 'showroom_qr_entities')
        op.drop_index('ix_showroom_qr_entities_entity_id', 'showroom_qr_entities')
        op.drop_index('ix_showroom_qr_entities_entity_type', 'showroom_qr_entities')
        op.drop_index('ix_showroom_qr_entities_id', 'showroom_qr_entities')
        op.drop_table('showroom_qr_entities')
