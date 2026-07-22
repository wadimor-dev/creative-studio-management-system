from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database.session import get_db
from app.models.product_movement import ProductMovement, ProductMovementType, ProductMovementReason
from app.schemas.product_movement import (
    ProductMovementCreate,
    ProductMovementResponse
)
from app.services.movement_engine import MovementEngine
from app.common.responses import SuccessResponse, create_success_response
from app.core.exceptions import CSMSException
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("", response_model=SuccessResponse[List[ProductMovementResponse]])
def get_product_movements(
    product_id: Optional[int] = Query(None),
    type: Optional[ProductMovementType] = Query(None),
    limit: int = Query(100),
    db: Session = Depends(get_db)
):
    query = db.query(ProductMovement)
    if product_id:
        query = query.filter(ProductMovement.product_id == product_id)
    if type:
        query = query.filter(ProductMovement.type == type)
        
    movements = query.order_by(ProductMovement.date.desc()).limit(limit).all()
    return create_success_response(data=movements, message="Product movements fetched successfully")

@router.post("", response_model=SuccessResponse[ProductMovementResponse])
def create_movement(
    movement_in: ProductMovementCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = MovementEngine(db)
    
    # Infer movement type from reason
    inferred_type = None
    if movement_in.reason == ProductMovementReason.RECEIVE_FROM_FACTORY:
        inferred_type = ProductMovementType.IN
    elif movement_in.reason in [ProductMovementReason.GIFT, ProductMovementReason.SALES_SAMPLE, ProductMovementReason.DAMAGED, ProductMovementReason.MISSING]:
        inferred_type = ProductMovementType.OUT
    elif movement_in.reason in [ProductMovementReason.SHOWROOM_TRANSFER, ProductMovementReason.PHOTO_SHOOT, ProductMovementReason.TV_STUDIO]:
        inferred_type = ProductMovementType.TRANSFER
    else:
        # For OTHER or any undefined reason, we require some inference. Since frontend doesn't send type,
        # we can default based on source/dest placements provided.
        if movement_in.source_placement_id and movement_in.destination_placement_id:
            inferred_type = ProductMovementType.TRANSFER
        elif movement_in.destination_placement_id:
            inferred_type = ProductMovementType.IN
        elif movement_in.source_placement_id:
            inferred_type = ProductMovementType.OUT
        else:
            raise CSMSException("Cannot infer movement type. Please provide appropriate placements.", status_code=400)
    
    movement = engine.execute_movement(
        product_id=movement_in.product_id,
        type=inferred_type,
        reason=movement_in.reason,
        quantity=movement_in.quantity,
        user_id=current_user.id,
        source_placement_id=movement_in.source_placement_id,
        destination_placement_id=movement_in.destination_placement_id,
        reference=movement_in.reference,
        reference_type=movement_in.reference_type,
        reference_id=movement_in.reference_id,
        notes=movement_in.notes
    )
    
    return create_success_response(data=movement, message="Product movement executed successfully")
