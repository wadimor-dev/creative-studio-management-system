from typing import List
from sqlalchemy.orm import Session, joinedload
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleUpdate, RoleWithPermissions
from app.repositories.role_repository import role_repo
from app.core.exceptions import CSMSException


class RoleService:
    def get_all_with_permissions(self, db: Session) -> List[RoleWithPermissions]:
        roles = role_repo.get_all_with_permissions(db)
        result = []
        for role in roles:
            perm_ids = [p.id for p in role.permissions] if role.permissions else []
            result.append(RoleWithPermissions(
                id=role.id,
                name=role.name,
                description=role.description,
                is_system=role.is_system,
                permission_ids=perm_ids,
            ))
        return result

    def create(self, db: Session, role_in: RoleCreate) -> Role:
        existing = role_repo.get_by_name(db, role_in.name)
        if existing:
            raise CSMSException(f"Role '{role_in.name}' already exists", status_code=400)
        return role_repo.create(db, obj_in=role_in)

    def update(self, db: Session, role_id: int, role_in: RoleUpdate) -> Role:
        role = role_repo.get_by_id(db, role_id)
        if not role:
            raise CSMSException("Role not found", status_code=404)
        if role.is_system:
            raise CSMSException("System role cannot be modified", status_code=400)
        update_data = role_in.model_dump(exclude_unset=True)
        return role_repo.update(db, db_obj=role, obj_in=update_data)

    def delete(self, db: Session, role_id: int) -> None:
        role = role_repo.get_by_id(db, role_id)
        if not role:
            raise CSMSException("Role not found", status_code=404)
        if role.is_system:
            raise CSMSException("System role cannot be deleted", status_code=400)
        role_repo.delete(db, role_id)


role_service = RoleService()
