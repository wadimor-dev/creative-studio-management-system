import logging
from sqlalchemy.orm import Session
from app.core.database.base import Base
from app.core.database.session import engine

logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    logger.info("Database initialized (No-op)")
