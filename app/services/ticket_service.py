from datetime import datetime

from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate
from fastapi import HTTPException
from sqlmodel import Session, select


# 1. FUNCIÓN PARA CREAR
def crear_ticket(db: Session, ticket_data: TicketCreate) -> Ticket:
    """
    Recibe el esquema de validación y lo transforma en un modelo de DB para guardarlo.
    """
    # Convertimos el Schema en Modelo (SQLModel)
    # .model_validate es como decir "copia estos datos al molde de la base de datos"
    nuevo_ticket = Ticket.model_validate(ticket_data)

    db.add(nuevo_ticket)
    db.commit()
    db.refresh(nuevo_ticket)  # Para que nos devuelva el ID que generó la DB
    return nuevo_ticket


# 2. FUNCIÓN PARA OBTENER TODOS (LECTURA)
def obtener_todos_los_tickets(db: Session):
    """
    Trae una lista de todos los tickets en la base de datos.
    """
    # Esto es como el "SELECT * FROM ticket"
    sentencia = select(Ticket)
    resultados = db.exec(sentencia).all()
    return resultados


# 3. FUNCIÓN PARA OBTENER UNO SOLO (DETALLE)
def obtener_ticket_por_id(db: Session, ticket_id: int):
    """
    Busca un ticket específico. Si no existe, lanza un error.
    """
    ticket = db.get(Ticket, ticket_id)
    if not ticket:
        # Aquí lanzamos el error 404 directamente
        raise HTTPException(status_code=404, detail="El ticket no existe")
    return ticket


def obtener_tikets_por_fecha(db: Session, init_date: datetime, last_date: datetime):
    sentencia = select(Ticket).where(Ticket.fecha.between(fecha_inicio, fecha_fin))
    resultados = db.exec(sentencia).all()
    return resultados


# 4. FUNCIÓN PARA ELIMINAR
def eliminar_ticket(db: Session, ticket_id: int):
    """
    Busca y borra un ticket.
    """
    ticket_db = obtener_ticket_por_id(
        db, ticket_id
    )  # Reutilizamos la función de arriba
    db.delete(ticket_db)
    db.commit()
    return {"ok": True, "message": f"Ticket {ticket_id} eliminado"}
