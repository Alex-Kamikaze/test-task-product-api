"""Удалено поле с датой добавления продукта

Revision ID: 538f964bf3e8
Revises: e460691a55ff
Create Date: 2024-09-05 04:48:29.210588

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '538f964bf3e8'
down_revision: Union[str, None] = 'e460691a55ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'product_date_of_addition')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('product_date_of_addition', sa.DATETIME(), nullable=True))
    # ### end Alembic commands ###
