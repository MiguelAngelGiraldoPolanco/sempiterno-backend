from datetime import datetime, timezone
from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True, index=True)
    password_hash: str
    is_admin: bool = Field(default=False)
    # CORRECCIÓN AQUÍ: Usamos una función que devuelva el tiempo actual
    create_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    update_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# Esto es crucial para Pydantic v2 / SQLModel moderno
model_config = {"arbitrary_types_allowed": True, "from_attributes": True}
