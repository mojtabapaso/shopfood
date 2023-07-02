"""Added table cart again

Revision ID: 708309faa33b
Revises: 26f0e0f58700
Create Date: 2023-06-01 10:16:26.968523

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '708309faa33b'
down_revision = '26f0e0f58700'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cart',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('qualify', sa.Integer(), nullable=True),
    sa.Column('user', sa.Integer(), nullable=True),
    sa.Column('restaurant', sa.Integer(), nullable=True),
    sa.Column('datatime', sa.DATETIME(), nullable=True),
    sa.Column('is_payment', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cart_id'), 'cart', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_cart_id'), table_name='cart')
    op.drop_table('cart')
    # ### end Alembic commands ###