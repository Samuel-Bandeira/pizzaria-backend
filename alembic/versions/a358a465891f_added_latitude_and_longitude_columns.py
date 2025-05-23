"""added latitude and longitude columns

Revision ID: a358a465891f
Revises: 697eedd50f81
Create Date: 2025-04-18 22:10:13.478271

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a358a465891f'
down_revision: Union[str, None] = '697eedd50f81'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lojas', sa.Column('latitude', sa.Float(), nullable=False))
    op.add_column('lojas', sa.Column('longitude', sa.Float(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('lojas', 'longitude')
    op.drop_column('lojas', 'latitude')
    # ### end Alembic commands ###
