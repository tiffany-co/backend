from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.api.tags import tags_metadata
from app.core import exceptions
from app.core import audit_listener  # Ensures the listener is registered on startup
from app.logging_config import setup_logging, logger
from seeding.seeder import seed_all
from app.core.config import settings

@asynccontextmanager
async def _lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events.
    """
    # On startup
    logger.info("--- Application Startup ---")
    setup_logging()
    
    # The listener is registered via the import, but this is a good place
    # to explicitly state that auditing is being initialized.
    logger.info("SQLAlchemy audit listener initialized.")
    
    seed_all()
    yield
    
    logger.info("--- Application Shutdown ---")

# --- API Documentation Metadata ---
_api_description = """
* **[tiffany-co/CaptainDock](https://github.com/tiffany-co/CaptainDock)** This repository contains backend and frontend services and deployment settings.
* **[tiffany-co/backend](https://github.com/tiffany-co/backend)** Includes the latest backend version.
* **[endpoints](https://docs.google.com/spreadsheets/d/1JgmLVSb6FHvnqpSDtkfoFL8P_RMvBwQI29TwQoFV8to/edit?usp=sharing)** Endpoints implementation status
* **[page-design](https://docs.google.com/document/d/19ZUVgY1yffjtw79bDdDd8vaOqb1wfyPaUicCtMLqm94/edit?usp=sharing)** Frontend page design outline
* If you have any questions about here: **[rahmat.ansari.dev@gmail.com](mailto:rahmat.ansari.dev@gmail.com?subject=goldshop%20api&body=Hey,%20I%20just%20had%20a%20quick%20question%20for%20you.)**
"""

def create_app() -> FastAPI:
    """
    Creates and configures the FastAPI application instance using a factory pattern.
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        description=_api_description,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        lifespan=_lifespan,
        openapi_tags=tags_metadata,
        swagger_ui_parameters={"docExpansion": "none"},
    )

    # --- Setup Middleware ---
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )

    # --- Setup Exception Handlers ---
    exceptions.add_exception_handlers(app)

    # --- Include API Router ---
    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    return app

