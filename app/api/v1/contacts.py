from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.models.user import User
from app.models.contact import Contact
from app.schema.contact import ContactCreate, ContactPublic
from app.services.contact import contact_service
from app.repository.contact import contact_repo

router = APIRouter()

@router.post("/", response_model=ContactPublic, status_code=status.HTTP_201_CREATED)
def create_contact(
    *,
    db: Session = Depends(deps.get_db),
    contact_in: ContactCreate,
    current_user: User = Depends(deps.get_current_user),
):
    """
    Create a new contact.

    The new contact will be associated with the currently authenticated user.
    A permission check can be added here later.
    """
    contact = contact_service.create_contact(
        db=db, contact_in=contact_in, creator_id=current_user.id
    )
    return contact

@router.get("/me", response_model=List[ContactPublic])
def read_own_contacts(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve all contacts created by the current user.
    """
    contacts = contact_repo.get_multi_by_creator(
        db=db, creator_user_id=current_user.id, skip=skip, limit=limit
    )
    return contacts
