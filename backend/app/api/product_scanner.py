from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database.session import get_db
from app.models.product_placement import ProductPlacement
from app.schemas.product_placement import ProductPlacementResponse
from app.common.responses import SuccessResponse, create_success_response
from app.core.exceptions import CSMSException
from app.models.product_stock import ProductPlacementStock
from app.models.product import Product

router = APIRouter()

@router.get("/{code}", response_model=SuccessResponse[dict])
def resolve_scanner_code(
    code: str,
    db: Session = Depends(get_db)
):
    """
    Resolve a scanned code. It could be a placement or a product.
    """
    # 1. Try to find a placement with this code
    placement = db.query(ProductPlacement).filter(ProductPlacement.code == code).first()
    if placement:
        stocks = db.query(ProductPlacementStock).filter(
            ProductPlacementStock.placement_id == placement.id,
            ProductPlacementStock.quantity > 0
        ).all()
        
        stock_data = []
        for stock in stocks:
            stock_data.append({
                "product_id": stock.product.id,
                "product_name": stock.product.display_name,
                "sku": stock.product.sku,
                "quantity": stock.quantity,
                "reserved_quantity": stock.reserved_quantity
            })
            
        return create_success_response(
            data={
                "type": "placement",
                "id": placement.id,
                "code": placement.code,
                "name": placement.name,
                "level": placement.level,
                "stocks": stock_data
            },
            message="Code resolved to a placement"
        )
        
    # 2. Try to find a product with this sku or barcode
    from app.models.product import Product
    product = db.query(Product).filter(Product.sku == code).first()
    if product:
        return create_success_response(
            data={
                "type": "product",
                "id": product.id,
                "sku": product.sku,
                "display_name": product.display_name,
            },
            message="Code resolved to a product"
        )
        
    raise CSMSException(f"Code '{code}' not recognized as a valid placement or product.", status_code=404)
