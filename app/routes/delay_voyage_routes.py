from fastapi import APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.busesdb.schemas import DelayVoyageSchema
from app.busesdb.models import DelaysVoyage
from app.database import database
from app.repo.delays_voyage_repo import DelayVoyageRepository

delay_router = APIRouter()
delay_repo = DelayVoyageRepository()

@delay_router.get("/delays", response_model=list[DelayVoyageSchema], status_code=status.HTTP_200_OK)
async def get_all_delays() -> list[DelayVoyageSchema]:
    """Получение всех задержек."""
    async with database.session() as session:
        delays = await delay_repo.get_all_delays(session=session)
    return delays

@delay_router.get("/delays/{number_vy}", response_model=DelayVoyageSchema, status_code=status.HTTP_200_OK)
async def get_delay_by_number_vy(number_vy: int) -> DelayVoyageSchema:
    """Получение задержки по номеру ВУ водителя."""
    async with database.session() as session:
        delay = await delay_repo.get_delay_by_number_vy(session=session, number_vy=number_vy)
        if not delay:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задержка не найдена")
    return delay

@delay_router.post("/delays", response_model=DelayVoyageSchema, status_code=status.HTTP_201_CREATED)
async def add_delay(delay_data: DelayVoyageSchema) -> DelayVoyageSchema:
    """Создание новой задержки."""
    async with database.session() as session:
        try:
            new_delay = await delay_repo.create_delay(session=session, delay_data=delay_data)
        except Exception as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return new_delay

@delay_router.put("/delays/{id}", response_model=DelayVoyageSchema, status_code=status.HTTP_200_OK)
async def update_delay(id: int, delay_data: DelayVoyageSchema) -> DelayVoyageSchema:
    """Обновление информации о задержке."""
    async with database.session() as session:
        updated_delay = await delay_repo.update_delay(session=session, id=id, delay_data=delay_data.dict())
        if not updated_delay:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задержка не найдена")
    return updated_delay

@delay_router.delete("/delays/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_delay(id: int) -> None:
    """Удаление задержки."""
    async with database.session() as session:
        success = await delay_repo.delete_delay(session=session, id=id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задержка не найдена")