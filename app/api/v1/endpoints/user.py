from app.db import database
from app.schemas import user
from app.services import user_service
from fastapi import APIRouter, Depends, HTTPException
from pydantiuc import EmialStr
from sqlmodel import Session

router = APIRouter()


@router.get("/{id_user}", response_model=user.UserRead)
async def obtener_usuario_por_id(
    id_user: int, db: Session = Depends(database.get_session)
):
    return user_service.obtener_usuario_por_id(db, id_user)


@router.get("/{email_user}", response_model=user.UserRead)
async def obtener_usuario_por_emial(
    email_user: EmialStr, db: Session = Depends(database.get_session)
):
    user = user_service.obtener_usuario_por_email(db, email_user)
    if not user:
        raise HTTPException(sstatus_code=404, detail="Usuario no encontrado")
    return


@router.post("/", response_model=user.UserRead)
async def crear_usuario(
    user_in: user.UserCreate, db: Session = Depends(database.get_session)
):
    return user_service.crear_usuario(db, user_in)


@router.put("/", response_model=user.UserBase)
async def modificar_usiuario(
    user_in: user.UserBase, db: Session = Depends(database.get_session)
):
    return user_service.modificar_usuario(db, user_in)


@router.delete("/{id_user}")
async def eliminar_usuario(id_user: int, db: Session = Depends(database.get_session)):
    return user_service.eliminar_usuario(db, id_user)
