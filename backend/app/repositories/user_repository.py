from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    def __init__(self):
        super().__init__(User)

    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        return db.query(self.model).filter(self.model.username == username).first()

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(self.model).filter(self.model.email == email).first()

user_repo = UserRepository()
