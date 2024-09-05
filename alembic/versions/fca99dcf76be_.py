"""empty message

Revision ID: fca99dcf76be
Revises: 15d80379f534
Create Date: 2024-09-01 09:45:45.316732

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'fca99dcf76be'
down_revision = '15d80379f534'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('user_histories',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False), 
    sa.Column('user_agent', sa.Text, nullable=True), 
    sa.Column('method', sa.String(length=20), nullable=True), 
    sa.Column('path',sa.String(length=255), nullable=True), 
    sa.Column('status_code',sa.String(length=5), nullable=True), 
    sa.PrimaryKeyConstraint('id')
    )



def downgrade():
    op.drop_table('user_histories')
