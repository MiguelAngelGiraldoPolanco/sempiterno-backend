from datetime import datetime, timezone
from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.ticket import Ticket


class Lead(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: EmailStr = Field(unique=True, index=True)
    create_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    marketing_consent: bool = False
    is_verify: bool = False
    verification_token: str | None = Field(default=None)

    tickets: list["Ticket"] = Relationship(back_populates="lead")

    # Esto es CRUCIAL en Pydantic v2 / SQLModel moderno
    model_config = {"arbitrary_types_allowed": True, "from_attributes": True}
