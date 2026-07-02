from datetime import datetime

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.api.deps import get_current_admin_user
from app.db import database
from app.models.user import User
from app.schemas import ticket
from app.services import ticket_service

router = APIRouter(prefix="/tikects", tags=["Tikects"])


@router.get(
    "/",
    response_model=list[ticket.TicketRead],
)
def read_tickets(
    db: Session = Depends(database.get_session),
    current_admin: User = Depends(get_current_admin_user),
):
    return ticket_service.obtener_todos_los_tickets(db)


@router.get(
    "/{ticket_id}",
    response_model=ticket.TicketRead,
)
def obtener_ticket(
    ticket_id: int,
    db: Session = Depends(database.get_session),
    current_admin: User = Depends(get_current_admin_user),
):
    return ticket_service.obtener_ticket_por_id(db, ticket_id)


@router.get(
    "/reporte/fechas",
    response_model=ticket.ReporteMensual,
)
def reporte_mensual(
    inicio: datetime,
    fin: datetime,
    db: Session = Depends(database.get_session),
    current_admin: User = Depends(get_current_admin_user),
):
    return ticket_service.obtener_tickets_por_fecha(db, inicio, fin)


@router.post(
    "/",
    response_model=ticket.TicketRead,
    status_code=status.HTTP_201_CREATED,
)
def crear_ticket(
    ticket_in: ticket.TicketCreate,
    db: Session = Depends(database.get_session),
    current_admin: User = Depends(get_current_admin_user),
):
    return ticket_service.crear_ticket(db, ticket_in)


@router.put(
    "/{ticket_id}",
    response_model=ticket.TicketRead,
)
def actualizar_ticket(
    ticket_id: int,
    ticket_in: ticket.TicketUpdate,
    db: Session = Depends(database.get_session),
    current_admin: User = Depends(get_current_admin_user),
):
    return ticket_service.actualizar_ticket(db, ticket_id, ticket_in)


@router.delete(
    "/{ticket_id}",
)
def delete_ticket(
    ticket_id: int,
    db: Session = Depends(database.get_session),
    current_admin: User = Depends(get_current_admin_user),
):
    return ticket_service.eliminar_ticket(db, ticket_id)
