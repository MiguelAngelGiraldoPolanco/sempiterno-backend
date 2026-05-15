from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api_v1 import api_router as api_v1_router
from app.core.config import settings
from app.db.database import create_db_and_tables, create_user

# Esta función se ejecuta al arrancar la app
app = FastAPI(title=settings.PROJECT_NAME)


origins = [
    "http://localhost.3000.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    create_user()


# Unimos la versión 1 a la aplicación principal
app.include_router(api_v1_router, prefix="/api/v1")
