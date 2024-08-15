"""empty message

Revision ID: 8e4071b4bd0b
Revises: 31f5ad5aec74
Create Date: 2024-07-16 15:15:58.820633

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e4071b4bd0b'
down_revision = '31f5ad5aec74'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('checks',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('patient_id', sa.Integer(), nullable=True), 
    sa.Column('user_id', sa.Integer(), nullable=True), 
    sa.Column('image_1', sa.Text, nullable=True), 
    sa.Column('image_2', sa.Text, nullable=True), 
    sa.Column('description', sa.Text, nullable=True), 
    sa.Column('date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('checks')
