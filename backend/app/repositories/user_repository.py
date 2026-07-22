from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from app.repositories.base_repository import BaseRepository
from app.models.user import User
from app.core.organization.employee.models import Employee
from app.schemas.user import UserCreate, UserUpdate

class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    def __init__(self):
        super().__init__(User)

    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        return db.query(self.model).filter(self.model.username == username).first()

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(self.model).filter(self.model.email == email).first()

    def get_by_id_with_roles(self, db: Session, user_id: int) -> Optional[User]:
        return (
            db.query(self.model)
            .options(joinedload(self.model.roles))
            .filter(self.model.id == user_id)
            .first()
        )

    def get_all_with_roles(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 10,
        search: Optional[str] = None,
    ):
        query = db.query(self.model).options(joinedload(self.model.roles))

        if search:
            like = f"%{search}%"
            query = query.outerjoin(Employee, Employee.user_id == User.id).filter(
                User.username.ilike(like) | User.email.ilike(like) | Employee.full_name.ilike(like)
            )

        total = query.count()
        users = query.order_by(User.id.desc()).offset(skip).limit(limit).all()
        return users, total

user_repo = UserRepository()
