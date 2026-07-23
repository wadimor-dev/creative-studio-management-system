from typing import Optional
from sqlalchemy.orm import Session, joinedload
from app.core.exceptions import CSMSException
from app.modules.hrd_ga.clinic.models.medicine_dispense import MedicineDispense
from app.modules.hrd_ga.clinic.models.prescription_item import PrescriptionItem
from app.modules.hrd_ga.clinic.schemas import MedicineDispenseCreate, MedicineDispenseResponse


class MedicineDispenseService:

    def get_by_id(self, db: Session, dispense_id: str) -> MedicineDispenseResponse:
        disp = db.query(MedicineDispense).filter(MedicineDispense.id == dispense_id).first()
        if not disp:
            raise CSMSException("Dispense record not found", status_code=404)
        return self._to_response(disp)

    def get_by_prescription_item(self, db: Session, item_id: str) -> Optional[MedicineDispenseResponse]:
        disp = db.query(MedicineDispense).filter(
            MedicineDispense.prescription_item_id == item_id
        ).first()
        if not disp:
            return None
        return self._to_response(disp)

    def create(self, db: Session, data: MedicineDispenseCreate) -> MedicineDispenseResponse:
        item = db.query(PrescriptionItem).filter(
            PrescriptionItem.id == data.prescription_item_id
        ).first()
        if not item:
            raise CSMSException("Prescription item not found", status_code=404)
        existing = db.query(MedicineDispense).filter(
            MedicineDispense.prescription_item_id == data.prescription_item_id
        ).first()
        if existing:
            raise CSMSException("Item already dispensed", status_code=409)
        if data.quantity > item.quantity:
            raise CSMSException("Dispense quantity exceeds prescribed quantity", status_code=400)
        disp = MedicineDispense(**data.model_dump())
        db.add(disp)
        db.commit()
        db.refresh(disp)
        return self._to_response(disp)

    def _to_response(self, disp: MedicineDispense) -> MedicineDispenseResponse:
        return MedicineDispenseResponse(
            id=disp.id,
            prescription_item_id=disp.prescription_item_id,
            quantity=disp.quantity,
            dispensed_by=disp.dispensed_by,
            dispensed_at=disp.dispensed_at,
            dispenser_name=None,
        )


medicine_dispense_service = MedicineDispenseService()
