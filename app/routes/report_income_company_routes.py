from fastapi import APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.busesdb.schemas import ReportIncomeCompanySchema
from app.busesdb.models import ReportIncomeCompany
from app.database import database
from app.repo.report_income_company_repo import ReportIncomeCompanyRepository

report_income_router = APIRouter(prefix="/report_income")
report_income_repo = ReportIncomeCompanyRepository()

@report_income_router.get("/reports", response_model=list[ReportIncomeCompanySchema], status_code=status.HTTP_200_OK)
async def get_all_reports() -> list[ReportIncomeCompanySchema]:
    """Получение всех отчетов о доходах компаний."""
    async with database.session() as session:
        reports = await report_income_repo.get_all_reports(session=session)
    return reports

@report_income_router.get("/reports/{id}", response_model=ReportIncomeCompanySchema, status_code=status.HTTP_200_OK)
async def get_report_by_id(id: int) -> ReportIncomeCompanySchema:
    """Получение отчета о доходах компании по ID."""
    async with database.session() as session:
        report = await report_income_repo.get_report_by_id(session=session, id=id)
        if not report:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Отчет не найден")
    return report

@report_income_router.post("/reports", response_model=ReportIncomeCompanySchema, status_code=status.HTTP_201_CREATED)
async def add_report(report_data: ReportIncomeCompanySchema) -> ReportIncomeCompanySchema:
    """Создание нового отчета о доходах компании."""
    async with database.session() as session:
        try:
            new_report = await report_income_repo.create_report(session=session, report_data=report_data)
        except Exception as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return new_report

@report_income_router.put("/reports/{id}", response_model=ReportIncomeCompanySchema, status_code=status.HTTP_200_OK)
async def update_report(id: int, report_data: ReportIncomeCompanySchema) -> ReportIncomeCompanySchema:
   """Обновление информации об отчете о доходах компании."""
   async with database.session () as session:
      updated_report=await report_income_repo.update_report (session=session ,id=id ,report_data=report_data.dict ())
      if not updated_report:
         raise HTTPException (status_code=status.HTTP_404_NOT_FOUND ,detail="Отчет не найден")
   return updated_report

@report_income_router.delete("/reports/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_report(id: int) -> None:
   """Удаление отчета о доходах компании."""
   async with database.session () as session:
      success=await report_income_repo.delete_report (session=session ,id=id)
      if not success:
         raise HTTPException (status_code=status.HTTP_404_NOT_FOUND ,detail="Отчет не найден")