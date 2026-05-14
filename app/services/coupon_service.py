from datetime import datetime, timezone
from typing import Sequence

from app.models.db_model import Coupon
from app.schemas.coupon import CouponCreate
from fastapi import HTTPException, status
from sqlmodel import Session, select


def crear_cupon(
    db: Session,
    coupon_data: CouponCreate,
) -> Coupon:

    if obtener_cupon_por_nombre(db, coupon_data.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El cupón '{coupon_data.name}' ya existe",
        )

    datos = coupon_data.model_dump()

    if datos.get("finish_at"):
        datos["finish_at"] = asegurar_utc(datos["finish_at"])

    nuevo_cupon = Coupon(**datos)

    db.add(nuevo_cupon)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error de integridad, intente de nuevo 123",
        )

    db.refresh(nuevo_cupon)

    return nuevo_cupon


def obtener_todos_los_cupones(
    db: Session,
) -> Sequence[Coupon]:
    return db.exec(select(Coupon)).all()


def obtener_cupones_por_fecha(
    db: Session,
    init_date: datetime,
    last_date: datetime,
) -> Sequence[Coupon]:

    if init_date > last_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha de inicio no puede ser posterior a la fecha de fin",
        )

    sentencia = select(Coupon).where(
        Coupon.create_at.between(asegurar_utc(init_date), asegurar_utc(last_date))
    )

    return db.exec(sentencia).all()


def obtener_cupon_por_nombre(
    db: Session,
    name: str,
) -> Coupon | None:
    sentencia = select(Coupon).where(Coupon.name == name)

    return db.exec(sentencia).first()


def asegurar_utc(
    dt: datetime,
) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)
