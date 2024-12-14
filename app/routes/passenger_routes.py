from fastapi import APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.busesdb.schemas import PassengerSchema
from app.busesdb.models import Passenger
from app.database import database
from app.repo.passengers_repo import PassengerRepository

passenger_router = APIRouter(prefix="/passenger")
passenger_repo = PassengerRepository()

@passenger_router.get("/passengers", response_model=list[PassengerSchema], status_code=status.HTTP_200_OK)
async def get_all_passengers() -> list[PassengerSchema]:
   """Получение всех пассажиров."""
   async with database.session () as session:
      passengers=await passenger_repo.get_all_passengers (session=session)
   return passengers

@passenger_router.get("/passengers/{id}", response_model=PassengerSchema,
                      status_code=status.HTTP_200_OK)

async def get_passenger_by_id(id:int)->PassengerSchema:

   """Получение пассажира по ID."""

   async with database.session () as session:

      passenger=await passenger_repo.get_passenger_by_id (session=session ,id=id)

      if not passenger:

         raise HTTPException (status_code=status.HTTP_404_NOT_FOUND ,detail="Пассажир не найден")

   return passenger

@passenger_router.post("/passengers", response_model=PassengerSchema,
                       status_code=status.HTTP_201_CREATED)

async def add_passenger(passenger_data :PassengerSchema)->PassengerSchema:

   """Создание нового пассажира."""

   async with database.session () as session:

      new_passenger=await passenger_repo.create_passenger (session=session ,passenger_data=passenger_data)

   return new_passenger

@passenger_router.put("/passengers/{id}",response_model=PassengerSchema,status_code=status.HTTP_200_OK)

async def update_passenger(id:int ,passenger_data :PassengerSchema)->PassengerSchema:

   """Обновление информации о пассажире."""

   async with database.session () as session:

      updated_passenger=await passenger_repo.update_passenger (session=session ,id=id ,passenger_data=passenger_data.dict ())

      if not updated_passenger:

         raise HTTPException (status_code=status.HTTP_404_NOT_FOUND ,detail="Пассажир не найден")

   return updated_passenger

@passenger_router.delete("/passengers/{id}",status_code=status.HTTP_204_NO_CONTENT)

async def delete_passenger(id:int)->None:

   """Удаление пассажира."""

   async with database.session () as session:

      success=await passenger_repo.delete_passenger (session=session ,id=id)

      if not success:

         raise HTTPException (status_code=status.HTTP_404_NOT_FOUND ,detail="Пассажир не найден")