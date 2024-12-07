from typing import Type, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.busesdb.schemas import ReportIncomeCompanySchema
from app.busesdb.models import ReportIncomeCompany
from app.config import settings


class ReportIncomeCompanyRepository:
    _collection: Type[ReportIncomeCompany] = ReportIncomeCompany

    async def get_all_reports(self, session: AsyncSession) -> list[ReportIncomeCompanySchema]:
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.report_income_company;")
        result = await session.execute(query)
        reports = result.mappings().all()
        return [ReportIncomeCompanySchema.model_validate(obj=report) for report in reports]

    async def get_report_by_id(self, session: AsyncSession, id_: int) -> Optional[ReportIncomeCompanySchema]:
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.report_income_company WHERE id = :id;")
        result = await session.execute(query, {"id": id_})
        report = result.mappings().first()
        return ReportIncomeCompanySchema.model_validate(obj=report) if report else None


async def create_report(self,
                        session: AsyncSession,
                        report_data: ReportIncomeCompanySchema) -> ReportIncomeCompanySchema:
    new_report = self._collection(**report_data.dict())
    session.add(new_report)
    await session.commit()
    await session.refresh(new_report)
    return ReportIncomeCompanySchema.model_validate(obj=new_report)


async def update_report(self,
                        session: AsyncSession,
                        id_: int,
                        report_data: dict) -> Optional[ReportIncomeCompanySchema]:
    query = text(f"""
           UPDATE {settings.POSTGRES_SCHEMA}.report_income_company 
           SET company_name=:company_name,
               start_period=:start_period,
               end_period=:end_period,
               revenue=:revenue,
               expenses=:expenses,
               profit=:profit 
           WHERE id=:id 
           RETURNING *;
       """)
    result = await(session.execute(query, {**report_data, "id": id_}))
    updated_report = result.mappings().first()
    await(session.commit())
    return ReportIncomeCompanySchema.model_validate(obj=updated_report) if updated_report else None


async def delete_report(self,
                        session: AsyncSession,
                        id_: int) -> bool:
    query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.report_income_company WHERE id=:id;")
    result = await(session.execute(query, {"id": id_}))
    await(session.commit())
    return (result.rowcount > 0)