from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.logging_config import app_logger

class AppException(Exception):
    """Custom exception class for the application."""
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code

async def app_exception_handler(request: Request, exc: AppException):
    """Handles custom application exceptions, logging and returning a clean JSON response."""
    app_logger.error(f"AppException: {exc.message} (Status Code: {exc.status_code})")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handles Pydantic validation errors, logging and returning a clean JSON response."""
    app_logger.error(f"Validation error for request {request.method} {request.url}: {exc.errors()}")
    # You can customize the error response format here if needed
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )
