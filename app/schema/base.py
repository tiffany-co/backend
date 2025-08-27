from pydantic import BaseModel as PydanticBaseModel
from datetime import datetime
import uuid

class BaseModel(PydanticBaseModel):
    """
    A base Pydantic model that includes common configuration.
    All other schemas will inherit from this model.
    """
    class Config:
        """
        Pydantic model configuration.
        - from_attributes = True: Allows the model to be created from ORM objects
          (e.g., SQLAlchemy models). This is key for converting database objects
          into API response schemas.
        """
        from_attributes = True

class BaseSchema(BaseModel):
    """
    A base schema that includes fields common to most database models.
    This helps to keep the code DRY (Don't Repeat Yourself).
    """
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
