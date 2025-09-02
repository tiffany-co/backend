from fastapi import FastAPI
from app.api.router import api_router
from app.core.config import settings
from app.core import exceptions
from app.logging_config import setup_logging

# --- Setup Logging ---
# This is a crucial step. It calls our logging configuration function
# to ensure that the loggers are set up before the application starts.
setup_logging()
# ---

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# --- Add Exception Handlers ---
exceptions.add_exception_handlers(app)
# ---

# --- Include API Router ---
# This includes all the versioned API routes from the api/router.py file.
app.include_router(api_router, prefix=settings.API_V1_STR)
# ---

