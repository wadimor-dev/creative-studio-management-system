from sqlalchemy.orm import Session
from app.models.product_movement import ProductMovement, ProductMovementType, ProductMovementReason
from app.models.product_stock import ProductPlacementStock
from app.models.product import Product
from app.models.product_placement import ProductPlacement
from app.exceptions.base import CSMSException
from typing import Optional

class MovementEngine:
    """
    Movement Engine handles all product stock modifications safely.
    It guarantees that no stock goes below 0 and that all movements are logged properly.
    """
    def __init__(self, db: Session):
        self.db = db

    def _update_stock(self, product_id: int, placement_id: int, quantity_change: int, user_id: Optional[int] = None) -> ProductPlacementStock:
        """
        Internal method to safely update stock for a product at a specific placement.
        Handles row locking, negative stock prevention, and row creation/deletion if needed.
        """
        stock = self.db.query(ProductPlacementStock).filter(
            ProductPlacementStock.product_id == product_id,
            ProductPlacementStock.placement_id == placement_id
        ).with_for_update().first()

        if stock:
            old_qty = stock.quantity
            new_quantity = stock.quantity + quantity_change
            if new_quantity < 0:
                raise CSMSException(f"Insufficient stock for product ID {product_id} at placement ID {placement_id}. Attempted to reduce by {abs(quantity_change)} but only {stock.quantity} available.", status_code=400)
            stock.quantity = new_quantity
            
            # Audit log
            from app.services.logger_service import logger_service
            logger_service.log_audit(
                db=self.db,
                user_id=user_id,
                table_name="product_placement_stocks",
                record_id=stock.id,
                action="UPDATE",
                old_value={"quantity": old_qty},
                new_value={"quantity": new_quantity}
            )
        else:
            if quantity_change < 0:
                raise CSMSException(f"Insufficient stock for product ID {product_id} at placement ID {placement_id}. No stock record found.", status_code=400)
            
            stock = ProductPlacementStock(
                product_id=product_id,
                placement_id=placement_id,
                quantity=quantity_change
            )
            self.db.add(stock)
            self.db.flush() # flush to get ID
            
            # Audit log
            from app.services.logger_service import logger_service
            logger_service.log_audit(
                db=self.db,
                user_id=user_id, 
                table_name="product_placement_stocks",
                record_id=stock.id,
                action="CREATE",
                old_value=None,
                new_value={"quantity": quantity_change}
            )
            
        self.db.flush()
        return stock

    def execute_movement(
        self,
        product_id: int,
        type: ProductMovementType,
        reason: ProductMovementReason,
        quantity: int,
        user_id: int,
        source_placement_id: Optional[int] = None,
        destination_placement_id: Optional[int] = None,
        reference: Optional[str] = None,
        reference_type: Optional[str] = None,
        reference_id: Optional[int] = None,
        notes: Optional[str] = None,
        commit: bool = True,
    ) -> ProductMovement:
        """
        Executes a stock movement and creates a movement record.
        """
        if quantity <= 0:
            raise CSMSException("Movement quantity must be greater than 0", status_code=400)
            
        # Validate product
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise CSMSException("Product not found", status_code=404)

        if type == ProductMovementType.IN:
            if not destination_placement_id:
                raise CSMSException("Destination placement is required for IN movement", status_code=400)
            if source_placement_id:
                raise CSMSException("Source placement must be null for IN movement", status_code=400)
                
            self._update_stock(product_id, destination_placement_id, quantity, user_id)
            
        elif type == ProductMovementType.OUT:
            if not source_placement_id:
                raise CSMSException("Source placement is required for OUT movement", status_code=400)
            if destination_placement_id:
                raise CSMSException("Destination placement must be null for OUT movement", status_code=400)
                
            self._update_stock(product_id, source_placement_id, -quantity, user_id)
            
        elif type == ProductMovementType.TRANSFER:
            if not source_placement_id or not destination_placement_id:
                raise CSMSException("Both source and destination placements are required for TRANSFER", status_code=400)
            if source_placement_id == destination_placement_id:
                raise CSMSException("Source and destination placements cannot be the same", status_code=400)
                
            # Perform transfer. To avoid deadlocks, lock the smaller placement ID first
            first_id = min(source_placement_id, destination_placement_id)
            second_id = max(source_placement_id, destination_placement_id)
            
            # Dummy reads to lock the rows in a consistent order
            self.db.query(ProductPlacementStock).filter(ProductPlacementStock.product_id == product_id, ProductPlacementStock.placement_id == first_id).with_for_update().first()
            self.db.query(ProductPlacementStock).filter(ProductPlacementStock.product_id == product_id, ProductPlacementStock.placement_id == second_id).with_for_update().first()
            
            self._update_stock(product_id, source_placement_id, -quantity, user_id)
            self._update_stock(product_id, destination_placement_id, quantity, user_id)

        # Record movement
        movement = ProductMovement(
            product_id=product_id,
            type=type,
            reason=reason,
            quantity=quantity,
            source_placement_id=source_placement_id,
            destination_placement_id=destination_placement_id,
            reference=reference,
            reference_type=reference_type,
            reference_id=reference_id,
            notes=notes,
            user_id=user_id
        )
        self.db.add(movement)
        if commit:
            self.db.commit()
        else:
            self.db.flush()
        self.db.refresh(movement)

        return movement
