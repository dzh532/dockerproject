from fastapi import APIRouter, HTTPException, status
from app.busesdb.schemas import BusesInCompanySchema
from app.database import database
from app.repo.buses_in_company_repo import BusInCompanyRepository

buses_in_company_router = APIRouter(prefix="/buses_in_company")
buses_in_company_repo = BusInCompanyRepository()

@buses_in_company_router.get(
    "/company/{company_name}",
    response_model=list[BusesInCompanySchema],
    status_code=status.HTTP_200_OK,
)
async def get_buses_by_company(company_name: str) -> list[BusesInCompanySchema]:
    """Получение всех автобусов для определенной компании."""
    async with database.session() as session:
        buses = await buses_in_company_repo.get_buses_by_company(session=session, company_name=company_name)
        if not buses:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Автобусы для компании не найдены")

    return buses


@buses_in_company_router.get(
    "/",
    response_model=list[BusesInCompanySchema],
    status_code=status.HTTP_200_OK,
)
async def get_all_buses_in_company() -> list[BusesInCompanySchema]:
    """Получение всех записей автобусов и компаний."""
    async with database.session() as session:
        buses_in_company = await buses_in_company_repo.get_all_buses_in_company(session=session)

    return buses_in_company


@buses_in_company_router.post(
    "/",
    response_model=BusesInCompanySchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_bus_in_company(data: BusesInCompanySchema) -> BusesInCompanySchema:
    """Добавление автобуса в компанию."""
    async with database.session() as session:
        try:
            new_record = await buses_in_company_repo.add_bus_in_company(session=session, data=data)
        except Exception as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    return new_record


@buses_in_company_router.delete(
    "/{gos_number}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_bus_in_company(gos_number: str) -> None:
    """Удаление автобуса."""
    async with database.session() as session:
        success = await buses_in_company_repo.delete_bus_by_company(session=session, gos_number=gos_number)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Автобус не найден")

