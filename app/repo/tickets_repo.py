from typing import Type, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.busesdb.schemas import TicketSchema
from app.busesdb.models import Ticket
from app.config import settings

class TicketRepository:
    _collection: Type[Ticket] = Ticket

    async def get_all_tickets(self, session: AsyncSession) -> list[TicketSchema]:
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.tickets;")
        result = await session.execute(query)
        tickets = result.mappings().all()
        return [TicketSchema.model_validate(obj=ticket) for ticket in tickets]

    async def get_ticket_by_id(self, session: AsyncSession, id_: int) -> Optional[TicketSchema]:
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.tickets WHERE id = :id;")
        result = await session.execute(query, {"id": id_})
        ticket = result.mappings().first()
        return TicketSchema.model_validate(obj=ticket) if ticket else None

    async def create_ticket(self, session: AsyncSession, ticket_data: TicketSchema) -> TicketSchema:
        new_ticket = self._collection(**ticket_data.dict())
        session.add(new_ticket)
        await session.commit()
        await session.refresh(new_ticket)
        return TicketSchema.model_validate(obj=new_ticket)

    async def update_ticket(self, session: AsyncSession, id_: int, ticket_data: dict) -> Optional[TicketSchema]:
        query = text(f"""
            UPDATE {settings.POSTGRES_SCHEMA}.tickets
            SET id_passenger = :id_passenger,
                cost_travel = :cost_travel,
                date_start = :date_start,
                start_stop = :start_stop,
                end_stop = :end_stop
            WHERE id = :id
            RETURNING *;
        """)
        result = await session.execute(query, {"id": id_, **ticket_data})
        updated_ticket = result.mappings().first()
        await session.commit()
        return TicketSchema.model_validate(obj=updated_ticket) if updated_ticket else None

    async def delete_ticket(self, session: AsyncSession, id_: int) -> bool:
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.tickets WHERE id = :id;")
        result = await session.execute(query, {"id": id_})
        await session.commit()
        return result.rowcount > 0