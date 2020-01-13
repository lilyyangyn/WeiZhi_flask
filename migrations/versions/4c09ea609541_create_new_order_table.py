"""create new order table

Revision ID: 4c09ea609541
Revises: 3c87058ffb33
Create Date: 2020-01-14 04:39:16.573352

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c09ea609541'
down_revision = '3c87058ffb33'
branch_labels = None
depends_on = None


def upgrade():
		op.drop_table('orders')
		op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dish_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('spot_id', sa.Integer(), nullable=False),
    sa.Column('to_be_paid', sa.Integer(), nullable=False),
    sa.Column('today_id', sa.String(length=16)),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('price_sold', sa.Integer(), nullable=True),
    sa.Column('original_price', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['dish_id'], ['dishes.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    

def downgrade():
    pass
