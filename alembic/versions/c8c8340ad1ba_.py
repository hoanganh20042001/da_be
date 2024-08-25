"""empty message

Revision ID: c8c8340ad1ba
Revises: 1290c236c341
Create Date: 2024-08-15 14:10:13.676033

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c8c8340ad1ba'
down_revision = '1290c236c341'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('roles',
    sa.Column('id', sa.String(length=1), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True), 
    sa.Column('description', sa.Text, nullable=True), 
    sa.PrimaryKeyConstraint('id')
    )
    # op.drop_column('users', 'role')
    # op.add_column('user', sa.Column('role_id', sa.String(length=1), nullable=False))
    # op.add_column('user', sa.Column('deleted', sa.Boolean(), nullable=True))
    # op.add_column('patients', sa.Column('deleted', sa.Boolean(), nullable=True))
def downgrade():
    op.drop_table('roles')
    # op.drop_column('users', 'role_id')
    # op.drop_column('users', 'deleted')
    # op.drop_column('patients', 'deleted')
    