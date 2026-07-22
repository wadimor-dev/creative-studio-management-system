from typing import Optional, List
from sqlalchemy.orm import Session
from app.core.organization.division.models import Division
from app.core.organization.division.schemas import DivisionCreate, DivisionUpdate
from app.core.database.helpers import get_or_404
from app.core.exceptions import CSMSException


class DivisionService:

    def get_all(self, db: Session) -> List[Division]:
        return db.query(Division).order_by(Division.name).all()

    def get_by_id(self, db: Session, division_id: int) -> Division:
        return get_or_404(db, Division, division_id, "Division")

    def create(self, db: Session, data: DivisionCreate) -> Division:
        existing = db.query(Division).filter(Division.name == data.name).first()
        if existing:
            raise CSMSException(f"Division '{data.name}' already exists", status_code=409)
        division = Division(**data.model_dump())
        db.add(division)
        db.commit()
        db.refresh(division)
        return division

    def update(self, db: Session, division_id: int, data: DivisionUpdate) -> Division:
        division = self.get_by_id(db, division_id)
        update_data = data.model_dump(exclude_unset=True)
        if "name" in update_data and update_data["name"] != division.name:
            existing = db.query(Division).filter(Division.name == update_data["name"]).first()
            if existing:
                raise CSMSException(f"Division '{update_data['name']}' already exists", status_code=409)
        for field, value in update_data.items():
            setattr(division, field, value)
        db.commit()
        db.refresh(division)
        return division

    def delete(self, db: Session, division_id: int) -> None:
        division = self.get_by_id(db, division_id)
        db.delete(division)
        db.commit()


division_service = DivisionService()
