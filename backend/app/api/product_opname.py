from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from app.core.database.session import get_db
from app.models.product_movement import ProductMovementType, ProductMovementReason
from app.models.product_stock import ProductPlacementStock
from app.services.movement_engine import MovementEngine
from app.common.responses import SuccessResponse, create_success_response
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter()

class OpnameItem(BaseModel):
    product_id: int
    actual_quantity: int
    
class OpnameRequest(BaseModel):
    placement_id: int
    items: List[OpnameItem]
    notes: str = "Stock Opname"

@router.post("", response_model=SuccessResponse[dict])
def process_opname(
    request: OpnameRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Process a stock opname. This compares the actual quantity scanned 
    with the system quantity and creates adjustment movements.
    """
    engine = MovementEngine(db)
    
    adjustments = []
    
    for item in request.items:
        # Get current system stock
        system_stock = db.query(ProductPlacementStock).filter(
            ProductPlacementStock.product_id == item.product_id,
            ProductPlacementStock.placement_id == request.placement_id
        ).first()
        
        system_qty = system_stock.quantity if system_stock else 0
        diff = item.actual_quantity - system_qty
        
        if diff > 0:
            # We have more actual stock than system stock -> IN movement
            engine.execute_movement(
                product_id=item.product_id,
                type=ProductMovementType.IN,
                reason=ProductMovementReason.STOCK_OPNAME,
                quantity=diff,
                user_id=current_user.id,
                destination_placement_id=request.placement_id,
                notes=request.notes
            )
            adjustments.append({"product_id": item.product_id, "adjustment": diff, "type": "IN"})
            
        elif diff < 0:
            # We have less actual stock than system stock -> OUT movement
            engine.execute_movement(
                product_id=item.product_id,
                type=ProductMovementType.OUT,
                reason=ProductMovementReason.STOCK_OPNAME,
                quantity=abs(diff),
                user_id=current_user.id,
                source_placement_id=request.placement_id,
                notes=request.notes
            )
            adjustments.append({"product_id": item.product_id, "adjustment": diff, "type": "OUT"})

    return create_success_response(
        data={"adjustments_made": adjustments},
        message="Stock opname processed successfully"
    )
