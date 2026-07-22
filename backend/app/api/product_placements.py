from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database.session import get_db
from app.models.product_placement import ProductPlacement, PlacementType
from app.schemas.product_placement import (
    ProductPlacementCreate,
    ProductPlacementUpdate,
    ProductPlacementResponse,
    ProductPlacementHierarchyResponse,
    PlacementTypeResponse,
    PlacementTypeCreate,
    PlacementTypeUpdate
)
from app.common.responses import SuccessResponse, create_success_response
from app.core.exceptions import CSMSException
from app.dependencies.permission import RequirePermission
from app.constants.permissions import Permission

router = APIRouter()

# --- Placement Types ---

@router.get("/types", response_model=SuccessResponse[List[PlacementTypeResponse]])
def get_placement_types(db: Session = Depends(get_db)):
    types = db.query(PlacementType).all()
    return create_success_response(data=types, message="Placement types fetched successfully")

@router.post("/types", response_model=SuccessResponse[PlacementTypeResponse])
def create_placement_type(type_in: PlacementTypeCreate, db: Session = Depends(get_db)):
    existing = db.query(PlacementType).filter(PlacementType.name == type_in.name).first()
    if existing:
        raise CSMSException(f"Placement type '{type_in.name}' already exists", status_code=400)
        
    placement_type = PlacementType(**type_in.model_dump())
    db.add(placement_type)
    db.commit()
    db.refresh(placement_type)
    return create_success_response(data=placement_type, message="Placement type created successfully")

@router.put("/types/{type_id}", response_model=SuccessResponse[PlacementTypeResponse])
def update_placement_type(type_id: int, type_in: PlacementTypeUpdate, db: Session = Depends(get_db)):
    placement_type = db.query(PlacementType).filter(PlacementType.id == type_id).first()
    if not placement_type:
        raise CSMSException("Placement type not found", status_code=404)
        
    if type_in.name:
        existing = db.query(PlacementType).filter(PlacementType.name == type_in.name, PlacementType.id != type_id).first()
        if existing:
            raise CSMSException(f"Placement type '{type_in.name}' already exists", status_code=400)
            
    update_data = type_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(placement_type, key, value)
        
    db.commit()
    db.refresh(placement_type)
    return create_success_response(data=placement_type, message="Placement type updated successfully")

# --- Product Placements ---

@router.get("", response_model=SuccessResponse[List[ProductPlacementResponse]])
def get_product_placements(db: Session = Depends(get_db)):
    placements = db.query(ProductPlacement).all()
    return create_success_response(data=placements, message="Product placements fetched successfully")

@router.get("/hierarchy", response_model=SuccessResponse[List[ProductPlacementHierarchyResponse]])
def get_product_placements_hierarchy(db: Session = Depends(get_db)):
    placements = db.query(ProductPlacement).filter(ProductPlacement.parent_id == None).all()
    return create_success_response(data=placements, message="Product placements hierarchy fetched successfully")

@router.post("", response_model=SuccessResponse[ProductPlacementResponse])
def create_product_placement(placement_in: ProductPlacementCreate, db: Session = Depends(get_db)):
    if placement_in.code:
        existing = db.query(ProductPlacement).filter(ProductPlacement.code == placement_in.code).first()
        if existing:
            raise CSMSException(f"Product placement with code '{placement_in.code}' already exists", status_code=400)
            
    # Verify type exists
    type_exists = db.query(PlacementType).filter(PlacementType.id == placement_in.type_id).first()
    if not type_exists:
        raise CSMSException(f"Placement type ID {placement_in.type_id} not found", status_code=400)

    placement = ProductPlacement(**placement_in.model_dump())
    db.add(placement)
    db.commit()
    db.refresh(placement)
    return create_success_response(data=placement, message="Product placement created successfully")

@router.put("/{placement_id}", response_model=SuccessResponse[ProductPlacementResponse])
def update_product_placement(placement_id: int, placement_in: ProductPlacementUpdate, db: Session = Depends(get_db)):
    placement = db.query(ProductPlacement).filter(ProductPlacement.id == placement_id).first()
    if not placement:
        raise CSMSException("Product placement not found", status_code=404)
        
    if placement_in.code:
        existing = db.query(ProductPlacement).filter(ProductPlacement.code == placement_in.code, ProductPlacement.id != placement_id).first()
        if existing:
            raise CSMSException(f"Product placement with code '{placement_in.code}' already exists", status_code=400)
            
    if placement_in.type_id:
        type_exists = db.query(PlacementType).filter(PlacementType.id == placement_in.type_id).first()
        if not type_exists:
            raise CSMSException(f"Placement type ID {placement_in.type_id} not found", status_code=400)
            
    update_data = placement_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(placement, key, value)
        
    db.commit()
    db.refresh(placement)
    return create_success_response(data=placement, message="Product placement updated successfully")

@router.delete("/{placement_id}", response_model=SuccessResponse[dict])
def delete_product_placement(placement_id: int, db: Session = Depends(get_db)):
    placement = db.query(ProductPlacement).filter(ProductPlacement.id == placement_id).first()
    if not placement:
        raise CSMSException("Product placement not found", status_code=404)
        
    if placement.children:
         raise CSMSException("Cannot delete placement with sub-placements. Delete them first.", status_code=400)
         
    from app.models.product_stock import ProductPlacementStock
    stocks = db.query(ProductPlacementStock).filter(ProductPlacementStock.placement_id == placement_id, ProductPlacementStock.quantity > 0).first()
    if stocks:
         raise CSMSException("Cannot delete placement with existing stock. Please move stock first.", status_code=400)
         
    db.delete(placement)
    db.commit()
    return create_success_response(data=None, message="Product placement deleted successfully")
