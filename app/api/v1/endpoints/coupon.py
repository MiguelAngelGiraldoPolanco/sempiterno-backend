# Archivo diseñado para recibir los correos de los posibles clientes pero aun no son usuarios de la tienda solo dejan sus correos para recibir descuerstos de los lanzamientos mensuales
from datetime import datetime

from app.api.deps import get_current_admin_user
from app.db import database
from app.models.user import User
from app.schemas import coupon
from app.services import coupon_service
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

router = APIRouter(prefix="/coupons", tags=["Coupons"])


@router.get(
    "/",
    response_model=list[coupon.CouponRead],
)
def read_coupon(
    db: Session = Depends(database.get_session),
    current_admin: User = Depends(get_current_admin_user),
):
    return coupon_service.obtener_todos_los_cupones(db)


@router.get(
    "/reporte/fechas",
    response_model=list[coupon.CouponRead],
)
def reporte_mensual(
    inicio: datetime,
    fin: datetime,
    db: Session = Depends(database.get_session),
    current_admin: User = Depends(get_current_admin_user),
):
    return coupon_service.obtener_cupones_por_fecha(db, inicio, fin)


@router.get(
    "/name/{name_coupon}",
    response_model=coupon.CouponRead,
)
def read_coupon_name(
    name_coupon: str,
    db: Session = Depends(database.get_session),
    current_admin: User = Depends(get_current_admin_user),
):
    coupon_name = coupon_service.obtener_cupon_por_nombre(db, name_coupon)

    if not coupon_name:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cupon no encontrado",
        )
    return coupon_name


@router.post(
    "/",
    response_model=coupon.CouponRead,
    status_code=status.HTTP_201_CREATED,
)
def crear_coupon(
    coupon_in: coupon.CouponCreate,
    db: Session = Depends(database.get_session),
    current_admin: User = Depends(get_current_admin_user),
):
    return coupon_service.crear_cupon(db, coupon_in)
