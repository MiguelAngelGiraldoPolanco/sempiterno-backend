from typing import Generator

from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import User
from sqlmodel import Session, SQLModel, create_engine

# El motor: "check_same_thread" es necesario solo para SQLite
engine = create_engine(settings.DATABASE_URL, echo=True)


# creamos un usuario para pruebas en sqlite
def create_user():
    with Session(engine) as session:
        admin = User(
            email="admin@admin.com",
            password_hash=get_password_hash("admin123"),
            is_admin=True,
        )
        session.add(admin)
        session.commit()
        session.refresh(admin)

        print("Created admin:", admin)


# Función para crear las tablas al iniciar la app
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# La "Dependencia" que usaremos en los endpoints
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
