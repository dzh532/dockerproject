"""initial

Revision ID: 1a4b6e48e969
Revises: 
Create Date: 2024-11-14 08:43:32.200474

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.config import settings


# revision identifiers, used by Alembic.
revision: str = '1a4b6e48e969'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('busestest',
    sa.Column('gos_number', sa.String(length=10), nullable=False),
    sa.Column('capacity', sa.Integer(), nullable=False),
    sa.Column('is_air_conditioner', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('gos_number'),
    schema=settings.POSTGRES_SCHEMA
    )


def downgrade() -> None:
    op.drop_table('busestest', schema=settings.POSTGRES_SCHEMA)
