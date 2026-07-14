from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from app.database.session import get_db
from app.models.product_stock import ProductStock
from app.models.product import Product
from app.schemas.product_movement import ProductStockResponse, StockOpnameRequest
from app.common.responses import SuccessResponse, create_success_response
from app.models.product_movement import ProductMovement, ProductMovementType
from app.dependencies.auth import get_current_user
from app.dependencies.permission import RequireRole
from app.constants.role import RoleType
from app.models.user import User

router = APIRouter()

@router.get("", response_model=SuccessResponse[List[ProductStockResponse]])
def get_stocks(
    product_id: Optional[int] = None,
    location_id: Optional[int] = None,
    type_id: Optional[int] = None,
    category_id: Optional[int] = None,
    motif_id: Optional[int] = None,
    sub_motif_id: Optional[int] = None,
    color_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(ProductStock).join(ProductStock.product).options(
        joinedload(ProductStock.product),
        joinedload(ProductStock.location)
    )
    
    if product_id:
        query = query.filter(ProductStock.product_id == product_id)
    if location_id:
        query = query.filter(ProductStock.location_id == location_id)
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
        
    stocks = query.all()
    
    return create_success_response(data=stocks, message="Stocks fetched successfully")

@router.post("/opname", response_model=SuccessResponse[dict], dependencies=[Depends(RequireRole([RoleType.ADMIN, RoleType.STAFF]))])
def perform_stock_opname(
    request: StockOpnameRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    adjustments_made = 0
    for item in request.items:
        # Get current stock
        stock = db.query(ProductStock).filter(
            ProductStock.product_id == item.product_id,
            ProductStock.location_id == request.location_id
        ).first()
        
        current_qty = stock.quantity if stock else 0
        diff = item.actual_quantity - current_qty
        
        if diff != 0:
            # Create movement record
            movement = ProductMovement(
                product_id=item.product_id,
                type=ProductMovementType.ADJUSTMENT,
                quantity=diff,
                destination_location_id=request.location_id,
                notes="Stock Opname Adjustment",
                user_id=current_user.id
            )
            db.add(movement)
            
            # Update or create stock
            if not stock:
                stock = ProductStock(
                    product_id=item.product_id,
                    location_id=request.location_id,
                    quantity=item.actual_quantity
                )
                db.add(stock)
            else:
                stock.quantity = item.actual_quantity
                
            adjustments_made += 1

    db.commit()
    
    return create_success_response(
        data={"adjustments_made": adjustments_made}, 
        message=f"Stock opname completed. {adjustments_made} adjustments made."
    )
