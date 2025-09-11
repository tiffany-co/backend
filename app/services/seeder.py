from sqlalchemy.orm import Session
from app.repository.item import item_repo
from app.logging_config import logger
from .seeder_data import PREDEFINED_ITEMS

def seed_items(db: Session):
    """
    Ensures that all predefined item templates exist in the database.
    This logic is now separate from the data it seeds.
    """
    logger.info("Checking for predefined items to seed...")
    count = 0
    for item_in in PREDEFINED_ITEMS:
        item = item_repo.get_by_name(db, name=item_in.name)
        if not item:
            item_repo.create(db, obj_in=item_in)
            logger.info(f"Created predefined item template: {item_in.name}")
            count += 1
    
    if count == 0:
        logger.info("All predefined items already exist in the database.")
    else:
        logger.info(f"Seeded {count} new item templates.")

