import sys
import os
import requests
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.session import SessionLocal
from app.models.user import User
from app.models.role import Role
from app.core.security import get_password_hash

def setup_test_user():
    db = SessionLocal()
    role = db.query(Role).filter(Role.name == "ADMIN").first()
    user = db.query(User).filter(User.username == "wa02user").first()
    if not user:
        user = User(
            username="wa02user", 
            email="wa02user@example.com", 
            hashed_password=get_password_hash("password123"), 
            role_id=role.id,
            division_id=1
        )
        db.add(user)
        db.commit()
    db.close()
    
# Create a dummy image
with open("test_image.jpg", "wb") as f:
    f.write(os.urandom(1024))
