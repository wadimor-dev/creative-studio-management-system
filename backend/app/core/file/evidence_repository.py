from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.core.file.models import WorkEvidence
from app.constants.work_activity import WorkEvidenceType
from app.schemas.work_evidence import WorkEvidenceCreate


class WorkEvidenceRepository:

    def create(self, db: Session, obj_in: WorkEvidenceCreate, work_activity_id: int,
               file_path: str, file_name: str, file_size: int, mime_type: str, user_id: int) -> WorkEvidence:
        latest = self.find_latest(db, work_activity_id, obj_in.type)
        order = 1
        if latest:
            order = latest.evidence_order + 1

        db_obj = WorkEvidence(
            work_activity_id=work_activity_id,
            type=obj_in.type,
            file_path=file_path,
            file_name=file_name,
            file_size=file_size,
            mime_type=mime_type,
            description=obj_in.description,
            evidence_order=order,
            uploaded_by=user_id,
        )
        db.add(db_obj)
        db.flush()
        return db_obj

    def find_by_activity(self, db: Session, activity_id: int) -> List[WorkEvidence]:
        return db.query(WorkEvidence).filter(
            WorkEvidence.work_activity_id == activity_id
        ).order_by(WorkEvidence.uploaded_at).all()

    def find_latest(self, db: Session, activity_id: int, evidence_type: WorkEvidenceType) -> Optional[WorkEvidence]:
        return db.query(WorkEvidence).filter(
            WorkEvidence.work_activity_id == activity_id,
            WorkEvidence.type == evidence_type
        ).order_by(desc(WorkEvidence.evidence_order)).first()

    def count_by_type(self, db: Session, activity_id: int, evidence_type: WorkEvidenceType) -> int:
        return db.query(WorkEvidence).filter(
            WorkEvidence.work_activity_id == activity_id,
            WorkEvidence.type == evidence_type
        ).count()

    def delete(self, db: Session, id: int) -> bool:
        db_obj = db.query(WorkEvidence).filter(WorkEvidence.id == id).first()
        if not db_obj:
            return False
        db.delete(db_obj)
        db.flush()
        return True


work_evidence_repository = WorkEvidenceRepository()
