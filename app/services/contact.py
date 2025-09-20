from sqlalchemy.orm import Session
import uuid
from typing import List, Optional

from app.core.exceptions import AppException
from fastapi import status
from app.models.user import User
from app.models.contact import Contact
from app.models.enums.permission import PermissionName
from app.models.enums.contact import ContactType
from app.repository.contact import contact_repo
from app.schema.contact import ContactCreate, ContactUpdate

class ContactService:
    """
    Service layer for contact-related business logic.
    """

    def get_contact_by_id(self, db: Session, *, contact_id: uuid.UUID) -> Contact:
        """Helper method to get a contact by ID or raise a 404 exception."""
        contact = contact_repo.get(db, id=contact_id)
        if not contact:
            raise AppException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Contact with ID {contact_id} not found.",
            )
        return contact

    def get_all_contacts(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Contact]:
        """Gets a paginated list of all contacts."""
        return contact_repo.get_multi(db, skip=skip, limit=limit)

    def create_contact(self, db: Session, *, contact_in: ContactCreate, current_user: User) -> Contact:
        """Handles the business logic for creating a new contact with validation."""
        # --- Check for duplicate phone number ---
        if contact_in.phone_number and contact_repo.get_by_phone_number(db, phone_number=contact_in.phone_number):
            raise AppException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"A contact with the phone number '{contact_in.phone_number}' already exists.",
            )
        # --- Check for duplicate national number ---
        if contact_in.national_number and contact_repo.get_by_national_number(db, national_number=contact_in.national_number):
            raise AppException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"A contact with the national number '{contact_in.national_number}' already exists.",
            )

        contact_data = contact_in.model_dump()
        contact_data['creator_user_id'] = current_user.id
        
        new_contact = contact_repo.create(db, obj_in=contact_data)
        return new_contact
    
    def update_contact(self, db: Session, *, contact_id: uuid.UUID, contact_in: ContactUpdate, current_user: User) -> Contact:
        """
        Handles the business logic for updating a contact with validation and permission checks.
        """
        contact_to_update = self.get_contact_by_id(db, contact_id=contact_id)
        
        is_owner = contact_to_update.creator_user_id == current_user.id
        has_permission = any(p.name == PermissionName.CONTACT_UPDATE_ALL for p in current_user.permissions)
        
        if not is_owner and not has_permission:
             raise AppException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to update this contact.",
            )

        # --- Check for duplicates on update ---
        if contact_in.phone_number:
            existing_contact = contact_repo.get_by_phone_number(db, phone_number=contact_in.phone_number)
            if existing_contact and existing_contact.id != contact_to_update.id:
                raise AppException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Another contact with the phone number '{contact_in.phone_number}' already exists.",
                )
        if contact_in.national_number:
            existing_contact = contact_repo.get_by_national_number(db, national_number=contact_in.national_number)
            if existing_contact and existing_contact.id != contact_to_update.id:
                raise AppException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Another contact with the national number '{contact_in.national_number}' already exists.",
                )

        updated_contact = contact_repo.update(db, db_obj=contact_to_update, obj_in=contact_in)
        return updated_contact
    
    def delete_contact(self, db: Session, *, contact_id: uuid.UUID) -> Contact:
        """Handles the business logic for deleting a contact."""
        self.get_contact_by_id(db, contact_id=contact_id)
        deleted_contact = contact_repo.remove(db, id=contact_id)
        return deleted_contact

    def search_contacts(
        self,
        db: Session,
        *,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        national_number: Optional[str] = None,
        phone_number: Optional[str] = None,
        type: Optional[ContactType] = None,
        national_number_last4: Optional[str] = None,
        creator_user_id: Optional[uuid.UUID] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Contact]:
        """Searches for contacts using the repository."""
        return contact_repo.search(
            db,
            first_name=first_name,
            last_name=last_name,
            national_number=national_number,
            phone_number=phone_number,
            type=type,
            national_number_last4=national_number_last4,
            creator_user_id=creator_user_id,
            skip=skip,
            limit=limit
        )

contact_service = ContactService()

