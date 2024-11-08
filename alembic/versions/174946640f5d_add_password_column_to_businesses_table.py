"""Add password column to businesses table

Revision ID: 174946640f5d
Revises: 1688ff82c92e
Create Date: 2024-11-08 06:16:12.023955

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '174946640f5d'
down_revision: Union[str, None] = '1688ff82c92e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add 'password' column to 'businesses' table
    op.add_column('businesses', sa.Column('password', sa.String(), nullable=False))

def downgrade():
    # Remove 'password' column from 'businesses' table
    op.drop_column('businesses', 'password')
