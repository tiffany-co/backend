# app/main.py

from fastapi import FastAPI, status
from app.core.config import settings

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

# --- API Routers will be included below ---
# Example:
# from app.api.v1 import users, auth
# app.include_router(users.router, prefix=settings.API_V1_STR, tags=["Users"])
# app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["Authentication"])
