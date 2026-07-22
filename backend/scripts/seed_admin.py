import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database.session import SessionLocal
from app.models.user import User
from app.models.role import Role
from app.core.auth.password import get_password_hash
from app.core.authorization.repositories import user_role_repo


def seed_admin():
    db = SessionLocal()
    try:
        admin_role = db.query(Role).filter(Role.name == "ADMIN").first()
        if not admin_role:
            admin_role = Role(name="ADMIN", description="System Administrator", is_system=True)
            db.add(admin_role)
            db.commit()
            db.refresh(admin_role)
            print("Role 'ADMIN' created.")

        admin_email = "admin@studio.com"
        admin_user = db.query(User).filter(User.email == admin_email).first()
        if not admin_user:
            admin_user = User(
                username="adminsuper",
                email=admin_email,
                hashed_password=get_password_hash("password123"),
                is_active=True,
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)

            user_role_repo.set_user_roles(db, admin_user.id, [admin_role.id])

            print(f"User '{admin_email}' with password 'password123' created successfully.")
        else:
            print(f"User '{admin_email}' already exists.")

    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_admin()
