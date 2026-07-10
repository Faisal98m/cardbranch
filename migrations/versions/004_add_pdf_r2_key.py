"""add pdf_r2_key to clients

Revision ID: 004_add_pdf_r2_key
Revises: 003_add_is_published
Create Date: 2026-07-09

"""
from alembic import op
import sqlalchemy as sa


revision = '004_add_pdf_r2_key'
down_revision = '003_add_is_published'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('clients', sa.Column('pdf_r2_key', sa.String(length=500), nullable=True))


def downgrade():
    op.drop_column('clients', 'pdf_r2_key')
