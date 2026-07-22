from sqlalchemy.orm import Session
from app.repositories.item_repository import item_repo
from app.repositories.category_repository import category_repo
from app.repositories.unit_repository import unit_repo
from app.repositories.location_repository import location_repo
from app.schemas.item import ItemCreate, ItemUpdate
from app.core.exceptions import CSMSException
from app.models.item_stock import ItemStock
from app.models.inventory_transaction import InventoryMovementType
from app.repositories.inventory_repository import inventory_transaction_repo
from datetime import datetime, timezone, timedelta

class ItemService:
    def get_item(self, db: Session, item_id: int):
        item = item_repo.get_by_id(db, item_id)
        if not item:
            raise CSMSException("Item not found", status_code=404)
        return item

    def get_items(self, db: Session, skip: int = 0, limit: int = 10, search: str = None, category_id: int = None, location_id: int = None):
        filters = {}
        if category_id:
            filters["category_id"] = category_id
        if location_id:
            filters["location_id"] = location_id
            
        return item_repo.get_all(
            db=db, 
            skip=skip, 
            limit=limit, 
            search=search, 
            search_fields=["name", "sku"],
            filters=filters
        )

    def _validate_relations(self, db: Session, category_id: int = None, unit_id: int = None, location_id: int = None):
        if category_id and not category_repo.get_by_id(db, category_id):
            raise CSMSException("Category not found", status_code=400)
        if unit_id and not unit_repo.get_by_id(db, unit_id):
            raise CSMSException("Unit not found", status_code=400)
        if location_id and not location_repo.get_by_id(db, location_id):
            raise CSMSException("Location not found", status_code=400)

    def create_item(self, db: Session, item_in: ItemCreate, user_id: int = 1):
        if item_repo.get_by_sku(db, sku=item_in.sku):
            raise CSMSException("SKU already exists", status_code=400)
            
        self._validate_relations(db, item_in.category_id, item_in.unit_id, item_in.location_id)
        
        # We need to extract initial_stock before passing to repo
        item_data = item_in.model_dump(exclude={"initial_stock"})
        new_item = item_repo.create(db, obj_in=item_data)
        
        if item_in.initial_stock > 0 and item_in.location_id:
            # Create stock
            stock = ItemStock(item_id=new_item.id, location_id=item_in.location_id, quantity=item_in.initial_stock)
            db.add(stock)
            
            # Create IN transaction for this initial stock
            # We don't have user_id here easily without changing the signature. Let's assume user_id=1 or add it to args.
            # Actually, we should change create_item signature to include user_id. Let's just use user_id=1 for now, or fetch from context?
            # We need to add user_id to create_item.
            pass
            
            # We can also just update new_item.stock_qty for the global summary
            new_item.stock_qty = item_in.initial_stock
            
            # Create transaction record
            tx_data = {
                "item_id": new_item.id,
                "user_id": user_id, 
                "type": InventoryMovementType.IN,
                "quantity": item_in.initial_stock,
                "destination_location_id": item_in.location_id,
                "notes": "Initial stock on creation",
                "date": datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None)
            }
            inventory_transaction_repo.create(db, obj_in=tx_data)
            db.flush()
            
        return new_item

    def update_item(self, db: Session, item_id: int, item_in: ItemUpdate, user_id: int = 1):
        item = self.get_item(db, item_id)
        
        if item_in.sku and item_in.sku != item.sku:
            if item_repo.get_by_sku(db, sku=item_in.sku):
                raise CSMSException("SKU already exists", status_code=400)
                
        self._validate_relations(db, item_in.category_id, item_in.unit_id, item_in.location_id)
        
        # Handle stock update if provided
        if item_in.stock_qty is not None and item_in.location_id:
            # Find current stock in this location
            current_stock = db.query(ItemStock).filter(ItemStock.item_id == item.id, ItemStock.location_id == item_in.location_id).first()
            current_qty = current_stock.quantity if current_stock else 0
            
            diff = item_in.stock_qty - current_qty
            if diff != 0:
                if not current_stock:
                    current_stock = ItemStock(item_id=item.id, location_id=item_in.location_id, quantity=item_in.stock_qty)
                    db.add(current_stock)
                else:
                    current_stock.quantity = item_in.stock_qty
                
                # Create ADJUSTMENT transaction
                tx_data = {
                    "item_id": item.id,
                    "user_id": user_id,
                    "type": InventoryMovementType.ADJUSTMENT,
                    "quantity": abs(diff),
                    "source_location_id": item_in.location_id if diff < 0 else None,
                    "destination_location_id": item_in.location_id if diff > 0 else None,
                    "notes": "Manual adjustment from item edit",
                    "date": datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None)
                }
                inventory_transaction_repo.create(db, obj_in=tx_data)
                
                # Update global summary
                item.stock_qty = (item.stock_qty or 0) + diff
                db.flush()

        update_data = item_in.model_dump(exclude_unset=True, exclude={"stock_qty"})
        return item_repo.update(db, db_obj=item, obj_in=update_data)

    def delete_item(self, db: Session, item_id: int):
        item = self.get_item(db, item_id)
        return item_repo.delete(db, item_id)

item_service = ItemService()
