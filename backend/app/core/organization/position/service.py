from typing import Optional, List
from sqlalchemy.orm import Session
from app.core.organization.position.models import Position
from app.core.organization.position.schemas import PositionCreate, PositionUpdate
from app.core.database.helpers import get_or_404
from app.core.exceptions import CSMSException


class PositionService:

    def get_all(self, db: Session, department_id: Optional[int] = None) -> List[Position]:
        query = db.query(Position)
        if department_id:
            query = query.filter(Position.department_id == department_id)
        return query.order_by(Position.name).all()

    def get_by_id(self, db: Session, position_id: int) -> Position:
        return get_or_404(db, Position, position_id, "Position")

    def create(self, db: Session, data: PositionCreate) -> Position:
        existing = db.query(Position).filter(Position.code == data.code).first()
        if existing:
            raise CSMSException(f"Position with code '{data.code}' already exists", status_code=409)
        position = Position(**data.model_dump())
        db.add(position)
        db.commit()
        db.refresh(position)
        return position

    def update(self, db: Session, position_id: int, data: PositionUpdate) -> Position:
        position = self.get_by_id(db, position_id)
        update_data = data.model_dump(exclude_unset=True)
        if "code" in update_data and update_data["code"] != position.code:
            existing = db.query(Position).filter(Position.code == update_data["code"]).first()
            if existing:
                raise CSMSException(f"Position with code '{update_data['code']}' already exists", status_code=409)
        for field, value in update_data.items():
            setattr(position, field, value)
        db.commit()
        db.refresh(position)
        return position

    def delete(self, db: Session, position_id: int) -> None:
        position = self.get_by_id(db, position_id)
        db.delete(position)
        db.commit()


position_service = PositionService()
