"""Otp Code and User Restaurant

Revision ID: 649a8703a758
Revises: 
Create Date: 2023-05-25 17:11:40.799010

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '649a8703a758'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('otp_code_restaurant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=7), nullable=True),
    sa.Column('expired', sa.Boolean(), nullable=True),
    sa.Column('phone_number', sa.String(length=11), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_otp_code_restaurant_code'), 'otp_code_restaurant', ['code'], unique=False)
    op.create_index(op.f('ix_otp_code_restaurant_id'), 'otp_code_restaurant', ['id'], unique=False)
    op.create_index(op.f('ix_otp_code_restaurant_phone_number'), 'otp_code_restaurant', ['phone_number'], unique=False)
    op.create_table('user_restaurant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('phone_number', sa.String(length=11), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_user_restaurant_id'), 'user_restaurant', ['id'], unique=False)
    op.create_index(op.f('ix_user_restaurant_phone_number'), 'user_restaurant', ['phone_number'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_restaurant_phone_number'), table_name='user_restaurant')
    op.drop_index(op.f('ix_user_restaurant_id'), table_name='user_restaurant')
    op.drop_table('user_restaurant')
    op.drop_index(op.f('ix_otp_code_restaurant_phone_number'), table_name='otp_code_restaurant')
    op.drop_index(op.f('ix_otp_code_restaurant_id'), table_name='otp_code_restaurant')
    op.drop_index(op.f('ix_otp_code_restaurant_code'), table_name='otp_code_restaurant')
    op.drop_table('otp_code_restaurant')
    # ### end Alembic commands ###