# --- OpenAPI Tags Metadata ---
# This provides descriptions for each group in the Swagger docs.
tags_metadata = [
    {"name": "Health Check", "description": "Endpoints to verify application health."},
    {"name": "Database Backup", "description": "[Admin Only] Endpoints for exporting and importing database backups."},
    {"name": "Authentication", "description": "Endpoints for user login and token management."},
    
    # --- User Groups ---
    {"name": "Users - Me", "description": "Endpoints for the currently authenticated user to manage their own profile."},
    {"name": "Users - Admin", "description": "[Admin Only] Endpoints for managing all non-investor users."},
    {"name": "Permissions", "description": "Endpoints for viewing available permissions."},

    # --- Investor Groups ---
    {"name": "Investors - Admin", "description": "[Admin Only] Endpoints for creating and managing investors."},
    {"name": "Investors - Me", "description": "[Investor Only] Endpoints for investors to manage their own profile and view their data."},
    {"name": "Investments", "description": "Endpoints for viewing and managing investments."},

    # --- Core Business Groups ---
    {"name": "Contacts", "description": "Operations with contacts (customers, suppliers, etc.)."},
    {"name": "Saved Bank Accounts", "description": "Operations with saved bank accounts for reference."},
    {"name": "Items", "description": "Endpoints for managing the definitions of inventory items."},
    {"name": "Item Financial Profiles", "description": "Endpoints for managing the default financial rules for items."},
    {"name": "inventory", "description": "Endpoints for viewing inventory history and current balances."},
    
    # --- Financial Transaction Groups ---
    {"name": "Transactions", "description": "Endpoints for creating and managing sales and purchase transactions."},
    {"name": "Transaction Items", "description": "Endpoints for managing the individual line items within a transaction."},
    {"name": "Account Ledgers", "description": "Endpoints for tracking debts and credits with contacts."},
    {"name": "Payments", "description": "Endpoints for recording and managing financial payments."},

    # --- System Administration ---
    {"name": "Audit Logs", "description": "[Admin Only] Endpoints for viewing the database audit trail."},
]

