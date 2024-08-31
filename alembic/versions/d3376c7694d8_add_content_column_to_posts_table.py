"""add content column to posts table

Revision ID: d3376c7694d8
Revises: b303aeab4122
Create Date: 2024-08-31 22:38:17.404098

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3376c7694d8'
down_revision: Union[str, None] = 'b303aeab4122'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))

def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
