from typing import Optional, List
from sqlalchemy.orm import Session
from app.core.exceptions import CSMSException
from app.modules.clinic.models.icd10_code import ICD10Code
from app.modules.clinic.schemas import ICD10CodeCreate, ICD10CodeUpdate, ICD10CodeResponse


class ICD10CodeService:

    def get_all(self, db: Session, skip: int = 0, limit: int = 100,
                search: Optional[str] = None, active_only: bool = True) -> List[ICD10CodeResponse]:
        query = db.query(ICD10Code)
        if active_only:
            query = query.filter(ICD10Code.is_active == 1)
        if search:
            query = query.filter(
                (ICD10Code.code.ilike(f"%{search}%")) | (ICD10Code.name.ilike(f"%{search}%"))
            )
        items = query.order_by(ICD10Code.code).offset(skip).limit(limit).all()
        return [ICD10CodeResponse.model_validate(c) for c in items]

    def get_by_id(self, db: Session, code_id: str) -> ICD10CodeResponse:
        code = db.query(ICD10Code).filter(ICD10Code.id == code_id).first()
        if not code:
            raise CSMSException("ICD-10 code not found", status_code=404)
        return ICD10CodeResponse.model_validate(code)

    def get_by_code(self, db: Session, code: str) -> Optional[ICD10CodeResponse]:
        item = db.query(ICD10Code).filter(ICD10Code.code == code).first()
        if not item:
            return None
        return ICD10CodeResponse.model_validate(item)

    def create(self, db: Session, data: ICD10CodeCreate) -> ICD10CodeResponse:
        existing = db.query(ICD10Code).filter(ICD10Code.code == data.code).first()
        if existing:
            raise CSMSException("ICD-10 code already exists", status_code=409)
        code = ICD10Code(**data.model_dump())
        db.add(code)
        db.commit()
        db.refresh(code)
        return ICD10CodeResponse.model_validate(code)

    def update(self, db: Session, code_id: str, data: ICD10CodeUpdate) -> ICD10CodeResponse:
        code = self._get_orm(db, code_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(code, field, value)
        db.commit()
        db.refresh(code)
        return ICD10CodeResponse.model_validate(code)

    def delete(self, db: Session, code_id: str) -> None:
        code = self._get_orm(db, code_id)
        db.delete(code)
        db.commit()

    def bulk_create(self, db: Session, items: List[ICD10CodeCreate]) -> List[ICD10CodeResponse]:
        codes = []
        for data in items:
            existing = db.query(ICD10Code).filter(ICD10Code.code == data.code).first()
            if existing:
                continue
            code = ICD10Code(**data.model_dump())
            db.add(code)
            codes.append(code)
        db.commit()
        for code in codes:
            db.refresh(code)
        return [ICD10CodeResponse.model_validate(c) for c in codes]

    def _get_orm(self, db: Session, code_id: str) -> ICD10Code:
        code = db.query(ICD10Code).filter(ICD10Code.id == code_id).first()
        if not code:
            raise CSMSException("ICD-10 code not found", status_code=404)
        return code


icd10_code_service = ICD10CodeService()
