from datetime import datetime, timezone
from typing import Optional

from app.models.user import User
from app.schemas.user import UserCreate
from fastapi import HTTPException
from pydantic import EmailStr
from sqlmodel import Session, select


def create_user(db: Session, user_data: UserCreate) -> Optional[User]:
    # if para asegurar que el cliente no exista en la base de datos
    if obtener_usuario_por_email(db, user_data.email):
        raise HTTPException(status_code=400, detail="EL usuario ya existe")
    nuevo_user = User(**user_data.model_dump())
    db.add(nuevo_user)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Error de integridad, intente de nuevo"
        )

    db.refresh(nuevo_user)

    return nuevo_user


def obtener_usuario_por_id(db: Session, user_id: int) -> Optional[User]:
    return db.get(User, user_id)


def obtener_usuario_por_email(db: Session, user_email: EmailStr) -> Optional[User]:
    sentencia = select(User).where(User.email == user_email)

    return db.exec(sentencia).first()


def modificar_usuario(db: Session, user_id: int, user_data: User) -> User:
    user_db = db.get(User, user_id)
    if not user_db:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado",
        )

    user_db.email = user_data.email
    user_db.password_hash = user_data.password_hash
    user_db.update_at = datetime.now(timezone.utc)

    db.add(user_db)
    try:
        db.commit()
        db.refresh(user_db)
        return user_db
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="No se pudo actualizar: el email ya está en uso o hubo un error interno",
        )


def eliminar_usuario(db: Session, user_id: int) -> dict:
    user_db = db.get(User, user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(user_db)
    db.commit()
    return {"ok": True, "message": "Usuario eliminado"}
