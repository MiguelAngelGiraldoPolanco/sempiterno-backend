from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=128)


class UserLogin(BaseModel):
    id: int
    access_token: str
    token_type: str


class UserRead(UserBase):
    id: int
    create_at: datetime
    update_at: datetime
    is_admin: bool = False

    model_config = ConfigDict(from_attributes=True)
