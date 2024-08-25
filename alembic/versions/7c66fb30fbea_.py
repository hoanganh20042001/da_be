"""empty message

Revision ID: 7c66fb30fbea
Revises: c8c8340ad1ba
Create Date: 2024-08-15 14:22:47.095508

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7c66fb30fbea'
down_revision = 'c8c8340ad1ba'
branch_labels = None
depends_on = None


def upgrade():
    # op.drop_column('users', 'role')
    op.add_column('user', sa.Column('role_id', sa.String(length=1), nullable=False))
    op.add_column('user', sa.Column('deleted', sa.Boolean(), nullable=True))
    op.add_column('patients', sa.Column('deleted', sa.Boolean(), nullable=True))


def downgrade():
    op.drop_column('users', 'role_id')
    op.drop_column('users', 'deleted')
    op.drop_column('patients', 'deleted')
