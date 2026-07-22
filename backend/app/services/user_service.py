from sqlalchemy.orm import Session
from app.repositories.user_repository import user_repo
from app.repositories.role_repository import role_repo
from app.core.authorization.repositories import user_role_repo
from app.schemas.user import UserCreate, UserUpdate, ProfileUpdate
from app.core.exceptions import CSMSException
from app.core.auth.password import get_password_hash


class UserService:
    def get_user(self, db: Session, user_id: int):
        user = user_repo.get_by_id_with_roles(db, user_id)
        if not user:
            raise CSMSException("User not found", status_code=404)
        return user

    def get_users(self, db: Session, skip: int = 0, limit: int = 10, search: str = None):
        return user_repo.get_all_with_roles(
            db=db,
            skip=skip,
            limit=limit,
            search=search,
        )

    def create_user(self, db: Session, user_in: UserCreate):
        if user_repo.get_by_username(db, username=user_in.username):
            raise CSMSException("Username already exists", status_code=400)
        if user_repo.get_by_email(db, email=user_in.email):
            raise CSMSException("Email already exists", status_code=400)

        for rid in user_in.role_ids:
            role = role_repo.get_by_id(db, rid)
            if not role:
                raise CSMSException(f"Role with id {rid} not found", status_code=400)

        user_data = user_in.model_dump(exclude={"role_ids", "password"})
        user_data["hashed_password"] = get_password_hash(user_in.password)

        user = user_repo.create(db, obj_in=user_data)

        user_role_repo.set_user_roles(db, user.id, user_in.role_ids)

        return user_repo.get_by_id_with_roles(db, user.id)

    def update_user(self, db: Session, user_id: int, user_in: UserUpdate):
        user = self.get_user(db, user_id)

        update_data = user_in.model_dump(exclude_unset=True)

        if "username" in update_data and update_data["username"] != user.username:
            if user_repo.get_by_username(db, username=update_data["username"]):
                raise CSMSException("Username already exists", status_code=400)

        if "email" in update_data and update_data["email"] != user.email:
            if user_repo.get_by_email(db, email=update_data["email"]):
                raise CSMSException("Email already exists", status_code=400)

        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

        role_ids = update_data.pop("role_ids", None)

        if update_data:
            user_repo.update(db, db_obj=user, obj_in=update_data)

        if role_ids is not None:
            for rid in role_ids:
                role = role_repo.get_by_id(db, rid)
                if not role:
                    raise CSMSException(f"Role with id {rid} not found", status_code=400)
            user_role_repo.set_user_roles(db, user.id, role_ids)

        return user_repo.get_by_id_with_roles(db, user.id)

    def delete_user(self, db: Session, user_id: int):
        user = self.get_user(db, user_id)
        return user_repo.delete(db, user_id)

    def update_profile(self, db: Session, user_id: int, profile_in: ProfileUpdate):
        user = self.get_user(db, user_id)
        update_data = profile_in.model_dump(exclude_unset=True)

        if "email" in update_data and update_data["email"] != user.email:
            if user_repo.get_by_email(db, email=update_data["email"]):
                raise CSMSException("Email already exists", status_code=400)

        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

        return user_repo.update(db, db_obj=user, obj_in=update_data)


user_service = UserService()
