from fastapi import APIRouter, Depends, status, Query, Response
from sqlalchemy.orm import Session
import uuid
from typing import List, Optional

from app.api import deps
from app.models.user import User, UserRole
from app.models.enums.contact import ContactType
from app.models.enums.permission import PermissionName
from app.schema.contact import ContactCreate, ContactPublic, ContactUpdate
from app.schema.error import ErrorDetail
from app.services.contact import contact_service


router = APIRouter()

@router.post(
    "/",
    response_model=ContactPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new contact",
    description="Allows an authenticated user to create a new contact.",
    responses={
        201: {"description": "Contact created successfully."},
        401: {"description": "Unauthorized.", "model": ErrorDetail},
        409: {"description": "Conflict. A contact with the same unique information already exists.", "model": ErrorDetail},
    }
)
def create_contact(
    contact_in: ContactCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """Endpoint to create a new contact, assigned to the current user."""
    return contact_service.create_contact(db=db, contact_in=contact_in, current_user=current_user)


@router.get(
    "/",
    response_model=List[ContactPublic],
    summary="Get all contacts",
    description="Allows an authenticated user to retrieve a paginated list of all contacts.",
    responses={
        200: {"description": "A list of contacts."},
        401: {"description": "Unauthorized.", "model": ErrorDetail, "content": {"application/json": {"example": {"detail": "Not authenticated"}}}},
    }
)
def read_all_contacts(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = Query(0, ge=0, description="Number of records to skip."),
    limit: int = Query(100, ge=1, le=200, description="Number of records to return."),
):
    """Endpoint to retrieve all contacts."""
    return contact_service.get_all_contacts(db, skip=skip, limit=limit)


@router.get(
    "/search",
    response_model=List[ContactPublic],
    summary="Search for contacts",
    description="Allows an authenticated user to search for contacts using various criteria.",
    responses={
        200: {"description": "A list of contacts matching the search criteria."},
        401: {"description": "Unauthorized.", "model": ErrorDetail},
    }
)
def search_contacts(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    first_name: Optional[str] = Query(None, description="Search by first name (case-insensitive, partial match)."),
    last_name: Optional[str] = Query(None, description="Search by last name (case-insensitive, partial match)."),
    national_number: Optional[str] = Query(None, description="Search by exact national number."),
    type: Optional[ContactType] = Query(None, description="Filter by contact type."),
    national_number_last4: Optional[str] = Query(None, min_length=4, max_length=4, description="Search by the last 4 digits of the national number."),
    creator_user_id: Optional[uuid.UUID] = Query(None, description="Filter by the ID of the user who created the contact."),
    skip: int = Query(0, ge=0, description="Number of records to skip."),
    limit: int = Query(100, ge=1, le=200, description="Number of records to return."),
):
    """Endpoint for searching and filtering contacts."""
    return contact_service.search_contacts(
        db,
        first_name=first_name,
        last_name=last_name,
        national_number=national_number,
        type=type,
        national_number_last4=national_number_last4,
        creator_user_id=creator_user_id,
        skip=skip,
        limit=limit
    )


@router.get(
    "/{contact_id}",
    response_model=ContactPublic,
    summary="Get a contact by ID",
    description="Allows an authenticated user to fetch a single contact by their unique ID.",
    responses={
        200: {"description": "Successful Response."},
        401: {"description": "Unauthorized.", "model": ErrorDetail},
        404: {"description": "Contact not found.", "model": ErrorDetail},
    }
)
def read_contact_by_id(
    contact_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """Endpoint to get a specific contact by its ID."""
    return contact_service.get_contact_by_id(db, contact_id=contact_id)


@router.put(
    "/{contact_id}",
    response_model=ContactPublic,
    summary="Update a contact",
    description="""
    Allows a user to update a contact.
    - A user can always update a contact they created themselves.
    - A user with the `contact_update_all` permission can update any contact.
    - An admin can update any contact.
    """,
    responses={
        200: {"description": "Contact updated successfully."},
        401: {"description": "Unauthorized.", "model": ErrorDetail},
        403: {"description": "Forbidden. User does not have permission to update this contact.", "model": ErrorDetail},
        404: {"description": "Contact not found.", "model": ErrorDetail},
        409: {"description": "Conflict. A contact with the same unique information already exists.", "model": ErrorDetail},
    }
)
def update_contact(
    contact_id: uuid.UUID,
    contact_in: ContactUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """Endpoint to update a contact's details with permission checks."""
    return contact_service.update_contact(db=db, contact_id=contact_id, contact_in=contact_in, current_user=current_user)


@router.delete(
    "/{contact_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a contact (Admin Only)",
    description="Allows an administrator to delete a contact from the system.",
    responses={
        204: {"description": "Contact deleted successfully. No content is returned."},
        401: {"description": "Unauthorized.", "model": ErrorDetail, "content": {"application/json": {"example": {"detail": "Not authenticated"}}}},
        403: {"description": "Forbidden. User is not an admin.", "model": ErrorDetail, "content": {"application/json": {"example": {"detail": "You do not have permission to access this resource"}}}},
        404: {"description": "Contact not found.", "model": ErrorDetail, "content": {"application/json": {"example": {"detail": "Contact with ID a1b2c3d4-e5f6-7890-1234-567890abcdef not found."}}}},
    }
)
def delete_contact(
    contact_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.require_role([UserRole.ADMIN])),
):
    """Admin-only endpoint to delete a contact."""
    contact_service.delete_contact(db, contact_id=contact_id, current_user=current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
