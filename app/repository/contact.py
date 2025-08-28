from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from app.models.contact import Contact
from app.schema.contact import ContactCreate, ContactUpdate
from .base import BaseRepository

class ContactRepository(BaseRepository[Contact, ContactCreate, ContactUpdate]):
    """
    Repository for Contact model operations.
    Inherits from BaseRepository and adds contact-specific query methods.
    """

    def get_multi_by_creator(
        self, db: Session, *, creator_user_id: uuid.UUID, skip: int = 0, limit: int = 100
    ) -> List[Contact]:
        """
        Retrieves multiple contacts created by a specific user.
        """
        return (
            db.query(self.model)
            .filter(Contact.creator_user_id == creator_user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def search(
        self,
        db: Session,
        *,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone_number: Optional[str] = None,
        national_number: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Contact]:
        """
        Searches for contacts based on various optional criteria.
        Uses ILIKE for case-insensitive partial matching.
        """
        query = db.query(self.model)
        if first_name:
            query = query.filter(Contact.first_name.ilike(f"%{first_name}%"))
        if last_name:
            query = query.filter(Contact.last_name.ilike(f"%{last_name}%"))
        if phone_number:
            query = query.filter(Contact.phone_number.ilike(f"%{phone_number}%"))
        if national_number:
            query = query.filter(Contact.national_number.ilike(f"%{national_number}%"))
        
        return query.offset(skip).limit(limit).all()

# Create a single, importable instance of the ContactRepository.
contact_repo = ContactRepository(Contact)
