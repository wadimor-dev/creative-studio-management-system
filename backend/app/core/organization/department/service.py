from typing import Optional, List
from sqlalchemy.orm import Session
from app.core.organization.department.models import Department
from app.core.organization.department.schemas import DepartmentCreate, DepartmentUpdate
from app.core.database.helpers import get_or_404
from app.core.exceptions import CSMSException


class DepartmentService:

    def get_all(self, db: Session) -> List[Department]:
        return db.query(Department).order_by(Department.name).all()

    def get_by_id(self, db: Session, department_id: int) -> Department:
        return get_or_404(db, Department, department_id, "Department")

    def get_by_code(self, db: Session, code: str) -> Optional[Department]:
        return db.query(Department).filter(Department.code == code).first()

    def create(self, db: Session, data: DepartmentCreate) -> Department:
        existing = self.get_by_code(db, data.code)
        if existing:
            raise CSMSException(f"Department with code '{data.code}' already exists", status_code=409)
        dept = Department(**data.model_dump())
        db.add(dept)
        db.commit()
        db.refresh(dept)
        return dept

    def update(self, db: Session, department_id: int, data: DepartmentUpdate) -> Department:
        dept = self.get_by_id(db, department_id)
        update_data = data.model_dump(exclude_unset=True)
        if "code" in update_data and update_data["code"] != dept.code:
            existing = self.get_by_code(db, update_data["code"])
            if existing:
                raise CSMSException(f"Department with code '{update_data['code']}' already exists", status_code=409)
        for field, value in update_data.items():
            setattr(dept, field, value)
        db.commit()
        db.refresh(dept)
        return dept

    def delete(self, db: Session, department_id: int) -> None:
        dept = self.get_by_id(db, department_id)
        db.delete(dept)
        db.commit()


department_service = DepartmentService()
