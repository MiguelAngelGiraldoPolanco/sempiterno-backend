from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, List

if TYPE_CHECKING:
    from app.models.coupon import Coupon
    from app.models.lead import Lead

from sqlmodel import JSON, Column, Field, Relationship, SQLModel


class Ticket(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customerName: str = Field(index=True)
    # Cambiamos List[dict] por List[Any] o simplemente Any para el tipo de Python
    # y nos aseguramos de que Pydantic permita modelos anidados
    products: List[Any] = Field(default=[], sa_column=Column(JSON))
    create_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    total: float
    iva: float = 0.0

    lead_id: int | None = Field(default=None, foreign_key="lead.id")
    coupon_id: int | None = Field(default=None, foreign_key="coupon.id")

    coupon: "Coupon" | None = Relationship(back_populates="tickets")

    lead: "Lead" | None = Relationship(back_populates="tickets")

    # Esto es CRUCIAL en Pydantic v2 / SQLModel moderno
    model_config = {"arbitrary_types_allowed": True, "from_attributes": True}
