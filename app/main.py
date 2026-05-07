from fastapi import FastAPI
from sqlmodel import SQLModel

from app.api.v1.api_v1 import api_router as api_v1_router
from app.db.database import engine


# Esta función se ejecuta al arrancar la app
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI(title="Sempiterno API")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# Unimos la versión 1 a la aplicación principal
app.include_router(api_v1_router, prefix="/api/v1")
