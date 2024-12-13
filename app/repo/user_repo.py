from typing import Type, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.busesdb.schemas import UserSchema
from app.busesdb.models import User
from app.config import settings


class UserRepository:
    _collection: Type[User] = User

    async def get_all_users(self, session: AsyncSession) -> list[UserSchema]:
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.users;")
        result = await session.execute(query)
        users = result.mappings().all()
        return [UserSchema.model_validate(obj=user) for user in users]

    async def get_user_by_id(self, session: AsyncSession, id: int) -> Optional[UserSchema]:
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.users WHERE id = :id;")
        result = await session.execute(query, {"id": id})
        user = result.mappings().first()
        return UserSchema.model_validate(obj=user) if user else None

    async def create_user(self, session: AsyncSession, user_data: UserSchema) -> UserSchema:
        new_user = self._collection(**user_data.dict())
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return UserSchema.model_validate(obj=new_user)

    async def update_user(self, session: AsyncSession, id: int, user_data: dict) -> Optional[UserSchema]:
        query = text(f"""
            UPDATE {settings.POSTGRES_SCHEMA}.users
            SET name = :name, email = :email, password = :password, is_admin = :is_admin
            WHERE id = :id
            RETURNING *;
        """)
        result = await session.execute(query, {"id": id, **user_data})
        updated_user = result.mappings().first()
        await session.commit()
        return UserSchema.model_validate(obj=updated_user) if updated_user else None

    async def delete_user(self, session: AsyncSession, id: int) -> bool:
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.users WHERE id = :id;")
        result = await session.execute(query, {"id": id})
        await session.commit()
        return result.rowcount > 0

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False
