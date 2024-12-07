from fastapi import APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.busesdb.schemas import StopSchema
from app.busesdb.models import Stop
from app.database import database
from app.repo.stops_repo import StopRepository

stop_router = APIRouter()
stop_repo = StopRepository()

@stop_router.get("/stops", response_model=list[StopSchema], status_code=status.HTTP_200_OK)
async def get_all_stops() -> list[StopSchema]:
    """Получение всех остановок."""
    async with database.session() as session:
        stops = await stop_repo.get_all_stops(session=session)
    return stops

@stop_router.get("/stops/{id}", response_model=StopSchema, status_code=status.HTTP_200_OK)
async def get_stop_by_id(id: int) -> StopSchema:
    """Получение остановки по ID."""
    async with database.session() as session:
        stop = await stop_repo.get_stop_by_id(session=session, id=id)
        if not stop:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Остановка не найдена")
    return stop

@stop_router.post("/stops", response_model=StopSchema, status_code=status.HTTP_201_CREATED)
async def add_stop(stop_data: StopSchema) -> StopSchema:
    """Создание новой остановки."""
    async with database.session() as session:
        new_stop = await stop_repo.create_stop(session=session, stop_data=stop_data)
    return new_stop

@stop_router.put("/stops/{id}", response_model=StopSchema, status_code=status.HTTP_200_OK)
async def update_stop(id: int, stop_data: StopSchema) -> StopSchema:
    """Обновление информации об остановке."""
    async with database.session() as session:
        updated_stop = await stop_repo.update_stop(session=session, id=id, stop_data=stop_data.dict())
        if not updated_stop:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Остановка не найдена")
    return updated_stop

@stop_router.delete("/stops/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_stop(id: int) -> None:
    """Удаление остановки."""
    async with database.session() as session:
        success = await stop_repo.delete_stop(session=session, id=id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Остановка не найдена")