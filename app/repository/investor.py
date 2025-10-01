from sqlalchemy.orm import Session
from typing import List, Optional

from app.repository.base import BaseRepository
from app.models.investor import Investor, InvestorStatus
from app.models.user import User
from app.schema.investor import InvestorCreate, InvestorUpdate

class InvestorRepository(BaseRepository[Investor, InvestorCreate, InvestorUpdate]):
    """Repository for investor-related database operations."""

    def get_by_username(self, db: Session, *, username: str) -> Optional[Investor]:
        """Gets a single investor by their associated username."""
        return db.query(self.model).join(Investor.user).filter(User.username == username).first()

    def search(
        self, 
        db: Session,
        *,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        national_number: Optional[str] = None,
        phone_number: Optional[str] = None,
        username: Optional[str] = None,
        status: Optional[InvestorStatus] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Investor]:
        """Searches for investors by joining with the contact table."""
        query = db.query(self.model)
        
        # Eagerly load related contact to allow searching on its fields
        if first_name or last_name or national_number or phone_number:
            from app.models.contact import Contact
            query = query.join(Contact)
            if first_name:
                query = query.filter(Contact.first_name.ilike(f"%{first_name}%"))
            if last_name:
                query = query.filter(Contact.last_name.ilike(f"%{last_name}%"))
            if national_number:
                query = query.filter(Contact.national_number == national_number)
            if phone_number:
                query = query.filter(Contact.phone_number == phone_number)

        if status:
            query = query.filter(self.model.status == status)
            
        # Join with User for username
        if username:
            from app.models.user import User
            query = query.join(User)
            # query = query.filter(User.username.ilike(f"%{username}%"))
            query = query.filter(User.username == username)
            
        return query.offset(skip).limit(limit).all()

investor_repo = InvestorRepository(Investor)
