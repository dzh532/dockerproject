from typing import Type, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.busesdb.schemas import TypeRepairSchema
from app.busesdb.models import TypeRepair
from app.config import settings

class TypeRepairRepository:
    _collection: Type[TypeRepair] = TypeRepair

    async def get_all_types(self, session: AsyncSession) -> list[TypeRepairSchema]:
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.type_repair;")
        result = await session.execute(query)
        types = result.mappings().all()
        return [TypeRepairSchema.model_validate(obj=type_) for type_ in types]

    async def get_type_by_detail(self, session: AsyncSession, detail: str) -> Optional[TypeRepairSchema]:
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.type_repair WHERE detail = :detail;")
        result = await session.execute(query, {"detail": detail})
        type_ = result.mappings().first()
        return TypeRepairSchema.model_validate(obj=type_) if type_ else None

    async def create_type(self, session: AsyncSession, type_data: TypeRepairSchema) -> TypeRepairSchema:
        new_type = self._collection(**type_data.dict())
        session.add(new_type)
        await session.commit()
        await session.refresh(new_type)
        return TypeRepairSchema.model_validate(obj=new_type)

    async def update_type(self, session: AsyncSession, id_: int, type_data: dict) -> Optional[TypeRepairSchema]:
        query = text(f"""
            UPDATE {settings.POSTGRES_SCHEMA}.type_repair
            SET detail = :detail, cost_detail = :cost_detail
            WHERE id = :id
            RETURNING *;
        """)
        result = await session.execute(query, {"id": id_, **type_data})
        updated_type = result.mappings().first()
        await session.commit()
        return TypeRepairSchema.model_validate(obj=updated_type) if updated_type else None

    async def delete_type(self, session: AsyncSession, id_: int) -> bool:
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.type_repair WHERE id = :id;")
        result = await session.execute(query, {"id": id_})
        await session.commit()
        return result.rowcount > 0