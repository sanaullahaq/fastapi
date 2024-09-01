"""add last few columns to posts table

Revision ID: 577f353d4990
Revises: 6e9c06f5087f
Create Date: 2024-09-01 17:56:24.566102

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '577f353d4990'
down_revision: Union[str, None] = '6e9c06f5087f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # published = Column(Boolean, server_default='True', nullable=False)
	# created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    op.add_column(table_name='posts', column=sa.Column('published', sa.Boolean(), nullable=False, server_default='True'),)
    op.add_column(table_name='posts', column=sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column(column_name='published', table_name='posts')
    op.drop_column(column_name='created_at', table_name='posts')
    pass
