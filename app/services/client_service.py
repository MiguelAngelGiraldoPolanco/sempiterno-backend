from datetime import datetime, timezone
from typing import Sequence

from app.models.client import Client
from app.schemas.client import ClientCreate
from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlmodel import Session, select


def crear_client(db: Session, client_data: ClientCreate) -> Client:
    # Evaluamos primero si el email existe para que no pueda acceder a muchos desceuntos con el mismo email
    if obtener_clients_por_email(db, client_data.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El cliente ya existe",
        )
    nuevo_cliente = Client(**client_data.model_dump())
    db.add(nuevo_cliente)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error de integridad, intente de nuevo",
        )

    db.refresh(nuevo_cliente)

    return nuevo_cliente


def obtener_todos_los_clients(db: Session) -> Sequence[Client]:
    return db.exec(select(Client)).all()


def obtener_clients_por_fecha(
    db: Session, init_date: datetime, last_date: datetime
) -> Sequence[Client]:
    sentencia = select(Client).where(
        Client.date.between(asegurar_utc(init_date), asegurar_utc(last_date))
    )

    return db.exec(sentencia).all()


def obtener_clients_por_email(db: Session, email: EmailStr) -> Client | None:
    sentencia = select(Client).where(Client.email == email)

    return db.exec(sentencia).first()


def asegurar_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)
