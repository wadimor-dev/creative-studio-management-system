from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.item import Item
from app.models.inventory_transaction import InventoryTransaction

class DashboardRepository:
    def get_total_items(self, db: Session) -> int:
        return db.query(Item).count()

    def get_total_stock(self, db: Session) -> int:
        return db.query(func.sum(Item.stock_qty)).scalar() or 0

dashboard_repo = DashboardRepository()
