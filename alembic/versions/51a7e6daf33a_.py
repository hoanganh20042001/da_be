"""empty message

Revision ID: 51a7e6daf33a
Revises: 8be979d3dfe5
Create Date: 2024-08-11 23:19:54.711898

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '51a7e6daf33a'
down_revision = '8be979d3dfe5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('checks', sa.Column('time', sa.INTEGER, nullable=True))
    op.add_column('results', sa.Column('image', sa.Text, nullable=True))
    op.add_column('results', sa.Column('accuracy', sa.FLOAT, nullable=True))

def downgrade():
    op.drop_column('checks', 'time')
    op.drop_column('results', 'image')
    op.drop_column('results', 'accuracy')

