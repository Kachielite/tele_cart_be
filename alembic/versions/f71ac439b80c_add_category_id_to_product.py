"""Add category_id to product

Revision ID: f71ac439b80c
Revises: e84e127b1725
Create Date: 2024-11-10 04:07:17.711548

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f71ac439b80c'
down_revision: Union[str, None] = 'e84e127b1725'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add the category_id column to the product table
    op.add_column('products', sa.Column('category_id', sa.Integer(), nullable=True))

    # Create a foreign key constraint between product.category_id and categories.id
    op.create_foreign_key('fk_product_category', 'products', 'categories', ['category_id'], ['id'])


def downgrade() -> None:
    # Drop the foreign key constraint
    op.drop_constraint('fk_product_category', 'products', type_='foreignkey')

    # Drop the category_id column from the product table
    op.drop_column('products', 'category_id')
