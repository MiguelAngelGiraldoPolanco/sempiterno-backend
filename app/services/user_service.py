from datetime import datetime, timezone

from app.core import security
from app.models.user import User
from app.schemas.user import UserCreate
from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlmodel import Session, select


def create_user(
    db: Session,
    user_data: UserCreate,
) -> User:
    # if para asegurar que el cliente no exista en la base de datos
    if obtener_usuario_por_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El usuaerio ya existe",
        )

    datos_usuario = user_data.model_dump()

    password_plana = datos_usuario.pop("password_hash")

    password_hasheada = security.get_password_hash(password_plana)

    nuevo_user = User(**datos_usuario, password_hash=password_hasheada)

    db.add(nuevo_user)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error de integridad, intente de nuevo",
        )

    db.refresh(nuevo_user)

    return nuevo_user


def user_login(
    db: Session,
    user_data: UserCreate,
) -> dict:
    user = obtener_usuario_por_email(db, user_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )

    if not security.verify_password(user_data.password_hash, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )
    token = security.create_access_token(subject=user.id)

    # 5. Respondemos con el formato estándar
    return {
        "access_token": token,
        "token_type": "bearer",
    }


def obtener_usuario_por_id(
    db: Session,
    user_id: int,
) -> User | None:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario no existe",
        )
    return user


def obtener_usuario_por_email(
    db: Session,
    user_email: EmailStr,
) -> User | None:
    sentencia = select(User).where(User.email == user_email)

    return db.exec(sentencia).first()


def modificar_usuario(
    db: Session,
    user_id: int,
    user_data: dict,
) -> User:
    user_db = db.get(User, user_id)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    datos_nuevos = (
        user_data
        if isinstance(user_data, dict)
        else user_data.model_dump(exclude_unset=True)
    )

    for llave, valor in datos_nuevos.items():
        setattr(user_db, llave, valor)

    user_db.update_at = datetime.now(timezone.utc)

    db.add(user_db)
    try:
        db.commit()
        db.refresh(user_db)
        return user_db
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al actualizar: el email ya está en uso o hubo un error interno",
        )


def eliminar_usuario(
    db: Session,
    user_id: int,
) -> dict:
    user_db = db.get(User, user_id)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    db.delete(user_db)
    db.commit()
    return {"ok": True, "message": "Usuario eliminado"}
