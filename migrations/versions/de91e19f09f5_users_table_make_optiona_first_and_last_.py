"""users_table make optiona first and last name

Revision ID: de91e19f09f5
Revises: 12d397a19414
Create Date: 2024-10-30 18:54:56.730189

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'de91e19f09f5'
down_revision: Union[str, None] = '12d397a19414'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'first_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('users', 'last_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'last_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('users', 'first_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###