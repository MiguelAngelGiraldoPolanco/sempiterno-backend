from datetime import datetime, timezone

from app.models.client import Client
from app.schemas.client import ClientCreate
from fastapi import HTTPException
from pydantic import EmailStr
from sqlmodel import Session, select


def crear_client(db: Session, client_data: ClientCreate) -> Client:
    # Evaluamos primero si el email existe para que no pueda acceder a muchos desceuntos con el mismo email
    if obtener_clients_por_email(db, client_data.email):
        raise HTTPException(status_code=400, detail="El cliente ya existe")
    nuevo_cliente = Client(**client_data.model_dump())
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)

    return nuevo_cliente


def obtener_todos_los_clients(db: Session):
    sentencia = select(Client)
    resultados = db.exec(sentencia).all()
    return resultados


def obtener_clients_por_fecha(db: Session, init_date: datetime, last_date: datetime):
    sentencia = select(Client).where(
        Client.date.between(asegurar_utc(init_date), asegurar_utc(last_date))
    )
    resultados = db.exec(sentencia).all()
    return resultados


def obtener_clients_por_email(db: Session, email: EmailStr):
    sentencia = select(Client).where(Client.email == email)
    resultados = db.exec(sentencia).first()
    if not resultados:
        raise HTTPException(status_code=404, detail="El cliente no existe.")
    return resultados


def asegurar_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)
