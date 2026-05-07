from datetime import datetime

from pydantic import BaseModel


# 1. El objeto que representa cada producto en el JSON
class ClientBase(BaseModel):
    emial: str


class ClientCreate(ClientBase):
    pass


class ClientRead(ClientBase):
    id: int
    date: datetime

    class Config:
        # Esto es vital para que Pydantic pueda leer
        # los datos desde SQLModel/Base de datos
        from_attributes = True
