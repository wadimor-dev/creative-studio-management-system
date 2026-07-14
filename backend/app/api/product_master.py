from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Type, Any

from app.database.session import get_db
from app.models.product_master import ProductType, ProductCategory, ProductMotif, ProductSubMotif, ProductColor
from app.schemas.product_master import ProductMasterCreate, ProductMasterUpdate, ProductMasterResponse
from app.common.responses import SuccessResponse, create_success_response
from app.dependencies.permission import RequirePermission
from app.constants.permissions import Permission
from app.exceptions.base import CSMSException

router = APIRouter()

def _get_model(entity_type: str) -> Type[Any]:
    mapping = {
        "types": ProductType,
        "categories": ProductCategory,
        "motifs": ProductMotif,
        "sub-motifs": ProductSubMotif,
        "colors": ProductColor
    }
    if entity_type not in mapping:
        raise CSMSException(f"Invalid entity type: {entity_type}", status_code=400)
    return mapping[entity_type]

@router.get("/{entity_type}", response_model=SuccessResponse[List[ProductMasterResponse]], dependencies=[Depends(RequirePermission(Permission.PRODUCT_MASTER_VIEW))])
def get_master_data(entity_type: str, db: Session = Depends(get_db)):
    model = _get_model(entity_type)
    items = db.query(model).all()
    return create_success_response(data=items, message=f"{entity_type.capitalize()} fetched successfully")

@router.post("/{entity_type}", response_model=SuccessResponse[ProductMasterResponse], dependencies=[Depends(RequirePermission(Permission.PRODUCT_MASTER_CREATE))])
def create_master_data(entity_type: str, item_in: ProductMasterCreate, db: Session = Depends(get_db)):
    model = _get_model(entity_type)
    
    # Check uniqueness
    existing_name = db.query(model).filter(model.name == item_in.name).first()
    if existing_name:
        raise CSMSException(f"{entity_type.capitalize()} with name '{item_in.name}' already exists", status_code=400)
        
    existing_code = db.query(model).filter(model.code == item_in.code).first()
    if existing_code:
        raise CSMSException(f"{entity_type.capitalize()} with code '{item_in.code}' already exists", status_code=400)
    
    item = model(**item_in.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return create_success_response(data=item, message=f"{entity_type.capitalize()} created successfully")

@router.put("/{entity_type}/{item_id}", response_model=SuccessResponse[ProductMasterResponse], dependencies=[Depends(RequirePermission(Permission.PRODUCT_MASTER_UPDATE))])
def update_master_data(entity_type: str, item_id: int, item_in: ProductMasterUpdate, db: Session = Depends(get_db)):
    model = _get_model(entity_type)
    item = db.query(model).filter(model.id == item_id).first()
    if not item:
        raise CSMSException(f"{entity_type.capitalize()} not found", status_code=404)
        
    if item_in.name and item_in.name != item.name:
        existing = db.query(model).filter(model.name == item_in.name).first()
        if existing:
            raise CSMSException(f"{entity_type.capitalize()} with name '{item_in.name}' already exists", status_code=400)
            
    if item_in.code and item_in.code != item.code:
        existing = db.query(model).filter(model.code == item_in.code).first()
        if existing:
            raise CSMSException(f"{entity_type.capitalize()} with code '{item_in.code}' already exists", status_code=400)
            
    update_data = item_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
        
    db.commit()
    db.refresh(item)
    return create_success_response(data=item, message=f"{entity_type.capitalize()} updated successfully")

@router.delete("/{entity_type}/{item_id}", response_model=SuccessResponse[dict], dependencies=[Depends(RequirePermission(Permission.PRODUCT_MASTER_DELETE))])
def delete_master_data(entity_type: str, item_id: int, db: Session = Depends(get_db)):
    model = _get_model(entity_type)
    item = db.query(model).filter(model.id == item_id).first()
    if not item:
        raise CSMSException(f"{entity_type.capitalize()} not found", status_code=404)
        
    db.delete(item)
    db.commit()
    return create_success_response(data=None, message=f"{entity_type.capitalize()} deleted successfully")
