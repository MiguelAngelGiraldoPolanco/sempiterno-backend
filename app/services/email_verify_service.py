from typing import Any

from app.models.db_model import Lead
from fastapi import HTTPException, status
from sqlmodel import Session, select


def verify_email(
    token: str,
    db: Session,
) -> dict[str, Any]:
    # 1. Buscar al lead
    statement = select(Lead).where(Lead.verification_token == token)
    lead = db.exec(statement).first()

    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El enlace es inválido o el cupón ya fue entregado.",
        )

    lead.is_verify = True
    lead.verification_token = None  # Quemamos el token

    db.add(lead)

    try:
        db.commit()
        db.refresh(lead)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al confirmar la verificación",
        )

    # 3. Respuesta final
    return {
        "success": True,
        "message": f"¡Felicidades {lead.name}! Tu correo ha sido verificado.",
        "coupon": "VELASMAGIA10",
    }
