from app.repositories.base_repository import BaseRepository
from app.models.location import Location
from app.schemas.location import LocationCreate, LocationUpdate
from sqlalchemy.orm import Session
from sqlalchemy import func

class LocationRepository(BaseRepository[Location, LocationCreate, LocationUpdate]):
    def __init__(self):
        super().__init__(Location)

    def find_by_name(self, db: Session, name: str) -> Location:
        return db.query(self.model).filter(func.lower(self.model.name) == func.lower(name)).first()

    def exists_name(self, db: Session, name: str) -> bool:
        return self.find_by_name(db, name) is not None

    def get_active(self, db: Session):
        return db.query(self.model).all()

location_repo = LocationRepository()
