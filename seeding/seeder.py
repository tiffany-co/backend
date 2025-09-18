import sys
from pathlib import Path

# --- Add project root to Python path ---
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))
# ---

from sqlalchemy.orm import Session
from app.repository.item import item_repo
from app.repository.permission import permission_repo
from app.repository.item_financial_profile import item_financial_profile_repo
from app.logging_config import logger
from app.db.session import SessionLocal
from seeding.data.item_data import PREDEFINED_ITEMS_WITH_PROFILES
from seeding.data.permission_data import PREDEFINED_PERMISSIONS

def seed_items(db: Session):
    """
    Ensures that all predefined items and their financial profiles exist in the database.
    Checks for items by name and profiles by transaction type to prevent duplicates.
    """
    logger.info("Checking for predefined items and profiles to seed...")
    item_count = 0
    profile_count = 0

    for data in PREDEFINED_ITEMS_WITH_PROFILES:
        item_data = data["item"]
        profile_data_list = data["profiles"]

        # Step 1: Find or create the parent Item
        item = item_repo.get_by_name(db, name=item_data.name)
        if not item:
            item = item_repo.create(db, obj_in=item_data)
            logger.info(f"Created predefined item: {item_data.name}")
            item_count += 1
        
        # Step 2: Check for and create missing financial profiles for this item
        for profile_data in profile_data_list:
            # Check if a profile with this transaction type already exists for the item
            exists = any(p.transaction_type == profile_data.transaction_type for p in item.financial_profiles)
            if not exists:
                profile_create_data = profile_data.model_dump()
                profile_create_data['item_id'] = item.id
                item_financial_profile_repo.create(db, obj_in=profile_create_data)
                logger.info(f"  - Created '{profile_data.transaction_type.value}' profile for {item.name}")
                profile_count += 1

    if item_count == 0 and profile_count == 0:
        logger.info("All predefined items and profiles already exist.")
    else:
        logger.info(f"Seeded {item_count} new items and {profile_count} new financial profiles.")

def seed_permissions(db: Session):
    """
    Ensures all permissions from the seeder data exist in the database.
    """
    logger.info("Checking for predefined permissions to seed...")
    count = 0
    for perm_data in PREDEFINED_PERMISSIONS:
        permission = permission_repo.get_by_name(db, name=perm_data["name"])
        if not permission:
            permission_repo.create(db, obj_in=perm_data)
            logger.info(f"Created predefined permission: {perm_data['name'].value}")
            count += 1
    
    if count > 0:
        logger.info(f"Seeded {count} new permissions.")
    else:
        logger.info(f"All predefined permissions already exist.")

def seed_all():
    """
    Master seeder function to run all individual seeders.
    """
    try:
        db = SessionLocal()
        seed_permissions(db)
        seed_items(db)
    finally:
        db.close()
        logger.info("Database connection closed successfully.")
