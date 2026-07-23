from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from app.core.exceptions import CSMSException
from app.modules.hrd_ga.clinic.models.visit_procedure import VisitProcedure
from app.modules.hrd_ga.clinic.models.medical_procedure import MedicalProcedure
from app.modules.hrd_ga.clinic.schemas import VisitProcedureCreate, VisitProcedureUpdate, VisitProcedureResponse


class VisitProcedureService:

    def get_by_id(self, db: Session, vp_id: str) -> VisitProcedureResponse:
        vp = db.query(VisitProcedure).options(
            joinedload(VisitProcedure.procedure)
        ).filter(VisitProcedure.id == vp_id).first()
        if not vp:
            raise CSMSException("Visit procedure not found", status_code=404)
        return self._to_response(vp)

    def get_by_visit(self, db: Session, visit_id: str) -> List[VisitProcedureResponse]:
        items = db.query(VisitProcedure).options(
            joinedload(VisitProcedure.procedure)
        ).filter(VisitProcedure.visit_id == visit_id).all()
        return [self._to_response(vp) for vp in items]

    def create(self, db: Session, data: VisitProcedureCreate) -> VisitProcedureResponse:
        proc = db.query(MedicalProcedure).filter(MedicalProcedure.id == data.procedure_id).first()
        if not proc:
            raise CSMSException("Medical procedure not found", status_code=404)
        vp = VisitProcedure(**data.model_dump())
        db.add(vp)
        db.commit()
        db.refresh(vp)
        return self.get_by_id(db, vp.id)

    def update(self, db: Session, vp_id: str, data: VisitProcedureUpdate) -> VisitProcedureResponse:
        vp = db.query(VisitProcedure).filter(VisitProcedure.id == vp_id).first()
        if not vp:
            raise CSMSException("Visit procedure not found", status_code=404)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(vp, field, value)
        db.commit()
        db.refresh(vp)
        return self.get_by_id(db, vp.id)

    def delete(self, db: Session, vp_id: str) -> None:
        vp = db.query(VisitProcedure).filter(VisitProcedure.id == vp_id).first()
        if not vp:
            raise CSMSException("Visit procedure not found", status_code=404)
        db.delete(vp)
        db.commit()

    def _to_response(self, vp: VisitProcedure) -> VisitProcedureResponse:
        return VisitProcedureResponse(
            id=vp.id,
            visit_id=vp.visit_id,
            procedure_id=vp.procedure_id,
            notes=vp.notes,
            procedure_name=vp.procedure.name if vp.procedure else None,
        )


visit_procedure_service = VisitProcedureService()
