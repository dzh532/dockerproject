from fastapi import APIRouter, HTTPException, status
from app.busesdb.schemas import BusSchema
from app.database import database
from app.user_repo import BusRepository

bus_router = APIRouter()
bus_repo = BusRepository()


@bus_router.get(
    "/buses",
    response_model=list[BusSchema],
    status_code=status.HTTP_200_OK,
)
async def get_all_buses() -> list[BusSchema]:
    """Получение всех автобусов."""
    async with database.session() as session:
        buses = await bus_repo.get_all_buses(session=session)

    return buses


@bus_router.get(
    "/buses/{gos_number}",
    response_model=BusSchema,
    status_code=status.HTTP_200_OK,
)
async def get_bus_by_gos_number(gos_number: str) -> BusSchema:
    """Получение автобуса по государственному номеру."""
    async with database.session() as session:
        bus = await bus_repo.get_bus_by_gos_number(session=session, gos_number=gos_number)
        if not bus:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Автобус не найден")

    return bus


@bus_router.post(
    "/buses",
    response_model=BusSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_bus(bus_data: BusSchema) -> BusSchema:
    """Создание нового автобуса."""
    async with database.session() as session:
        try:
            new_bus = await bus_repo.create_bus(session=session, bus_data=bus_data)
        except Exception as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    return new_bus


@bus_router.put(
    "/buses/{gos_number}",
    response_model=BusSchema,
    status_code=status.HTTP_200_OK,
)
async def update_bus(gos_number: str, bus_data: BusSchema) -> BusSchema:
    """Обновление информации об автобусе."""
    async with database.session() as session:
        updated_bus = await bus_repo.update_bus(session=session, gos_number=gos_number, bus_data=bus_data.dict())
        if not updated_bus:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Автобус не найден")

    return updated_bus


@bus_router.delete(
    "/buses/{gos_number}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_bus(gos_number: str) -> None:
    """Удаление автобуса."""
    async with database.session() as session:
        success = await bus_repo.delete_bus(session=session, gos_number=gos_number)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Автобус не найден")
