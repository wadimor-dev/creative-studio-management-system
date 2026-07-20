from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.showroom_location import ShowroomLocation
from app.modules.showroom_v2.schemas import (
    HandoverCreate, TransferCreate, BorrowCreate, ReturnCreate, AdjustCreate,
    LocationCreate, LocationUpdate, LocationResponse, SuccessResponse,
)
from app.modules.showroom_v2.services.sample_service import SampleService

router = APIRouter()


@router.get("/stock")
def get_stock(
    location_id: int = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if location_id:
        stock = SampleService.get_stock_by_location(db, location_id)
    else:
        stock = SampleService.get_stock_summary(db)
    return SuccessResponse(data=stock)


@router.get("/stock/{product_id}")
def get_stock_by_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stock = SampleService.get_stock_by_location(db)
    filtered = [s for s in stock if s.get("product_id") == product_id]
    return SuccessResponse(data=filtered)


@router.post("/handover")
def handover(
    data: HandoverCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = SampleService.handover_from_inventory(db, data, current_user.id)
    return SuccessResponse(data=result, message="Handover completed")


@router.post("/transfer")
def transfer(
    data: TransferCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = SampleService.transfer_stock(db, data, current_user.id)
    return SuccessResponse(data=result, message="Transfer completed")


@router.post("/borrow")
def borrow(
    data: BorrowCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = SampleService.borrow_sample(db, data, current_user.id)
    return SuccessResponse(data=result, message="Borrow completed")


@router.post("/return/{borrowing_id}")
def return_sample(
    borrowing_id: int,
    data: ReturnCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = SampleService.return_sample(db, borrowing_id, data, current_user.id)
    return SuccessResponse(data=result, message="Return completed")


@router.post("/adjust")
def adjust(
    data: AdjustCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = SampleService.adjust_stock(db, data, current_user.id)
    return SuccessResponse(data=result, message="Adjustment completed")


@router.get("/locations")
def get_locations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    locations = SampleService.get_locations(db)
    data = [{"id": l.id, "code": l.code, "name": l.name, "type": l.type, "description": l.description, "image_url": l.image_url} for l in locations]
    return SuccessResponse(data=data)


@router.get("/movements")
def get_movements(
    product_id: int = Query(None),
    movement_type: str = Query(None),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    movements = SampleService.get_movements(db, product_id, movement_type, limit)
    return SuccessResponse(data=movements)


@router.get("/locations-all")
def get_all_locations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    locations = db.query(ShowroomLocation).order_by(ShowroomLocation.code).all()
    data = [LocationResponse.model_validate(l).model_dump() for l in locations]
    return SuccessResponse(data=data)


@router.post("/locations")
def create_location(
    data: LocationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = db.query(ShowroomLocation).filter(ShowroomLocation.code == data.code).first()
    if existing:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=f"Kode lokasi '{data.code}' sudah digunakan")

    location = ShowroomLocation(code=data.code, name=data.name, type=data.type, description=data.description, image_url=data.image_url)
    db.add(location)
    db.commit()
    db.refresh(location)
    return SuccessResponse(data=LocationResponse.model_validate(location).model_dump(), message="Lokasi berhasil dibuat")


@router.put("/locations/{location_id}")
def update_location(
    location_id: int,
    data: LocationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from fastapi import HTTPException
    location = db.query(ShowroomLocation).filter(ShowroomLocation.id == location_id).first()
    if not location:
        raise HTTPException(status_code=404, detail="Lokasi tidak ditemukan")

    if data.code and data.code != location.code:
        dup = db.query(ShowroomLocation).filter(ShowroomLocation.code == data.code, ShowroomLocation.id != location_id).first()
        if dup:
            raise HTTPException(status_code=400, detail=f"Kode lokasi '{data.code}' sudah digunakan")

    for field in ["code", "name", "type", "description", "image_url", "is_active"]:
        val = getattr(data, field)
        if val is not None:
            setattr(location, field, val)

    db.commit()
    db.refresh(location)
    return SuccessResponse(data=LocationResponse.model_validate(location).model_dump(), message="Lokasi berhasil diupdate")


@router.delete("/locations/{location_id}")
def delete_location(
    location_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from fastapi import HTTPException
    from app.models.showroom_sample_stock import ShowroomSampleStock

    location = db.query(ShowroomLocation).filter(ShowroomLocation.id == location_id).first()
    if not location:
        raise HTTPException(status_code=404, detail="Lokasi tidak ditemukan")

    has_stock = db.query(ShowroomSampleStock).filter(ShowroomSampleStock.location_id == location_id).first()
    if has_stock:
        raise HTTPException(status_code=400, detail="Tidak bisa menghapus lokasi yang masih memiliki stok")

    db.delete(location)
    db.commit()
    return SuccessResponse(message="Lokasi berhasil dihapus")
