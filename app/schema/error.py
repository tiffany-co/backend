from pydantic import BaseModel, Field

class ErrorDetail(BaseModel):
    """
    A standard schema for returning error details in API responses.
    """
    detail: str = Field(..., example="A specific error message explaining the issue.")
