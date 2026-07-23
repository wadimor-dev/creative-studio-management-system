from typing import List
from sqlalchemy.orm import Session, joinedload
from app.core.exceptions import CSMSException
from app.modules.clinic.models.prescription_item import PrescriptionItem
from app.models.item import Item
from app.modules.clinic.schemas import PrescriptionItemCreate, PrescriptionItemUpdate, PrescriptionItemResponse


class PrescriptionItemService:

    def get_by_id(self, db: Session, item_id: str) -> PrescriptionItemResponse:
        item = db.query(PrescriptionItem).options(
            joinedload(PrescriptionItem.medicine)
        ).filter(PrescriptionItem.id == item_id).first()
        if not item:
            raise CSMSException("Prescription item not found", status_code=404)
        return self._to_response(item)

    def get_by_prescription(self, db: Session, prescription_id: str) -> List[PrescriptionItemResponse]:
        items = db.query(PrescriptionItem).options(
            joinedload(PrescriptionItem.medicine)
        ).filter(PrescriptionItem.prescription_id == prescription_id).all()
        return [self._to_response(item) for item in items]

    def create(self, db: Session, data: PrescriptionItemCreate) -> PrescriptionItemResponse:
        medicine = db.query(Item).filter(Item.id == data.medicine_id).first()
        if not medicine:
            raise CSMSException("Medicine not found in inventory", status_code=404)
        item = PrescriptionItem(**data.model_dump())
        db.add(item)
        db.commit()
        db.refresh(item)
        return self.get_by_id(db, item.id)

    def update(self, db: Session, item_id: str, data: PrescriptionItemUpdate) -> PrescriptionItemResponse:
        item = db.query(PrescriptionItem).filter(PrescriptionItem.id == item_id).first()
        if not item:
            raise CSMSException("Prescription item not found", status_code=404)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return self.get_by_id(db, item.id)

    def delete(self, db: Session, item_id: str) -> None:
        item = db.query(PrescriptionItem).filter(PrescriptionItem.id == item_id).first()
        if not item:
            raise CSMSException("Prescription item not found", status_code=404)
        db.delete(item)
        db.commit()

    def _to_response(self, item: PrescriptionItem) -> PrescriptionItemResponse:
        return PrescriptionItemResponse(
            id=item.id,
            prescription_id=item.prescription_id,
            medicine_id=item.medicine_id,
            dosage=item.dosage,
            frequency=item.frequency,
            duration=item.duration,
            quantity=item.quantity,
            instruction=item.instruction,
            medicine_name=item.medicine.name if item.medicine else None,
        )


prescription_item_service = PrescriptionItemService()
