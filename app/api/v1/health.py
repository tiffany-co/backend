from fastapi import APIRouter, status
from app.schema.health import HealthCheckResponse

router = APIRouter()

@router.get(
    "/",
    tags=["Health Check"],
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Perform a Health Check",
    description="Checks if the application is up and running. Returns a status message.",
    responses={
        200: {
            "description": "Application is healthy and operational.",
            "content": {
                "application/json": {
                    "examples": {
                        "Success": {
                            "summary": "Successful Response",
                            "value": {"status": "ok"}
                        }
                    }
                }
            },
        }
    },
)
@router.options(
    "/",
    tags=["Health Check"],
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Perform a Health Check (OPTIONS)",
    include_in_schema=False, # Hide the OPTIONS route from the main docs for clarity
)
def health_check() -> HealthCheckResponse:
    """
    Health check endpoint.

    Returns the status of the application. Supports GET and OPTIONS for various health checkers.
    """
    return HealthCheckResponse(status="ok")

