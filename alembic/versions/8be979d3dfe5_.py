"""empty message

Revision ID: 8be979d3dfe5
Revises: d2d8a65da71c
Create Date: 2024-07-25 20:10:38.273809

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8be979d3dfe5'
down_revision = 'd2d8a65da71c'
branch_labels = None
depends_on = None


def upgrade():
      op.create_table('units',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True), 
    sa.Column('symbol', sa.String(length=255), nullable=True), 
    sa.Column('description', sa.Text, nullable=True), 
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('units')
