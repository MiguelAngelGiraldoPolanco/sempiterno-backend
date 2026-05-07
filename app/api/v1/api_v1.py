from app.api.v1.endpoints import ticket
from fastapi import APIRouter

api_router = APIRouter()

# Aquí va cada módulo de la v1
api_router.include_router(ticket.router, prefix="/ticket", tags=["Ticket"])

api_router.include_router(ticket.router, prefix="/client", tags=["Client"])
