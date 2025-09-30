from fastapi import APIRouter
from app.api.v1 import (
    auth,
    contacts,
    saved_bank_accounts,
    health,
    permissions,
    items,
    item_financial_profiles,
    inventory,
    users_me,
    users_admin,
    audit_logs,
    transactions,
    transaction_items,
    account_ledgers,
    payments,
    backup
)

# --- Main API Router ---
# This router includes all the version 1 routers, organizing them by domain.
api_router = APIRouter()

# --- Core & System Endpoints ---
api_router.include_router(health.router, prefix="", tags=["Health Check"])
api_router.include_router(audit_logs.router, prefix="/audit-logs", tags=["Audit Logs"])
api_router.include_router(backup.router, prefix="/backup", tags=["Database Backup"])

# --- User & Authentication Endpoints ---
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users_me.router, prefix="/users", tags=["Users - Me"])
api_router.include_router(users_admin.router, prefix="/users", tags=["Users - Admin"])
api_router.include_router(permissions.router, prefix="/permissions", tags=["Permissions"])

# --- Core Business Entities ---
api_router.include_router(contacts.router, prefix="/contacts", tags=["Contacts"])
api_router.include_router(items.router, prefix="/items", tags=["Items"])
api_router.include_router(
    item_financial_profiles.router, 
    prefix="/financial-profiles", 
    tags=["Item Financial Profiles"]
)
api_router.include_router(
    saved_bank_accounts.router,
    prefix="/bank-accounts",
    tags=["Saved Bank Accounts"],
)

# --- Financial & Inventory Operations ---
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
api_router.include_router(transaction_items.router, prefix="/transaction-items", tags=["Transaction Items"])
api_router.include_router(account_ledgers.router, prefix="/account-ledgers", tags=["Account Ledgers"])
api_router.include_router(payments.router, prefix="/payments", tags=["Payments"])

