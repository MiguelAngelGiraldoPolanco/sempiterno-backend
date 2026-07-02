from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.v1.api_v1 import api_router as api_v1_router
from app.core.config import settings
from app.core.limiter import limiter
from app.db.database import create_db_and_tables, create_user

# Esta función se ejecuta al arrancar la app
app = FastAPI(title=settings.PROJECT_NAME)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

origins = settings.CORS_ORIGINS


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    create_user()


# Unimos la versión 1 a la aplicación principal
app.include_router(api_v1_router, prefix="/api/v1")
