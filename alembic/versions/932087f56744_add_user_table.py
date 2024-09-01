"""add user table

Revision ID: 932087f56744
Revises: d3376c7694d8
Create Date: 2024-09-01 17:23:51.370597

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '932087f56744'
down_revision: Union[str, None] = 'd3376c7694d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer, nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                )
    #The `primary_key` and `unique_key` constraints can be added inside the `Column` object,
    #But what we have used here is alternative way    
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
