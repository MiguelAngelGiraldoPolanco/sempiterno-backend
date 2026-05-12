from datetime import datetime

from pydantic import BaseModel, EmailStr


# 1. El objeto que representa cada producto en el JSON
class ClientBase(BaseModel):
    email: EmailStr


class ClientCreate(ClientBase):
    pass


class ClientRead(ClientBase):
    id: int
    create_at: datetime

    class Config:
        # Esto es vital para que Pydantic pueda leer
        # los datos desde SQLModel/Base de datos
        from_attributes = True
