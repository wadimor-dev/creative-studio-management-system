from app.repositories.base_repository import BaseRepository
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleUpdate

class RoleRepository(BaseRepository[Role, RoleCreate, RoleUpdate]):
    def __init__(self):
        super().__init__(Role)

role_repo = RoleRepository()
