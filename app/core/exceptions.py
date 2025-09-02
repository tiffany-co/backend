from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.logging_config import logger

class AppException(Exception):
    """
    Custom exception class for the application.
    Used for raising exceptions related to business logic.
    """
    def __init__(self, detail: str, status_code: int):
        self.detail = detail
        self.status_code = status_code

async def app_exception_handler(request: Request, exc: AppException):
    """Handles custom application exceptions, logging and returning a clean JSON response."""
    logger.error(f"AppException handled: {exc.detail} (Status Code: {exc.status_code}) for request {request.method} {request.url}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handles Pydantic validation errors, logging and returning a clean JSON response."""
    logger.error(f"Validation error for request {request.method} {request.url}: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )

def add_exception_handlers(app: FastAPI) -> None:
    """
    Adds custom exception handlers to the FastAPI application instance.
    """
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)

