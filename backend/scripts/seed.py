import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import logging
from app.core.database.session import SessionLocal

logger = logging.getLogger(__name__)

def seed_database():
    logger.info("Starting database seeder...")
    db = SessionLocal()
    try:
        # Initial seeder logic will go here
        # Example: create admin role, admin user, etc.
        logger.info("Database seeded successfully.")
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    seed_database()
