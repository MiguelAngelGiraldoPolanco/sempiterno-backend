from app.db import database
from app.schemas import coupon
from app.services import email_verify_service
from fastapi import APIRouter, Depends
from sqlmodel import Session

router = APIRouter(prefix="/verify", tags=["Verify"])


@router.get("/verify", response_model=coupon.CouponRead)
def verify_email(
    token: str,
    db: Session = Depends(database.get_session),
):

    return email_verify_service.verify_email(token, db)
