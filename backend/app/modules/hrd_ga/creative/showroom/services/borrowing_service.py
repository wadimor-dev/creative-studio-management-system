from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.showroom_borrowing import ShowroomBorrowing
from app.models.showroom_movement import ShowroomMovement, ShowroomMovementType
from app.models.showroom_sample_stock import ShowroomSampleStock
from app.models.product import Product
from app.models.showroom_location import ShowroomLocation
from app.models.user import User
from app.modules.hrd_ga.creative.showroom.schemas import BorrowingResponse
from app.modules.hrd_ga.creative.showroom.services.base import jakarta_now, get_or_404


class BorrowingService:

    @staticmethod
    def _to_dict(b: ShowroomBorrowing, db: Session) -> dict:
        product = db.query(Product).filter(Product.id == b.product_id).first()
        from_loc = db.query(ShowroomLocation).filter(ShowroomLocation.id == b.from_location_id).first() if b.from_location_id else None
        borrower_loc = db.query(ShowroomLocation).filter(ShowroomLocation.id == b.borrower_location_id).first() if b.borrower_location_id else None
        user = db.query(User).filter(User.id == b.user_id).first()
        return {
            "id": b.id,
            "product": {"id": product.id, "name": product.display_name} if product else None,
            "from_location": {"id": from_loc.id, "name": from_loc.name, "code": from_loc.code} if from_loc else None,
            "borrower_name": b.borrower_name,
            "borrower_location": {"id": borrower_loc.id, "name": borrower_loc.name} if borrower_loc else None,
            "quantity": b.quantity,
            "sample_type": b.sample_type,
            "purpose": b.purpose,
            "borrow_date": str(b.borrow_date),
            "expected_return_date": str(b.expected_return_date) if b.expected_return_date else None,
            "actual_return_date": str(b.actual_return_date) if b.actual_return_date else None,
            "borrowed_at": str(b.borrowed_at) if b.borrowed_at else None,
            "status": b.status,
            "user": {"id": user.id, "name": user.full_name} if user else None,
            "movement_id": b.movement_id,
            "return_movement_id": b.return_movement_id,
            "notes": b.notes,
            "created_at": str(b.created_at) if b.created_at else None,
        }

    @staticmethod
    def get_all(db: Session, status: str = None):
        query = db.query(ShowroomBorrowing).order_by(ShowroomBorrowing.created_at.desc())
        if status:
            query = query.filter(ShowroomBorrowing.status == status.upper())
        borrowings = query.all()
        return [BorrowingService._to_dict(b, db) for b in borrowings]

    @staticmethod
    def get_by_id(db: Session, borrowing_id: int):
        b = get_or_404(db, ShowroomBorrowing, borrowing_id, "Borrowing")
        return BorrowingService._to_dict(b, db)

    @staticmethod
    def extend_borrowing(db: Session, borrowing_id: int, expected_return_date: str):
        from datetime import datetime as dt
        b = get_or_404(db, ShowroomBorrowing, borrowing_id, "Borrowing")
        if b.status not in ("BORROWED",):
            raise HTTPException(status_code=400, detail=f"Cannot extend borrowing with status {b.status}")
        b.expected_return_date = dt.strptime(expected_return_date, "%Y-%m-%d").date()
        db.commit()
        return BorrowingService._to_dict(b, db)

    @staticmethod
    def cancel_borrowing(db: Session, borrowing_id: int, user_id: int):
        b = get_or_404(db, ShowroomBorrowing, borrowing_id, "Borrowing")
        if b.status not in ("BORROWED",):
            raise HTTPException(status_code=400, detail=f"Cannot cancel borrowing with status {b.status}")

        movement = ShowroomMovement(
            movement_type=ShowroomMovementType.RETURN,
            product_id=b.product_id,
            quantity=b.quantity,
            to_location_id=b.from_location_id,
            sample_type=b.sample_type,
            purpose="Borrowing cancelled",
            user_id=user_id,
            date=jakarta_now(),
            reference_type="borrowing",
            reference_id=b.id,
        )
        db.add(movement)
        db.flush()

        stock = db.query(ShowroomSampleStock).filter(
            ShowroomSampleStock.product_id == b.product_id,
            ShowroomSampleStock.location_id == b.from_location_id,
            ShowroomSampleStock.sample_type == b.sample_type,
        ).first()
        if stock:
            stock.quantity += b.quantity
        else:
            stock = ShowroomSampleStock(
                product_id=b.product_id,
                location_id=b.from_location_id,
                sample_type=b.sample_type,
                quantity=b.quantity,
            )
            db.add(stock)

        b.status = "CANCELLED"
        b.return_movement_id = movement.id
        db.commit()
        return {"status": "cancelled", "movement_id": movement.id}

    @staticmethod
    def get_overdue(db: Session):
        from datetime import date as dt_date
        today = dt_date.today()
        borrowings = db.query(ShowroomBorrowing).filter(
            ShowroomBorrowing.status == "BORROWED",
            ShowroomBorrowing.expected_return_date < today,
        ).all()
        return [BorrowingService._to_dict(b, db) for b in borrowings]

    @staticmethod
    def get_stats(db: Session):
        from datetime import date as dt_date
        today = dt_date.today()
        borrowed = db.query(ShowroomBorrowing).filter(ShowroomBorrowing.status == "BORROWED").count()
        overdue = db.query(ShowroomBorrowing).filter(
            ShowroomBorrowing.status == "BORROWED",
            ShowroomBorrowing.expected_return_date < today,
        ).count()
        returned_this_month = db.query(ShowroomBorrowing).filter(
            ShowroomBorrowing.status == "RETURNED",
            ShowroomBorrowing.actual_return_date >= today.replace(day=1),
        ).count()
        return {
            "borrowed": borrowed,
            "overdue": overdue,
            "returned_this_month": returned_this_month,
        }
