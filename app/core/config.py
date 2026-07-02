from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # 1. Definimos las variables que pusiste en el .env
    # Pydantic validará que existan y sean del tipo correcto
    DATABASE_URL: str
    SECRET_KEY: str
    PROJECT_NAME: str = "My App"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    RESEND_APY_KEY: str | None = None
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str
    DB_ECHO: bool = False
    CORS_ORIGINS: list[str] = []

    # 2. Configuración para leer el archivo .env
    # 'extra="ignore"' evita que la app truene si hay más variables en el .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


# Instanciamos para que el resto de la app lo use
settings = Settings()
