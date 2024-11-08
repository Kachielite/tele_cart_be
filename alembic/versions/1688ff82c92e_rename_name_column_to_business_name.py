"""Rename name column to business_name

Revision ID: 1688ff82c92e
Revises: 
Create Date: 2024-11-08 05:55:33.718021

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1688ff82c92e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Rename column 'name' to 'business_name'
    op.alter_column('businesses', 'name', new_column_name='business_name')

def downgrade():
    # Revert column name back to 'name'
    op.alter_column('businesses', 'business_name', new_column_name='name')
