from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from app.repositories.base_repository import BaseRepository
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleUpdate

class RoleRepository(BaseRepository[Role, RoleCreate, RoleUpdate]):
    def __init__(self):
        super().__init__(Role)

    def get_by_name(self, db: Session, name: str) -> Optional[Role]:
        return db.query(self.model).filter(self.model.name == name).first()

    def get_with_permissions(self, db: Session, role_id: int) -> Optional[Role]:
        return (
            db.query(self.model)
            .options(joinedload(self.model.permissions))
            .filter(self.model.id == role_id)
            .first()
        )

    def get_all_with_permissions(self, db: Session) -> List[Role]:
        return (
            db.query(self.model)
            .options(joinedload(self.model.permissions))
            .order_by(self.model.name)
            .all()
        )

role_repo = RoleRepository()
