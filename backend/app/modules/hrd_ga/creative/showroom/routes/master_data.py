from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.modules.hrd_ga.creative.showroom.schemas import MasterDataCreate, MasterDataUpdate, SuccessResponse
from app.modules.hrd_ga.creative.showroom.services.master_data_service import MasterDataService

router = APIRouter()


@router.get("/")
def get_master_data(
    type: str = None,
    active_only: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items = MasterDataService.get_all(db, item_type=type, active_only=active_only)
    return SuccessResponse(data=items)


@router.get("/types")
def get_master_types(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return SuccessResponse(data=MasterDataService.VALID_TYPES)


@router.get("/{item_id}")
def get_master_data_by_id(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = MasterDataService.get_by_id(db, item_id)
    return SuccessResponse(data=item)


@router.post("/")
def create_master_data(
    data: MasterDataCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = MasterDataService.create(db, data)
    return SuccessResponse(data=item, message="Master data created")


@router.put("/{item_id}")
def update_master_data(
    item_id: int,
    data: MasterDataUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = MasterDataService.update(db, item_id, data)
    return SuccessResponse(data=item, message="Master data updated")


@router.delete("/{item_id}")
def delete_master_data(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = MasterDataService.delete(db, item_id)
    return SuccessResponse(data=result, message="Master data deleted")


@router.post("/seed")
def seed_master_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = MasterDataService.seed_defaults(db)
    return SuccessResponse(data=result, message="Master data seeded")
