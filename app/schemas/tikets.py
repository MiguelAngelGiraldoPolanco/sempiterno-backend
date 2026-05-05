from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


# 1. Definimos qué tiene cada producto personalizado
class ProductoItem(BaseModel):
    nombre: str
    cantidad: int
    precio_unidad: float


# 2. Definimos el Ticket principal
class Ticket(BaseModel):
    id: int  # Mejor int si es un ID de base de datos
    number: str
    customerName: str
    # Esto es un array de objetos con nombre, cantidad y precio
    products: List[ProductoItem]
    date: datetime = Field(default_factory=datetime.now)
    total: float
    iva: float
