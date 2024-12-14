"""add all table

Revision ID: a16ac989b4f1
Revises: 1a4b6e48e969
Create Date: 2024-12-07 21:08:03.376168

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.config import settings


# revision identifiers, used by Alembic.
revision: str = 'a16ac989b4f1'
down_revision: Union[str, None] = '1a4b6e48e969'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False, unique=True),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=False, default=False),
    sa.Column('active', sa.Boolean(), nullable=False, default=True),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('buses',
    sa.Column('gos_number', sa.String(length=10), nullable=False),
    sa.Column('capacity', sa.Integer(), nullable=False),
    sa.Column('is_air_conditioner', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('gos_number'),
    schema='public'
    )
    op.create_table('company',
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('duration_work', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(length=100), nullable=False),
    sa.Column('number_phone', sa.String(length=11), nullable=True),
    sa.PrimaryKeyConstraint('name'),
    schema='public'
    )
    op.create_table('drivers',
    sa.Column('number_vy', sa.Integer(), nullable=False),
    sa.Column('fio', sa.String(length=100), nullable=False),
    sa.Column('experience', sa.Integer(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('number_vy'),
    schema='public'
    )
    op.create_table('passengers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fio', sa.String(length=100), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('stops',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    schema='public'
    )
    op.create_table('type_repair',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('detail', sa.String(length=50), nullable=False),
    sa.Column('cost_detail', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('detail'),
    schema='public'
    )
    op.create_table('buses_in_company',
    sa.Column('buses_gos_number', sa.String(length=10), nullable=False),
    sa.Column('company_name', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['buses_gos_number'], ['public.buses.gos_number'], ),
    sa.ForeignKeyConstraint(['company_name'], ['public.company.name'], ),
    sa.PrimaryKeyConstraint('buses_gos_number', 'company_name'),
    schema='public'
    )
    op.create_table('delays_voyage',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number_vy', sa.Integer(), nullable=True),
    sa.Column('cause', sa.String(length=100), nullable=False),
    sa.Column('duration', sa.Time(), nullable=False),
    sa.ForeignKeyConstraint(['number_vy'], ['public.drivers.number_vy'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('order_repair',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('buses_gos_number', sa.String(length=10), nullable=True),
    sa.Column('detail_name', sa.String(length=50), nullable=True),
    sa.Column('date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['buses_gos_number'], ['public.buses.gos_number'], ),
    sa.ForeignKeyConstraint(['detail_name'], ['public.type_repair.detail'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('report_income_company',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_name', sa.String(length=50), nullable=True),
    sa.Column('start_period', sa.Date(), nullable=False),
    sa.Column('end_period', sa.Date(), nullable=False),
    sa.Column('revenue', sa.Integer(), nullable=False),
    sa.Column('expenses', sa.Integer(), nullable=False),
    sa.Column('profit', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['company_name'], ['public.company.name'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('review_passenger',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_passenger', sa.Integer(), nullable=True),
    sa.Column('gos_number_bus', sa.String(length=10), nullable=True),
    sa.Column('grade', sa.Integer(), nullable=False),
    sa.Column('text_review', sa.String(length=500), nullable=True),
    sa.Column('date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['gos_number_bus'], ['public.buses.gos_number'], ),
    sa.ForeignKeyConstraint(['id_passenger'], ['public.passengers.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('routes',
    sa.Column('number_route', sa.String(length=10), nullable=False),
    sa.Column('count_stops', sa.Integer(), nullable=False),
    sa.Column('start_stop', sa.String(length=50), nullable=True),
    sa.Column('end_stop', sa.String(length=50), nullable=True),
    sa.Column('time_start', sa.Time(), nullable=False),
    sa.Column('time_end', sa.Time(), nullable=False),
    sa.Column('cost_travel', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['end_stop'], ['public.stops.name'], ),
    sa.ForeignKeyConstraint(['start_stop'], ['public.stops.name'], ),
    sa.PrimaryKeyConstraint('number_route'),
    schema='public'
    )
    op.create_table('tickets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_passenger', sa.Integer(), nullable=True),
    sa.Column('cost_travel', sa.Integer(), nullable=False),
    sa.Column('date_start', sa.Date(), nullable=False),
    sa.Column('start_stop', sa.String(length=50), nullable=True),
    sa.Column('end_stop', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['end_stop'], ['public.stops.name'], ),
    sa.ForeignKeyConstraint(['id_passenger'], ['public.passengers.id'], ),
    sa.ForeignKeyConstraint(['start_stop'], ['public.stops.name'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('route_sheet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number_vy', sa.Integer(), nullable=True),
    sa.Column('number_route', sa.String(length=10), nullable=True),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('gos_number_bus', sa.String(length=10), nullable=True),
    sa.ForeignKeyConstraint(['gos_number_bus'], ['public.buses.gos_number'], ),
    sa.ForeignKeyConstraint(['number_route'], ['public.routes.number_route'], ),
    sa.ForeignKeyConstraint(['number_vy'], ['public.drivers.number_vy'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('stops_and_routes',
    sa.Column('id_stops', sa.Integer(), nullable=False),
    sa.Column('number_route', sa.String(length=10), nullable=False),
    sa.ForeignKeyConstraint(['id_stops'], ['public.stops.id'], ),
    sa.ForeignKeyConstraint(['number_route'], ['public.routes.number_route'], ),
    sa.PrimaryKeyConstraint('id_stops', 'number_route'),
    schema='public'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stops_and_routes', schema='public')
    op.drop_table('route_sheet', schema='public')
    op.drop_table('tickets', schema='public')
    op.drop_table('routes', schema='public')
    op.drop_table('review_passenger', schema='public')
    op.drop_table('report_income_company', schema='public')
    op.drop_table('order_repair', schema='public')
    op.drop_table('delays_voyage', schema='public')
    op.drop_table('buses_in_company', schema='public')
    op.drop_table('type_repair', schema='public')
    op.drop_table('stops', schema='public')
    op.drop_table('passengers', schema='public')
    op.drop_table('drivers', schema='public')
    op.drop_table('company', schema='public')
    op.drop_table('buses', schema='public')
    op.drop_table('users', schema='public')
    # ### end Alembic commands ###
