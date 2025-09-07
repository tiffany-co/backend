from pydantic import BaseModel, Field

class HealthCheckResponse(BaseModel):
    """Schema for the health check response."""
    status: str = Field(..., example="ok", description="The operational status of the application.")
