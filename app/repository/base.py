from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.models.base import BaseModel as BaseSQLModel # Import our abstract base model

# Define custom types for SQLAlchemy model and Pydantic schemas
ModelType = TypeVar("ModelType", bound=BaseSQLModel) # Use our BaseModel as the bound
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    A generic base class for data repositories.
    Provides standard CRUD (Create, Read, Update, Delete) operations.

    This class is designed to be inherited by specific repository classes
    (e.g., UserRepository) that are tied to a particular SQLAlchemy model.
    """

    def __init__(self, model: Type[ModelType]):
        """
        Initializes the repository with the SQLAlchemy model it will manage.

        :param model: The SQLAlchemy model class.
        """
        self.model = model

    def get(self, db: Session, id: Union[UUID, str]) -> Optional[ModelType]:
        """
        Retrieves a single record by its ID.

        :param db: The database session.
        :param id: The ID of the record to retrieve.
        :return: The model instance if found, otherwise None.
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        Retrieves multiple records with optional pagination.

        :param db: The database session.
        :param skip: The number of records to skip.
        :param limit: The maximum number of records to return.
        :return: A list of model instances.
        """
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Creates a new record in the database.

        :param db: The database session.
        :param obj_in: A Pydantic schema with the data for the new record.
        :return: The newly created model instance.
        """
        # Convert Pydantic schema to a dictionary
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)  # Create a model instance
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
        """
        Updates an existing record in the database.

        :param db: The database session.
        :param db_obj: The existing model instance to update.
        :param obj_in: A Pydantic schema or a dictionary with the new data.
        :return: The updated model instance.
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            # Use exclude_unset=True to only include fields that were provided
            update_data = obj_in.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
            
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: UUID) -> Optional[ModelType]:
        """
        Deletes a record from the database by its ID.

        :param db: The database session.
        :param id: The ID of the record to delete.
        :return: The deleted model instance.
        """
        obj = db.query(self.model).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj
