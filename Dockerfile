FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 1. Instalamos dependencias de sistema necesarias para Pandas/Numpy en slim
# Esto es vital porque la versión 'slim' es muy ligera y a veces le faltan librerías de C
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    libcairo2 \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

# 2. Instalamos FastAPI y Uvicorn primero
RUN pip install --no-cache-dir "fastapi[all]"

RUN pip install sqlmodel

# 3. Copiamos e instalamos TU requirements.txt (Pandas, Numpy, etc.)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiamos el resto del código
COPY . .

EXPOSE 8000

# 5. Comando de PRODUCCIÓN: sin --reload, y escuchando en el puerto que asigne el host ($PORT).
#    En local, docker-compose sobreescribe este comando para reactivar --reload.
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
