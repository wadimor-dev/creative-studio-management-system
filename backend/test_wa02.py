import sys
import os
import requests
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database.session import SessionLocal
from app.models.user import User
from app.models.role import Role
from app.core.auth.password import get_password_hash
from app.core.authorization.repositories import user_role_repo

def setup_test_user():
    db = SessionLocal()
    role = db.query(Role).filter(Role.name == "ADMIN").first()
    user = db.query(User).filter(User.username == "wa02user").first()
    if not user:
        user = User(
            username="wa02user",
            email="wa02user@example.com",
            hashed_password=get_password_hash("password123"),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        if role:
            user_role_repo.set_user_roles(db, user.id, [role.id])
    db.close()
    
# Create a dummy image
with open("test_image.jpg", "wb") as f:
    f.write(os.urandom(1024))
