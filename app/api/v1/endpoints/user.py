from app.db import database
from app.schemas import user
from app.services import user_service
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr
from sqlmodel import Session

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/{id_user}",
    response_model=user.UserRead,
)
def obtener_usuario_por_id(
    id_user: int,
    db: Session = Depends(database.get_session),
):
    return user_service.obtener_usuario_por_id(db, id_user)


@router.get(
    "/email/{email_user}",
    response_model=user.UserRead,
)
def obtener_usuario_por_email(
    email_user: EmailStr,
    db: Session = Depends(database.get_session),
):
    user = user_service.obtener_usuario_por_email(
        db,
        email_user,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    return user


@router.post(
    "/",
    response_model=user.UserRead,
    status_code=status.HTTP_201_CREATED,
)
def crear_usuario(
    user_in: user.UserCreate,
    db: Session = Depends(database.get_session),
):
    return user_service.create_user(db, user_in)


@router.put(
    "/{user_id}",
    response_model=user.UserRead,
)
def modificar_usuario(
    user_in: user.UserUpdate,
    user_id: int,
    db: Session = Depends(database.get_session),
):
    return user_service.modificar_usuario(db, user_id, user_in)


@router.delete(
    "/{id_user}",
)
def eliminar_usuario(
    id_user: int,
    db: Session = Depends(database.get_session),
):
    return user_service.eliminar_usuario(db, id_user)
