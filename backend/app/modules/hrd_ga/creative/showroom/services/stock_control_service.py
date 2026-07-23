from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.showroom_opname import ShowroomOpnameSession
from app.models.showroom_opname_item import ShowroomOpnameItem
from app.models.showroom_sample_stock import ShowroomSampleStock
from app.models.showroom_movement import ShowroomMovement, ShowroomMovementType
from app.models.showroom_restock import ShowroomRestockRequest
from app.models.showroom_maintenance import ShowroomMaintenance
from app.models.showroom_location import ShowroomLocation
from app.models.showroom_reservation import ShowroomReservation
from app.models.product import Product
from app.models.user import User
from app.modules.hrd_ga.creative.showroom.schemas import (
    OpnameSessionCreate, OpnameItemCreate, RestockRequestCreate, MaintenanceCreate, ReservationCreate,
)
from app.modules.hrd_ga.creative.showroom.services.base import jakarta_now, get_or_404
from datetime import date


class StockControlService:

    @staticmethod
    def get_opname_sessions(db: Session, status: str = None):
        query = db.query(ShowroomOpnameSession).order_by(ShowroomOpnameSession.created_at.desc())
        if status:
            query = query.filter(ShowroomOpnameSession.status == status.lower())
        sessions = query.all()
        result = []
        for s in sessions:
            loc = db.query(ShowroomLocation).filter(ShowroomLocation.id == s.location_id).first() if s.location_id else None
            creator = db.query(User).filter(User.id == s.created_by).first()
            approver = db.query(User).filter(User.id == s.approved_by).first() if s.approved_by else None
            result.append({
                "id": s.id, "name": s.name, "status": s.status,
                "location": {"id": loc.id, "name": loc.name} if loc else None,
                "creator": {"id": creator.id, "name": creator.full_name} if creator else None,
                "approver": {"id": approver.id, "name": approver.full_name} if approver else None,
                "notes": s.notes,
                "created_at": str(s.created_at), "completed_at": str(s.completed_at) if s.completed_at else None,
                "approved_at": str(s.approved_at) if s.approved_at else None,
            })
        return result

    @staticmethod
    def create_opname_session(db: Session, data: OpnameSessionCreate, user_id: int):
        session = ShowroomOpnameSession(
            name=data.name,
            location_id=data.location_id,
            created_by=user_id,
            notes=data.notes,
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return {"id": session.id, "name": session.name, "status": session.status}

    @staticmethod
    def add_opname_item(db: Session, session_id: int, data: OpnameItemCreate):
        session = get_or_404(db, ShowroomOpnameSession, session_id, "Opname Session")
        if session.status not in ("draft", "in_progress"):
            raise HTTPException(status_code=400, detail="Session is not open for editing")

        existing = db.query(ShowroomSampleStock).filter(
            ShowroomSampleStock.product_id == data.product_id,
            ShowroomSampleStock.location_id == data.location_id,
            ShowroomSampleStock.sample_type == data.sample_type,
        ).first()
        expected = existing.quantity if existing else 0
        variance = data.actual_quantity - expected

        item = ShowroomOpnameItem(
            session_id=session_id,
            product_id=data.product_id,
            location_id=data.location_id,
            expected_quantity=expected,
            actual_quantity=data.actual_quantity,
            variance=variance,
            notes=data.notes,
        )
        db.add(item)
        if session.status == "draft":
            session.status = "in_progress"
        db.commit()
        return {"id": item.id, "variance": variance, "expected": expected, "actual": data.actual_quantity}

    @staticmethod
    def complete_opname(db: Session, session_id: int, user_id: int):
        session = get_or_404(db, ShowroomOpnameSession, session_id, "Opname Session")
        if session.status not in ("draft", "in_progress"):
            raise HTTPException(status_code=400, detail="Session is not in editable state")

        items = db.query(ShowroomOpnameItem).filter(ShowroomOpnameItem.session_id == session_id).all()
        for item in items:
            if item.variance and item.variance != 0:
                movement_type = ShowroomMovementType.ADJUSTMENT
                movement = ShowroomMovement(
                    movement_type=movement_type,
                    product_id=item.product_id,
                    quantity=abs(item.variance),
                    from_location_id=item.location_id if item.variance < 0 else None,
                    to_location_id=item.location_id if item.variance > 0 else None,
                    purpose=f"Opname adjustment: {session.name}",
                    user_id=user_id,
                    date=jakarta_now(),
                    reference_type="opname",
                    reference_id=session.id,
                )
                db.add(movement)
                db.flush()

                existing = db.query(ShowroomSampleStock).filter(
                    ShowroomSampleStock.product_id == item.product_id,
                    ShowroomSampleStock.location_id == item.location_id,
                ).first()
                if existing:
                    existing.quantity = item.actual_quantity
                elif item.actual_quantity > 0:
                    stock = ShowroomSampleStock(
                        product_id=item.product_id,
                        location_id=item.location_id,
                        quantity=item.actual_quantity,
                    )
                    db.add(stock)
                item.adjustment_movement_id = movement.id

        session.status = "completed"
        session.completed_at = jakarta_now()
        db.commit()
        return {"status": "completed", "items_adjusted": len([i for i in items if i.variance and i.variance != 0])}

    @staticmethod
    def approve_opname(db: Session, session_id: int, user_id: int):
        session = get_or_404(db, ShowroomOpnameSession, session_id, "Opname Session")
        if session.status != "completed":
            raise HTTPException(status_code=400, detail="Session must be completed first")
        session.status = "approved"
        session.approved_by = user_id
        session.approved_at = jakarta_now()
        db.commit()
        return {"status": "approved"}

    @staticmethod
    def get_restock_requests(db: Session, status: str = None):
        query = db.query(ShowroomRestockRequest).order_by(ShowroomRestockRequest.created_at.desc())
        if status:
            query = query.filter(ShowroomRestockRequest.status == status.upper())
        requests = query.all()
        result = []
        for r in requests:
            product = db.query(Product).filter(Product.id == r.product_id).first()
            location = db.query(ShowroomLocation).filter(ShowroomLocation.id == r.location_id).first()
            requester = db.query(User).filter(User.id == r.requested_by).first()
            approver = db.query(User).filter(User.id == r.approved_by).first() if r.approved_by else None
            result.append({
                "id": r.id,
                "product": {"id": product.id, "name": product.display_name} if product else None,
                "location": {"id": location.id, "name": location.name} if location else None,
                "sample_type": r.sample_type,
                "minimum_quantity": r.minimum_quantity,
                "current_quantity": r.current_quantity,
                "requested_quantity": r.requested_quantity,
                "source": r.source,
                "status": r.status,
                "requester": {"id": requester.id, "name": requester.full_name} if requester else None,
                "approver": {"id": approver.id, "name": approver.full_name} if approver else None,
                "notes": r.notes,
                "created_at": str(r.created_at),
            })
        return result

    @staticmethod
    def create_restock_request(db: Session, data: RestockRequestCreate, user_id: int):
        get_or_404(db, Product, data.product_id, "Product")
        get_or_404(db, ShowroomLocation, data.location_id, "Location")

        existing = db.query(ShowroomSampleStock).filter(
            ShowroomSampleStock.product_id == data.product_id,
            ShowroomSampleStock.location_id == data.location_id,
            ShowroomSampleStock.sample_type == data.sample_type,
        ).first()
        current_qty = existing.quantity if existing else 0

        request = ShowroomRestockRequest(
            product_id=data.product_id,
            location_id=data.location_id,
            sample_type=data.sample_type,
            minimum_quantity=data.minimum_quantity,
            current_quantity=current_qty,
            requested_quantity=data.requested_quantity,
            source=data.source or "manual",
            requested_by=user_id,
            notes=data.notes,
        )
        db.add(request)
        db.commit()
        db.refresh(request)
        return {"id": request.id, "status": request.status, "source": request.source}

    @staticmethod
    def approve_restock(db: Session, request_id: int, user_id: int):
        request = get_or_404(db, ShowroomRestockRequest, request_id, "Restock Request")
        if request.status != "PENDING":
            raise HTTPException(status_code=400, detail=f"Cannot approve request with status {request.status}")
        request.status = "APPROVED"
        request.approved_by = user_id
        db.commit()
        return {"status": "approved"}

    @staticmethod
    def get_maintenance(db: Session, status: str = None):
        query = db.query(ShowroomMaintenance).order_by(ShowroomMaintenance.created_at.desc())
        if status:
            query = query.filter(ShowroomMaintenance.status == status.upper())
        records = query.all()
        result = []
        for m in records:
            product = db.query(Product).filter(Product.id == m.product_id).first()
            location = db.query(ShowroomLocation).filter(ShowroomLocation.id == m.location_id).first() if m.location_id else None
            creator = db.query(User).filter(User.id == m.created_by).first()
            completer = db.query(User).filter(User.id == m.completed_by).first() if m.completed_by else None
            result.append({
                "id": m.id,
                "product": {"id": product.id, "name": product.display_name} if product else None,
                "location": {"id": location.id, "name": location.name} if location else None,
                "maintenance_type": m.maintenance_type,
                "status": m.status,
                "quantity": m.quantity,
                "sample_type": m.sample_type,
                "notes": m.notes,
                "creator": {"id": creator.id, "name": creator.full_name} if creator else None,
                "completer": {"id": completer.id, "name": completer.full_name} if completer else None,
                "created_at": str(m.created_at),
                "completed_at": str(m.completed_at) if m.completed_at else None,
            })
        return result

    @staticmethod
    def create_maintenance(db: Session, data: MaintenanceCreate, user_id: int):
        from app.modules.hrd_ga.creative.showroom.services.sample_service import SampleService
        get_or_404(db, Product, data.product_id, "Product")

        movement = None
        if data.location_id:
            get_or_404(db, ShowroomLocation, data.location_id, "Location")

        maintenance = ShowroomMaintenance(
            product_id=data.product_id,
            location_id=data.location_id,
            maintenance_type=data.maintenance_type,
            quantity=data.quantity,
            sample_type=data.sample_type,
            notes=data.notes,
            created_by=user_id,
        )
        db.add(maintenance)
        db.flush()

        if data.location_id and data.maintenance_type.upper() != "RETIRED":
            movement = SampleService._create_movement(
                db=db,
                movement_type=ShowroomMovementType.MAINTENANCE_OUT,
                product_id=data.product_id,
                quantity=data.quantity,
                user_id=user_id,
                from_location_id=data.location_id,
                sample_type=data.sample_type,
                purpose=f"Maintenance: {data.maintenance_type}",
                notes=data.notes,
                reference_type="maintenance",
                reference_id=maintenance.id,
            )
            SampleService._update_stock(db, data.product_id, data.location_id, -data.quantity, data.sample_type)
            maintenance.movement_id = movement.id

        elif data.maintenance_type.upper() == "RETIRED":
            movement = SampleService._create_movement(
                db=db,
                movement_type=ShowroomMovementType.RETIRED,
                product_id=data.product_id,
                quantity=data.quantity,
                user_id=user_id,
                from_location_id=data.location_id,
                sample_type=data.sample_type,
                purpose="Sample retired",
                notes=data.notes,
                reference_type="maintenance",
                reference_id=maintenance.id,
            )
            if data.location_id:
                SampleService._update_stock(db, data.product_id, data.location_id, -data.quantity, data.sample_type)
            maintenance.movement_id = movement.id
            maintenance.status = "COMPLETED"

        db.commit()
        return {"id": maintenance.id, "status": maintenance.status}

    @staticmethod
    def get_reservations(db: Session, status: str = None):
        query = db.query(ShowroomReservation).order_by(ShowroomReservation.created_at.desc())
        if status:
            query = query.filter(ShowroomReservation.status == status.upper())
        records = query.all()
        result = []
        for r in records:
            product = db.query(Product).filter(Product.id == r.product_id).first()
            user = db.query(User).filter(User.id == r.reserved_by).first()
            result.append({
                "id": r.id,
                "product": {"id": product.id, "display_name": product.display_name} if product else None,
                "quantity": r.quantity,
                "purpose": r.purpose,
                "reserved_from": str(r.reserved_from),
                "reserved_until": str(r.reserved_until),
                "status": r.status,
                "notes": r.notes,
                "user": {"id": user.id, "full_name": user.full_name} if user else None,
                "created_at": str(r.created_at),
                "updated_at": str(r.updated_at) if r.updated_at else None,
            })
        return result

    @staticmethod
    def create_reservation(db: Session, data: ReservationCreate, user_id: int):
        get_or_404(db, Product, data.product_id, "Product")
        from_str = data.reserved_from if isinstance(data.reserved_from, date) else date.fromisoformat(data.reserved_from)
        until_str = data.reserved_until if isinstance(data.reserved_until, date) else date.fromisoformat(data.reserved_until)
        reservation = ShowroomReservation(
            product_id=data.product_id,
            quantity=data.quantity,
            reserved_by=user_id,
            purpose=data.purpose,
            reserved_from=from_str,
            reserved_until=until_str,
            notes=data.notes,
        )
        db.add(reservation)
        db.commit()
        db.refresh(reservation)
        return {"id": reservation.id, "status": reservation.status}

    @staticmethod
    def complete_maintenance(db: Session, maintenance_id: int, user_id: int):
        from app.modules.hrd_ga.creative.showroom.services.sample_service import SampleService
        maintenance = get_or_404(db, ShowroomMaintenance, maintenance_id, "Maintenance")
        if maintenance.status == "COMPLETED":
            raise HTTPException(status_code=400, detail="Already completed")
        if maintenance.maintenance_type.upper() == "RETIRED":
            raise HTTPException(status_code=400, detail="Retired items cannot be completed")

        if maintenance.location_id:
            movement = SampleService._create_movement(
                db=db,
                movement_type=ShowroomMovementType.MAINTENANCE_RETURN,
                product_id=maintenance.product_id,
                quantity=maintenance.quantity,
                user_id=user_id,
                to_location_id=maintenance.location_id,
                sample_type=maintenance.sample_type,
                purpose=f"Maintenance completed: {maintenance.maintenance_type}",
                reference_type="maintenance",
                reference_id=maintenance.id,
            )
            SampleService._update_stock(db, maintenance.product_id, maintenance.location_id, maintenance.quantity, maintenance.sample_type)
            maintenance.return_movement_id = movement.id

        maintenance.status = "COMPLETED"
        maintenance.completed_by = user_id
        maintenance.completed_at = jakarta_now()
        db.commit()
        return {"status": "completed"}
