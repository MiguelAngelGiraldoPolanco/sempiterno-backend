from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict


# 1. El objeto que representa cada producto en el JSON
class ProductoItem(BaseModel):
    nombre: str
    cantidad: int
    precio_unidad: float


# 2. Esquema base (lo que comparten creación y lectura)
# tiket base hereda de base model que seria la clase padre
class TicketBase(BaseModel):
    customerName: str
    products: List[ProductoItem]
    total: float
    iva: float = 0.0


# 3. Esquema para CREAR (Lo que el cliente envía)
# No pedimos el ID porque la base de datos lo genera solo
# tiketcreate hereda de tiketbase que seria la clase padre para conservar sus atributos
class TicketCreate(TicketBase):
    pass


# 4. Esquema para LEER (Lo que tu API devuelve)
# Aquí sí incluimos el ID y la fecha que generó la DB
class TicketRead(TicketBase):
    id: int
    create_at: datetime
    paid: bool
    model_config = ConfigDict(from_attributes=True)


class TicketUpdate(BaseModel):
    products: List[ProductoItem] | None = None
    total: float | None = None
    iva: float | None = None
    paid: bool | None = None
    model_config = ConfigDict(from_attributes=True)


class ReporteMensual(BaseModel):
    total_ventas: float
    cantidad_tickets: int
    tickets: List[TicketRead]
