"""set order.today_id nullable so that it can be generated later in constructor

Revision ID: 3c87058ffb33
Revises: 38e8350c2bd1
Create Date: 2020-01-14 04:04:12.621351

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c87058ffb33'
down_revision = '38e8350c2bd1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('orders', 'today_id',
               existing_type=sa.VARCHAR(length=16),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('orders', 'today_id',
               existing_type=sa.VARCHAR(length=16),
               nullable=False)
    # ### end Alembic commands ###