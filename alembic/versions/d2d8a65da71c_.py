"""empty message

Revision ID: d2d8a65da71c
Revises: 6e058e3bdc1f
Create Date: 2024-07-19 14:18:43.894892

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd2d8a65da71c'
down_revision = '6e058e3bdc1f'
branch_labels = None
depends_on = None


def upgrade():
   op.add_column('patients', sa.Column('avatar', sa.Text, nullable=True))
   op.add_column('patients', sa.Column('enlistment_date', sa.DateTime(), nullable=True))
   op.add_column('patients', sa.Column('unit_id', sa.Integer, nullable=True))
   op.add_column('patients', sa.Column('rank', sa.String(length=255), nullable=True))
   op.add_column('user', sa.Column('date_birth', sa.DateTime(), nullable=True))
   op.add_column('user', sa.Column('sex', sa.Boolean, nullable=True))
   op.add_column('user', sa.Column('unit_id', sa.Integer, nullable=True))
   op.add_column('user', sa.Column('phone_number', sa.String(length=10), nullable=True))
   op.add_column('user', sa.Column('rank', sa.String(length=255), nullable=True))
   op.add_column('user', sa.Column('position', sa.String(length=255), nullable=True))
   op.alter_column('patients', 'date_birth',
               existing_type=sa.Date,
               type_=sa.DateTime(),
               nullable=True)
   op.alter_column('relative', 'date_birth',
               existing_type=sa.Date,
               type_=sa.DateTime(),
               nullable=True)
    

def downgrade():
    op.drop_column('patients', 'image')
    op.drop_column('patients', 'enlistment_date')
    op.drop_column('patients', 'unit_id')
    op.drop_column('patients', 'rank')
    op.drop_column('user', 'date_birth')
    op.drop_column('user', 'sex')
    op.drop_column('user', 'unit_id')
    op.drop_column('user', 'phone_number')
    op.drop_column('user', 'rank')
    op.drop_column('user', 'position')
    op.alter_column('patients', 'date_birth',
               existing_type=sa.DateTime(),
               type_=sa.Date,
               nullable=True)
    op.alter_column('relative', 'date_birth',
               existing_type=sa.DateTime(),
               type_=sa.Date,
               nullable=True)