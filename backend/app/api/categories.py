from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.common.responses import SuccessResponse, create_success_response
from app.dependencies.permission import RequireRole
from app.constants.role import RoleType
from app.exceptions.base import CSMSException

router = APIRouter()

@router.get("", response_model=SuccessResponse[List[CategoryResponse]])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return create_success_response(data=categories, message="Categories fetched successfully")

@router.post("", response_model=SuccessResponse[CategoryResponse], dependencies=[Depends(RequireRole([RoleType.ADMIN, RoleType.STAFF]))])
def create_category(category_in: CategoryCreate, db: Session = Depends(get_db)):
    existing = db.query(Category).filter(Category.name == category_in.name).first()
    if existing:
        raise CSMSException(f"Category with name '{category_in.name}' already exists", status_code=400)
    
    category = Category(**category_in.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return create_success_response(data=category, message="Category created successfully")

@router.put("/{category_id}", response_model=SuccessResponse[CategoryResponse], dependencies=[Depends(RequireRole([RoleType.ADMIN, RoleType.STAFF]))])
def update_category(category_id: int, category_in: CategoryUpdate, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise CSMSException("Category not found", status_code=404)
        
    if category_in.name:
        existing = db.query(Category).filter(Category.name == category_in.name, Category.id != category_id).first()
        if existing:
            raise CSMSException(f"Category with name '{category_in.name}' already exists", status_code=400)
            
    update_data = category_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(category, key, value)
        
    db.commit()
    db.refresh(category)
    return create_success_response(data=category, message="Category updated successfully")

@router.delete("/{category_id}", response_model=SuccessResponse[dict], dependencies=[Depends(RequireRole([RoleType.ADMIN]))])
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise CSMSException("Category not found", status_code=404)
        
    db.delete(category)
    db.commit()
    return create_success_response(data=None, message="Category deleted successfully")
