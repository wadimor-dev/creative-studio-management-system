import secrets
import json
from typing import Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.showroom_qr_entity import ShowroomQREntity
from app.modules.showroom_v2.services.base import jakarta_now, log_activity
from app.modules.showroom_v2.core.qr_resolvers import resolve_qr_token


def _generate_token() -> str:
    raw = secrets.token_urlsafe(16)
    return raw[:20]


class QREntityService:

    @staticmethod
    def get_all(db: Session, entity_type: str = None) -> list:
        query = db.query(ShowroomQREntity).filter(ShowroomQREntity.is_active == True)
        if entity_type:
            query = query.filter(ShowroomQREntity.entity_type == entity_type)
        entities = query.order_by(ShowroomQREntity.created_at.desc()).all()
        return [QREntityService._to_dict(e, db) for e in entities]

    @staticmethod
    def get_by_id(db: Session, qr_id: int) -> dict:
        qr = db.query(ShowroomQREntity).filter(ShowroomQREntity.id == qr_id).first()
        if not qr:
            raise HTTPException(status_code=404, detail="QR entity not found")
        return QREntityService._to_dict(qr, db)

    @staticmethod
    def get_by_token(db: Session, token: str) -> dict:
        qr = db.query(ShowroomQREntity).filter(
            ShowroomQREntity.token == token, ShowroomQREntity.is_active == True
        ).first()
        if not qr:
            raise HTTPException(status_code=404, detail="QR entity not found")
        return QREntityService._to_dict(qr, db)

    @staticmethod
    def create(db: Session, data: dict, user_id: int) -> dict:
        token = _generate_token()
        while db.query(ShowroomQREntity).filter(ShowroomQREntity.token == token).first():
            token = _generate_token()

        qr = ShowroomQREntity(
            entity_type=data["entity_type"],
            entity_id=data["entity_id"],
            token=token,
            label=data.get("label"),
            storage_location_id=data.get("storage_location_id"),
            is_active=True,
            version=1,
        )
        db.add(qr)
        db.flush()

        log_activity(
            db, action="QR_CREATE", entity_type="qr_entity",
            entity_id=qr.id, user_id=user_id,
            new_value=json.dumps(QREntityService._to_dict(qr, db), default=str),
        )

        db.commit()
        return QREntityService._to_dict(qr, db)

    @staticmethod
    def update(db: Session, qr_id: int, data: dict, user_id: int) -> dict:
        qr = db.query(ShowroomQREntity).filter(ShowroomQREntity.id == qr_id).first()
        if not qr:
            raise HTTPException(status_code=404, detail="QR entity not found")

        old_val = QREntityService._to_dict(qr, db)

        for field in ["entity_type", "entity_id", "label", "storage_location_id", "is_active"]:
            if field in data:
                setattr(qr, field, data[field])

        qr.version += 1
        db.flush()

        log_activity(
            db, action="QR_UPDATE", entity_type="qr_entity",
            entity_id=qr.id, user_id=user_id,
            old_value=json.dumps(old_val, default=str),
            new_value=json.dumps(QREntityService._to_dict(qr, db), default=str),
        )

        db.commit()
        return QREntityService._to_dict(qr, db)

    @staticmethod
    def delete(db: Session, qr_id: int, user_id: int):
        qr = db.query(ShowroomQREntity).filter(ShowroomQREntity.id == qr_id).first()
        if not qr:
            raise HTTPException(status_code=404, detail="QR entity not found")

        qr.is_active = False
        qr.version += 1
        db.flush()

        log_activity(
            db, action="QR_DELETE", entity_type="qr_entity",
            entity_id=qr.id, user_id=user_id,
        )

        db.commit()
        return {"message": "QR entity deactivated", "id": qr_id}

    @staticmethod
    def resolve(db: Session, token: str) -> dict:
        return resolve_qr_token(db, token)

    @staticmethod
    def _to_dict(qr: ShowroomQREntity, db: Session) -> dict:
        return {
            "id": qr.id,
            "entity_type": qr.entity_type,
            "entity_id": qr.entity_id,
            "token": qr.token,
            "label": qr.label,
            "storage_location_id": qr.storage_location_id,
            "is_active": qr.is_active,
            "version": qr.version,
            "created_at": str(qr.created_at) if qr.created_at else None,
            "updated_at": str(qr.updated_at) if qr.updated_at else None,
        }
