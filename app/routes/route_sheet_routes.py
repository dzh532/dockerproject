from fastapi import APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.busesdb.schemas import RouteSheetSchema
from app.busesdb.models import RouteSheet
from app.database import database
from app.repo.route_sheet_repo import RouteSheetRepository

route_sheet_router = APIRouter(prefix="/route_sheet")
route_sheet_repo = RouteSheetRepository()

@route_sheet_router.get("/route_sheets", response_model=list[RouteSheetSchema], status_code=status.HTTP_200_OK)
async def get_all_route_sheets() -> list[RouteSheetSchema]:
    """Получение всех маршрутных листов."""
    async with database.session() as session:
        route_sheets = await route_sheet_repo.get_all_sheets(session=session)
    return route_sheets

@route_sheet_router.get("/route_sheets/{id}", response_model=RouteSheetSchema, status_code=status.HTTP_200_OK)
async def get_route_sheet_by_id(id: int) -> RouteSheetSchema:
    """Получение маршрутного листа по ID."""
    async with database.session() as session:
        route_sheet = await route_sheet_repo.get_sheet_by_id(session=session, id=id)
        if not route_sheet:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Маршрутный лист не найден")
    return route_sheet

@route_sheet_router.post("/route_sheets", response_model=RouteSheetSchema, status_code=status.HTTP_201_CREATED)
async def add_route_sheet(route_sheet_data: RouteSheetSchema) -> RouteSheetSchema:
    """Создание нового маршрутного листа."""
    async with database.session() as session:
        new_route_sheet = await route_sheet_repo.create_sheet(session=session, sheet_data=route_sheet_data)
    return new_route_sheet

@route_sheet_router.put("/route_sheets/{id}", response_model=RouteSheetSchema, status_code=status.HTTP_200_OK)
async def update_route_sheet(id: int, route_sheet_data: RouteSheetSchema) -> RouteSheetSchema:
    """Обновление информации о маршрутном листе."""
    async with database.session() as session:
        updated_route_sheet = await route_sheet_repo.update_sheet(session=session, id=id, sheet_data=route_sheet_data.dict())
        if not updated_route_sheet:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Маршрутный лист не найден")
    return updated_route_sheet

@route_sheet_router.delete("/route_sheets/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_route_sheet(id: int) -> None:
    """Удаление маршрутного листа."""
    async with database.session() as session:
        success = await route_sheet_repo.delete_sheet(session=session, id=id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Маршрутный лист не найден")