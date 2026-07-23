from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from app.core.exceptions import CSMSException
from app.modules.clinic.models.prescription import Prescription, PrescriptionStatus
from app.modules.clinic.models.prescription_item import PrescriptionItem
from app.modules.clinic.schemas import (
    PrescriptionCreate, PrescriptionUpdate, PrescriptionResponse,
    PrescriptionItemResponse,
)
from app.modules.clinic.services.prescription_item_service import prescription_item_service


class PrescriptionService:

    def get_by_id(self, db: Session, rx_id: str) -> PrescriptionResponse:
        rx = db.query(Prescription).options(
            joinedload(Prescription.items).joinedload(PrescriptionItem.medicine),
        ).filter(Prescription.id == rx_id).first()
        if not rx:
            raise CSMSException("Prescription not found", status_code=404)
        return self._to_response(rx)

    def get_by_visit_id(self, db: Session, visit_id: str) -> Optional[PrescriptionResponse]:
        rx = db.query(Prescription).options(
            joinedload(Prescription.items).joinedload(PrescriptionItem.medicine),
        ).filter(Prescription.visit_id == visit_id).first()
        if not rx:
            return None
        return self._to_response(rx)

    def create(self, db: Session, data: PrescriptionCreate) -> PrescriptionResponse:
        existing = db.query(Prescription).filter(Prescription.visit_id == data.visit_id).first()
        if existing:
            raise CSMSException("Prescription already exists for this visit", status_code=409)
        rx = Prescription(**data.model_dump())
        db.add(rx)
        db.commit()
        db.refresh(rx)
        return self.get_by_id(db, rx.id)

    def update(self, db: Session, rx_id: str, data: PrescriptionUpdate) -> PrescriptionResponse:
        rx = db.query(Prescription).filter(Prescription.id == rx_id).first()
        if not rx:
            raise CSMSException("Prescription not found", status_code=404)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(rx, field, value)
        db.commit()
        db.refresh(rx)
        return self.get_by_id(db, rx.id)

    def dispense(self, db: Session, rx_id: str) -> PrescriptionResponse:
        rx = db.query(Prescription).filter(Prescription.id == rx_id).first()
        if not rx:
            raise CSMSException("Prescription not found", status_code=404)
        rx.status = PrescriptionStatus.DISPENSED
        db.commit()
        db.refresh(rx)
        return self.get_by_id(db, rx.id)

    def cancel(self, db: Session, rx_id: str) -> PrescriptionResponse:
        return self.update(db, rx_id, PrescriptionUpdate(status=PrescriptionStatus.CANCELLED))

    def _to_response(self, rx: Prescription) -> PrescriptionResponse:
        items = [prescription_item_service._to_response(item) for item in (rx.items or [])]
        return PrescriptionResponse(
            id=rx.id,
            visit_id=rx.visit_id,
            healthcare_professional_id=rx.healthcare_professional_id,
            prescription_date=rx.prescription_date,
            status=rx.status,
            doctor_name=None,
            items=items,
        )


prescription_service = PrescriptionService()
