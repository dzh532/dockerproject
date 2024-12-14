from typing import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jwt.exceptions import InvalidTokenError
from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    status,
)
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
)
from pydantic import BaseModel, EmailStr
from app.auth import utils as auth_utils
from app.busesdb.schemas import UserSchema
from app.database import database
from app.busesdb.models import User

# http_bearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/jwt/login/",
)

async def get_db() -> AsyncIterator[AsyncSession]:
    async with database.session() as session:
        yield session

class TokenInfo(BaseModel):
    access_token: str
    token_type: str

router = APIRouter()

# john = UserSchema(
#     username="john",
#     password=auth_utils.hash_password("qwerty"),
#     email="john@example.com",
# )
#
# sam = UserSchema(
#     username="sam",
#     password=auth_utils.hash_password("secret"),
# )
#
# users_db: dict[str, UserSchema] = {
#     john.username: john,
#     sam.username: sam,
# }

async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
    db: AsyncSession = Depends(get_db)
):
    # query = await db.execute(
    #     User.select().where(User.name == name)
    # )
    # user = query.scalar_one_or_none()
    query = select(User).where(User.name == username)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверное имя пользователя или пароль",
    )
    if not user or not auth_utils.validate_password(password, user.password):
        raise unauthed_exc

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользвоатель не активен",
        )
    return user

def get_current_token_payload(
    # credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
    token: str = Depends(oauth2_scheme),
)-> UserSchema:
    # token = credentials.credentials
    try:
        payload = auth_utils.decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            # detail=f"invalid token error: {e}",
            detail=f"неверный токен",
        )
    return payload

async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    db: AsyncSession = Depends(get_db)
):
    username = payload.get("sub")
    # query = await db.execute(
    #     User.select().where(User.name == name)
    # )
    # user = query.scalar_one_or_none()

    query = select(User).where(User.name == username)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен неверный (пользователь не найден)",
        )
    return user


def get_current_active_auth_user(
    user: UserSchema = Depends(get_current_auth_user),
):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Пользователь не активен",
    )

async def get_current_admin_user(
    user: User = Depends(get_current_auth_user),
):
    if user.is_admin:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Вы не имеете привелегий админа",
    )

@router.post("/login/", response_model=TokenInfo)
async def auth_user_issue_jwt(
    user: User = Depends(validate_auth_user),
):
    jwt_payload = {
        "sub": user.name,
        "name": user.name,
        "email": user.email,
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )

@router.get("users/me/")
def auth_user_check_self_info(
    user: UserSchema = Depends(get_current_active_auth_user),
):
    return{
        "name": user.name,
        "email": user.email,
    }

@router.get("/admin/protected/")
async def admin_route(
    admin: User = Depends(get_current_admin_user),
):
    return {"message": "Вы вошли как админ"}

@router.post("/register/")
async def register_user(
    username: str = Form(),
    email: EmailStr = Form(),
    password: str = Form(),
    db: AsyncSession = Depends(get_db)
):
    hashed_password = auth_utils.hash_password(password).decode()
    new_user = User(name=username, email=email, password=hashed_password)
    db.add(new_user)
    await db.commit()
    return {"message": "Вы успешно зарегистрировались"}
