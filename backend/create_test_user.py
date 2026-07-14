import sys
import os
import bcrypt

# Add backend dir to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.session import SessionLocal
from app.models.user import User
from app.models.role import Role

def create_test_user():
    db = SessionLocal()
    try:
        # Get or create role
        admin_role = db.query(Role).filter(Role.name == "ADMIN").first()
        if not admin_role:
            admin_role = Role(name="ADMIN", description="Administrator")
            db.add(admin_role)
            db.commit()
        
        # Hash password using bcrypt directly
        password = "admin123"
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Check if user already exists by email
        existing_user = db.query(User).filter(User.email == "admin@studio.com").first()
        if existing_user:
            # Update existing admin password
            existing_user.hashed_password = hashed
            db.commit()
            print("✅ Test user password updated:")
            print(f"   Username: {existing_user.username}")
            print(f"   Email: {existing_user.email}")
            print(f"   Password: admin123")
        else:
            # Create test user
            test_user = User(
                username="admin",
                email="admin@studio.com",
                hashed_password=hashed,
                is_active=True,
                role_id=admin_role.id
            )
            db.add(test_user)
            db.commit()
            print("✅ Test user created:")
            print(f"   Username: admin")
            print(f"   Email: admin@studio.com")
            print(f"   Password: admin123")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    create_test_user()
