"""empty message

Revision ID: 15d80379f534
Revises: 4f7838f24a68
Create Date: 2024-08-31 23:50:17.289266

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '15d80379f534'
down_revision = '4f7838f24a68'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('patients', sa.Column('email', sa.String(length=255), nullable=True))
    op.add_column('patients', sa.Column('position', sa.String(length=255), nullable=True))


def downgrade():
    op.drop_column('patients', 'email')
    op.drop_column('patients', 'position')
    