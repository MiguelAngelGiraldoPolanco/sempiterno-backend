from typing import Generator

from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import User
from app.services.user_service import obtener_usuario_por_email

# El motor: "check_same_thread" es necesario solo para SQLite
engine = create_engine(settings.DATABASE_URL, echo=True)


# creamos un usuario para pruebas en sqlite
def create_user():
    with Session(engine) as session:
        admin = obtener_usuario_por_email(session, settings.ADMIN_EMAIL)

        if admin:
            return

        admin = User(
            email=settings.ADMIN_EMAIL,
            password_hash=get_password_hash(settings.ADMIN_PASSWORD),
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
