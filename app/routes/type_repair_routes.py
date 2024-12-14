from fastapi import APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.busesdb.schemas import TypeRepairSchema
from app.busesdb.models import TypeRepair
from app.database import database
from app.repo.type_repair_repo import TypeRepairRepository

type_repair_router = APIRouter(prefix="/type_repair")
type_repair_repo = TypeRepairRepository()

@type_repair_router.get("/type_repair", response_model=list[TypeRepairSchema], status_code=status.HTTP_200_OK)
async def get_all_types() -> list[TypeRepairSchema]:
    """Получение всех типов ремонта."""
    async with database.session() as session:
        types = await type_repair_repo.get_all_types(session=session)
    return types

@type_repair_router.get("/type_repair/{id}", response_model=TypeRepairSchema, status_code=status.HTTP_200_OK)
async def get_type_by_id(id: int) -> TypeRepairSchema:
    """Получение типа ремонта по ID."""
    async with database.session() as session:
        type_ = await type_repair_repo.get_type_by_id(session=session, id=id)
        if not type_:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Тип ремонта не найден")
    return type_

@type_repair_router.post("/type_repair", response_model=TypeRepairSchema, status_code=status.HTTP_201_CREATED)
async def add_type(type_data: TypeRepairSchema) -> TypeRepairSchema:
    """Создание нового типа ремонта."""
    async with database.session() as session:
        new_type = await type_repair_repo.create_type(session=session, type_data=type_data)
    return new_type

@type_repair_router.put("/type_repair/{id}", response_model=TypeRepairSchema, status_code=status.HTTP_200_OK)
async def update_type(id: int, type_data: TypeRepairSchema) -> TypeRepairSchema:
    """Обновление информации о типе ремонта."""
    async with database.session() as session:
        updated_type = await type_repair_repo.update_type(session=session, id=id, type_data=type_data.dict())
        if not updated_type:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Тип ремонта не найден")
    return updated_type

@type_repair_router.delete("/type_repair/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_type(id: int) -> None:
    """Удаление типа ремонта."""
    async with database.session() as session:
        success = await type_repair_repo.delete_type(session=session, id=id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Тип ремонта не найден")