import sys
import os

# Add backend dir to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database.session import SessionLocal
from app.models.division import Division
from app.models.work_category import WorkCategory

def seed_data():
    db = SessionLocal()
    try:
        # Seed Divisions
        divisions = ["Creative", "Marketing", "Production", "Administration", "Management"]
        for div_name in divisions:
            existing = db.query(Division).filter(Division.name == div_name).first()
            if not existing:
                div = Division(name=div_name)
                db.add(div)
                
        # Seed Work Categories
        categories = [
            "Video Editing", 
            "Graphic Design", 
            "Photography", 
            "Videography", 
            "Administration", 
            "Meeting", 
            "Maintenance", 
            "Other"
        ]
        for cat_name in categories:
            existing = db.query(WorkCategory).filter(WorkCategory.name == cat_name).first()
            if not existing:
                cat = WorkCategory(name=cat_name)
                db.add(cat)
                
        db.commit()
        print("Data seeded successfully!")
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    seed_data()
