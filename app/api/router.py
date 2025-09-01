from fastapi import APIRouter
from app.api.v1 import auth, users, contacts, saved_bank_accounts, items, health
from app.core.config import settings

# --- Main API Router ---
# This router includes all the version 1 routers.
# It's the single entry point for all API routes that will be included in the main app.
api_router = APIRouter()

# Include health check router at the root of the API
api_router.include_router(health.router, prefix="", tags=["Health Check"])

# Include v1 authentication router
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Include all other v1 resource routers
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(contacts.router, prefix="/contacts", tags=["Contacts"])
api_router.include_router(
    saved_bank_accounts.router,
    prefix="/bank-accounts",
    tags=["Saved Bank Accounts"],
)
api_router.include_router(items.router, prefix="/items", tags=["Items"])
