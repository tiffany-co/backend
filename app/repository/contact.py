from sqlalchemy.orm import Session
from typing import List
import uuid
from app.models.contact import Contact
from app.schema.contact import ContactCreate, ContactUpdate
from .base import BaseRepository

class ContactRepository(BaseRepository[Contact, ContactCreate, ContactUpdate]):
    """
    Repository for Contact model operations.
    Inherits from BaseRepository and can be extended with contact-specific methods.
    """

    def get_multi_by_creator(
        self, db: Session, *, creator_user_id: uuid.UUID, skip: int = 0, limit: int = 100
    ) -> List[Contact]:
        """
        Retrieves multiple contacts created by a specific user.

        :param db: The database session.
        :param creator_user_id: The ID of the user who created the contacts.
        :param skip: The number of records to skip.
        :param limit: The maximum number of records to return.
        :return: A list of Contact instances.
        """
        return (
            db.query(self.model)
            .filter(Contact.creator_user_id == creator_user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

# Create a single, importable instance of the ContactRepository.
contact_repo = ContactRepository(Contact)
