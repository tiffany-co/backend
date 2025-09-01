from fastapi import APIRouter

router = APIRouter()

@router.get("/", tags=["Health Check"])
@router.options("/", tags=["Health Check"])
def health_check():
    """
    Health check endpoint.
    Returns the status of the application. Supports GET and OPTIONS for various health checkers.
    """
    return {"status": "ok"}
