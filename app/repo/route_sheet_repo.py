from typing import Type, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.busesdb.schemas import RouteSheetSchema
from app.busesdb.models import RouteSheet
from app.config import settings

class RouteSheetRepository:
    _collection: Type[RouteSheet] = RouteSheet

    async def get_all_sheets(self, session: AsyncSession) -> list[RouteSheetSchema]:
        """Получение списка всех маршрутных листов."""
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.route_sheet;")
        result = await session.execute(query)
        sheets = result.mappings().all()
        return [RouteSheetSchema.model_validate(obj=sheet) for sheet in sheets]

    async def get_sheet_by_id(self, session: AsyncSession, id_: int) -> Optional[RouteSheetSchema]:
        """Получение маршрутного листа по его ID."""
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.route_sheet WHERE id = :id;")
        result = await session.execute(query, {"id": id_})
        sheet = result.mappings().first()
        return RouteSheetSchema.model_validate(obj=sheet) if sheet else None

    async def create_sheet(self, session: AsyncSession, sheet_data: RouteSheetSchema) -> RouteSheetSchema:
        """Создание нового маршрутного листа."""
        new_sheet = self._collection(**sheet_data.dict())
        session.add(new_sheet)
        await session.commit()
        await session.refresh(new_sheet)
        return RouteSheetSchema.model_validate(obj=new_sheet)

    async def update_sheet(self, session: AsyncSession, id_: int, sheet_data: dict) -> Optional[RouteSheetSchema]:
        """Обновление данных маршрутного листа."""
        query = text(f"""
            UPDATE {settings.POSTGRES_SCHEMA}.route_sheet
            SET number_vy = :number_vy,
                number_route = :number_route,
                date = :date,
                gos_number_bus = :gos_number_bus
            WHERE id = :id
            RETURNING *;
        """)
        result = await session.execute(query, {"id": id_, **sheet_data})
        updated_sheet = result.mappings().first()
        await session.commit()
        return RouteSheetSchema.model_validate(obj=updated_sheet) if updated_sheet else None

    async def delete_sheet(self, session: AsyncSession, id_: int) -> bool:
        """Удаление маршрутного листа по его ID."""
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.route_sheet WHERE id = :id;")
        result = await session.execute(query, {"id": id_})
        await session.commit()
        return result.rowcount > 0