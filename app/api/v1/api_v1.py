from app.api.v1.endpoints import client, ticket, user
from fastapi import APIRouter

api_router = APIRouter()

# Aquí va cada módulo de la v1
api_router.include_router(ticket.router)

api_router.include_router(client.router)

api_router.include_router(user.router)
