from app.repositories.base_repository import BaseRepository
from app.models.unit import Unit
from app.schemas.unit import UnitCreate, UnitUpdate

class UnitRepository(BaseRepository[Unit, UnitCreate, UnitUpdate]):
    def __init__(self):
        super().__init__(Unit)

unit_repo = UnitRepository()
