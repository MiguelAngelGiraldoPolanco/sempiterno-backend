from app.db import database
from app.schemas import email_verify
from app.services import email_verify_service
from fastapi import APIRouter, Depends
from sqlmodel import Session

router = APIRouter(prefix="/leads", tags=["Leads"])


@router.get("/email_verify", response_model=email_verify.VerificationResponse)
def verify_email(
    token: str,
    db: Session = Depends(database.get_session),
):

    return email_verify_service.verify_email(token, db)
