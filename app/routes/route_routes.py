from fastapi import APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.busesdb.schemas import RouteSchema
from app.busesdb.models import Route
from app.database import database
from app.repo.routes_repo import RouteRepository

route_router = APIRouter()
route_repo = RouteRepository()

@route_router.get("/routes", response_model=list[RouteSchema], status_code=status.HTTP_200_OK)
async def get_all_routes() -> list[RouteSchema]:
    """Получение всех маршрутов."""
    async with database.session() as session:
        routes = await route_repo.get_all_routes(session=session)
    return routes

@route_router.get("/routes/{number_route}", response_model=RouteSchema, status_code=status.HTTP_200_OK)
async def get_route_by_number(number_route: str) -> RouteSchema:
   """Получение маршрута по номеру маршрута."""
   async with database.session () as session:
      route=await route_repo.get_route_by_number (session=session ,number_route=number_route)
      if not route:
         raise HTTPException (status_code=status.HTTP_404_NOT_FOUND ,detail="Маршрут не найден")
   return route

@route_router.post("/routes", response_model=RouteSchema, status_code=status.HTTP_201_CREATED)
async def add_route(route_data: RouteSchema) -> RouteSchema:
   """Создание нового маршрута."""
   async with database.session () as session:
      new_route=await route_repo.create_route (session=session ,route_data=route_data)
   return new_route

@route_router.put("/routes/{number_route}", response_model=RouteSchema, status_code=status.HTTP_200_OK)
async def update_route(number_route: str, route_data: RouteSchema) -> RouteSchema:
   """Обновление информации о маршруте."""
   async with database.session () as session:
      updated_route=await route_repo.update_route (session=session ,number_route=number_route ,route_data=route_data.dict ())
      if not updated_route:
         raise HTTPException (status_code=status.HTTP_404_NOT_FOUND ,detail="Маршрут не найден")
   return updated_route

@route_router.delete("/routes/{number_route}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_route(number_route: str) -> None:
   """Удаление маршрута."""
   async with database.session () as session:
      success=await route_repo.delete_route (session=session ,number_route=number_route)
      if not success:
         raise HTTPException (status_code=status.HTTP_404_NOT_FOUND ,detail="Маршрут не найден")