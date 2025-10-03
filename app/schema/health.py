from pydantic import BaseModel, Field

class HealthCheckResponse(BaseModel):
    """Schema for the health check response."""
    status: str = Field(..., json_schema_extra={"example": "ok"}, description="The operational status of the application.")
