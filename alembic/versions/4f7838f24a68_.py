"""empty message

Revision ID: 4f7838f24a68
Revises: 7c66fb30fbea
Create Date: 2024-08-25 23:34:26.671592

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4f7838f24a68'
down_revision = '7c66fb30fbea'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('checks', sa.Column('result', sa.Boolean, nullable=True))
    op.add_column('units', sa.Column('unit_father_id', sa.Integer(), nullable=True))
    


def downgrade():
    op.drop_column('checks', 'result')
    op.drop_column('units', 'unit_father_id')
    