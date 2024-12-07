from fastapi import APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.busesdb.schemas import TicketSchema
from app.busesdb.models import Ticket
from app.database import database
from app.repo.tickets_repo import TicketRepository

ticket_router = APIRouter()
ticket_repo = TicketRepository()

@ticket_router.get("/tickets", response_model=list[TicketSchema], status_code=status.HTTP_200_OK)
async def get_all_tickets() -> list[TicketSchema]:
    """Получение всех билетов."""
    async with database.session() as session:
        tickets = await ticket_repo.get_all_tickets(session=session)
    return tickets

@ticket_router.get("/tickets/{id}", response_model=TicketSchema, status_code=status.HTTP_200_OK)
async def get_ticket_by_id(id: int) -> TicketSchema:
    """Получение билета по ID."""
    async with database.session() as session:
        ticket = await ticket_repo.get_ticket_by_id(session=session, id=id)
        if not ticket:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Билет не найден")
    return ticket

@ticket_router.post("/tickets", response_model=TicketSchema, status_code=status.HTTP_201_CREATED)
async def add_ticket(ticket_data: TicketSchema) -> TicketSchema:
    """Создание нового билета."""
    async with database.session() as session:
        new_ticket = await ticket_repo.create_ticket(session=session, ticket_data=ticket_data)
    return new_ticket

@ticket_router.put("/tickets/{id}", response_model=TicketSchema, status_code=status.HTTP_200_OK)
async def update_ticket(id: int, ticket_data: TicketSchema) -> TicketSchema:
    """Обновление информации о билете."""
    async with database.session() as session:
        updated_ticket = await ticket_repo.update_ticket(session=session, id=id, ticket_data=ticket_data.dict())
        if not updated_ticket:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Билет не найден")
    return updated_ticket

@ticket_router.delete("/tickets/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ticket(id: int) -> None:
    """Удаление билета."""
    async with database.session() as session:
        success = await ticket_repo.delete_ticket(session=session, id=id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Билет не найден")