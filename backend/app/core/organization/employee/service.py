from typing import Optional, List
from sqlalchemy.orm import Session
from app.core.organization.employee.models import Employee
from app.core.organization.employee.schemas import EmployeeCreate, EmployeeUpdate
from app.core.database.helpers import get_or_404
from app.core.exceptions import CSMSException
from app.core.organization.position.models import Position


def _validate_department_position(db: Session, department_id: Optional[int], position_id: Optional[int]) -> None:
    """Ensure Position.department_id matches Employee.department_id when both are set."""
    if department_id is not None and position_id is not None:
        pos = db.query(Position).filter(Position.id == position_id).first()
        if pos and pos.department_id != department_id:
            raise CSMSException(
                f"Position '{pos.name}' belongs to department id {pos.department_id}, "
                f"but employee's department is id {department_id}. "
                "Position must be in the same department.",
                status_code=422,
            )


class EmployeeCoreService:

    def get_all(self, db: Session, branch_id: Optional[int] = None) -> List[Employee]:
        query = db.query(Employee)
        if branch_id:
            query = query.filter(Employee.branch_id == branch_id)
        return query.order_by(Employee.employee_number).all()

    def get_by_id(self, db: Session, employee_id: int) -> Employee:
        return get_or_404(db, Employee, employee_id, "Employee")

    def get_by_user_id(self, db: Session, user_id: int) -> Optional[Employee]:
        return db.query(Employee).filter(Employee.user_id == user_id).first()

    def get_by_employee_number(self, db: Session, employee_number: str) -> Optional[Employee]:
        return db.query(Employee).filter(Employee.employee_number == employee_number).first()

    def create(self, db: Session, data: EmployeeCreate) -> Employee:
        existing = self.get_by_employee_number(db, data.employee_number)
        if existing:
            raise CSMSException(
                f"Employee with number '{data.employee_number}' already exists", status_code=409
            )
        existing = self.get_by_user_id(db, data.user_id)
        if existing:
            raise CSMSException(
                f"User {data.user_id} already linked to employee {existing.employee_number}",
                status_code=409,
            )
        _validate_department_position(db, data.department_id, data.position_id)
        emp = Employee(**data.model_dump())
        db.add(emp)
        db.commit()
        db.refresh(emp)
        return emp

    def update(self, db: Session, employee_id: int, data: EmployeeUpdate) -> Employee:
        emp = self.get_by_id(db, employee_id)
        updates = data.model_dump(exclude_unset=True)
        if "employee_number" in updates and updates["employee_number"] != emp.employee_number:
            existing = self.get_by_employee_number(db, updates["employee_number"])
            if existing:
                raise CSMSException(
                    f"Employee number '{updates['employee_number']}' already exists", status_code=409
                )

        dept_id = updates.get("department_id", emp.department_id)
        pos_id = updates.get("position_id", emp.position_id)
        _validate_department_position(db, dept_id, pos_id)

        for field, value in updates.items():
            setattr(emp, field, value)
        db.commit()
        db.refresh(emp)
        return emp

    def soft_delete(self, db: Session, employee_id: int, deleted_by_user_id: int, reason: str | None = None) -> Employee:
        emp = self.get_by_id(db, employee_id)
        from datetime import datetime, timezone, timedelta
        emp.deleted_at = datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None)
        emp.deleted_by_user_id = deleted_by_user_id
        if reason:
            emp.delete_reason = reason
        db.commit()
        db.refresh(emp)
        return emp

    def delete(self, db: Session, employee_id: int) -> None:
        emp = self.get_by_id(db, employee_id)
        db.delete(emp)
        db.commit()


employee_core_service = EmployeeCoreService()
