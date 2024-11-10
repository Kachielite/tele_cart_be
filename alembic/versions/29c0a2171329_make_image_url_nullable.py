"""Make image_url nullable

Revision ID: 29c0a2171329
Revises: f71ac439b80c
Create Date: 2024-11-10 13:34:30.754929

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '29c0a2171329'
down_revision: Union[str, None] = 'f71ac439b80c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Alter the image_url column to be nullable
    op.alter_column('products', 'image_url', existing_type=sa.String(), nullable=True)

def downgrade() -> None:
    # Revert the image_url column to be non-nullable
    op.alter_column('products', 'image_url', existing_type=sa.String(), nullable=False)