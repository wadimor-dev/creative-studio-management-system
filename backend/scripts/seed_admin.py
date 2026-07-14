import sys
import os

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.session import SessionLocal
from app.models.user import User
from app.models.role import Role
from app.core.password import get_password_hash

def seed_admin():
    db = SessionLocal()
    try:
        # Check if Admin role exists
        admin_role = db.query(Role).filter(Role.name == "Admin").first()
        if not admin_role:
            admin_role = Role(name="Admin", description="System Administrator")
            db.add(admin_role)
            db.commit()
            db.refresh(admin_role)
            print("Role 'Admin' created.")
        
        # Check if admin user exists
        admin_email = "admin@studio.com"
        admin_user = db.query(User).filter(User.email == admin_email).first()
        if not admin_user:
            admin_user = User(
                username="adminsuper",
                email=admin_email,
                full_name="Super Administrator",
                hashed_password=get_password_hash("password123"),
                is_active=True,
                role_id=admin_role.id
            )
            db.add(admin_user)
            db.commit()
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
