# app/core/config.py

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# --- Determine the base directory ---
# This helps in reliably locating the .env file.
# The current file is at backend/app/core/config.py
# The .env file is at CaptainDock/.env
# So we need to go up three parent directories.
env_path = Path(__file__).resolve().parents[3] / ".env"


class Settings(BaseSettings):
    """
    Pydantic settings class for managing application configuration.
    It automatically reads environment variables from a .env file and validates their types.
    """
    # project informations
    PROJECT_NAME: str = 'GOLDSHOP'
    API_V1_STR: str = "/api/v1"
    
    # --- Application Environment ---
    APP_ENV: str = "docker"

    # --- PostgreSQL Configuration ---
    POSTGRES_SERVER: str
    POSTGRES_SERVER_LOCAL: str = "localhost"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432

    # --- Redis Configuration ---
    REDIS_HOST: str
    REDIS_PORT: int = 6379

    # --- FastAPI Server Configuration ---
    BACKEND_PORT: int = 8000
    DB_PORT: int = 5433  # Port for the database service

    # --- JWT Configuration ---
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # --- Computed Database URL ---
    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        """
        Dynamically builds the database connection URL based on the APP_ENV.
        - If APP_ENV is 'local', it connects to localhost.
        - Otherwise, it connects to the Docker service name ('db').
        """
        host = self.POSTGRES_SERVER
        if self.APP_ENV == "local":
            host = self.POSTGRES_SERVER_LOCAL
            
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{host}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # --- Pydantic Settings Configuration ---
    model_config = SettingsConfigDict(
        env_file=str(env_path),
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


# Create a single, globally accessible instance of the settings.
settings = Settings()

