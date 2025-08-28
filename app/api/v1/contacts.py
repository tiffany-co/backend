from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from app.api import deps
from app.models.user import User, UserRole
from app.schema.contact import ContactCreate, ContactPublic, ContactUpdate
from app.services.contact import contact_service
from app.repository.contact import contact_repo

router = APIRouter()

# Dependency for requiring admin role
require_admin = deps.require_role([UserRole.ADMIN])

@router.post("/", response_model=ContactPublic, status_code=status.HTTP_201_CREATED)
def create_contact(
    *,
    db: Session = Depends(deps.get_db),
    contact_in: ContactCreate,
    current_user: User = Depends(deps.get_current_active_user),
):
    """
    Create a new contact.
    The new contact will be automatically associated with the current user.
    """
    contact = contact_service.create_contact(
        db=db, contact_in=contact_in, creator_id=current_user.id
    )
    return contact

@router.get(
    "/search", 
    response_model=List[ContactPublic],
    dependencies=[Depends(require_admin)] # Secure this endpoint
)
def search_contacts(
    db: Session = Depends(deps.get_db),
    first_name: Optional[str] = Query(None, description="Search by first name (case-insensitive, partial match)"),
    last_name: Optional[str] = Query(None, description="Search by last name (case-insensitive, partial match)"),
    phone_number: Optional[str] = Query(None, description="Search by phone number (partial match)"),
    national_number: Optional[str] = Query(None, description="Search by the last four digits of the national number"),
    skip: int = 0,
    limit: int = 100,
):
    """
    Search for contacts. (Admin only)
    """
    contacts = contact_repo.search(
        db,
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        national_number=national_number,
        skip=skip,
        limit=limit
    )
    return contacts


@router.get("/me", response_model=List[ContactPublic])
def read_contacts_me(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
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

@router.get(
    "/", 
    response_model=List[ContactPublic],
    dependencies=[Depends(require_admin)] # Secure this endpoint
)
def read_all_contacts(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve all contacts in the system. (Admin only)
    """
    return contact_repo.get_multi(db, skip=skip, limit=limit)


@router.get("/{contact_id}", response_model=ContactPublic)
def read_contact_by_id(
    contact_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """
    Retrieve a specific contact by its ID.
    An admin can retrieve any contact. A regular user can only retrieve their own.
    """
    contact = contact_repo.get(db, id=contact_id)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    if contact.creator_user_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
    return contact

@router.put("/{contact_id}", response_model=ContactPublic)
def update_contact(
    contact_id: uuid.UUID,
    contact_in: ContactUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """
    Update a contact.
    An admin can update any contact. A regular user can only update their own.
    """
    contact = contact_repo.get(db, id=contact_id)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    if contact.creator_user_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this resource",
        )
    
    updated_contact = contact_service.update_contact(db=db, db_obj=contact, obj_in=contact_in)
    return updated_contact
