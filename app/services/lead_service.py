import secrets
from datetime import datetime, timezone
from typing import Sequence

from app.api.resend import email_verify
from app.models.lead import Lead
from app.schemas.lead import LeadCreate
from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlmodel import Session, select


def crear_lead(
    db: Session,
    lead_data: LeadCreate,
) -> Lead:
    # 1. Buscamos si el lead ya existe
    lead_existente = obtener_leads_por_email(db, lead_data.email)

    if lead_existente:
        # Caso A: Ya está verificado
        if lead_existente.is_verify:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Este correo ya canjeó su cupón anteriormente.",
            )

        # Caso B: Existe pero NO está verificado (Re-intento)
        # Generamos nuevo token para el registro que ya tenemos
        token = token = secrets.token_urlsafe(32)
        lead_existente.verification_token = token
        # Actualizamos el nombre por si lo escribió distinto
        lead_existente.name = lead_data.name

        db.add(lead_existente)
        try:
            db.commit()
            db.refresh(lead_existente)
            email_verify(lead_existente.email, lead_existente.name, token)
            return lead_existente
        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=500, detail="Error al actualizar el registro"
            )

    # 2. Si NO existe, creamos uno nuevo desde cero
    token = token = secrets.token_urlsafe(32)

    nuevo_lead = Lead(
        **lead_data.model_dump(), verification_token=token, is_verify=False
    )

    db.add(nuevo_lead)
    try:
        db.commit()
        db.refresh(nuevo_lead)
        # Pasamos el token a la función de email para que cree el link
        email_verify(nuevo_lead.email, nuevo_lead.name, token)
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error de integridad, intente de nuevo",
        )

    return nuevo_lead


def obtener_todos_los_leads(
    db: Session,
) -> Sequence[Lead]:
    return db.exec(select(Lead)).all()


def obtener_leads_por_fecha(
    db: Session,
    init_date: datetime,
    last_date: datetime,
) -> Sequence[Lead]:

    if init_date > last_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha de inicio no puede ser posterior a la fecha de fin",
        )

    sentencia = select(Lead).where(
        Lead.create_at.between(asegurar_utc(init_date), asegurar_utc(last_date))
    )

    return db.exec(sentencia).all()


def obtener_leads_por_email(
    db: Session,
    email: EmailStr,
) -> Lead | None:
    sentencia = select(Lead).where(Lead.email == email)

    return db.exec(sentencia).first()


def asegurar_utc(
    dt: datetime,
) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)
