from fastapi import APIRouter, HTTPException, status
from sqlalchemy.testing.suite.test_reflection import users

from app.busesdb.schemas import UserSchema
from app.database import database
from app.repo.user_repo import UserRepository

user_router = APIRouter()
user_repo = UserRepository()


@user_router.get(
    "/users",
    response_model=list[UserSchema],
    status_code=status.HTTP_200_OK,
)
async def get_all_users() -> list[UserSchema]:
    async with database.session() as session:
        users = await user_repo.get_all_users(session=session)

    return users


@user_router.get(
    "/users/{id}",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
)
async def get_user_by_id(id: int) -> UserSchema:
    async with database.session() as session:
        user = await user_repo.get_user_by_id(session=session, id=id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    return user


@user_router.post(
    "/users",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_user(user_data: UserSchema) -> UserSchema:
    async with database.session() as session:
        try:
            new_user = await user_repo.create_user(session=session, user_data=user_data)
        except Exception as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    return new_user


@user_router.put(
    "/users/{id}",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
)
async def update_user(id: int, user_data: UserSchema) -> UserSchema:
    async with database.session() as session:
        updated_user = await user_repo.update_user(session=session, id=id, user_data=user_data.dict())
        if not updated_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    return updated_user


@user_router.delete(
    "/users/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(id: int) -> None:
    async with database.session() as session:
        success = await user_repo.delete_user(session=session, id=id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
