"""Ajout du stock

Revision ID: b414a3bc46c0
Revises: 09ac3171ba17
Create Date: 2021-05-10 22:02:26.884273

"""
from alembic import op
import sqlalchemy as sa
from api.models import products


# revision identifiers, used by Alembic.
revision = 'b414a3bc46c0'
down_revision = '09ac3171ba17'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('stock', sa.Boolean(), default=True, nullable=True))
    op.execute(products.update().values(stock=True))
    op.alter_column('products', 'stock', existing_type=sa.BOOLEAN(), nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'stock')
    # ### end Alembic commands ###
