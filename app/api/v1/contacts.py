from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.api import deps
from app.models.user import User
from app.models.contact import Contact
from app.schema.contact import ContactCreate, ContactPublic, ContactUpdate
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

    This endpoint allows an authenticated user to create a new contact.
    The new contact will be automatically associated with the current user.
    """
    contact = contact_service.create_contact(
        db=db, contact_in=contact_in, creator_id=current_user.id
    )
    return contact

@router.get("/me", response_model=List[ContactPublic])
def read_contacts_me(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve all contacts created by the currently authenticated user.
    """
    contacts = contact_repo.get_multi_by_creator(
        db=db, creator_user_id=current_user.id, skip=skip, limit=limit
    )
    return contacts

@router.get("/{contact_id}", response_model=ContactPublic)
def read_contact_by_id(
    contact_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Retrieve a specific contact by its ID.

    A user can only retrieve contacts they have created.
    (This logic can be expanded later based on permissions).
    """
    contact = contact_repo.get(db, id=contact_id)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    # Basic authorization: check if the user is the creator of the contact
    if contact.creator_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
    return contact
