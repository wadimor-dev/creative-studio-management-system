from typing import Optional, List
from sqlalchemy.orm import Session
from app.core.organization.company.models import Company
from app.core.organization.company.schemas import CompanyCreate, CompanyUpdate
from app.core.database.helpers import get_or_404
from app.core.exceptions import CSMSException


class CompanyService:

    def get_all(self, db: Session) -> List[Company]:
        return db.query(Company).order_by(Company.name).all()

    def get_by_id(self, db: Session, company_id: int) -> Company:
        return get_or_404(db, Company, company_id, "Company")

    def get_by_code(self, db: Session, code: str) -> Optional[Company]:
        return db.query(Company).filter(Company.code == code).first()

    def create(self, db: Session, data: CompanyCreate) -> Company:
        existing = self.get_by_code(db, data.code)
        if existing:
            raise CSMSException(f"Company with code '{data.code}' already exists", status_code=409)
        company = Company(**data.model_dump())
        db.add(company)
        db.commit()
        db.refresh(company)
        return company

    def update(self, db: Session, company_id: int, data: CompanyUpdate) -> Company:
        company = self.get_by_id(db, company_id)
        update_data = data.model_dump(exclude_unset=True)
        if "code" in update_data and update_data["code"] != company.code:
            existing = self.get_by_code(db, update_data["code"])
            if existing:
                raise CSMSException(f"Company with code '{update_data['code']}' already exists", status_code=409)
        for field, value in update_data.items():
            setattr(company, field, value)
        db.commit()
        db.refresh(company)
        return company

    def delete(self, db: Session, company_id: int) -> None:
        company = self.get_by_id(db, company_id)
        db.delete(company)
        db.commit()


company_service = CompanyService()
