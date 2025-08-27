# app/services/contact.py

from sqlalchemy.orm import Session
import uuid
from app.models.contact import Contact
from app.repository.contact import contact_repo
from app.schema.contact import ContactCreate

class ContactService:
    """
    Service layer for contact-related business logic.
    """

    def create_contact(
        self, db: Session, *, contact_in: ContactCreate, creator_id: uuid.UUID
    ) -> Contact:
        """
        Handles the business logic for creating a new contact.

        - Associates the contact with the user who created it.
        - Calls the repository to save the contact.

        :param db: The database session.
        :param contact_in: The Pydantic schema with the new contact's data.
        :param creator_id: The UUID of the user creating the contact.
        :return: The newly created Contact model instance.
        """
        # Convert the Pydantic schema to a dictionary
        contact_data = contact_in.model_dump()
        # Add the creator's user ID to the data
        contact_data['creator_user_id'] = creator_id

        # Create the contact using the repository
        db_contact = contact_repo.create(db, obj_in=contact_data)
        return db_contact

# Create a single, importable instance of the ContactService.
contact_service = ContactService()
