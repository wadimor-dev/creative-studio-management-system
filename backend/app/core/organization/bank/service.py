from typing import Optional, List
from sqlalchemy.orm import Session
from app.core.organization.bank.models import Bank
from app.core.organization.bank.schemas import BankCreate, BankUpdate
from app.core.database.helpers import get_or_404
from app.core.exceptions import CSMSException


class BankService:

    def get_all(self, db: Session, is_active: Optional[bool] = None) -> List[Bank]:
        query = db.query(Bank)
        if is_active is not None:
            query = query.filter(Bank.is_active == is_active)
        return query.order_by(Bank.code).all()

    def get_by_id(self, db: Session, bank_id: int) -> Bank:
        return get_or_404(db, Bank, bank_id, "Bank")

    def get_by_code(self, db: Session, code: str) -> Optional[Bank]:
        return db.query(Bank).filter(Bank.code == code).first()

    def create(self, db: Session, data: BankCreate) -> Bank:
        existing = self.get_by_code(db, data.code)
        if existing:
            raise CSMSException(f"Bank with code '{data.code}' already exists", status_code=409)
        bank = Bank(**data.model_dump())
        db.add(bank)
        db.commit()
        db.refresh(bank)
        return bank

    def update(self, db: Session, bank_id: int, data: BankUpdate) -> Bank:
        bank = self.get_by_id(db, bank_id)
        updates = data.model_dump(exclude_unset=True)
        if "code" in updates and updates["code"] != bank.code:
            existing = self.get_by_code(db, updates["code"])
            if existing:
                raise CSMSException(f"Bank code '{updates['code']}' already exists", status_code=409)
        for field, value in updates.items():
            setattr(bank, field, value)
        db.commit()
        db.refresh(bank)
        return bank

    def delete(self, db: Session, bank_id: int) -> None:
        bank = self.get_by_id(db, bank_id)
        db.delete(bank)
        db.commit()


bank_service = BankService()
