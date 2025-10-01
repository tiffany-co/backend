import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import status

from app.core.exceptions import AppException
from app.models.user import User, UserRole
from app.models.investor import Investor, InvestorStatus
from app.models.enums.contact import ContactType
from app.repository.investor import investor_repo
from app.schema.investor import InvestorCreate, InvestorUpdate
from app.services.user import user_service
from app.services.contact import contact_service

class InvestorService:
    """Service layer for investor-related business logic."""

    def get_by_id(self, db: Session, *, investor_id: uuid.UUID) -> Investor:
        investor = investor_repo.get(db, id=investor_id)
        if not investor:
            raise AppException(status_code=status.HTTP_404_NOT_FOUND, detail="Investor not found.")
        return investor

    def create(self, db: Session, *, investor_in: InvestorCreate, current_user: User) -> Investor:
        """Orchestrates the creation of a Contact, User, and Investor profile in a single transaction."""
        contact_in = {
            "first_name": investor_in.first_name,
            "last_name": investor_in.last_name,
            "national_number": investor_in.national_number,
            "phone_number": investor_in.phone_number,
            "type": ContactType.INVESTOR
        }
        user_in = {
            "username": investor_in.username,
            "password": investor_in.password,
            "role": UserRole.INVESTOR,
            "full_name": None,
            "phone_number": None
        }
        
        # The services for contact and user already handle validation and hashing
        new_contact = contact_service.create_contact(db, contact_in=contact_in, current_user=current_user)
        new_user = user_service.create_user(db, user_in=user_in)
        
        new_investor = investor_repo.create(db, obj_in={
            "user_id": new_user.id,
            "contact_id": new_contact.id,
            "credit": 0,
            "status": InvestorStatus.ACTIVE
        })
        
        return new_investor

    def update(self, db: Session, *, investor_id: uuid.UUID, investor_in: InvestorUpdate) -> Investor:
        """Updates an investor's status and syncs the associated user's active state."""
        investor_to_update = self.get_by_id(db, investor_id=investor_id)
        
        # Sync user's active status if the investor status changes
        if investor_in.status is not None and investor_in.status != investor_to_update.status:
            user_to_update = investor_to_update.user
            if investor_in.status == InvestorStatus.CLOSED:
                user_to_update.is_active = False
            # elif investor_to_update.status == InvestorStatus.CLOSED and investor_in.status != InvestorStatus.CLOSED:
            elif investor_to_update.status == InvestorStatus.CLOSED: # we don't need second condition because it is checked first
                user_to_update.is_active = True
            db.add(user_to_update)

        return investor_repo.update(db, db_obj=investor_to_update, obj_in=investor_in)

    def delete(self, db: Session, *, investor_id: uuid.UUID) -> Investor:
        """Deletes an investor and their associated contact and user."""
        investor_to_delete = self.get_by_id(db, investor_id=investor_id)

        # Check for financial ties before deleting
        if investor_to_delete.investments or any(p.status != 'draft' for p in investor_to_delete.payments):
             raise AppException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete investor with existing investments or approved payments.")

        # Manually delete related user and contact
        user_id_to_delete = investor_to_delete.user_id
        contact_id_to_delete = investor_to_delete.contact_id
        
        # Deleting the investor will cascade and delete their investments
        investor_repo.remove(db, id=investor_id)
        
        # These must be deleted separately as they are not directly cascaded from Investor
        user_service.delete_user(db, user_id=user_id_to_delete, current_user=investor_to_delete.user) # Pass dummy user
        contact_service.delete_contact(db, contact_id=contact_id_to_delete)
        
        return investor_to_delete
    
    def search(self, db: Session, **kwargs) -> List[Investor]:
        return investor_repo.search(db, **kwargs)


investor_service = InvestorService()
