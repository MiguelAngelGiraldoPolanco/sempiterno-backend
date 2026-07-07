from datetime import datetime, timezone

from pydantic import EmailStr
from sqlmodel import Field, SQLModel, String


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True, index=True)
    password_hash: str = Field(sa_type=String(255))
    is_admin: bool = Field(default=False)
    # CORRECCIÓN AQUÍ: Usamos una función que devuelva el tiempo actual
    create_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    update_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = Field(default=True)
    # Esto es crucial para Pydantic v2 / SQLModel moderno
    model_config = {"arbitrary_types_allowed": True, "from_attributes": True}
