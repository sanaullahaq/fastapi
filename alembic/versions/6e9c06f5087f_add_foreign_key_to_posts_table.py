"""add foreign key to posts table

Revision ID: 6e9c06f5087f
Revises: 932087f56744
Create Date: 2024-09-01 17:42:23.575646

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e9c06f5087f'
down_revision: Union[str, None] = '932087f56744'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key(constraint_name='posts_users_fkey', source_table='posts', referent_table='users',
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    # `posts_users_fkey` ->Foreign Key Constraint name
    # `source_table` -> table which will contain the fkey
    # `referent_table` -> from which table fkey will come
    # `local_cols` -> column list in the source table what will hold the fkey
    # `remote_cols` -> column list what will come as fkey from referent_table
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fkey', table_name='posts')
    op.drop_column(column_name='owner_id', table_name='posts')
    pass
