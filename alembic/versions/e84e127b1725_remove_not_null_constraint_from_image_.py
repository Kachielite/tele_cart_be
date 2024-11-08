"""Remove not-null constraint from image_url column

Revision ID: e84e127b1725
Revises: 174946640f5d
Create Date: 2024-11-08 07:13:48.004290

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e84e127b1725'
down_revision: Union[str, None] = '174946640f5d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Remove NOT NULL constraint from 'image_url' column
    op.alter_column('businesses', 'image_url', nullable=True)

def downgrade():
    # Revert NOT NULL constraint on 'image_url' column
    op.alter_column('businesses', 'image_url', nullable=False)
