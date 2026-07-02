from datetime import datetime, timezone
from typing import Any, List, Optional

from pydantic import EmailStr
from sqlmodel import JSON, Column, Field, Relationship, SQLModel


class Coupon(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    create_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    finish_at: datetime | None = Field(default=None)
    discount: float = 0.0

    tickets: list["Ticket"] = Relationship(back_populates="coupon")

    leads: list["Lead"] = Relationship(back_populates="coupon")
    # Esto es CRUCIAL en Pydantic v2 / SQLModel moderno


class Lead(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: EmailStr = Field(unique=True, index=True)
    create_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    marketing_consent: bool = False
    is_verify: bool = False
    verification_token: Optional[str] = Field(default=None)

    tickets: list["Ticket"] = Relationship(back_populates="lead")

    coupon_id: Optional[int] = Field(default=None, foreign_key="coupon.id")

    coupon: Coupon | None = Relationship(back_populates="leads")
    # Esto es CRUCIAL en Pydantic v2 / SQLModel moderno


class Ticket(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customerName: str = Field(index=True)
    products: List[Any] = Field(default=[], sa_column=Column(JSON))
    create_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    update_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    total: float
    iva: float = 0.0
    paid: bool = False

    lead_id: Optional[int] = Field(default=None, foreign_key="lead.id")
    coupon_id: Optional[int] = Field(default=None, foreign_key="coupon.id")

    coupon: Coupon | None = Relationship(back_populates="tickets")

    lead: Lead | None = Relationship(back_populates="tickets")

    # Esto es CRUCIAL en Pydantic v2 / SQLModel moderno
