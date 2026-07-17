import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.session import SessionLocal
from app.models.role import Role

ROLES = [
    {
        "name": "ADMIN",
        "description": "System Administrator"
    },
    {
        "name": "MANAGER",
        "description": "System Manager"
    },
    {
        "name": "STAFF",
        "description": "System Staff"
    },
    {
        "name": "CREATIVE",
        "description": "System Creative"
    },
]


def seed_roles():
    db = SessionLocal()

    try:
        for role in ROLES:
            exists = db.query(Role).filter(Role.name == role["name"]).first()

            if exists:
                print(f"Role {role['name']} already exists.")
                continue

            db.add(Role(**role))

        db.commit()
        print("Roles seeded successfully.")

    except Exception as e:
        db.rollback()
        print(e)

    finally:
        db.close()


if __name__ == "__main__":
    seed_roles()