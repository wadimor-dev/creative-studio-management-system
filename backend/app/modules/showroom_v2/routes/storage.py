from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.modules.showroom_v2.schemas import SuccessResponse
from app.modules.showroom_v2.services.storage_service import StorageService
from app.modules.showroom_v2.services.qr_entity_service import QREntityService

router = APIRouter()


@router.get("")
def list_storage(
    location_id: int = Query(None),
    parent_id: int = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return SuccessResponse(data=StorageService.get_all(db, location_id=location_id, parent_id=parent_id))


@router.get("/tree")
def get_tree(
    location_id: int = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return SuccessResponse(data=StorageService.get_tree(db, location_id=location_id))


@router.get("/qr")
@router.get("/qr/all")
def list_qr_entities(
    entity_type: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return SuccessResponse(data=QREntityService.get_all(db, entity_type=entity_type))


@router.get("/qr/{qr_id}")
def get_qr_entity(
    qr_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return SuccessResponse(data=QREntityService.get_by_id(db, qr_id))


@router.post("/qr")
def create_qr_entity(
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return SuccessResponse(data=QREntityService.create(db, data, current_user.id), message="QR entity created")


@router.put("/qr/{qr_id}")
def update_qr_entity(
    qr_id: int,
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return SuccessResponse(data=QREntityService.update(db, qr_id, data, current_user.id), message="QR entity updated")


@router.delete("/qr/{qr_id}")
def delete_qr_entity(
    qr_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return SuccessResponse(data=QREntityService.delete(db, qr_id, current_user.id), message="QR entity deleted")


@router.get("/{storage_id}")
def get_storage(
    storage_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return SuccessResponse(data=StorageService.get_by_id(db, storage_id))


@router.post("")
def create_storage(
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return SuccessResponse(data=StorageService.create(db, data, current_user.id), message="Storage location created")


@router.put("/{storage_id}")
def update_storage(
    storage_id: int,
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return SuccessResponse(data=StorageService.update(db, storage_id, data, current_user.id), message="Storage location updated")


@router.delete("/{storage_id}")
def delete_storage(
    storage_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return SuccessResponse(data=StorageService.delete(db, storage_id, current_user.id), message="Storage location deleted")
