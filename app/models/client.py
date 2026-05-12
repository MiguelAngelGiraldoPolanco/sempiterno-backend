from datetime import datetime, timezone
from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class Client(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True, index=True)
    create_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# Esto es CRUCIAL en Pydantic v2 / SQLModel moderno
model_config = {"arbitrary_types_allowe": True, "from_attributes": True}
