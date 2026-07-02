from datetime import datetime, timezone
from typing import Sequence

from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models.db_model import Ticket
from app.schemas.ticket import TicketCreate, TicketUpdate


def crear_ticket(
    db: Session,
    ticket_data: TicketCreate,
) -> Ticket:

    nuevo_ticket = Ticket(**ticket_data.model_dump())
    db.add(nuevo_ticket)
    try:
        db.commit()
        db.refresh(nuevo_ticket)
        return nuevo_ticket
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error de integridad, intente de nuevo",
        )


def obtener_todos_los_tickets(
    db: Session,
) -> Sequence[Ticket]:

    return db.exec(select(Ticket)).all()


def obtener_ticket_por_id(
    db: Session,
    ticket_id: int,
) -> Ticket | None:

    ticket = db.get(Ticket, ticket_id)
    if not ticket:
        # Aquí lanzamos el error 404 directamente
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El ticket no existe",
        )
    return ticket


def obtener_tickets_por_fecha(
    db: Session,
    init_date: datetime,
    last_date: datetime,
) -> Sequence[Ticket]:

    if init_date > last_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha de inicio no puede ser posterior a la fecha de fin",
        )

    sentencia = select(Ticket).where(
        Ticket.create_at.between(
            asegurar_utc(init_date),
            asegurar_utc(last_date),
        )
    )

    tickets = db.exec(sentencia).all()
    total = sum(t.total for t in tickets)
    cantidad = len(tickets)

    return {
        "total_ventas": total,
        "cantidad_tickets": cantidad,
        "tickets": tickets,
    }


def actualizar_ticket(
    db: Session,
    ticket_id: int,
    ticket_data: TicketUpdate,
) -> Ticket:

    ticket_db = db.get(Ticket, ticket_id)
    if not ticket_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket no encontrado",
        )

    datos_nuevos = (
        ticket_data
        if isinstance(ticket_data, dict)
        else ticket_data.model_dump(exclude_unset=True)
    )

    if "products" in datos_nuevos:
        ticket_db.products = datos_nuevos["products"]

    if "total" in datos_nuevos:
        ticket_db.total = datos_nuevos["total"]

    if "iva" in datos_nuevos:
        ticket_db.iva = datos_nuevos["iva"]

    if "paid" in datos_nuevos:
        ticket_db.paid = datos_nuevos["paid"]

    ticket_db.update_at = datetime.now(timezone.utc)

    db.add(ticket_db)
    try:
        db.commit()
        db.refresh(ticket_db)
        return ticket_db
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error de integridad, intente de nuevo",
        )


def eliminar_ticket(
    db: Session,
    ticket_id: int,
) -> dict:

    ticket_db = db.get(Ticket, ticket_id)
    if not ticket_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket no encontrado",
        )
    db.delete(ticket_db)
    db.commit()
    return {"ok": True, "message": "Ticket eliminado"}


def asegurar_utc(
    dt: datetime,
) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)
