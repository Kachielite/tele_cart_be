"""Add Cart table

Revision ID: f4f6ed698efe
Revises: 29c0a2171329
Create Date: 2024-11-24 09:55:00.431812

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4f6ed698efe'
down_revision: Union[str, None] = '29c0a2171329'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create the 'cart' table
    op.create_table(
        'cart',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('business_id', sa.Integer, sa.ForeignKey('businesses.id'), nullable=True),
        sa.Column('customer_id', sa.Integer, sa.ForeignKey('customers.id'), nullable=True),
        sa.Column('product_id', sa.Integer, sa.ForeignKey('products.id'), nullable=True),
        sa.Column('added_at', sa.DateTime, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())
    )


def downgrade():
    # Drop the 'cart' table
    op.drop_table('cart')

