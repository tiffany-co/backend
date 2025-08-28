from sqlalchemy.orm import Session
import uuid
from app.models.contact import Contact
from app.repository.contact import contact_repo
from app.schema.contact import ContactCreate, ContactUpdate

class ContactService:
    """
    Service layer for contact-related business logic.
    """

    def create_contact(
        self, db: Session, *, contact_in: ContactCreate, creator_id: uuid.UUID
    ) -> Contact:
        """
        Handles the business logic for creating a new contact.
        """
        # Convert the Pydantic schema to a dictionary
        contact_data = contact_in.model_dump()
        # Add the creator's user ID to the data
        contact_data['creator_user_id'] = creator_id

        # Create the contact using the repository
        # We need to pass the data as a dictionary to the repository's create method
        db_contact = contact_repo.create(db, obj_in=ContactCreate(**contact_data))
        return db_contact

    def update_contact(
        self, db: Session, *, db_obj: Contact, obj_in: ContactUpdate
    ) -> Contact:
        """
        Handles the business logic for updating a contact.
        """
        return contact_repo.update(db, db_obj=db_obj, obj_in=obj_in)


# Create a single, importable instance of the ContactService.
contact_service = ContactService()
