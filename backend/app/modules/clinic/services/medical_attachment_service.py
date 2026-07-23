from typing import List
from sqlalchemy.orm import Session
from app.core.exceptions import CSMSException
from app.modules.clinic.models.medical_attachment import MedicalAttachment
from app.modules.clinic.schemas import MedicalAttachmentCreate, MedicalAttachmentUpdate, MedicalAttachmentResponse


class MedicalAttachmentService:

    def get_by_id(self, db: Session, att_id: str) -> MedicalAttachmentResponse:
        att = db.query(MedicalAttachment).filter(MedicalAttachment.id == att_id).first()
        if not att:
            raise CSMSException("Attachment not found", status_code=404)
        return MedicalAttachmentResponse.model_validate(att)

    def get_by_visit(self, db: Session, visit_id: str) -> List[MedicalAttachmentResponse]:
        items = db.query(MedicalAttachment).filter(MedicalAttachment.visit_id == visit_id).all()
        return [MedicalAttachmentResponse.model_validate(a) for a in items]

    def create(self, db: Session, data: MedicalAttachmentCreate) -> MedicalAttachmentResponse:
        att = MedicalAttachment(**data.model_dump())
        db.add(att)
        db.commit()
        db.refresh(att)
        return MedicalAttachmentResponse.model_validate(att)

    def update(self, db: Session, att_id: str, data: MedicalAttachmentUpdate) -> MedicalAttachmentResponse:
        att = db.query(MedicalAttachment).filter(MedicalAttachment.id == att_id).first()
        if not att:
            raise CSMSException("Attachment not found", status_code=404)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(att, field, value)
        db.commit()
        db.refresh(att)
        return MedicalAttachmentResponse.model_validate(att)

    def delete(self, db: Session, att_id: str) -> None:
        att = db.query(MedicalAttachment).filter(MedicalAttachment.id == att_id).first()
        if not att:
            raise CSMSException("Attachment not found", status_code=404)
        db.delete(att)
        db.commit()


medical_attachment_service = MedicalAttachmentService()
