"""add index on orders.user_id

Revision ID: 91ffe8dcdb49
Revises: 4c09ea609541
Create Date: 2020-01-14 04:51:30.431895

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91ffe8dcdb49'
down_revision = '4c09ea609541'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index(op.f('ix_orders_user_id'), 'orders', ['user_id'], unique=False)


def downgrade():
    pass
