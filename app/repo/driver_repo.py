from typing import Type, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.busesdb.schemas import DriverSchema
from app.busesdb.models import Driver
from app.config import settings

class DriverRepository:
    _collection: Type[Driver] = Driver

    async def get_all_drivers(self, session: AsyncSession) -> list[DriverSchema]:
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.drivers;")
        result = await session.execute(query)
        drivers = result.mappings().all()
        return [DriverSchema.model_validate(obj=driver) for driver in drivers]

    async def get_driver_by_number_vy(self, session: AsyncSession, number_vy: int) -> Optional[DriverSchema]:
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.drivers WHERE number_vy = :number_vy;")
        result = await session.execute(query, {"number_vy": number_vy})
        driver = result.mappings().first()
        return DriverSchema.model_validate(obj=driver) if driver else None

    async def create_driver(self, session: AsyncSession, driver_data: DriverSchema) -> DriverSchema:
        new_driver = self._collection(**driver_data.dict())
        session.add(new_driver)
        await session.commit()
        await session.refresh(new_driver)
        return DriverSchema.model_validate(obj=new_driver)

    async def update_driver(self, session: AsyncSession, number_vy: int, driver_data: dict) -> Optional[DriverSchema]:
        query = text(f"""
            UPDATE {settings.POSTGRES_SCHEMA}.drivers
            SET fio = :fio, experience = :experience, age = :age
            WHERE number_vy = :number_vy
            RETURNING *;
        """)
        result = await session.execute(query, {"number_vy": number_vy, **driver_data})
        updated_driver = result.mappings().first()
        await session.commit()
        return DriverSchema.model_validate(obj=updated_driver) if updated_driver else None

    async def delete_driver(self, session: AsyncSession, number_vy: int) -> bool:
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.drivers WHERE number_vy = :number_vy;")
        result = await session.execute(query, {"number_vy": number_vy})
        await session.commit()
        return result.rowcount > 0