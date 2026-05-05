from fastapi import FastAPI

from app.api.v1.api_v1 import api_router as api_v1_router

app = FastAPI(title="Sempiterno API")

# Unimos la versión 1 a la aplicación principal
app.include_router(api_v1_router, prefix="/api/v1")
