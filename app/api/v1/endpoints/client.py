# Archivo diseñado para recibir los correos de los posibles clientes pero aun no son usuarios de la tienda solo dejan sus correos para recibir descuerstos de los lanzamientos mensuales

from datetime import datetime
from typing import List

from app.db import database
from app.schemas import client
from app.services import client_service
from fastapi import APIRouter, Depends
from pydantic import EmailStr
from sqlmodel import Session

router = APIRouter()


@router.get("/", response_model=List[client.ClientRead])
def read_client(db: Session = Depends(database.get_session)):
    return client_service.obtener_todos_los_clients(db)


@router.get("/reporte/fechas", response_model=List[client.ClientRead])
def reporte_mensual(
    inicio: datetime, fin: datetime, db: Session = Depends(database.get_session)
):
    return client_service.obtener_clients_por_fecha(db, inicio, fin)


@router.get("/buscar", response_model=client.ClientRead)
def read_client_email(email: EmailStr, db: Session = Depends(database.get_session)):
    return client_service.obtener_clients_por_email(db, email)


@router.post("/", response_model=client.ClientRead)
def crear_cliente(
    client_in: client.ClientCreate, db: Session = Depends(database.get_session)
):
    return client_service.crear_client(db, client_in)
