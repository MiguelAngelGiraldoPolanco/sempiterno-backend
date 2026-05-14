from pydantic import BaseModel


class VerificationResponse(BaseModel):
    success: bool
    message: str
    coupon: str
