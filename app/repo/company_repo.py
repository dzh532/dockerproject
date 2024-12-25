from typing import Type, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.busesdb.schemas import CompanySchema
from app.busesdb.models import Company
from app.config import settings

class CompanyRepository:
    _collection: Type[Company] = Company

    async def get_all_companies(self, session: AsyncSession) -> list[CompanySchema]:
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.company;")
        result = await session.execute(query)
        companies = result.mappings().all()
        return [CompanySchema.model_validate(obj=company) for company in companies]

    async def get_company_by_name(self, session: AsyncSession, name: str) -> Optional[CompanySchema]:
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.company WHERE name = :name;")
        result = await session.execute(query, {"name": name})
        company = result.mappings().first()
        return CompanySchema.model_validate(obj=company) if company else None

    async def get_company_by_duration_work(self, session: AsyncSession, min_dur: int) -> list[CompanySchema]:
        query = text(f"SELECT * FROM get_companies_by_duration(:min_dur)")
        result = await session.execute(query, {"min_dur": min_dur})
        company = result.mappings().all()
        return [CompanySchema.model_validate(obj=comp) for comp in company]


    async def create_company(self, session: AsyncSession, company_data: CompanySchema) -> CompanySchema:
        new_company = self._collection(**company_data.dict())
        session.add(new_company)
        await session.commit()
        await session.refresh(new_company)
        return CompanySchema.model_validate(obj=new_company)

    async def update_company(self, session: AsyncSession, name: str, company_data: dict) -> Optional[CompanySchema]:
        query = text(f"""
            UPDATE {settings.POSTGRES_SCHEMA}.company
            SET duration_work = :duration_work, address = :address, number_phone = :number_phone
            WHERE name = :name
            RETURNING *;
        """)
        result = await session.execute(query, {"name": name, **company_data})
        updated_company = result.mappings().first()
        await session.commit()
        return CompanySchema.model_validate(obj=updated_company) if updated_company else None

    async def delete_company(self, session: AsyncSession, name: str) -> bool:
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.company WHERE name = :name;")
        result = await session.execute(query, {"name": name})
        await session.commit()
        return result.rowcount > 0