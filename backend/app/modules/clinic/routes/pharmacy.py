from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.common.responses import create_success_response
from app.core.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.modules.clinic.schemas import (
    PrescriptionCreate, PrescriptionUpdate,
    PrescriptionItemCreate, PrescriptionItemUpdate,
    MedicineDispenseCreate,
)
from app.modules.clinic.services import (
    prescription_service, prescription_item_service, medicine_dispense_service,
)

router = APIRouter()


# ──────── PRESCRIPTIONS ────────

@router.get("/prescriptions/{rx_id}", tags=["clinic-prescriptions"])
def get_prescription(rx_id: str, db: Session = Depends(get_db)):
    data = prescription_service.get_by_id(db, rx_id)
    return create_success_response(data=data.model_dump())

@router.get("/prescriptions/by-visit/{visit_id}", tags=["clinic-prescriptions"])
def get_prescription_by_visit(visit_id: str, db: Session = Depends(get_db)):
    data = prescription_service.get_by_visit_id(db, visit_id)
    return create_success_response(data=data.model_dump() if data else None)

@router.post("/prescriptions", status_code=status.HTTP_201_CREATED, tags=["clinic-prescriptions"])
def create_prescription(body: PrescriptionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = prescription_service.create(db, body)
    return create_success_response(data=data.model_dump(), message="Prescription created")

@router.put("/prescriptions/{rx_id}", tags=["clinic-prescriptions"])
def update_prescription(rx_id: str, body: PrescriptionUpdate, db: Session = Depends(get_db)):
    data = prescription_service.update(db, rx_id, body)
    return create_success_response(data=data.model_dump(), message="Prescription updated")

@router.put("/prescriptions/{rx_id}/dispense", tags=["clinic-prescriptions"])
def dispense_prescription(rx_id: str, db: Session = Depends(get_db)):
    data = prescription_service.dispense(db, rx_id)
    return create_success_response(data=data.model_dump(), message="Prescription dispensed")

@router.put("/prescriptions/{rx_id}/cancel", tags=["clinic-prescriptions"])
def cancel_prescription(rx_id: str, db: Session = Depends(get_db)):
    data = prescription_service.cancel(db, rx_id)
    return create_success_response(data=data.model_dump(), message="Prescription cancelled")


# ──────── PRESCRIPTION ITEMS ────────

@router.get("/prescription-items/by-prescription/{rx_id}", tags=["clinic-prescription-items"])
def get_items_by_prescription(rx_id: str, db: Session = Depends(get_db)):
    items = prescription_item_service.get_by_prescription(db, rx_id)
    return create_success_response(data=[item.model_dump() for item in items])

@router.post("/prescription-items", status_code=status.HTTP_201_CREATED, tags=["clinic-prescription-items"])
def create_prescription_item(body: PrescriptionItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = prescription_item_service.create(db, body)
    return create_success_response(data=data.model_dump(), message="Item added to prescription")

@router.put("/prescription-items/{item_id}", tags=["clinic-prescription-items"])
def update_prescription_item(item_id: str, body: PrescriptionItemUpdate, db: Session = Depends(get_db)):
    data = prescription_item_service.update(db, item_id, body)
    return create_success_response(data=data.model_dump(), message="Item updated")

@router.delete("/prescription-items/{item_id}", tags=["clinic-prescription-items"])
def delete_prescription_item(item_id: str, db: Session = Depends(get_db)):
    prescription_item_service.delete(db, item_id)
    return create_success_response(message="Item removed from prescription")


# ──────── MEDICINE DISPENSES ────────

@router.get("/medicine-dispenses/{dispense_id}", tags=["clinic-dispenses"])
def get_dispense(dispense_id: str, db: Session = Depends(get_db)):
    data = medicine_dispense_service.get_by_id(db, dispense_id)
    return create_success_response(data=data.model_dump())

@router.post("/medicine-dispenses", status_code=status.HTTP_201_CREATED, tags=["clinic-dispenses"])
def create_dispense(body: MedicineDispenseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = medicine_dispense_service.create(db, body)
    return create_success_response(data=data.model_dump(), message="Medicine dispensed")
