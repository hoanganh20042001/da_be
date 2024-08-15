"""empty message

Revision ID: 31f5ad5aec74
Revises: e75c154255ca
Create Date: 2024-07-16 15:11:10.362896

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31f5ad5aec74'
down_revision = 'e75c154255ca'
branch_labels = None
depends_on = None


def upgrade():
   op.create_table('diseases',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True), 
    sa.Column('name_E', sa.String(length=255), nullable=True), 
    sa.Column('symbol', sa.String(length=255), nullable=True), 
    sa.Column('description', sa.Text, nullable=True), 
    sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('diseases')
