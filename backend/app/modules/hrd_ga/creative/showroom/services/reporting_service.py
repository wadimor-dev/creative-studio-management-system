from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.showroom_sample_stock import ShowroomSampleStock
from app.models.showroom_movement import ShowroomMovement
from app.models.showroom_borrowing import ShowroomBorrowing
from app.models.showroom_guest_release import ShowroomGuestRelease
from app.models.showroom_maintenance import ShowroomMaintenance
from app.models.showroom_restock import ShowroomRestockRequest
from app.models.showroom_location import ShowroomLocation
from app.models.product import Product


class ReportingService:

    @staticmethod
    def get_kpi(db: Session):
        from datetime import date as dt_date
        today = dt_date.today()
        first_of_month = today.replace(day=1)

        all_stock = db.query(ShowroomSampleStock).all()
        total_sample = sum(s.quantity for s in all_stock)

        borrowed_count = db.query(ShowroomBorrowing).filter(
            ShowroomBorrowing.status == "BORROWED"
        ).count()
        borrowed_qty = db.query(func.coalesce(func.sum(ShowroomBorrowing.quantity), 0)).filter(
            ShowroomBorrowing.status == "BORROWED"
        ).scalar()

        released_count = db.query(ShowroomGuestRelease).filter(
            ShowroomGuestRelease.status == "APPROVED",
            ShowroomGuestRelease.release_date >= first_of_month,
        ).count()

        maintenance_count = db.query(ShowroomMaintenance).filter(
            ShowroomMaintenance.status.in_(["PENDING", "IN_PROGRESS"])
        ).count()

        retired_count = db.query(ShowroomMaintenance).filter(
            ShowroomMaintenance.status == "COMPLETED",
            ShowroomMaintenance.maintenance_type == "RETIRED",
        ).count()

        restock_count = db.query(ShowroomRestockRequest).filter(
            ShowroomRestockRequest.status == "PENDING"
        ).count()

        overdue_count = db.query(ShowroomBorrowing).filter(
            ShowroomBorrowing.status == "BORROWED",
            ShowroomBorrowing.expected_return_date < today,
        ).count()

        top_borrowed = db.query(
            ShowroomBorrowing.product_id,
            func.count(ShowroomBorrowing.id).label("cnt")
        ).filter(
            ShowroomBorrowing.status == "BORROWED"
        ).group_by(ShowroomBorrowing.product_id).order_by(func.count(ShowroomBorrowing.id).desc()).first()

        top_borrowed_product = None
        if top_borrowed:
            p = db.query(Product).filter(Product.id == top_borrowed[0]).first()
            if p:
                top_borrowed_product = {"id": p.id, "name": p.display_name, "borrow_count": top_borrowed[1]}

        top_released = db.query(
            ShowroomGuestRelease.product_id,
            func.count(ShowroomGuestRelease.id).label("cnt")
        ).filter(
            ShowroomGuestRelease.status == "APPROVED"
        ).group_by(ShowroomGuestRelease.product_id).order_by(func.count(ShowroomGuestRelease.id).desc()).first()

        top_released_product = None
        if top_released:
            p = db.query(Product).filter(Product.id == top_released[0]).first()
            if p:
                top_released_product = {"id": p.id, "name": p.display_name, "release_count": top_released[1]}

        return {
            "total_sample": total_sample,
            "at_showroom": total_sample - borrowed_qty,
            "borrowed": borrowed_qty,
            "released_this_month": released_count,
            "maintenance": maintenance_count,
            "retired": retired_count,
            "need_restock": restock_count,
            "missing": 0,
            "overdue_borrowing": overdue_count,
            "top_borrowed_product": top_borrowed_product,
            "top_released_product": top_released_product,
            "stock_accuracy": None,
        }

    @staticmethod
    def get_movement_summary(db: Session, days: int = 30):
        from datetime import datetime, timedelta
        from app.models.showroom_movement import ShowroomMovementType
        cutoff = datetime.now() - timedelta(days=days)
        movements = db.query(ShowroomMovement).filter(ShowroomMovement.date >= cutoff).all()

        summary = {}
        for m in movements:
            mtype = m.movement_type.value if hasattr(m.movement_type, 'value') else m.movement_type
            if mtype not in summary:
                summary[mtype] = {"type": mtype, "count": 0, "total_quantity": 0}
            summary[mtype]["count"] += 1
            summary[mtype]["total_quantity"] += m.quantity

        return list(summary.values())

    @staticmethod
    def get_stock_by_location(db: Session):
        stocks = db.query(ShowroomSampleStock).all()
        location_map = {}
        for s in stocks:
            loc = db.query(ShowroomLocation).filter(ShowroomLocation.id == s.location_id).first()
            loc_name = loc.name if loc else "Unknown"
            loc_code = loc.code if loc else ""
            key = s.location_id
            if key not in location_map:
                location_map[key] = {"location_id": key, "location_name": loc_name, "location_code": loc_code, "total_quantity": 0, "products": []}
            product = db.query(Product).filter(Product.id == s.product_id).first()
            location_map[key]["total_quantity"] += s.quantity
            location_map[key]["products"].append({
                "product_id": s.product_id,
                "product_name": product.display_name if product else "Unknown",
                "sample_type": s.sample_type,
                "quantity": s.quantity,
            })
        return list(location_map.values())

    @staticmethod
    def get_product_movement_history(db: Session, product_id: int, limit: int = 50):
        movements = db.query(ShowroomMovement).filter(
            ShowroomMovement.product_id == product_id
        ).order_by(ShowroomMovement.date.desc()).limit(limit).all()

        result = []
        for m in movements:
            from_loc = db.query(ShowroomLocation).filter(ShowroomLocation.id == m.from_location_id).first() if m.from_location_id else None
            to_loc = db.query(ShowroomLocation).filter(ShowroomLocation.id == m.to_location_id).first() if m.to_location_id else None
            from app.models.user import User
            user = db.query(User).filter(User.id == m.user_id).first()
            result.append({
                "id": m.id,
                "movement_type": m.movement_type.value if hasattr(m.movement_type, 'value') else m.movement_type,
                "from_location": {"id": from_loc.id, "name": from_loc.name} if from_loc else None,
                "to_location": {"id": to_loc.id, "name": to_loc.name} if to_loc else None,
                "quantity": m.quantity,
                "sample_type": m.sample_type,
                "purpose": m.purpose,
                "user": {"id": user.id, "name": user.full_name} if user else None,
                "date": str(m.date),
                "notes": m.notes,
                "reference_type": m.reference_type,
                "reference_id": m.reference_id,
            })
        return result

    @staticmethod
    def get_borrowing_summary(db: Session):
        from datetime import date as dt_date
        today = dt_date.today()
        borrowings = db.query(ShowroomBorrowing).all()
        total = len(borrowings)
        active = len([b for b in borrowings if b.status == "BORROWED"])
        overdue = len([b for b in borrowings if b.status == "BORROWED" and b.expected_return_date and b.expected_return_date < today])
        returned = len([b for b in borrowings if b.status == "RETURNED"])
        cancelled = len([b for b in borrowings if b.status == "CANCELLED"])
        return {"total": total, "active": active, "overdue": overdue, "returned": returned, "cancelled": cancelled}

    @staticmethod
    def get_guest_summary(db: Session):
        releases = db.query(ShowroomGuestRelease).all()
        total = len(releases)
        draft = len([r for r in releases if r.status == "DRAFT"])
        approved = len([r for r in releases if r.status == "APPROVED"])
        rejected = len([r for r in releases if r.status == "REJECTED"])
        returned = len([r for r in releases if r.status == "RETURNED"])
        return {"total": total, "draft": draft, "approved": approved, "rejected": rejected, "returned": returned}
