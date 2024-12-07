from typing import Type, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.busesdb.schemas import OrderRepairSchema
from app.busesdb.models import OrderRepair
from app.config import settings

class OrderRepairRepository:
    _collection: Type[OrderRepair] = OrderRepair

    async def get_all_orders(self, session: AsyncSession) -> list[OrderRepairSchema]:
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.order_repair;")
        result = await session.execute(query)
        orders = result.mappings().all()
        return [OrderRepairSchema.model_validate(obj=order) for order in orders]

    async def get_order_by_id(self, session: AsyncSession, id_: int) -> Optional[OrderRepairSchema]:
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.order_repair WHERE id = :id;")
        result = await session.execute(query, {"id": id_})
        order = result.mappings().first()
        return OrderRepairSchema.model_validate(obj=order) if order else None

    async def create_order(self, session: AsyncSession, order_data: OrderRepairSchema) -> OrderRepairSchema:
        new_order = self._collection(**order_data.dict())
        session.add(new_order)
        await session.commit()
        await session.refresh(new_order)
        return OrderRepairSchema.model_validate(obj=new_order)

    async def update_order(self, session: AsyncSession, id_: int, order_data: dict) -> Optional[OrderRepairSchema]:
        query = text(f"""
            UPDATE {settings.POSTGRES_SCHEMA}.order_repair
            SET buses_gos_number = :buses_gos_number,
                detail_name = :detail_name,
                date = :date
            WHERE id = :id
            RETURNING *;
        """)
        result = await session.execute(query, {"id": id_, **order_data})
        updated_order = result.mappings().first()
        await session.commit()
        return OrderRepairSchema.model_validate(obj=updated_order) if updated_order else None

    async def delete_order(self, session: AsyncSession, id_: int) -> bool:
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.order_repair WHERE id = :id;")
        result = await session.execute(query, {"id": id_})
        await session.commit()
        return result.rowcount > 0