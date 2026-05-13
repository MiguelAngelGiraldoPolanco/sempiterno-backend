from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.ticket import Ticket


class Coupon(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    create_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    finish_at: datetime | None = Field(default=None)
    discount: float = 0.0

    tickets: list["Ticket"] = Relationship(back_populates="coupon")

    # Esto es CRUCIAL en Pydantic v2 / SQLModel moderno
    model_config = {"arbitrary_types_allowed": True, "from_attributes": True}
