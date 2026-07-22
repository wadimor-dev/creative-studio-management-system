import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database.session import SessionLocal
from app.models.user import User
from app.core.password import verify_password

def check_user():
    db = SessionLocal()
    user = db.query(User).filter(User.email == "admin@studio.com").first()
    if user:
        print(f"User found: {user.email}")
        print(f"Hashed password: {user.hashed_password}")
        is_valid = verify_password("password123", user.hashed_password)
        print(f"Password valid: {is_valid}")
    else:
        print("User not found.")
    db.close()

if __name__ == "__main__":
    check_user()
