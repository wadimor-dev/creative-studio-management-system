from typing import Optional, List
from sqlalchemy.orm import Session
from app.core.organization.branch.models import Branch
from app.core.organization.branch.schemas import BranchCreate, BranchUpdate
from app.core.database.helpers import get_or_404
from app.core.exceptions import CSMSException


class BranchService:

    def get_all(self, db: Session, company_id: Optional[int] = None) -> List[Branch]:
        query = db.query(Branch)
        if company_id:
            query = query.filter(Branch.company_id == company_id)
        return query.order_by(Branch.name).all()

    def get_by_id(self, db: Session, branch_id: int) -> Branch:
        return get_or_404(db, Branch, branch_id, "Branch")

    def create(self, db: Session, data: BranchCreate) -> Branch:
        existing = db.query(Branch).filter(Branch.code == data.code).first()
        if existing:
            raise CSMSException(f"Branch with code '{data.code}' already exists", status_code=409)
        branch = Branch(**data.model_dump())
        db.add(branch)
        db.commit()
        db.refresh(branch)
        return branch

    def update(self, db: Session, branch_id: int, data: BranchUpdate) -> Branch:
        branch = self.get_by_id(db, branch_id)
        update_data = data.model_dump(exclude_unset=True)
        if "code" in update_data and update_data["code"] != branch.code:
            existing = db.query(Branch).filter(Branch.code == update_data["code"]).first()
            if existing:
                raise CSMSException(f"Branch with code '{update_data['code']}' already exists", status_code=409)
        for field, value in update_data.items():
            setattr(branch, field, value)
        db.commit()
        db.refresh(branch)
        return branch

    def delete(self, db: Session, branch_id: int) -> None:
        branch = self.get_by_id(db, branch_id)
        db.delete(branch)
        db.commit()


branch_service = BranchService()
