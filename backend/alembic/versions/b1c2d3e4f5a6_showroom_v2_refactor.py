"""showroom_v2_refactor

Revision ID: b1c2d3e4f5a6
Revises: 8d25a464bff9
Create Date: 2026-07-18 20:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'b1c2d3e4f5a6'
down_revision: Union[str, Sequence[str], None] = '8d25a464bff9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
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
    sa.UniqueConstraint('type', 'value', name='uix_master_data_type_value')
    )
    op.create_index(op.f('ix_showroom_master_data_id'), 'showroom_master_data', ['id'], unique=False)
    op.create_index(op.f('ix_showroom_master_data_type'), 'showroom_master_data', ['type'], unique=False)

    op.add_column('showroom_sample_stocks', sa.Column('sample_type', sa.String(length=50), nullable=True))

    op.add_column('showroom_movements', sa.Column('sample_type', sa.String(length=50), nullable=True))

    op.add_column('showroom_guest_releases', sa.Column('status', sa.String(length=20), nullable=False, server_default='DRAFT'))
    op.add_column('showroom_guest_releases', sa.Column('location_id', sa.Integer(), nullable=True))
    op.add_column('showroom_guest_releases', sa.Column('rejected_by', sa.Integer(), nullable=True))
    op.add_column('showroom_guest_releases', sa.Column('rejected_at', sa.DateTime(), nullable=True))
    op.create_foreign_key('fk_guest_release_location', 'showroom_guest_releases', 'showroom_locations', ['location_id'], ['id'])
    op.create_foreign_key('fk_guest_release_rejected_by', 'showroom_guest_releases', 'users', ['rejected_by'], ['id'])

    op.add_column('showroom_borrowings', sa.Column('borrowed_at', sa.DateTime(), nullable=True))
    op.add_column('showroom_borrowings', sa.Column('sample_type', sa.String(length=50), nullable=True))

    op.add_column('showroom_restock_requests', sa.Column('source', sa.String(length=20), nullable=False, server_default='auto'))

    op.alter_column('showroom_maintenance', 'maintenance_type',
        existing_type=sa.Enum('LAUNDRY', 'REPAIR', 'CLEANING', 'OTHER', name='showroommaintenancetype'),
        type_=sa.String(length=50),
        nullable=False)
    op.add_column('showroom_maintenance', sa.Column('sample_type', sa.String(length=50), nullable=True))


def downgrade() -> None:
    op.drop_column('showroom_maintenance', 'sample_type')
    op.alter_column('showroom_maintenance', 'maintenance_type',
        existing_type=sa.String(length=50),
        type_=sa.Enum('LAUNDRY', 'REPAIR', 'CLEANING', 'OTHER', name='showroommaintenancetype'),
        nullable=False)

    op.drop_column('showroom_restock_requests', 'source')

    op.drop_column('showroom_borrowings', 'sample_type')
    op.drop_column('showroom_borrowings', 'borrowed_at')

    op.drop_constraint('fk_guest_release_rejected_by', 'showroom_guest_releases', type_='foreignkey')
    op.drop_constraint('fk_guest_release_location', 'showroom_guest_releases', type_='foreignkey')
    op.drop_column('showroom_guest_releases', 'rejected_at')
    op.drop_column('showroom_guest_releases', 'rejected_by')
    op.drop_column('showroom_guest_releases', 'location_id')
    op.drop_column('showroom_guest_releases', 'status')

    op.drop_column('showroom_movements', 'sample_type')

    op.drop_column('showroom_sample_stocks', 'sample_type')

    op.drop_index(op.f('ix_showroom_master_data_type'), table_name='showroom_master_data')
    op.drop_index(op.f('ix_showroom_master_data_id'), table_name='showroom_master_data')
    op.drop_table('showroom_master_data')
