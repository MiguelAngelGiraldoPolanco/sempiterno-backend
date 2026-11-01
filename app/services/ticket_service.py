from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path

from fastapi import HTTPException, status
from jinja2 import Environment, FileSystemLoader
from sqlmodel import Session, select
from weasyprint import HTML

from app.core.config import settings
from app.models.db_model import Ticket
from app.schemas.ticket import ProductoItem, TicketCreate, TicketUpdate

BASE_DIR = Path(__file__).resolve().parents[2]
templates = Environment(loader=FileSystemLoader("app/templates"))


def crear_ticket(
    db: Session,
    ticket_data: TicketCreate,
) -> Ticket:

    nuevo_ticket = Ticket(**ticket_data.model_dump())

    nuevo_ticket.total = calcular_total_con_iva(ticket_data.products, ticket_data.iva)

    db.add(nuevo_ticket)
    try:
        db.commit()
        db.refresh(nuevo_ticket)
        return nuevo_ticket
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error de integridad, intente de nuevo",
        )


def obtener_todos_los_tickets(
    db: Session,
) -> Sequence[Ticket]:

    return db.exec(select(Ticket)).all()


def obtener_ticket_por_id(
    db: Session,
    ticket_id: int,
) -> Ticket | None:

    ticket = db.get(Ticket, ticket_id)
    if not ticket:
        # Aquí lanzamos el error 404 directamente
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El ticket no existe",
        )
    return ticket


def obtener_tickets_por_fecha(
    db: Session,
    init_date: datetime,
    last_date: datetime,
) -> Sequence[Ticket]:

    if init_date > last_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha de inicio no puede ser posterior a la fecha de fin",
        )

    sentencia = select(Ticket).where(
        Ticket.create_at.between(
            asegurar_utc(init_date),
            asegurar_utc(last_date),
        )
    )

    tickets = db.exec(sentencia).all()
    total = sum(t.total for t in tickets)
    cantidad = len(tickets)

    return {
        "total_ventas": total,
        "cantidad_tickets": cantidad,
        "tickets": tickets,
    }


def actualizar_ticket(
    db: Session,
    ticket_id: int,
    ticket_data: TicketUpdate,
) -> Ticket:

    ticket_db = db.get(Ticket, ticket_id)
    if not ticket_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket no encontrado",
        )

    datos_nuevos = (
        ticket_data
        if isinstance(ticket_data, dict)
        else ticket_data.model_dump(exclude_unset=True)
    )
    if "iva" in datos_nuevos:
        ticket_db.iva = datos_nuevos["iva"]

    # Incluimos la fecha de venta modificada si viene en la request
    if "sale_date" in datos_nuevos:
        ticket_db.sale_date = datos_nuevos["sale_date"]

    if "products" in datos_nuevos:
        ticket_db.products = datos_nuevos["products"]

        ticket_db.total = calcular_total_con_iva(ticket_data.products, ticket_db.iva)

    if "paid" in datos_nuevos:
        ticket_db.paid = datos_nuevos["paid"]

    if "delivered" in datos_nuevos:
        ticket_db.delivered = datos_nuevos["delivered"]

    if "first_payment" in datos_nuevos:
        ticket_db.first_payment = datos_nuevos["first_payment"]

    ticket_db.update_at = datetime.now(UTC)

    db.add(ticket_db)
    try:
        db.commit()
        db.refresh(ticket_db)
        return ticket_db
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error de integridad, intente de nuevo",
        )


def eliminar_ticket(
    db: Session,
    ticket_id: int,
) -> dict:

    ticket_db = db.get(Ticket, ticket_id)
    if not ticket_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket no encontrado",
        )
    db.delete(ticket_db)
    db.commit()
    return {"ok": True, "message": "Ticket eliminado"}


def asegurar_utc(
    dt: datetime,
) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


def calcular_total_con_iva(
    products: list[ProductoItem],
    iva: float,
) -> float:
    total_productos = sum(p.cantidad * p.precio_unidad for p in products)
    return total_productos * (1 + iva / 100)


def generar_factura_pdf(ticket) -> bytes:
    template = templates.get_template("factura.html")
    html = template.render(
        numero=ticket.id,
        cliente=ticket.customerName,
        fecha=ticket.create_at.strftime("%d/%m/%Y"),
        productos=ticket.products,
        total=ticket.total,
        abono=ticket.first_payment,
        saldo=ticket.total - ticket.first_payment,
        pagado=ticket.paid,
        nequi=settings.NEQUI,
        daviplata=settings.DAVIPLATA,
        cc=settings.CC,
        direction=settings.DIRECTION,
        responsible=settings.RESPONSIBLE,
        nit=settings.NIT,
    )
    return HTML(string=html, base_url=str(BASE_DIR)).write_pdf()
