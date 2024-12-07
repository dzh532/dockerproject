from fastapi import APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.busesdb.schemas import DriverSchema
from app.busesdb.models import Driver
from app.database import database
from app.repo.driver_repo import DriverRepository

driver_router = APIRouter()
driver_repo = DriverRepository()

@driver_router.get("/drivers", response_model=list[DriverSchema], status_code=status.HTTP_200_OK)
async def get_all_drivers() -> list[DriverSchema]:
    """Получение всех водителей."""
    async with database.session() as session:
        drivers = await driver_repo.get_all_drivers(session=session)
    return drivers

@driver_router.get("/drivers/{number_vy}", response_model=DriverSchema, status_code=status.HTTP_200_OK)
async def get_driver_by_number_vy(number_vy: int) -> DriverSchema:
    """Получение водителя по номеру ВУ."""
    async with database.session() as session:
        driver = await driver_repo.get_driver_by_number_vy(session=session, number_vy=number_vy)
        if not driver:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Водитель не найден")
    return driver

@driver_router.post("/drivers", response_model=DriverSchema, status_code=status.HTTP_201_CREATED)
async def add_driver(driver_data: DriverSchema) -> DriverSchema:
    """Создание нового водителя."""
    async with database.session() as session:
        try:
            new_driver = await driver_repo.create_driver(session=session, driver_data=driver_data)
        except Exception as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return new_driver

@driver_router.put("/drivers/{number_vy}", response_model=DriverSchema, status_code=status.HTTP_200_OK)
async def update_driver(number_vy: int, driver_data: DriverSchema) -> DriverSchema:
    """Обновление информации о водителе."""
    async with database.session() as session:
        updated_driver = await driver_repo.update_driver(session=session, number_vy=number_vy, driver_data=driver_data.dict())
        if not updated_driver:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Водитель не найден")
    return updated_driver

@driver_router.delete("/drivers/{number_vy}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_driver(number_vy: int) -> None:
    """Удаление водителя."""
    async with database.session() as session:
        success = await driver_repo.delete_driver(session=session, number_vy=number_vy)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Водитель не найден")