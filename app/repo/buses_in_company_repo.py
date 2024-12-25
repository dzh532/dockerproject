from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.busesdb.schemas import BusesInCompanySchema
from app.busesdb.models import Bus, Company
from app.config import settings


class BusInCompanyRepository:
    async def get_all_buses_in_company(self, session: AsyncSession) -> list[BusesInCompanySchema]:
        """Получение списка всех автобусов и их компаний."""
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.buses_in_company;")
        result = await session.execute(query)
        records = result.mappings().all()
        return [BusesInCompanySchema.model_validate(obj=record) for record in records]

    async def add_bus_in_company(self, session: AsyncSession, data: BusesInCompanySchema) -> BusesInCompanySchema:
        """Добавление записи автобуса и компании."""
        query = text(f"""
            INSERT INTO {settings.POSTGRES_SCHEMA}.buses_in_company (buses_gos_number, company_name)
            VALUES (:buses_gos_number, :company_name)
            RETURNING buses_gos_number, company_name;
        """)
        result = await session.execute(query, data.dict())
        await session.commit()
        new_record = result.mappings().first()
        return BusesInCompanySchema.model_validate(obj=new_record)

    async def get_buses_by_company(self, session: AsyncSession, company_name: str) -> list[BusesInCompanySchema]:
        """Получение автобусов по названию компании."""
        query = text(f"""
            SELECT * 
            FROM {settings.POSTGRES_SCHEMA}.buses_in_company
            WHERE company_name = :company_name;
        """)
        result = await session.execute(query, {"company_name": company_name})
        records = result.mappings().all()
        return [BusesInCompanySchema.model_validate(obj=record) for record in records]

    async def delete_bus_by_company(self, session: AsyncSession, gos_number: str) -> bool:
        """Удаление автобуса по гос. номеру."""
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.buses_in_company WHERE buses_gos_number = :gos_number;")
        result = await session.execute(query, {"gos_number": gos_number})
        await session.commit()
        return result.rowcount > 0