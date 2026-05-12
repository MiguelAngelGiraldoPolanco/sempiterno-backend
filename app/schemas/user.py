from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password_hash: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password_hash: Optional[str] = None


class UserRead(UserBase):
    id: int
    create_at: datetime
    update_at: datetime
    is_admin: bool = False

    class Config:
        from_attributes = True
