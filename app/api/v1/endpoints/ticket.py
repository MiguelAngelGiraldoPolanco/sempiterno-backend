from datetime import datetime
from typing import List

from app.db import database
from app.schemas import ticket
from app.services import ticket_service
from fastapi import APIRouter, Depends
from sqlmodel import Session

router = APIRouter()


@router.get("/", response_model=List[ticket.TicketRead])
async def read_tickets(db: Session = Depends(database.get_session)):
    return ticket_service.obtener_todos_los_tickets(db)


@router.get("/{ticket_id}", response_model=ticket.TicketRead)
async def obtener_ticket(ticket_id: int, db: Session = Depends(database.get_session)):
    return ticket_service.obtener_ticket_por_id(db, ticket_id)


@router.get("/reporte/fechas", response_model=List[ticket.ReporteMensual])
async def reporte_mensual(
    inicio: datetime, fin: datetime, db: Session = Depends(database.get_session)
):
    return ticket_service.obtener_tikets_por_fecha(db, inicio, fin)


@router.post("/", response_model=ticket.TicketRead)
async def crear_ticket(
    ticket_in: ticket.TicketCreate, db: Session = Depends(database.get_session)
):
    return ticket_service.crear_ticket(db, ticket_in)


@router.delete("/{ticket_id}")
async def delete_ticket(ticket_id: int, db: Session = Depends(database.get_session)):
    return ticket_service.eliminar_ticket(db, ticket_id)
