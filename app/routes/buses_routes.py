from fastapi import APIRouter, HTTPException, status, Query
from typing import Optional
from app.busesdb.schemas import BusSchema
from app.database import database
from app.repo.buses_repo import BusRepository
from sqlalchemy.sql import text

bus_router = APIRouter(prefix="/buses")
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
    "/buses/with_air_conditioner",
    response_model=list[BusSchema],
    status_code=status.HTTP_200_OK,
)
async def get_buses_with_air_conditioner() -> list[BusSchema]:
    """Получение автобусов с кондиционером."""
    async with database.session() as session:
        buses = await bus_repo.get_buses_with_air_conditioner(session=session)

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


@bus_router.get(
    "/search_buses",
    response_model=list[BusSchema],
    status_code=status.HTTP_200_OK,
)
async def search_buses(
    company_name: Optional[str] = Query(None),
    is_air_conditioner: Optional[bool] = Query(None),
    min_capacity: Optional[int] = Query(None),
    max_capacity: Optional[int] = Query(None),
):
    """Поиск автобусов по критериям."""
    async with database.session() as session:
        # Строим текстовый SQL запрос с параметрами
        query = text("""
            SELECT
                b.gos_number,
                b.capacity,
                b.is_air_conditioner,
                c.name AS company_name,
                c.address
            FROM
                buses b
            JOIN
                buses_in_company bic ON b.gos_number = bic.buses_gos_number
            JOIN
                company c ON bic.company_name = c.name
            WHERE
                (c.name ILIKE :company_name OR :company_name IS NULL)
                AND (b.is_air_conditioner = :is_air_conditioner OR :is_air_conditioner IS NULL)
                AND (b.capacity >= :min_capacity OR :min_capacity IS NULL)
                AND (b.capacity <= :max_capacity OR :max_capacity IS NULL);
        """)

        # Выполняем запрос с передачей параметров
        result = await session.execute(query, {
            "company_name": f"%{company_name}%" if company_name else None,
            "is_air_conditioner": is_air_conditioner,
            "min_capacity": min_capacity,
            "max_capacity": max_capacity
        })

        # Извлекаем результаты
        buses = result.fetchall()

        # Преобразуем результаты в модели BusSchema
        buses_schema = [BusSchema.model_validate(obj=bus) for bus in buses]

    return buses_schema
