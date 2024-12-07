from typing import Type, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.busesdb.schemas import StopSchema
from app.busesdb.models import Stop
from app.config import settings

class StopRepository:
    _collection: Type[Stop] = Stop

    async def get_all_stops(self, session: AsyncSession) -> list[StopSchema]:
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.stops;")
        result = await session.execute(query)
        stops = result.mappings().all()
        return [StopSchema.model_validate(obj=stop) for stop in stops]

    async def get_stop_by_id(self, session: AsyncSession, id_: int) -> Optional[StopSchema]:
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.stops WHERE id = :id;")
        result = await session.execute(query, {"id": id_})
        stop = result.mappings().first()
        return StopSchema.model_validate(obj=stop) if stop else None

    async def create_stop(self, session: AsyncSession, stop_data: StopSchema) -> StopSchema:
        new_stop = self._collection(**stop_data.dict())
        session.add(new_stop)
        await session.commit()
        await session.refresh(new_stop)
        return StopSchema.model_validate(obj=new_stop)

    async def update_stop(self, session: AsyncSession, id_: int, stop_data: dict) -> Optional[StopSchema]:
        query = text(f"""
            UPDATE {settings.POSTGRES_SCHEMA}.stops
            SET name = :name
            WHERE id = :id
            RETURNING *;
        """)
        result = await session.execute(query, {"id": id_, **stop_data})
        updated_stop = result.mappings().first()
        await session.commit()
        return StopSchema.model_validate(obj=updated_stop) if updated_stop else None

    async def delete_stop(self, session: AsyncSession, id_: int) -> bool:
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.stops WHERE id = :id;")
        result = await session.execute(query, {"id": id_})
        await session.commit()
        return result.rowcount > 0