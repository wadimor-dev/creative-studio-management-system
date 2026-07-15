from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from app.database.session import get_db
from app.models.product_stock import ProductPlacementStock
from app.models.product import Product
from app.schemas.product_placement import ProductPlacementStockResponse
from app.common.responses import SuccessResponse, create_success_response
from app.dependencies.auth import get_current_user
from app.dependencies.permission import RequirePermission
from app.constants.permissions import Permission
from app.models.user import User

router = APIRouter()

@router.get("", response_model=SuccessResponse[List[ProductPlacementStockResponse]])
def get_stocks(
    product_id: Optional[int] = None,
    placement_id: Optional[int] = None,
    type_id: Optional[int] = None,
    category_id: Optional[int] = None,
    motif_id: Optional[int] = None,
    sub_motif_id: Optional[int] = None,
    color_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(ProductPlacementStock).join(ProductPlacementStock.product).options(
        joinedload(ProductPlacementStock.product),
        joinedload(ProductPlacementStock.placement)
    )
    
    if product_id:
        query = query.filter(ProductPlacementStock.product_id == product_id)
    if placement_id:
        query = query.filter(ProductPlacementStock.placement_id == placement_id)
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
