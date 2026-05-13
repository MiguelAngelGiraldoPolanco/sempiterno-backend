from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


# 1. El objeto que representa cada producto en el JSON
class LeadBase(BaseModel):
    email: EmailStr
    name: str
    marketing_consent: Optional[bool] = False


class LeadCreate(LeadBase):
    pass


class LeadVerify(BaseModel):
    token: str


class LeadRead(LeadBase):
    id: int
    create_at: datetime
    marketing_consent: bool
    is_verify: bool

    model_config = ConfigDict(from_attributes=True)
