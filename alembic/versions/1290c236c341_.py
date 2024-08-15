"""empty message

Revision ID: 1290c236c341
Revises: 51a7e6daf33a
Create Date: 2024-08-14 20:52:12.174140

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1290c236c341'
down_revision = '51a7e6daf33a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('diseases', sa.Column('reason', sa.Text, nullable=True))
    op.add_column('diseases', sa.Column('expression', sa.Text, nullable=True))
    op.add_column('diseases', sa.Column('advice', sa.Text, nullable=True))


def downgrade():
    op.drop_column('diseases', 'reason')
    op.drop_column('diseases', 'expression')
    op.drop_column('diseases', 'advice')
    