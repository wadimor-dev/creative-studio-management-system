from app.repositories.base_repository import BaseRepository
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate
from sqlalchemy.orm import Session
from sqlalchemy import func

class CategoryRepository(BaseRepository[Category, CategoryCreate, CategoryUpdate]):
    def __init__(self):
        super().__init__(Category)

    def find_by_name(self, db: Session, name: str) -> Category:
        return db.query(self.model).filter(func.lower(self.model.name) == func.lower(name)).first()

    def exists_name(self, db: Session, name: str) -> bool:
        return self.find_by_name(db, name) is not None

    def get_active(self, db: Session):
        return db.query(self.model).all()

category_repo = CategoryRepository()
