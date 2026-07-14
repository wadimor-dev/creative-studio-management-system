from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate

class ItemRepository(BaseRepository[Item, ItemCreate, ItemUpdate]):
    def __init__(self):
        super().__init__(Item)

    def get_by_sku(self, db: Session, sku: str) -> Optional[Item]:
        return db.query(self.model).filter(self.model.sku == sku).first()

item_repo = ItemRepository()
