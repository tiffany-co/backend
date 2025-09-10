from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uuid

from app.db.base import Base
from app.models.base import BaseModel as AbstractBaseModel

# Define custom types for SQLAlchemy model, Pydantic create schema, and Pydantic update schema
ModelType = TypeVar("ModelType", bound=AbstractBaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    A generic base class for repositories that provides default CRUD operations.
    """
    def __init__(self, model: Type[ModelType]):
        """
        Initializes the repository with the SQLAlchemy model.
        """
        self.model = model

    def get(self, db: Session, id: uuid.UUID) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(
        self, db: Session, *, obj_in: Union[CreateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        Creates a new record in the database.
        Accepts either a Pydantic schema or a dictionary.
        This allows the service layer to handle logic (like password hashing)
        and pass a clean dictionary to the repository.
        """
        if isinstance(obj_in, dict):
            obj_in_data = obj_in
        else:
            obj_in_data = obj_in.model_dump()
            
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = db_obj.__dict__
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: uuid.UUID) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

