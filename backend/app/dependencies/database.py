from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.session import get_db

def get_db_session(db: Session = Depends(get_db)) -> Session:
    """
    Dependency for database session.
    Delegates to the core database session generator.
    """
    return db
