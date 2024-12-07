from typing import Type, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.busesdb.schemas import StopsAndRoutesSchema
from app.busesdb.models import StopsAndRoutes
from app.config import settings

class StopsAndRoutesRepository:
    _collection: Type[StopsAndRoutes] = StopsAndRoutes

    async def get_all_stops_and_routes(self, session: AsyncSession) -> list[StopsAndRoutesSchema]:
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.stops_and_routes;")
        result = await session.execute(query)
        stops_and_routes = result.mappings().all()
        return [StopsAndRoutesSchema.model_validate(obj=stops_and_route) for stops_and_route in stops_and_routes]

    async def get_stops_and_routes_by_id(self, session: AsyncSession, id_stops: int, number_route: str) -> Optional[StopsAndRoutesSchema]:
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.stops_and_routes WHERE id_stops = :id_stops AND number_route = :number_route;")
        result = await session.execute(query, {"id_stops": id_stops, "number_route": number_route})
        stops_and_route = result.mappings().first()
        return StopsAndRoutesSchema.model_validate(obj=stops_and_route) if stops_and_route else None

    async def create_stops_and_routes(self, session: AsyncSession, stops_and_routes_data: StopsAndRoutesSchema) -> StopsAndRoutesSchema:
        new_stops_and_routes = self._collection(**stops_and_routes_data.dict())
        session.add(new_stops_and_routes)
        await session.commit()
        await session.refresh(new_stops_and_routes)
        return StopsAndRoutesSchema.model_validate(obj=new_stops_and_routes)

    async def update_stops_and_routes(self, session: AsyncSession, id_stops: int, number_route: str, stops_and_routes_data: dict) -> Optional[StopsAndRoutesSchema]:
        query = text(f"""
            UPDATE {settings.POSTGRES_SCHEMA}.stops_and_routes
            SET id_stops = :id_stops,
                number_route = :number_route
            WHERE id_stops = :id_stops AND number_route = :number_route
            RETURNING *;
        """)
        result = await session.execute(query, {"id_stops": id_stops, "number_route": number_route, **stops_and_routes_data})
        updated_stops_and_routes = result.mappings().first()
        await session.commit()
        return StopsAndRoutesSchema.model_validate(obj=updated_stops_and_routes) if updated_stops_and_routes else None

    async def delete_stops_and_routes(self, session: AsyncSession, id_stops: int, number_route: str) -> bool:
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.stops_and_routes WHERE id_stops = :id_stops AND number_route = :number_route;")
        result = await session.execute(query, {"id_stops": id_stops, "number_route": number_route})
        await session.commit()
        return result.rowcount > 0