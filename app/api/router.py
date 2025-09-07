from fastapi import APIRouter
from app.api.v1 import auth, contacts, saved_bank_accounts, items, health, permissions
from app.core.config import settings
from app.api.v1 import users_admin, users_me

# --- Main API Router ---
# This router includes all the version 1 routers.
# It's the single entry point for all API routes that will be included in the main app.
api_router = APIRouter()

# Include health check router at the root of the API
api_router.include_router(health.router, prefix="", tags=["Health Check"])

# Include v1 authentication router
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Include the router for the current user's own profile management
api_router.include_router(users_me.router, prefix="/users", tags=["Users - Me"])
# Include the router for admin-level user management
api_router.include_router(users_admin.router, prefix="/users", tags=["Users - Admin"])

api_router.include_router(permissions.router, prefix="/permissions", tags=["Permissions"])

api_router.include_router(contacts.router, prefix="/contacts", tags=["Contacts"])
api_router.include_router(
    saved_bank_accounts.router,
    prefix="/bank-accounts",
    tags=["Saved Bank Accounts"],
)
api_router.include_router(items.router, prefix="/items", tags=["Items"])
