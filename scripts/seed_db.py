import sys
from pathlib import Path

# --- Add project root to Python path ---
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))
# ---

from dotenv import load_dotenv
from rich.console import Console
from seeding.seeder import seed_all
from app.logging_config import setup_logging, logger

console = Console()

def run_seeder():
    """
    Runs the master seeder function to populate the database with initial data.
    """
    # Initialize application logging to get rich output
    setup_logging()
    
    logger.info("--- Running Database Seeder ---")
    try:
        seed_all()
        logger.info("Seeding complete!")
    except Exception as e:
        logger.error(f"An unexpected error occurred during seeding: {e}")

if __name__ == "__main__":
    # Load environment variables to ensure the database connection is available.
    env_path = root_dir.parent / ".env"
    load_dotenv(dotenv_path=env_path)
    
    run_seeder()

