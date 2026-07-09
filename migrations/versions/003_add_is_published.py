"""add is_published and published_at to clients

Revision ID: 003_add_is_published
Revises: 363419dae104
Create Date: 2026-07-09

"""
from alembic import op
import sqlalchemy as sa

revision = '003_add_is_published'
down_revision = '363419dae104'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('clients', sa.Column('is_published', sa.Boolean(),
        nullable=False, server_default=sa.text('false')))
    op.add_column('clients', sa.Column('published_at', sa.DateTime(),
        nullable=True))
    op.execute("UPDATE clients SET is_published = true")
    op.alter_column('clients', 'is_published', server_default=None)


def downgrade():
    op.drop_column('clients', 'published_at')
    op.drop_column('clients', 'is_published')
