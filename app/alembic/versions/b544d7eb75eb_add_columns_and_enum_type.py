"""add columns and enum type

Revision ID: b544d7eb75eb
Revises: 2c7a238d821e
Create Date: 2025-04-03 10:47:47.965434

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b544d7eb75eb'
down_revision: Union[str, None] = '2c7a238d821e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('my_rating', sa.Float(), nullable=True))
    op.add_column('books', sa.Column('read_status', sa.Enum('Read', 'To-read', 'None', name='read_status_enum'), nullable=True))
    op.add_column('books', sa.Column('private_notes', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('books', 'private_notes')
    op.drop_column('books', 'read_status')
    op.drop_column('books', 'my_rating')
    # ### end Alembic commands ###
