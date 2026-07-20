from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException

from app.models.showroom_sample_stock import ShowroomSampleStock
from app.models.showroom_movement import ShowroomMovement, ShowroomMovementType
from app.models.showroom_location import ShowroomLocation
from app.models.product import Product
from app.modules.showroom_v2.schemas import (
    HandoverCreate, TransferCreate, BorrowCreate, ReturnCreate, AdjustCreate,
    SampleStockDetailResponse, SampleStockResponse, MovementResponse,
)
from app.modules.showroom_v2.services.base import jakarta_now, get_or_404, validate_quantity


class SampleService:

    @staticmethod
    def _create_movement(
        db: Session,
        movement_type: ShowroomMovementType,
        product_id: int,
        quantity: int,
        user_id: int,
        from_location_id: int = None,
        to_location_id: int = None,
        sample_type: str = None,
        purpose: str = None,
        notes: str = None,
        reference_type: str = None,
        reference_id: int = None,
    ) -> ShowroomMovement:
        movement = ShowroomMovement(
            movement_type=movement_type,
            product_id=product_id,
            from_location_id=from_location_id,
            to_location_id=to_location_id,
            quantity=quantity,
            sample_type=sample_type,
            purpose=purpose,
            user_id=user_id,
            date=jakarta_now(),
            notes=notes,
            reference_type=reference_type,
            reference_id=reference_id,
        )
        db.add(movement)
        db.flush()
        return movement

    @staticmethod
    def _update_stock(
        db: Session,
        product_id: int,
        location_id: int,
        quantity_delta: int,
        sample_type: str = None,
        storage_location_id: int = None,
    ) -> ShowroomSampleStock:
        stock = db.query(ShowroomSampleStock).filter(
            ShowroomSampleStock.product_id == product_id,
            ShowroomSampleStock.location_id == location_id,
            ShowroomSampleStock.sample_type == sample_type,
        ).first()

        if stock is None:
            if quantity_delta < 0:
                raise HTTPException(status_code=400, detail="Cannot reduce stock that does not exist")
            stock = ShowroomSampleStock(
                product_id=product_id,
                location_id=location_id,
                sample_type=sample_type,
                quantity=quantity_delta,
                storage_location_id=storage_location_id,
                version=1,
            )
            db.add(stock)
        else:
            stock.quantity += quantity_delta
            if storage_location_id and not stock.storage_location_id:
                stock.storage_location_id = storage_location_id
            if stock.quantity < 0:
                raise HTTPException(status_code=400, detail=f"Insufficient stock at location (have {stock.quantity - quantity_delta}, need {abs(quantity_delta)})")
            if stock.quantity == 0:
                db.delete(stock)
                db.flush()
                return None
        db.flush()
        return stock

    @staticmethod
    def _stock_to_dict(stock: ShowroomSampleStock, db: Session) -> dict:
        product = db.query(Product).filter(Product.id == stock.product_id).first()
        location = db.query(ShowroomLocation).filter(ShowroomLocation.id == stock.location_id).first()
        return {
            "id": stock.id,
            "product_id": stock.product_id,
            "product_name": product.display_name if product else "Unknown",
            "sku": getattr(product, "sku", None) or "",
            "location_id": stock.location_id,
            "location_name": location.name if location else "Unknown",
            "location_code": location.code if location else "",
            "sample_type": stock.sample_type,
            "quantity": stock.quantity,
        }

    @staticmethod
    def _movement_to_dict(movement: ShowroomMovement, db: Session) -> dict:
        product = db.query(Product).filter(Product.id == movement.product_id).first()
        from_loc = db.query(ShowroomLocation).filter(ShowroomLocation.id == movement.from_location_id).first() if movement.from_location_id else None
        to_loc = db.query(ShowroomLocation).filter(ShowroomLocation.id == movement.to_location_id).first() if movement.to_location_id else None
        from app.models.user import User
        user = db.query(User).filter(User.id == movement.user_id).first()
        return {
            "id": movement.id,
            "movement_type": movement.movement_type.value if hasattr(movement.movement_type, 'value') else movement.movement_type,
            "product_id": movement.product_id,
            "product_name": product.display_name if product else "Unknown",
            "from_location": {"id": from_loc.id, "name": from_loc.name, "code": from_loc.code} if from_loc else None,
            "to_location": {"id": to_loc.id, "name": to_loc.name, "code": to_loc.code} if to_loc else None,
            "quantity": movement.quantity,
            "sample_type": movement.sample_type,
            "purpose": movement.purpose,
            "user": {"id": user.id, "name": user.full_name} if user else None,
            "date": str(movement.date),
            "notes": movement.notes,
            "reference_type": movement.reference_type,
            "reference_id": movement.reference_id,
        }

    @staticmethod
    def get_stock_by_location(db: Session, location_id: int = None):
        query = db.query(ShowroomSampleStock)
        if location_id:
            query = query.filter(ShowroomSampleStock.location_id == location_id)
        stocks = query.all()
        return [SampleService._stock_to_dict(s, db) for s in stocks]

    @staticmethod
    def get_stock_summary(db: Session):
        stocks = db.query(ShowroomSampleStock).all()
        grouped = {}
        for s in stocks:
            key = (s.product_id, s.sample_type)
            if key not in grouped:
                product = db.query(Product).filter(Product.id == s.product_id).first()
                grouped[key] = {
                    "product_id": s.product_id,
                    "product_name": product.display_name if product else "Unknown",
                    "sku": getattr(product, "sku", None) or "",
                    "sample_type": s.sample_type,
                    "total_quantity": 0,
                    "locations": [],
                }
            loc = db.query(ShowroomLocation).filter(ShowroomLocation.id == s.location_id).first()
            grouped[key]["total_quantity"] += s.quantity
            grouped[key]["locations"].append({
                "location_id": s.location_id,
                "location_name": loc.name if loc else "Unknown",
                "location_code": loc.code if loc else "",
                "quantity": s.quantity,
            })
        return list(grouped.values())

    @staticmethod
    def handover_from_inventory(db: Session, data: HandoverCreate, user_id: int):
        validate_quantity(data.quantity)
        get_or_404(db, ShowroomLocation, data.to_location_id, "Location")
        get_or_404(db, Product, data.product_id, "Product")

        movement = SampleService._create_movement(
            db=db,
            movement_type=ShowroomMovementType.HANDOVER,
            product_id=data.product_id,
            quantity=data.quantity,
            user_id=user_id,
            to_location_id=data.to_location_id,
            sample_type=data.sample_type,
            purpose=data.purpose,
            notes=data.notes,
        )
        SampleService._update_stock(
            db, data.product_id, data.to_location_id, data.quantity, data.sample_type,
            storage_location_id=getattr(data, 'storage_location_id', None),
        )
        db.commit()
        return SampleService._movement_to_dict(movement, db)

    @staticmethod
    def transfer_stock(db: Session, data: TransferCreate, user_id: int):
        validate_quantity(data.quantity)
        get_or_404(db, ShowroomLocation, data.from_location_id, "From Location")
        get_or_404(db, ShowroomLocation, data.to_location_id, "To Location")
        get_or_404(db, Product, data.product_id, "Product")

        if data.from_location_id == data.to_location_id:
            raise HTTPException(status_code=400, detail="Source and destination cannot be the same")

        existing = db.query(ShowroomSampleStock).filter(
            ShowroomSampleStock.product_id == data.product_id,
            ShowroomSampleStock.location_id == data.from_location_id,
            ShowroomSampleStock.sample_type == data.sample_type,
        ).first()
        if not existing or existing.quantity < data.quantity:
            avail = existing.quantity if existing else 0
            raise HTTPException(status_code=400, detail=f"Insufficient stock at source (available: {avail})")

        movement = SampleService._create_movement(
            db=db,
            movement_type=ShowroomMovementType.TRANSFER,
            product_id=data.product_id,
            quantity=data.quantity,
            user_id=user_id,
            from_location_id=data.from_location_id,
            to_location_id=data.to_location_id,
            sample_type=data.sample_type,
            purpose=data.purpose,
            notes=data.notes,
        )
        SampleService._update_stock(
            db, data.product_id, data.from_location_id, -data.quantity, data.sample_type,
            storage_location_id=getattr(data, 'from_storage_location_id', None),
        )
        SampleService._update_stock(
            db, data.product_id, data.to_location_id, data.quantity, data.sample_type,
            storage_location_id=getattr(data, 'to_storage_location_id', None),
        )
        db.commit()
        return SampleService._movement_to_dict(movement, db)

    @staticmethod
    def borrow_sample(db: Session, data: BorrowCreate, user_id: int):
        validate_quantity(data.quantity)
        get_or_404(db, ShowroomLocation, data.from_location_id, "Location")
        get_or_404(db, Product, data.product_id, "Product")

        existing = db.query(ShowroomSampleStock).filter(
            ShowroomSampleStock.product_id == data.product_id,
            ShowroomSampleStock.location_id == data.from_location_id,
            ShowroomSampleStock.sample_type == data.sample_type,
        ).first()
        if not existing or existing.quantity < data.quantity:
            avail = existing.quantity if existing else 0
            raise HTTPException(status_code=400, detail=f"Insufficient stock (available: {avail})")

        movement = SampleService._create_movement(
            db=db,
            movement_type=ShowroomMovementType.BORROW,
            product_id=data.product_id,
            quantity=data.quantity,
            user_id=user_id,
            from_location_id=data.from_location_id,
            sample_type=data.sample_type,
            purpose=data.purpose,
            notes=data.notes,
        )
        SampleService._update_stock(db, data.product_id, data.from_location_id, -data.quantity, data.sample_type)

        from app.models.showroom_borrowing import ShowroomBorrowing
        from datetime import datetime as dt
        borrow_date = dt.strptime(data.borrow_date, "%Y-%m-%d").date() if data.borrow_date else jakarta_now().date()
        expected_return = dt.strptime(data.expected_return_date, "%Y-%m-%d").date() if data.expected_return_date else None

        borrowing = ShowroomBorrowing(
            product_id=data.product_id,
            from_location_id=data.from_location_id,
            borrower_name=data.borrower_name,
            borrower_location_id=data.borrower_location_id,
            quantity=data.quantity,
            sample_type=data.sample_type,
            purpose=data.purpose,
            borrow_date=borrow_date,
            expected_return_date=expected_return,
            status="BORROWED",
            user_id=user_id,
            borrowed_at=jakarta_now(),
            movement_id=movement.id,
            notes=data.notes,
        )
        db.add(borrowing)
        db.commit()
        db.refresh(borrowing)

        return {
            "movement": SampleService._movement_to_dict(movement, db),
            "borrowing_id": borrowing.id,
            "borrowing_status": borrowing.status,
        }

    @staticmethod
    def return_sample(db: Session, borrowing_id: int, data: ReturnCreate, user_id: int):
        from app.models.showroom_borrowing import ShowroomBorrowing
        borrowing = get_or_404(db, ShowroomBorrowing, borrowing_id, "Borrowing")
        if borrowing.status != "BORROWED":
            raise HTTPException(status_code=400, detail=f"Cannot return borrowing with status {borrowing.status}")

        movement = SampleService._create_movement(
            db=db,
            movement_type=ShowroomMovementType.RETURN,
            product_id=borrowing.product_id,
            quantity=borrowing.quantity,
            user_id=user_id,
            to_location_id=data.location_id,
            sample_type=borrowing.sample_type,
            purpose="Sample return",
            notes=data.notes,
            reference_type="borrowing",
            reference_id=borrowing.id,
        )
        SampleService._update_stock(db, borrowing.product_id, data.location_id, borrowing.quantity, borrowing.sample_type)

        from datetime import date as dt_date
        borrowing.actual_return_date = dt_date.today()
        borrowing.status = "RETURNED"
        borrowing.return_movement_id = movement.id
        db.commit()
        return SampleService._movement_to_dict(movement, db)

    @staticmethod
    def adjust_stock(db: Session, data: AdjustCreate, user_id: int):
        get_or_404(db, ShowroomLocation, data.location_id, "Location")
        get_or_404(db, Product, data.product_id, "Product")

        if data.adjustment == 0:
            raise HTTPException(status_code=400, detail="Adjustment cannot be zero")

        movement = SampleService._create_movement(
            db=db,
            movement_type=ShowroomMovementType.ADJUSTMENT,
            product_id=data.product_id,
            quantity=abs(data.adjustment),
            user_id=user_id,
            from_location_id=data.location_id if data.adjustment < 0 else None,
            to_location_id=data.location_id if data.adjustment > 0 else None,
            sample_type=data.sample_type,
            purpose=data.purpose,
            notes=data.notes,
        )
        SampleService._update_stock(
            db, data.product_id, data.location_id, data.adjustment, data.sample_type,
            storage_location_id=getattr(data, 'storage_location_id', None),
        )
        db.commit()
        return SampleService._movement_to_dict(movement, db)

    @staticmethod
    def get_locations(db: Session):
        return db.query(ShowroomLocation).filter(ShowroomLocation.is_active == True).all()

    @staticmethod
    def get_movements(db: Session, product_id: int = None, movement_type: str = None, limit: int = 50):
        query = db.query(ShowroomMovement).order_by(ShowroomMovement.date.desc())
        if product_id:
            query = query.filter(ShowroomMovement.product_id == product_id)
        if movement_type:
            query = query.filter(ShowroomMovement.movement_type == movement_type)
        movements = query.limit(limit).all()
        return [SampleService._movement_to_dict(m, db) for m in movements]
