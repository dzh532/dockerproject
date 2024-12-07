from typing import Type, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.busesdb.schemas import PassengerSchema
from app.busesdb.models import Passenger
from app.config import settings

class PassengerRepository:
    _collection: Type[Passenger] = Passenger

    async def get_all_passengers(self, session: AsyncSession) -> list[PassengerSchema]:
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.passengers;")
        result = await session.execute(query)
        passengers = result.mappings().all()
        return [PassengerSchema.model_validate(obj=passenger) for passenger in passengers]

    async def get_passenger_by_id(self, session: AsyncSession, id_: int) -> Optional[PassengerSchema]:
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.passengers WHERE id = :id;")
        result = await session.execute(query, {"id": id_})
        passenger = result.mappings().first()
        return PassengerSchema.model_validate(obj=passenger) if passenger else None

    async def create_passenger(self, session: AsyncSession, passenger_data: PassengerSchema) -> PassengerSchema:
        new_passenger = self._collection(**passenger_data.dict())
        session.add(new_passenger)
        await session.commit()
        await session.refresh(new_passenger)
        return PassengerSchema.model_validate(obj=new_passenger)

    async def update_passenger(self, session: AsyncSession, id_: int, passenger_data: dict) -> Optional[PassengerSchema]:
        query = text(f"""
            UPDATE {settings.POSTGRES_SCHEMA}.passengers
            SET fio = :fio,
                age = :age
            WHERE id = :id
            RETURNING *;
        """)
        result = await session.execute(query, {"id": id_, **passenger_data})
        updated_passenger = result.mappings().first()
        await session.commit()
        return PassengerSchema.model_validate(obj=updated_passenger) if updated_passenger else None

    async def delete_passenger(self, session: AsyncSession, id_: int) -> bool:
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.passengers WHERE id = :id;")
        result = await session.execute(query, {"id": id_})
        await session.commit()
        return result.rowcount > 0