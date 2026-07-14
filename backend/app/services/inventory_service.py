from sqlalchemy.orm import Session
from app.repositories.inventory_repository import inventory_transaction_repo
from app.repositories.item_repository import item_repo
from app.schemas.inventory import TransactionCreate
from app.models.inventory_transaction import InventoryMovementType
from app.models.item_stock import ItemStock
from app.exceptions.base import CSMSException
from datetime import datetime, timezone, timedelta

class InventoryService:
    def _get_or_create_stock(self, db: Session, item_id: int, location_id: int) -> ItemStock:
        stock = db.query(ItemStock).filter(
            ItemStock.item_id == item_id,
            ItemStock.location_id == location_id
        ).first()
        if not stock:
            stock = ItemStock(item_id=item_id, location_id=location_id, quantity=0)
            db.add(stock)
            db.flush()
        return stock

    def _recalculate_global_stock(self, db: Session, item_id: int):
        stocks = db.query(ItemStock).filter(ItemStock.item_id == item_id).all()
        total = sum(stock.quantity for stock in stocks)
        item = item_repo.get_by_id(db, item_id)
        if item:
            item.stock_qty = total
            db.add(item)
            db.flush()

    def process_transaction(self, db: Session, user_id: int, tx_in: TransactionCreate, commit: bool = True):
        if tx_in.quantity <= 0:
            raise CSMSException("Quantity must be greater than zero", status_code=400)
            
        item = item_repo.get_by_id(db, tx_in.item_id)
        if not item:
            raise CSMSException("Item not found", status_code=404)

        if tx_in.type == InventoryMovementType.IN:
            if not tx_in.destination_location_id:
                raise CSMSException("Destination location is required for IN transactions", status_code=400)
            
            dest_stock = self._get_or_create_stock(db, item.id, tx_in.destination_location_id)
            dest_stock.quantity += tx_in.quantity
            db.add(dest_stock)

        elif tx_in.type == InventoryMovementType.OUT:
            if not tx_in.source_location_id:
                raise CSMSException("Source location is required for OUT transactions", status_code=400)
            
            src_stock = self._get_or_create_stock(db, item.id, tx_in.source_location_id)
            if src_stock.quantity < tx_in.quantity:
                raise CSMSException("Insufficient stock in source location", status_code=400)
            
            src_stock.quantity -= tx_in.quantity
            db.add(src_stock)

        elif tx_in.type == InventoryMovementType.TRANSFER:
            if not tx_in.source_location_id or not tx_in.destination_location_id:
                raise CSMSException("Both source and destination locations are required for TRANSFER", status_code=400)
            if tx_in.source_location_id == tx_in.destination_location_id:
                raise CSMSException("Source and destination must be different", status_code=400)
                
            src_stock = self._get_or_create_stock(db, item.id, tx_in.source_location_id)
            if src_stock.quantity < tx_in.quantity:
                raise CSMSException("Insufficient stock in source location", status_code=400)
                
            dest_stock = self._get_or_create_stock(db, item.id, tx_in.destination_location_id)
            src_stock.quantity -= tx_in.quantity
            dest_stock.quantity += tx_in.quantity
            db.add(src_stock)
            db.add(dest_stock)
            
        elif tx_in.type == InventoryMovementType.ADJUSTMENT:
            if not tx_in.destination_location_id:
                raise CSMSException("Location (destination) is required for ADJUSTMENT", status_code=400)
            
            dest_stock = self._get_or_create_stock(db, item.id, tx_in.destination_location_id)
            dest_stock.quantity += tx_in.quantity
            db.add(dest_stock)
            
        db.flush()
        
        # Update Item global stock_qty sum for backward compatibility
        self._recalculate_global_stock(db, item.id)

        # Create transaction record
        tx_data = tx_in.model_dump()
        tx_data["user_id"] = user_id
        if not tx_data.get("date"):
            tx_data["date"] = datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None)

        return inventory_transaction_repo.create(db, obj_in=tx_data, commit=commit)

    def get_transaction_history(
        self, db: Session, skip: int = 0, limit: int = 10, 
        item_id: int = None, user_id: int = None, type: str = None,
        category_id: int = None, location_id: int = None
    ):
        from app.models.inventory_transaction import InventoryTransaction
        from app.models.item import Item
        from sqlalchemy import or_
        from sqlalchemy.orm import joinedload
        
        query = db.query(InventoryTransaction).options(
            joinedload(InventoryTransaction.item),
            joinedload(InventoryTransaction.source_location),
            joinedload(InventoryTransaction.destination_location),
            joinedload(InventoryTransaction.user)
        )
        
        if category_id:
            query = query.join(InventoryTransaction.item).filter(Item.category_id == category_id)
            
        if item_id:
            query = query.filter(InventoryTransaction.item_id == item_id)
        if user_id:
            query = query.filter(InventoryTransaction.user_id == user_id)
        if type:
            query = query.filter(InventoryTransaction.type == type)
            
        if location_id:
            query = query.filter(
                or_(
                    InventoryTransaction.source_location_id == location_id,
                    InventoryTransaction.destination_location_id == location_id
                )
            )
            
        total = query.count()
        items = query.order_by(InventoryTransaction.date.desc()).offset(skip).limit(limit).all()
        return items, total

inventory_service = InventoryService()
