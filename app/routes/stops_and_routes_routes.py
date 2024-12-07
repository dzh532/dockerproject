from fastapi import APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.busesdb.schemas import StopsAndRoutesSchema
from app.busesdb.models import StopsAndRoutes
from app.database import database
from app.repo.stops_and_routes_repo import StopsAndRoutesRepository

stops_and_routes_router = APIRouter()
stops_and_routes_repo = StopsAndRoutesRepository()

@stops_and_routes_router.get("/stops_and_routes", response_model=list[StopsAndRoutesSchema], status_code=status.HTTP_200_OK)
async def get_all_stops_and_routes() -> list[StopsAndRoutesSchema]:
   """Получение всех связей между остановками и маршрутами."""
   async with database.session () as session:
      stops_and_routes=await stops_and_routes_repo.get_all_stops_and_routes (session=session)
   return stops_and_routes

@stops_and_routes_router.get("/stops_and_routes/{id_stops}/{number_route}", response_model=StopsAndRoutesSchema,
                              status_code=status.HTTP_200_OK)
async def get_stops_and_routes_by_id(id_stops: int, number_route: str) -> StopsAndRoutesSchema:
   """Получение связи между остановкой и маршрутом по их идентификаторам."""
   async with database.session () as session:
      stops_and_route=await stops_and_routes_repo.get_stops_and_routes_by_id (session=session ,id_stops=id_stops ,number_route=number_route)
      if not stops_and_route:
         raise HTTPException (status_code=status.HTTP_404_NOT_FOUND ,detail="Связь не найдена")
   return stops_and_route

@stops_and_routes_router.post("/stops_and_routes", response_model=StopsAndRoutesSchema,
                               status_code=status.HTTP_201_CREATED)
async def add_stops_and_routes(stops_and_routes_data: StopsAndRoutesSchema) -> StopsAndRoutesSchema:
   """Создание новой связи между остановкой и маршрутом."""
   async with database.session () as session:
      new_stops_and_routes=await stops_and_routes_repo.create_stops_and_routes (session=session ,stops_and_routes_data=stops_and_routes_data)
   return new_stops_and_routes

@stops_and_routes_router.put("/stops_and_routes/{id_stops}/{number_route}",
                              response_model=StopsAndRoutesSchema,
                              status_code=status.HTTP_200_OK)
async def update_stops_and_routes(id_stops: int,
                                   number_route: str,
                                   stops_and_routes_data: StopsAndRoutesSchema) -> StopsAndRoutesSchema:

   """Обновление информации о связи между остановкой и маршрутом."""
   async with database.session () as session:
      updated_stops_and_routes=await stops_and_routes_repo.update_stops_and_routes (session=session ,
                                                                           id_stops=id_stops ,
                                                                           number_route=number_route ,
                                                                           stops_and_routes_data=stops_and_routes_data.dict ())
      if not updated_stops_and_routes:
         raise HTTPException (status_code=status.HTTP_404_NOT_FOUND ,detail="Связь не найдена")
   return updated_stops_and_routes

@stops_and_routes_router.delete("/stops_and_routes/{id_stops}/{number_route}",
                                 status_code=status.HTTP_204_NO_CONTENT)
async def delete_stops_and_routes(id_stops: int,
                                   number_route: str) -> None:

   """Удаление связи между остановкой и маршрутом."""
   async with database.session () as session:
      success=await stops_and_routes_repo.delete_stops_and_routes (session=session ,
                                                                  id_stops=id_stops ,
                                                                  number_route=number_route)
      if not success:
         raise HTTPException (status_code=status.HTTP_404_NOT_FOUND ,detail="Связь не найдена")