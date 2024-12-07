from typing import Type, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.busesdb.schemas import ReviewPassengerSchema
from app.busesdb.models import ReviewPassenger
from app.config import settings

class ReviewPassengerRepository:
    _collection: Type[ReviewPassenger] = ReviewPassenger

    async def get_all_reviews(self, session: AsyncSession) -> list[ReviewPassengerSchema]:
        """Получение списка всех отзывов пассажиров."""
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.review_passenger;")
        result = await session.execute(query)
        reviews = result.mappings().all()
        return [ReviewPassengerSchema.model_validate(obj=review) for review in reviews]

    async def get_review_by_id(self, session: AsyncSession, id_: int) -> Optional[ReviewPassengerSchema]:
        """Получение отзыва пассажира по его ID."""
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.review_passenger WHERE id = :id;")
        result = await session.execute(query, {"id": id_})
        review = result.mappings().first()
        return ReviewPassengerSchema.model_validate(obj=review) if review else None

    async def create_review(self, session: AsyncSession, review_data: ReviewPassengerSchema) -> ReviewPassengerSchema:
        """Создание нового отзыва пассажира."""
        new_review = self._collection(**review_data.dict())
        session.add(new_review)
        await session.commit()
        await session.refresh(new_review)
        return ReviewPassengerSchema.model_validate(obj=new_review)

    async def update_review(self, session: AsyncSession, id_: int, review_data: dict) -> Optional[ReviewPassengerSchema]:
        """Обновление данных отзыва пассажира."""
        query = text(f"""
            UPDATE {settings.POSTGRES_SCHEMA}.review_passenger
            SET id_passenger = :id_passenger,
                gos_number_bus = :gos_number_bus,
                grade = :grade,
                text_review = :text_review,
                date = :date
            WHERE id = :id
            RETURNING *;
        """)
        result = await session.execute(query, {"id": id_, **review_data})
        updated_review = result.mappings().first()
        await session.commit()
        return ReviewPassengerSchema.model_validate(obj=updated_review) if updated_review else None

    async def delete_review(self, session: AsyncSession, id_: int) -> bool:
        """Удаление отзыва пассажира по его ID."""
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.review_passenger WHERE id = :id;")
        result = await session.execute(query, {"id": id_})
        await session.commit()
        return result.rowcount > 0