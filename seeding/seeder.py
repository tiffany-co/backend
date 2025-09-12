import sys
from pathlib import Path

# --- Add project root to Python path ---
# This allows this script, which is outside the 'app' package,
# to import modules from within 'app'.
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))
# ---

from sqlalchemy.orm import Session
from app.repository.item import item_repo
from app.repository.permission import permission_repo
from app.logging_config import logger
from seeding.data.item_data import PREDEFINED_ITEMS
from seeding.data.permission_data import PREDEFINED_PERMISSIONS

def seed_items(db: Session):
    """
    Ensures that all predefined item templates exist in the database.
    """
    logger.info("Checking for predefined items to seed...")
    count = 0
    for item_data in PREDEFINED_ITEMS:
        item = item_repo.get_by_name(db, name=item_data.name)
        if not item:
            item_repo.create(db, obj_in=item_data)
            logger.info(f"Created predefined item template: {item_data.name}")
            count += 1
    
    if count > 0:
        logger.info(f"Seeded {count} new item templates.")

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

def seed_all(db: Session):
    """
    Master seeder function to run all individual seeders.
    """
    seed_permissions(db)
    # seed_items(db) # Temporarily disabled as per user request to focus on permissions

