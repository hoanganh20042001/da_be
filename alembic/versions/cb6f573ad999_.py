"""empty message

Revision ID: cb6f573ad999
Revises: fca99dcf76be
Create Date: 2024-09-09 15:01:32.112152

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'cb6f573ad999'
down_revision = 'fca99dcf76be'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('checks', sa.Column('status', sa.Boolean(), nullable=True))


def downgrade():
    op.drop_column('checks', 'status')