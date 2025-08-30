# app/main.py

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api.router import api_router
from app.core.config import settings
from app.core.exceptions import (
    AppException,
    app_exception_handler,
    validation_exception_handler,
)
from app.logging_config import setup_logging

# Apply logging configuration at startup
setup_logging()

# --- FastAPI App Initialization ---
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"/{settings.API_V1_STR}/openapi.json"
)

# --- Register Exception Handlers ---
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# --- Include Main API Router ---
# All routes are now managed in the api_router
app.include_router(api_router, prefix=settings.API_V1_STR)

