import logging
from sqlalchemy.orm import Session
from app.database.base import Base
from app.database.session import engine

logger = logging.getLogger(__name__)

def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    logger.info("Database initialized (No-op)")
