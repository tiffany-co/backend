from pydantic import BaseModel, Field

class ErrorDetail(BaseModel):
    """
    A standard schema for returning error details in API responses.
    """
    detail: str = Field(..., json_schema_extra={"example": "A specific error message explaining the issue."})
