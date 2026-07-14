from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List

from app.database.session import get_db
from app.models.product import Product
from app.models.product_master import ProductType, ProductCategory, ProductMotif, ProductSubMotif, ProductColor
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.common.responses import SuccessResponse, create_success_response
from app.common.pagination import PaginatedResponse, create_paginated_response, PaginationParams
from app.dependencies.permission import RequireRole
from app.constants.role import RoleType
from app.exceptions.base import CSMSException

router = APIRouter()

def _generate_product_identity(db: Session, product_in, product_id: int = 0):
    """Helper to fetch master data and generate SKU and Display Name"""
    p_type = db.query(ProductType).filter(ProductType.id == product_in.type_id).first()
    category = db.query(ProductCategory).filter(ProductCategory.id == product_in.category_id).first()
    motif = db.query(ProductMotif).filter(ProductMotif.id == product_in.motif_id).first()
    color = db.query(ProductColor).filter(ProductColor.id == product_in.color_id).first()
    
    if not all([p_type, category, motif, color]):
        raise CSMSException("Invalid master data ID provided", status_code=400)
        
    sub_motif = None
    if product_in.sub_motif_id:
        sub_motif = db.query(ProductSubMotif).filter(ProductSubMotif.id == product_in.sub_motif_id).first()
        if not sub_motif:
            raise CSMSException("Invalid sub_motif_id provided", status_code=400)

    # 1. Generate Display Name
    name_parts = [p_type.name, category.name, motif.name]
    if sub_motif:
        name_parts.append(sub_motif.name)
    name_parts.append(color.name)
    if product_in.variant:
        name_parts.append(product_in.variant)
        
    display_name = " ".join(name_parts)

    # 2. Generate SKU Prefix
    sku_parts = [p_type.code, category.code, motif.code]
    if sub_motif:
        sku_parts.append(sub_motif.code)
    sku_parts.append(color.code)
    if product_in.variant:
        # Use first 3 letters of variant as code, upper cased
        sku_parts.append(product_in.variant[:3].upper())
        
    sku_prefix = "-".join(sku_parts)
    sku = f"{sku_prefix}-{product_id:04d}" if product_id > 0 else f"{sku_prefix}-TBD"
    
    return sku, display_name


@router.get("", response_model=PaginatedResponse[ProductResponse])
def get_products(
    type_id: int = None,
    category_id: int = None,
    motif_id: int = None,
    sub_motif_id: int = None,
    color_id: int = None,
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends()
):
    query = db.query(Product).options(
        joinedload(Product.type),
        joinedload(Product.category),
        joinedload(Product.motif),
        joinedload(Product.sub_motif),
        joinedload(Product.color)
    )
    
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
        
    total = query.count()
    items = query.offset(pagination.skip).limit(pagination.size).all()
    
    return create_paginated_response(
        data=items,
        total=total,
        page=pagination.page,
        size=pagination.size,
        message="Products fetched successfully"
    )

@router.post("", response_model=SuccessResponse[ProductResponse], status_code=status.HTTP_201_CREATED, dependencies=[Depends(RequireRole([RoleType.ADMIN, RoleType.STAFF]))])
def create_product(product_in: ProductCreate, db: Session = Depends(get_db)):
    # Validate and generate temp SKU & name
    _, display_name = _generate_product_identity(db, product_in, 0)
    
    # Create product without final SKU (using a temp one to satisfy NOT NULL constraint if needed, but we can flush first)
    product = Product(**product_in.model_dump(), sku="TEMP", display_name=display_name)
    db.add(product)
    db.flush() # Get the auto-incremented ID
    
    # Generate final SKU with the ID
    final_sku, _ = _generate_product_identity(db, product_in, product.id)
    product.sku = final_sku
    
    db.commit()
    db.refresh(product)
    return create_success_response(data=product, message="Product created successfully")

@router.put("/{product_id}", response_model=SuccessResponse[ProductResponse], dependencies=[Depends(RequireRole([RoleType.ADMIN, RoleType.STAFF]))])
def update_product(product_id: int, product_in: ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise CSMSException("Product not found", status_code=404)
        
    update_data = product_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)
        
    # If any master data relation or variant changed, we need to regenerate the name and SKU
    if any(k in update_data for k in ['type_id', 'category_id', 'motif_id', 'sub_motif_id', 'color_id', 'variant']):
        # Create a mock object that combines existing data with new updates to pass to the generator
        class MockProduct:
            pass
        mock_p = MockProduct()
        mock_p.type_id = product.type_id
        mock_p.category_id = product.category_id
        mock_p.motif_id = product.motif_id
        mock_p.sub_motif_id = product.sub_motif_id
        mock_p.color_id = product.color_id
        mock_p.variant = product.variant
        
        final_sku, display_name = _generate_product_identity(db, mock_p, product.id)
        product.sku = final_sku
        product.display_name = display_name

    db.commit()
    db.refresh(product)
    return create_success_response(data=product, message="Product updated successfully")

@router.delete("/{product_id}", response_model=SuccessResponse[dict], dependencies=[Depends(RequireRole([RoleType.ADMIN]))])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise CSMSException("Product not found", status_code=404)
        
    db.delete(product)
    db.commit()
    return create_success_response(data=None, message="Product deleted successfully")
