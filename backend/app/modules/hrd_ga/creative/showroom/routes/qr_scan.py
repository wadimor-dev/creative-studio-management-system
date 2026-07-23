from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.orm import Session
import uuid

from app.core.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.modules.hrd_ga.creative.showroom.schemas import SuccessResponse
from app.core.qr.scan_service import QRScanService
from app.core.qr.entity_service import QREntityService

router = APIRouter()


@router.post("/resolve")
def resolve_qr(
    token: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    qr_data = QREntityService.resolve(db, token)
    return SuccessResponse(data=qr_data)


@router.post("/storage-scan")
def storage_scan(
    token: str = Body(...),
    action: str = Body(...),
    product_id: int = Body(None),
    quantity: int = Body(None),
    sample_type: str = Body(None),
    items: list = Body(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    request_id = str(uuid.uuid4())
    qr_data = QREntityService.resolve(db, token)
    return SuccessResponse(data=QRScanService.process_storage_scan(
        db=db,
        qr_data=qr_data,
        action=action,
        product_id=product_id,
        quantity=quantity,
        sample_type=sample_type,
        items=items,
        user_id=current_user.id,
        request_id=request_id,
    ))


@router.post("/product-scan")
def product_scan(
    token: str = Body(...),
    action: str = Body(...),
    storage_location_id: int = Body(None),
    quantity: int = Body(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    qr_data = QREntityService.resolve(db, token)
    return SuccessResponse(data=QRScanService.process_product_scan(
        db=db,
        qr_data=qr_data,
        action=action,
        storage_location_id=storage_location_id,
        quantity=quantity,
        user_id=current_user.id,
    ))
