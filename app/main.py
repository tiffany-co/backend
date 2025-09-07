from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.router import api_router
from app.core import exceptions
from app.logging_config import setup_logging
from app.db.session import SessionLocal
from app.services.permission import permission_service
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events.
    """
    # On startup
    print("--- Application Startup ---")
    setup_logging()
    
    # Seed permissions into the database
    db = SessionLocal()
    try:
        permission_service.seed_permissions(db)
    finally:
        db.close()
        
    yield
    # On shutdown
    print("--- Application Shutdown ---")

# Initialize the FastAPI application with the lifespan event handler and metadata
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# --- Add Exception Handlers ---
exceptions.add_exception_handlers(app)

# --- Include API Router ---
app.include_router(api_router, prefix=settings.API_V1_STR)

