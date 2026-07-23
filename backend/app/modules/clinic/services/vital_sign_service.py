from typing import Optional
from decimal import Decimal
from sqlalchemy.orm import Session
from app.core.exceptions import CSMSException
from app.modules.clinic.models.vital_sign import VitalSign
from app.modules.clinic.schemas import VitalSignCreate, VitalSignUpdate, VitalSignResponse


class VitalSignService:

    def get_by_id(self, db: Session, vs_id: str) -> VitalSignResponse:
        vs = db.query(VitalSign).filter(VitalSign.id == vs_id).first()
        if not vs:
            raise CSMSException("Vital sign not found", status_code=404)
        return VitalSignResponse.model_validate(vs)

    def get_by_visit_id(self, db: Session, visit_id: str) -> Optional[VitalSignResponse]:
        vs = db.query(VitalSign).filter(VitalSign.visit_id == visit_id).first()
        if not vs:
            return None
        return VitalSignResponse.model_validate(vs)

    def create(self, db: Session, data: VitalSignCreate) -> VitalSignResponse:
        existing = db.query(VitalSign).filter(VitalSign.visit_id == data.visit_id).first()
        if existing:
            raise CSMSException("Vital sign already exists for this visit", status_code=409)
        data_dict = data.model_dump()
        height = data_dict.get("height")
        weight = data_dict.get("weight")
        if height and weight and float(height) > 0:
            bmi = round(float(weight) / ((float(height) / 100) ** 2), 2)
            data_dict["bmi"] = Decimal(str(bmi))
        vs = VitalSign(**data_dict)
        db.add(vs)
        db.commit()
        db.refresh(vs)
        return VitalSignResponse.model_validate(vs)

    def update(self, db: Session, vs_id: str, data: VitalSignUpdate) -> VitalSignResponse:
        vs = db.query(VitalSign).filter(VitalSign.id == vs_id).first()
        if not vs:
            raise CSMSException("Vital sign not found", status_code=404)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(vs, field, value)
        if data.height is not None and data.weight is not None and float(data.height) > 0:
            bmi = round(float(data.weight) / ((float(data.height) / 100) ** 2), 2)
            vs.bmi = Decimal(str(bmi))
        elif vs.height and vs.weight and float(vs.height) > 0:
            bmi = round(float(vs.weight) / ((float(vs.height) / 100) ** 2), 2)
            vs.bmi = Decimal(str(bmi))
        db.commit()
        db.refresh(vs)
        return VitalSignResponse.model_validate(vs)

    def upsert(self, db: Session, visit_id: str, data: VitalSignUpdate) -> VitalSignResponse:
        vs = db.query(VitalSign).filter(VitalSign.visit_id == visit_id).first()
        if vs:
            return self.update(db, vs.id, data)
        create_data = VitalSignCreate(visit_id=visit_id, **data.model_dump(exclude_unset=True, exclude={"visit_id"}))
        return self.create(db, create_data)


vital_sign_service = VitalSignService()
