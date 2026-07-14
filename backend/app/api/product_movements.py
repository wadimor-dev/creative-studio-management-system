from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from pydantic import BaseModel

from app.database.session import get_db
from app.models.product_movement import ProductMovement, ProductMovementType
from app.models.product_stock import ProductStock
from app.models.product import Product
from app.schemas.product_movement import ProductMovementCreate, ProductMovementResponse, ProductStockResponse
from app.common.responses import SuccessResponse, create_success_response
from app.common.pagination import PaginatedResponse, create_paginated_response, PaginationParams
from app.dependencies.permission import RequirePermission
from app.constants.permissions import Permission
from app.dependencies.auth import get_current_user
from app.exceptions.base import CSMSException
from app.models.user import User

router = APIRouter()

def _update_stock(db: Session, product_id: int, location_id: int, quantity_change: int):
    stock = db.query(ProductStock).filter(
        ProductStock.product_id == product_id,
        ProductStock.location_id == location_id
    ).first()
    
    if not stock:
        # If it doesn't exist and we are reducing stock, that's an error
        if quantity_change < 0:
            raise CSMSException(f"Insufficient stock for product {product_id} at location {location_id}", status_code=400)
            
        stock = ProductStock(product_id=product_id, location_id=location_id, quantity=quantity_change)
        db.add(stock)
    else:
        new_quantity = stock.quantity + quantity_change
        if new_quantity < 0:
            raise CSMSException(f"Insufficient stock for product {product_id} at location {location_id}", status_code=400)
        stock.quantity = new_quantity

@router.get("", response_model=PaginatedResponse[ProductMovementResponse], dependencies=[Depends(RequirePermission(Permission.PRODUCT_MOVEMENT_VIEW))])
def get_movements(
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends(),
    product_id: Optional[int] = None,
    location_id: Optional[int] = None,
    user_id: Optional[int] = None,
    type_id: Optional[int] = None,
    category_id: Optional[int] = None,
    motif_id: Optional[int] = None,
    sub_motif_id: Optional[int] = None,
    color_id: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    query = db.query(ProductMovement).join(ProductMovement.product).options(
        joinedload(ProductMovement.product),
        joinedload(ProductMovement.source_location),
        joinedload(ProductMovement.destination_location),
        joinedload(ProductMovement.user)
    ).order_by(ProductMovement.date.desc())
    
    if product_id:
        query = query.filter(ProductMovement.product_id == product_id)
        
    if location_id:
        from sqlalchemy import or_
        query = query.filter(
            or_(
                ProductMovement.source_location_id == location_id,
                ProductMovement.destination_location_id == location_id
            )
        )
        
    if user_id:
        query = query.filter(ProductMovement.user_id == user_id)
        
    if type_id:
        query = query.filter(Product.type_id == type_id)
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if motif_id:
        query = query.filter(Product.motif_id == motif_id)
    if sub_motif_id:
        query = query.filter(Product.sub_motif_id == sub_motif_id)
    if color_id:
        query = query.filter(Product.color_id == color_id)
        
    if start_date:
        query = query.filter(ProductMovement.date >= start_date)
        
    if end_date:
        query = query.filter(ProductMovement.date <= f"{end_date} 23:59:59")
        
    total = query.count()
    items = query.offset(pagination.skip).limit(pagination.size).all()
    
    return create_paginated_response(
        data=items,
        total=total,
        page=pagination.page,
        size=pagination.size,
        message="Movements fetched successfully"
    )

@router.post("", response_model=SuccessResponse[ProductMovementResponse], status_code=status.HTTP_201_CREATED, dependencies=[Depends(RequirePermission(Permission.PRODUCT_MOVEMENT_CREATE))])
def create_movement(movement_in: ProductMovementCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    if movement_in.type != ProductMovementType.ADJUSTMENT and movement_in.quantity <= 0:
        raise CSMSException("Quantity must be greater than zero", status_code=400)

    if movement_in.type == ProductMovementType.ADJUSTMENT and movement_in.quantity == 0:
        raise CSMSException("Adjustment quantity cannot be zero", status_code=400)

    # Logic to handle IN, OUT, TRANSFER, ADJUSTMENT
    if movement_in.type == ProductMovementType.IN:
        if not movement_in.destination_location_id:
            raise CSMSException("IN movement requires a destination location", status_code=400)
        _update_stock(db, movement_in.product_id, movement_in.destination_location_id, movement_in.quantity)
        
    elif movement_in.type == ProductMovementType.OUT:
        if not movement_in.source_location_id:
            raise CSMSException("OUT movement requires a source location", status_code=400)
        _update_stock(db, movement_in.product_id, movement_in.source_location_id, -movement_in.quantity)
        
    elif movement_in.type == ProductMovementType.TRANSFER:
        if not movement_in.source_location_id or not movement_in.destination_location_id:
            raise CSMSException("TRANSFER movement requires both source and destination locations", status_code=400)
        if movement_in.source_location_id == movement_in.destination_location_id:
            raise CSMSException("Source and destination locations cannot be the same", status_code=400)
            
        _update_stock(db, movement_in.product_id, movement_in.source_location_id, -movement_in.quantity)
        _update_stock(db, movement_in.product_id, movement_in.destination_location_id, movement_in.quantity)
        
    elif movement_in.type == ProductMovementType.ADJUSTMENT:
        if not movement_in.destination_location_id:
            raise CSMSException("ADJUSTMENT movement requires a destination location", status_code=400)
        _update_stock(db, movement_in.product_id, movement_in.destination_location_id, movement_in.quantity)

    # Save movement record
    movement = ProductMovement(**movement_in.model_dump(), user_id=current_user.id)
    db.add(movement)
    db.commit()
    db.refresh(movement)
    
    # Refresh to load relationships for Pydantic
    db.query(ProductMovement).options(
        joinedload(ProductMovement.product),
        joinedload(ProductMovement.source_location),
        joinedload(ProductMovement.destination_location),
        joinedload(ProductMovement.user)
    ).filter(ProductMovement.id == movement.id).first()

    return create_success_response(data=movement, message="Movement created successfully")
