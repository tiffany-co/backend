from sqlalchemy.orm import Session
from typing import List, Optional, Union

from app.repository.base import BaseRepository
from app.models.contact import Contact
from app.schema.contact import ContactCreate, ContactUpdate
from app.models.enums.contact import ContactType
import uuid

class ContactRepository(BaseRepository[Contact, Union[ContactCreate, dict], ContactUpdate]):
    """
    Repository for contact-related database operations.
    """
    def get_by_phone_number(self, db: Session, *, phone_number: str) -> Contact | None:
        """Get a contact by their phone number."""
        return db.query(self.model).filter(self.model.phone_number == phone_number).first()

    def get_by_national_number(self, db: Session, *, national_number: str) -> Contact | None:
        """Get a contact by their national number."""
        return db.query(self.model).filter(self.model.national_number == national_number).first()

    def search(
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
        """
        Searches for contacts based on a combination of criteria.
        """
        query = db.query(self.model)
        
        if first_name:
            query = query.filter(self.model.first_name.ilike(f"%{first_name}%"))
        if last_name:
            query = query.filter(self.model.last_name.ilike(f"%{last_name}%"))
        if national_number:
            query = query.filter(self.model.national_number == national_number)
        if phone_number:
            query = query.filter(self.model.phone_number == phone_number)
        if type:
            query = query.filter(self.model.type == type)
        if national_number_last4:
            query = query.filter(self.model.national_number.like(f"%{national_number_last4}"))
        if creator_user_id:
            query = query.filter(self.model.creator_user_id == creator_user_id)
            
        return query.offset(skip).limit(limit).all()

contact_repo = ContactRepository(Contact)

