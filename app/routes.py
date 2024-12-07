from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from app.busesdb.models import Bus
from app.busesdb.schemas import BusSchema
from app.database import database

router = APIRouter()


@router.get("/buses", response_model=list[BusSchema], status_code=status.HTTP_200_OK)
async def read_buses(skip: int = 0, limit: int = 10) -> list[BusSchema]:
    async with database.session() as session:
        result = await session.execute(select(Bus).offset(skip).limit(limit))
        buses = result.scalars().all()

    if not buses:
        raise HTTPException(status_code=404, detail="Автобусы не найдены")

    return [BusSchema.model_validate(obj=bus) for bus in buses]



# @router.get("/healthcheck", response_model=HealthCheckSchema, status_code=status.HTTP_200_OK)
# async def check_health() -> HealthCheckSchema:
#     async with database.session() as session:
#         db_is_ok = await user_repo.check_connection(session=session)

#     return HealthCheckSchema(
#         db_is_ok=db_is_ok,
#     )
