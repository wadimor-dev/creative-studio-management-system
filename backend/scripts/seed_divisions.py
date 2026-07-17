import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.session import SessionLocal
from app.models.division import Division

DIVISIONS = [
    "Creative",
    "Marketing",
    "Production",
    "Administration",
    "Management",
]


def seed_divisions():
    db = SessionLocal()

    try:
        for name in DIVISIONS:

            exists = db.query(Division).filter(
                Division.name == name
            ).first()

            if exists:
                print(f"{name} already exists.")
                continue

            db.add(Division(name=name))

        db.commit()
        print("Divisions seeded.")

    except Exception as e:
        db.rollback()
        print(e)

    finally:
        db.close()


if __name__ == "__main__":
    seed_divisions()