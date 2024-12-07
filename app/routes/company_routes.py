from fastapi import APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.busesdb.schemas import CompanySchema
from app.busesdb.models import Company
from app.database import database
from app.repo.company_repo import CompanyRepository

company_router = APIRouter()
company_repo = CompanyRepository()

@company_router.get("/companies", response_model=list[CompanySchema], status_code=status.HTTP_200_OK)
async def get_all_companies() -> list[CompanySchema]:
    """Получение всех компаний."""
    async with database.session() as session:
        companies = await company_repo.get_all_companies(session=session)
    return companies

@company_router.get("/companies/{name}", response_model=CompanySchema, status_code=status.HTTP_200_OK)
async def get_company_by_name(name: str) -> CompanySchema:
    """Получение компании по имени."""
    async with database.session() as session:
        company = await company_repo.get_company_by_name(session=session, name=name)
        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Компания не найдена")
    return company

@company_router.post("/companies", response_model=CompanySchema, status_code=status.HTTP_201_CREATED)
async def add_company(company_data: CompanySchema) -> CompanySchema:
    """Создание новой компании."""
    async with database.session() as session:
        try:
            new_company = await company_repo.create_company(session=session, company_data=company_data)
        except Exception as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return new_company

@company_router.put("/companies/{name}", response_model=CompanySchema, status_code=status.HTTP_200_OK)
async def update_company(name: str, company_data: CompanySchema) -> CompanySchema:
    """Обновление информации о компании."""
    async with database.session() as session:
        updated_company = await company_repo.update_company(session=session, name=name, company_data=company_data.dict())
        if not updated_company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Компания не найдена")
    return updated_company

@company_router.delete("/companies/{name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(name: str) -> None:
    """Удаление компании."""
    async with database.session() as session:
        success = await company_repo.delete_company(session=session, name=name)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Компания не найдена")