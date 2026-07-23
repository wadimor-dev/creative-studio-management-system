from typing import Optional
from sqlalchemy.orm import Session
from app.core.exceptions import CSMSException
from app.modules.hrd_ga.clinic.models.soap_note import SOAPNote
from app.modules.hrd_ga.clinic.schemas import SOAPNoteCreate, SOAPNoteUpdate, SOAPNoteResponse


class SOAPNoteService:

    def get_by_id(self, db: Session, note_id: str) -> SOAPNoteResponse:
        note = db.query(SOAPNote).filter(SOAPNote.id == note_id).first()
        if not note:
            raise CSMSException("SOAP note not found", status_code=404)
        return SOAPNoteResponse.model_validate(note)

    def get_by_visit_id(self, db: Session, visit_id: str) -> Optional[SOAPNoteResponse]:
        note = db.query(SOAPNote).filter(SOAPNote.visit_id == visit_id).first()
        if not note:
            return None
        return SOAPNoteResponse.model_validate(note)

    def create(self, db: Session, data: SOAPNoteCreate) -> SOAPNoteResponse:
        existing = db.query(SOAPNote).filter(SOAPNote.visit_id == data.visit_id).first()
        if existing:
            raise CSMSException("SOAP note already exists for this visit", status_code=409)
        note = SOAPNote(**data.model_dump())
        db.add(note)
        db.commit()
        db.refresh(note)
        return SOAPNoteResponse.model_validate(note)

    def update(self, db: Session, note_id: str, data: SOAPNoteUpdate) -> SOAPNoteResponse:
        note = db.query(SOAPNote).filter(SOAPNote.id == note_id).first()
        if not note:
            raise CSMSException("SOAP note not found", status_code=404)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(note, field, value)
        db.commit()
        db.refresh(note)
        return SOAPNoteResponse.model_validate(note)

    def upsert(self, db: Session, visit_id: str, data: SOAPNoteUpdate) -> SOAPNoteResponse:
        note = db.query(SOAPNote).filter(SOAPNote.visit_id == visit_id).first()
        if note:
            return self.update(db, note.id, data)
        return self.create(db, SOAPNoteCreate(visit_id=visit_id, **data.model_dump(exclude_unset=True)))


soap_note_service = SOAPNoteService()
