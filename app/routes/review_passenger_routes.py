from fastapi import APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.busesdb.schemas import ReviewPassengerSchema
from app.busesdb.models import ReviewPassenger
from app.database import database
from app.repo.review_passenger_repo import ReviewPassengerRepository

review_passenger_router = APIRouter(prefix="/review_passenger")
review_passenger_repo = ReviewPassengerRepository()

@review_passenger_router.get("/reviews", response_model=list[ReviewPassengerSchema], status_code=status.HTTP_200_OK)
async def get_all_reviews() -> list[ReviewPassengerSchema]:
    """Получение всех отзывов пассажиров."""
    async with database.session() as session:
        reviews = await review_passenger_repo.get_all_reviews(session=session)
    return reviews

@review_passenger_router.get("/reviews/{id}", response_model=ReviewPassengerSchema, status_code=status.HTTP_200_OK)
async def get_review_by_id(id: int) -> ReviewPassengerSchema:
    """Получение отзыва пассажира по ID."""
    async with database.session() as session:
        review = await review_passenger_repo.get_review_by_id(session=session, id=id)
        if not review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Отзыв не найден")
    return review

@review_passenger_router.post("/reviews", response_model=ReviewPassengerSchema, status_code=status.HTTP_201_CREATED)
async def add_review(review_data: ReviewPassengerSchema) -> ReviewPassengerSchema:
    """Создание нового отзыва пассажира."""
    async with database.session() as session:
        new_review = await review_passenger_repo.create_review(session=session, review_data=review_data)
    return new_review

@review_passenger_router.put("/reviews/{id}", response_model=ReviewPassengerSchema, status_code=status.HTTP_200_OK)
async def update_review(id: int, review_data: ReviewPassengerSchema) -> ReviewPassengerSchema:
    """Обновление информации об отзыве пассажира."""
    async with database.session() as session:
        updated_review = await review_passenger_repo.update_review(session=session, id=id, review_data=review_data.dict())
        if not updated_review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Отзыв не найден")
    return updated_review

@review_passenger_router.delete("/reviews/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(id: int) -> None:
    """Удаление отзыва пассажира."""
    async with database.session() as session:
        success = await review_passenger_repo.delete_review(session=session, id=id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Отзыв не найден")