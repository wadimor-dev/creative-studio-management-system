from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database.session import get_db
from app.models.location import Location
from app.schemas.location import LocationCreate, LocationUpdate, LocationResponse
from app.common.responses import SuccessResponse, create_success_response
from app.common.pagination import PaginatedResponse, create_paginated_response, PaginationParams
from app.dependencies.permission import RequirePermission
from app.constants.permissions import Permission
from app.core.exceptions import CSMSException

router = APIRouter()

@router.get("", response_model=PaginatedResponse[LocationResponse], dependencies=[Depends(RequirePermission(Permission.LOCATION_VIEW))])
def get_locations(db: Session = Depends(get_db), pagination: PaginationParams = Depends()):
    query = db.query(Location)
    total = query.count()
    if pagination.size == 0:
        items = query.all()
    else:
        items = query.offset(pagination.skip).limit(pagination.size).all()
    return create_paginated_response(data=items, total=total, page=pagination.page, size=pagination.size if pagination.size > 0 else total,
                                      message="Locations fetched successfully")

@router.post("", response_model=SuccessResponse[LocationResponse], dependencies=[Depends(RequirePermission(Permission.LOCATION_CREATE))])
def create_location(location_in: LocationCreate, db: Session = Depends(get_db)):
    existing_name = db.query(Location).filter(Location.name == location_in.name).first()
    if existing_name:
        raise CSMSException(f"Location with name '{location_in.name}' already exists", status_code=400)
    
    location = Location(**location_in.model_dump())
    db.add(location)
    db.commit()
    db.refresh(location)
    return create_success_response(data=location, message="Location created successfully")

@router.put("/{location_id}", response_model=SuccessResponse[LocationResponse], dependencies=[Depends(RequirePermission(Permission.LOCATION_UPDATE))])
def update_location(location_id: int, location_in: LocationUpdate, db: Session = Depends(get_db)):
    location = db.query(Location).filter(Location.id == location_id).first()
    if not location:
        raise CSMSException("Location not found", status_code=404)
        
    if location_in.name:
        existing_name = db.query(Location).filter(Location.name == location_in.name, Location.id != location_id).first()
        if existing_name:
            raise CSMSException(f"Location with name '{location_in.name}' already exists", status_code=400)
            
    update_data = location_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(location, key, value)
        
    db.commit()
    db.refresh(location)
    return create_success_response(data=location, message="Location updated successfully")

@router.delete("/{location_id}", response_model=SuccessResponse[dict], dependencies=[Depends(RequirePermission(Permission.LOCATION_DELETE))])
def delete_location(location_id: int, db: Session = Depends(get_db)):
    location = db.query(Location).filter(Location.id == location_id).first()
    if not location:
        raise CSMSException("Location not found", status_code=404)
        
    # Later check if it has WorkAsset items before deleting
    
    db.delete(location)
    db.commit()
    return create_success_response(data=None, message="Location deleted successfully")
