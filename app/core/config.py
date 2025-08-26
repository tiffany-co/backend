# app/core/config.py

from pathlib import Path
from pydantic_settings import BaseSettings

# Build a robust path to the .env file.
# Path(__file__) is the path to the current file (config.py).
# .resolve() makes it an absolute path.
# .parents[2] goes up two directories (from app/core/ to the backend/ root).
# We then go up one more parent to reach CaptainDock and find the .env file.
env_path = Path(__file__).resolve().parents[2].parent / ".env"

class Settings(BaseSettings):
    """
    Settings class to manage environment variables for the application.
    pydantic-settings automatically reads variables from the environment or a .env file
    and validates their types.
    """

    # --- PostgreSQL Database Configuration ---
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int
    
    @property
    def DATABASE_URL(self) -> str:
        """
        Construct the database URL from the individual components.
        This URL is used by SQLAlchemy to connect to the database.
        """
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # --- Redis Cache Configuration ---
    REDIS_HOST: str
    REDIS_PORT: int

    # --- Backend App Configuration ---
    BACKEND_PORT: int

    # --- JWT Authentication Configuration ---
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str = "HS256"

    # --- Project Metadata ---
    PROJECT_NAME: str = "Gold Shop Management API"
    API_V1_STR: str = "/api/v1"

    class Config:
        # Specifies the path to the .env file to load the variables from.
        # We convert the Path object to a string for compatibility.
        env_file = str(env_path)
        case_sensitive = True

# Create a single, importable instance of the Settings.
settings = Settings()
