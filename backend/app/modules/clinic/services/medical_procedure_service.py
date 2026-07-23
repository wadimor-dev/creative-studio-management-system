from typing import Optional, List
from sqlalchemy.orm import Session
from app.core.exceptions import CSMSException
from app.modules.clinic.models.medical_procedure import MedicalProcedure
from app.modules.clinic.schemas import MedicalProcedureCreate, MedicalProcedureUpdate, MedicalProcedureResponse


class MedicalProcedureService:

    def get_all(self, db: Session, skip: int = 0, limit: int = 100,
                search: Optional[str] = None) -> List[MedicalProcedureResponse]:
        query = db.query(MedicalProcedure)
        if search:
            query = query.filter(
                (MedicalProcedure.code.ilike(f"%{search}%")) | (MedicalProcedure.name.ilike(f"%{search}%"))
            )
        items = query.order_by(MedicalProcedure.code).offset(skip).limit(limit).all()
        return [MedicalProcedureResponse.model_validate(p) for p in items]

    def get_by_id(self, db: Session, procedure_id: str) -> MedicalProcedureResponse:
        proc = db.query(MedicalProcedure).filter(MedicalProcedure.id == procedure_id).first()
        if not proc:
            raise CSMSException("Medical procedure not found", status_code=404)
        return MedicalProcedureResponse.model_validate(proc)

    def create(self, db: Session, data: MedicalProcedureCreate) -> MedicalProcedureResponse:
        existing = db.query(MedicalProcedure).filter(MedicalProcedure.code == data.code).first()
        if existing:
            raise CSMSException("Procedure code already exists", status_code=409)
        proc = MedicalProcedure(**data.model_dump())
        db.add(proc)
        db.commit()
        db.refresh(proc)
        return MedicalProcedureResponse.model_validate(proc)

    def update(self, db: Session, procedure_id: str, data: MedicalProcedureUpdate) -> MedicalProcedureResponse:
        proc = self._get_orm(db, procedure_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(proc, field, value)
        db.commit()
        db.refresh(proc)
        return MedicalProcedureResponse.model_validate(proc)

    def delete(self, db: Session, procedure_id: str) -> None:
        proc = self._get_orm(db, procedure_id)
        db.delete(proc)
        db.commit()

    def bulk_create(self, db: Session, items: List[MedicalProcedureCreate]) -> List[MedicalProcedureResponse]:
        procs = []
        for data in items:
            existing = db.query(MedicalProcedure).filter(MedicalProcedure.code == data.code).first()
            if existing:
                continue
            proc = MedicalProcedure(**data.model_dump())
            db.add(proc)
            procs.append(proc)
        db.commit()
        for proc in procs:
            db.refresh(proc)
        return [MedicalProcedureResponse.model_validate(p) for p in procs]

    def _get_orm(self, db: Session, procedure_id: str) -> MedicalProcedure:
        proc = db.query(MedicalProcedure).filter(MedicalProcedure.id == procedure_id).first()
        if not proc:
            raise CSMSException("Medical procedure not found", status_code=404)
        return proc


medical_procedure_service = MedicalProcedureService()
