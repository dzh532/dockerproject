import asyncio
import logging
import uvicorn

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config import settings

from app.routes.buses_routes import bus_router
from app.routes.company_routes import company_router
from app.routes.delay_voyage_routes import delay_router
from app.routes.driver_routes import driver_router
from app.routes.order_repair_routes import order_repair_router
from app.routes.passenger_routes import passenger_router
from app.routes.report_income_company_routes import report_income_router
from app.routes.review_passenger_routes import review_passenger_router
from app.routes.route_routes import route_router
from app.routes.route_sheet_routes import route_sheet_router
from app.routes.stop_routes import stop_router
from app.routes.stops_and_routes_routes import stops_and_routes_router
from app.routes.ticket_routes import ticket_router
from app.routes.type_repair_routes import type_repair_router

from app.auth.jwt_auth import router as jwt_router

routers = [
    bus_router,
    company_router,
    driver_router,
    delay_router,
    report_income_router,
    type_repair_router,
    order_repair_router,
    stop_router,
    route_router,
    stops_and_routes_router,
    passenger_router,
    ticket_router,
    route_sheet_router,
    review_passenger_router,
]

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app_options = {}
    if settings.ENV.lower() == "prod":
        app_options = {
            "docs_url": None,
            "redoc_url": None,
        }
    if settings.LOG_LEVEL in ["DEBUG", "INFO"]:
        app_options["debug"] = True

    app = FastAPI(root_path=settings.ROOT_PATH, **app_options)
    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=settings.ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(jwt_router, prefix="/jwt", tags=["JWT"])
    for router in routers:
        app.include_router(router, prefix="/api", tags=[router.prefix.strip("/")])

    return app


app = create_app()


async def run() -> None:
    config = uvicorn.Config("main:app", host="0.0.0.0", port=8000, reload=False)
    server = uvicorn.Server(config=config)
    tasks = (
        asyncio.create_task(server.serve()),
    )

    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)


if __name__ == "__main__":
    logger.debug(f"{settings.postgres_url}=")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
