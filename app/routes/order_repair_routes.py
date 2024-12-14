from fastapi import APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.busesdb.schemas import OrderRepairSchema
from app.busesdb.models import OrderRepair
from app.database import database
from app.repo.order_repair_repo import OrderRepairRepository

order_repair_router = APIRouter(prefix="/order_repair")
order_repair_repo = OrderRepairRepository()

@order_repair_router.get("/order_repair", response_model=list[OrderRepairSchema], status_code=status.HTTP_200_OK)
async def get_all_orders() -> list[OrderRepairSchema]:
    """Получение всех заказов на ремонт."""
    async with database.session() as session:
        orders = await order_repair_repo.get_all_orders(session=session)
    return orders

@order_repair_router.get("/order_repair/{id}", response_model=OrderRepairSchema, status_code=status.HTTP_200_OK)
async def get_order_by_id(id: int) -> OrderRepairSchema:
    """Получение заказа на ремонт по ID."""
    async with database.session() as session:
        order = await order_repair_repo.get_order_by_id(session=session, id=id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Заказ не найден")
    return order

@order_repair_router.post("/order_repair", response_model=OrderRepairSchema, status_code=status.HTTP_201_CREATED)
async def add_order(order_data: OrderRepairSchema) -> OrderRepairSchema:
    """Создание нового заказа на ремонт."""
    async with database.session() as session:
        new_order = await order_repair_repo.create_order(session=session, order_data=order_data)
    return new_order

@order_repair_router.put("/order_repair/{id}", response_model=OrderRepairSchema, status_code=status.HTTP_200_OK)
async def update_order(id: int, order_data: OrderRepairSchema) -> OrderRepairSchema:
    """Обновление информации о заказе на ремонт."""
    async with database.session() as session:
        updated_order = await order_repair_repo.update_order(session=session, id=id, order_data=order_data.dict())
        if not updated_order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Заказ не найден")
    return updated_order

@order_repair_router.delete("/order_repair/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(id: int) -> None:
    """Удаление заказа на ремонт."""
    async with database.session() as session:
        success = await order_repair_repo.delete_order(session=session, id=id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Заказ не найден")