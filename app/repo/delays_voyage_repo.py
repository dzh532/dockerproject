from typing import Type, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.busesdb.schemas import DelayVoyageSchema
from app.busesdb.models import DelaysVoyage
from app.config import settings

class DelayVoyageRepository:
    _collection: Type[DelaysVoyage] = DelaysVoyage

    async def get_all_delays(self, session: AsyncSession) -> list[DelayVoyageSchema]:
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.delays_voyage;")
        result = await session.execute(query)
        delays = result.mappings().all()
        return [DelayVoyageSchema.model_validate(obj=delay) for delay in delays]

    async def get_delay_by_number_vy(self, session: AsyncSession, number_vy: int) -> Optional[DelayVoyageSchema]:
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.delays_voyage WHERE number_vy = :number_vy;")
        result = await session.execute(query, {"number_vy": number_vy})
        delay = result.mappings().first()
        return DelayVoyageSchema.model_validate(obj=delay) if delay else None

    async def create_delay(self, session: AsyncSession, delay_data: DelayVoyageSchema) -> DelayVoyageSchema:
        new_delay = self._collection(**delay_data.dict())
        session.add(new_delay)
        await session.commit()
        await session.refresh(new_delay)
        return DelayVoyageSchema.model_validate(obj=new_delay)

    async def update_delay(self, session: AsyncSession, id_: int, delay_data: dict) -> Optional[DelayVoyageSchema]:
        query = text(f"""
            UPDATE {settings.POSTGRES_SCHEMA}.delays_voyage
            SET cause = :cause, duration = :duration
            WHERE id = :id
            RETURNING *;
        """)
        result = await session.execute(query, {"id": id_, **delay_data})
        updated_delay = result.mappings().first()
        await session.commit()
        return DelayVoyageSchema.model_validate(obj=updated_delay) if updated_delay else None

    async def delete_delay(self, session: AsyncSession, id_: int) -> bool:
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.delays_voyage WHERE id = :id;")
        result = await session.execute(query, {"id": id_})
        await session.commit()
        return result.rowcount > 0