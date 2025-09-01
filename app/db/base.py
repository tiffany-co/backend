# app/db/base.py
# This file is used to ensure all models are registered with SQLAlchemy's metadata.
# When a script or process starts, importing this file will trigger the import of all
# concrete models, making them available to tools like Alembic.

# Import the declarative base which all models inherit from.
from app.db.session import Base

# --- Import all concrete models here to register them with the declarative base ---
from app.models.user import User
from app.models.contact import Contact
from app.models.permission import Permission
from app.models.item import Item
from app.models.saved_bank_account import SavedBankAccount

