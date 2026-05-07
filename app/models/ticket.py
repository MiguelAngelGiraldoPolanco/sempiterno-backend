from datetime import datetime
from typing import Any, List, Optional

from sqlmodel import JSON, Column, Field, SQLModel


class Ticket(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customerName: str
    # Cambiamos List[dict] por List[Any] o simplemente Any para el tipo de Python
    # y nos aseguramos de que Pydantic permita modelos anidados
    products: List[Any] = Field(default=[], sa_column=Column(JSON))
    date: datetime = Field(default_factory=datetime.now)
    total: float
    iva: float = 0.0

    # Esto es CRUCIAL en Pydantic v2 / SQLModel moderno
    class Config:
        arbitrary_types_allowed = True
