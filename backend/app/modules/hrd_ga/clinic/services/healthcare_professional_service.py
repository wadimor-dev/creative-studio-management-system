from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from app.core.exceptions import CSMSException
from app.modules.hrd_ga.clinic.models.healthcare_professional import HealthcareProfessional
from app.modules.hrd_ga.clinic.models.healthcare_professional import Profession, ProfessionalStatus
from app.modules.hrd_ga.clinic.schemas import HealthcareProfessionalCreate, HealthcareProfessionalUpdate, HealthcareProfessionalResponse


class HealthcareProfessionalService:

    def get_all(self, db: Session, skip: int = 0, limit: int = 100,
                profession: Optional[Profession] = None,
                status: Optional[ProfessionalStatus] = None) -> List[HealthcareProfessionalResponse]:
        query = db.query(HealthcareProfessional).options(joinedload(HealthcareProfessional.employee))
        if profession:
            query = query.filter(HealthcareProfessional.profession == profession)
        if status:
            query = query.filter(HealthcareProfessional.status == status)
        items = query.offset(skip).limit(limit).all()
        return [self._to_response(hp) for hp in items]

    def get_by_id(self, db: Session, hp_id: str) -> HealthcareProfessionalResponse:
        hp = db.query(HealthcareProfessional).options(joinedload(HealthcareProfessional.employee)).filter(
            HealthcareProfessional.id == hp_id
        ).first()
        if not hp:
            raise CSMSException("Healthcare professional not found", status_code=404)
        return self._to_response(hp)

    def get_by_employee_id(self, db: Session, employee_id: int) -> Optional[HealthcareProfessionalResponse]:
        hp = db.query(HealthcareProfessional).options(joinedload(HealthcareProfessional.employee)).filter(
            HealthcareProfessional.employee_id == employee_id
        ).first()
        if not hp:
            return None
        return self._to_response(hp)

    def create(self, db: Session, data: HealthcareProfessionalCreate) -> HealthcareProfessionalResponse:
        existing = db.query(HealthcareProfessional).filter(
            HealthcareProfessional.employee_id == data.employee_id
        ).first()
        if existing:
            raise CSMSException("Employee is already registered as healthcare professional", status_code=409)
        hp = HealthcareProfessional(**data.model_dump())
        db.add(hp)
        db.commit()
        db.refresh(hp)
        return self._to_response(hp)

    def update(self, db: Session, hp_id: str, data: HealthcareProfessionalUpdate) -> HealthcareProfessionalResponse:
        hp = self._get_orm(db, hp_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(hp, field, value)
        db.commit()
        db.refresh(hp)
        return self._to_response(hp)

    def delete(self, db: Session, hp_id: str) -> None:
        hp = self._get_orm(db, hp_id)
        db.delete(hp)
        db.commit()

    def _get_orm(self, db: Session, hp_id: str) -> HealthcareProfessional:
        hp = db.query(HealthcareProfessional).filter(HealthcareProfessional.id == hp_id).first()
        if not hp:
            raise CSMSException("Healthcare professional not found", status_code=404)
        return hp

    def _to_response(self, hp: HealthcareProfessional) -> HealthcareProfessionalResponse:
        return HealthcareProfessionalResponse(
            id=hp.id,
            employee_id=hp.employee_id,
            profession=hp.profession,
            specialization=hp.specialization,
            license_number=hp.license_number,
            status=hp.status,
            employee_name=hp.employee.full_name if hp.employee else None,
        )


healthcare_professional_service = HealthcareProfessionalService()
