"""empty message

Revision ID: 6e058e3bdc1f
Revises: 8e4071b4bd0b
Create Date: 2024-07-16 15:41:03.211735

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6e058e3bdc1f'
down_revision = '8e4071b4bd0b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('results',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('check_id', sa.Integer(), nullable=True), 
    sa.Column('disease_id', sa.Integer(), nullable=True), 
    sa.Column('location', sa.String(length=255), nullable=True), 
    sa.Column('content', sa.Text, nullable=True), 
    sa.Column('description', sa.Text, nullable=True), 
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('results')