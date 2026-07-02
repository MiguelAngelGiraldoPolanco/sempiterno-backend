from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db import database
from app.schemas import email_verify
from app.services import email_verify_service

router = APIRouter(prefix="/email_verify", tags=["Email Verification"])


@router.get("/verify", response_model=email_verify.VerificationResponse)
def verify_email(
    token: str,
    db: Session = Depends(database.get_session),
):

    return email_verify_service.verify_email(token, db)
