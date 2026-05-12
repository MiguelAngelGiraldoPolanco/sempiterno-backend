# Archivo diseñado para recibir los correos de los posibles clientes pero aun no son usuarios de la tienda solo dejan sus correos para recibir descuerstos de los lanzamientos mensuales

from datetime import datetime

from app.db import database
from app.schemas import lead
from app.services import lead_service
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr
from sqlmodel import Session

router = APIRouter(prefix="/leads", tags=["Leads"])


@router.get(
    "/",
    response_model=list[lead.LeadRead],
)
def read_lead(
    db: Session = Depends(database.get_session),
):
    return lead_service.obtener_todos_los_leads(db)


@router.get(
    "/reporte/fechas",
    response_model=list[lead.LeadRead],
)
def reporte_mensual(
    inicio: datetime,
    fin: datetime,
    db: Session = Depends(database.get_session),
):
    return lead_service.obtener_leads_por_fecha(db, inicio, fin)


@router.get(
    "/email/{email_lead}",
    response_model=lead.LeadRead,
)
def read_lead_email(
    email_lead: EmailStr,
    db: Session = Depends(database.get_session),
):
    lead = lead_service.obtener_leads_por_email(db, email_lead)
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead no encontrado",
        )
    return lead


@router.post(
    "/",
    response_model=lead.LeadRead,
    status_code=status.HTTP_201_CREATED,
)
def crear_lead(
    lead_in: lead.LeadCreate,
    db: Session = Depends(database.get_session),
):
    return lead_service.crear_lead(db, lead_in)
