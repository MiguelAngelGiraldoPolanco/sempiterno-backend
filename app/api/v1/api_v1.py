from app.api.v1.endpoints import tickets
from fastapi import APIRouter

api_router = APIRouter()

# Aquí "cuelgas" cada módulo de la v1
api_router.include_router(tickets.router, prefix="/tickets", tags=["Tickets"])
