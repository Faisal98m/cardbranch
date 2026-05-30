"""add tier and delivery fields to orders

Revision ID: 001_add_order_fields
Revises:
Create Date: 2026-05-30

"""
from alembic import op
import sqlalchemy as sa

revision = '001_add_order_fields'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('orders', sa.Column('stripe_session_id', sa.String(255), nullable=True, server_default=''))
    op.add_column('orders', sa.Column('tier', sa.String(50), nullable=True, server_default='standard'))
    op.add_column('orders', sa.Column('delivery_name', sa.String(255), nullable=True, server_default=''))
    op.add_column('orders', sa.Column('delivery_line1', sa.String(255), nullable=True, server_default=''))
    op.add_column('orders', sa.Column('delivery_line2', sa.String(255), nullable=True, server_default=''))
    op.add_column('orders', sa.Column('delivery_city', sa.String(100), nullable=True, server_default=''))
    op.add_column('orders', sa.Column('delivery_postcode', sa.String(20), nullable=True, server_default=''))


def downgrade():
    op.drop_column('orders', 'delivery_postcode')
    op.drop_column('orders', 'delivery_city')
    op.drop_column('orders', 'delivery_line2')
    op.drop_column('orders', 'delivery_line1')
    op.drop_column('orders', 'delivery_name')
    op.drop_column('orders', 'tier')
    op.drop_column('orders', 'stripe_session_id')
