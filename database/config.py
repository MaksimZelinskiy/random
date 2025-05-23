from pydantic_settings import BaseSettings

class DatabaseSettings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "trafficmedia"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"

    class Config:
        env_file = ".env"

db_settings = DatabaseSettings()

POSTGRES_URL = (
    f"postgresql+asyncpg://{db_settings.DB_USER}:{db_settings.DB_PASSWORD}@"
    f"{db_settings.DB_HOST}:{db_settings.DB_PORT}/{db_settings.DB_NAME}"
) 