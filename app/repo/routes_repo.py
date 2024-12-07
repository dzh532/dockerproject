from typing import Type, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.busesdb.schemas import RouteSchema
from app.busesdb.models import Route
from app.config import settings

class RouteRepository:
    _collection: Type[Route] = Route

    async def get_all_routes(self, session: AsyncSession) -> list[RouteSchema]:
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.routes;")
        result = await session.execute(query)
        routes = result.mappings().all()
        return [RouteSchema.model_validate(obj=route) for route in routes]

    async def get_route_by_number(self, session: AsyncSession, number_route: str) -> Optional[RouteSchema]:
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.routes WHERE number_route = :number_route;")
        result = await session.execute(query, {"number_route": number_route})
        route = result.mappings().first()
        return RouteSchema.model_validate(obj=route) if route else None

    async def create_route(self, session: AsyncSession, route_data: RouteSchema) -> RouteSchema:
        new_route = self._collection(**route_data.dict())
        session.add(new_route)
        await session.commit()
        await session.refresh(new_route)
        return RouteSchema.model_validate(obj=new_route)

    async def update_route(self, session: AsyncSession, number_route: str, route_data: dict) -> Optional[RouteSchema]:
        query = text(f"""
            UPDATE {settings.POSTGRES_SCHEMA}.routes
            SET count_stops = :count_stops,
                start_stop = :start_stop,
                end_stop = :end_stop,
                time_start = :time_start,
                time_end = :time_end,
                cost_travel = :cost_travel
            WHERE number_route = :number_route
            RETURNING *;
        """)
        result = await session.execute(query, {"number_route": number_route, **route_data})
        updated_route = result.mappings().first()
        await session.commit()
        return RouteSchema.model_validate(obj=updated_route) if updated_route else None

    async def delete_route(self, session: AsyncSession, number_route: str) -> bool:
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.routes WHERE number_route = :number_route;")
        result = await session.execute(query, {"number_route": number_route})
        await session.commit()
        return result.rowcount > 0