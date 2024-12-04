from typing import Type, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from busesdb.schemas import BusSchema
from busesdb.models import Bus
from app.config import settings


class BusRepository:
    _collection: Type[Bus] = Bus

    async def get_all_buses(self, session: AsyncSession) -> list[BusSchema]:
        """Получение списка всех автобусов."""
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.busestest;")
        result = await session.execute(query)
        buses = result.mappings().all()
        return [BusSchema.model_validate(obj=bus) for bus in buses]

    async def get_bus_by_gos_number(self, session: AsyncSession, gos_number: str) -> Optional[BusSchema]:
        """Получение автобуса по его гос. номеру."""
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.busestest WHERE gos_number = :gos_number;")
        result = await session.execute(query, {"gos_number": gos_number})
        bus = result.mappings().first()
        return BusSchema.model_validate(obj=bus) if bus else None

    async def create_bus(self, session: AsyncSession, bus_data: BusSchema) -> BusSchema:
        """Создание нового автобуса."""
        new_bus = self._collection(**bus_data.dict())
        session.add(new_bus)
        await session.commit()
        await session.refresh(new_bus)
        return BusSchema.model_validate(obj=new_bus)

    async def update_bus(self, session: AsyncSession, gos_number: str, bus_data: dict) -> Optional[BusSchema]:
        """Обновление данных автобуса."""
        query = text(f"""
            UPDATE {settings.POSTGRES_SCHEMA}.busestest
            SET capacity = :capacity, is_air_conditioner = :is_air_conditioner
            WHERE gos_number = :gos_number
            RETURNING *;
        """)
        result = await session.execute(query, {"gos_number": gos_number, **bus_data})
        updated_bus = result.mappings().first()
        await session.commit()
        return BusSchema.model_validate(obj=updated_bus) if updated_bus else None

    async def delete_bus(self, session: AsyncSession, gos_number: str) -> bool:
        """Удаление автобуса по гос. номеру."""
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.busestest WHERE gos_number = :gos_number;")
        result = await session.execute(query, {"gos_number": gos_number})
        await session.commit()
        return result.rowcount > 0

    async def check_connection(self, session: AsyncSession) -> bool:
        """Проверка подключения к базе данных."""
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False
