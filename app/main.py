from fastapi import FastAPI, status
from app.core.config import settings
from app.api.v1 import auth, users, contacts

# Create the FastAPI application instance.
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# A flexible root endpoint for health checks that accepts both GET and OPTIONS.
@app.api_route(
    "/",
    methods=["GET", "OPTIONS"],
    status_code=status.HTTP_200_OK,
    tags=["Health Check"]
)
def root():
    """
    Root endpoint for health checks.
    Responds to both GET and OPTIONS methods, useful for simple uptime checks
    and pre-flight requests from web clients.
    """
    return {"status": "ok", "message": f"Welcome to {settings.PROJECT_NAME}"}

# --- Include API Routers ---
# Add the authentication and user routers to the main application.
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["Users"])
app.include_router(contacts.router, prefix=f"{settings.API_V1_STR}/contacts", tags=["Contacts"])
