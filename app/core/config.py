from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, computed_field

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # --- Project Info ---
    PROJECT_NAME: str = "Gold Shop API"
    API_V1_STR: str = "/api/v1"

    # --- Database Configuration ---
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB_PORT: int = 5432

    # --- JWT Settings ---
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # --- Pydantic Model Config ---
    # --- UPDATED: The path now correctly points to the .env file in the parent directory. ---
    # This works because all local scripts and the dev server are run from the 'backend' directory.
    model_config = SettingsConfigDict(env_file="../.env", extra="ignore")

    # --- Computed Database URL ---
    @computed_field
    @property
    def DATABASE_URL(self) -> PostgresDsn:
        return str(PostgresDsn.build(
            scheme="postgresql",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.DB_PORT,
            path=self.POSTGRES_DB,
        ))

settings = Settings()

