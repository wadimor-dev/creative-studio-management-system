from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta, date

from app.models.showroom_sample_stock import ShowroomSampleStock
from app.models.showroom_movement import ShowroomMovement
from app.models.showroom_borrowing import ShowroomBorrowing
from app.models.showroom_guest_release import ShowroomGuestRelease
from app.models.showroom_maintenance import ShowroomMaintenance
from app.models.showroom_restock import ShowroomRestockRequest
from app.models.showroom_storage_location import ShowroomStorageLocation
from app.models.showroom_location import ShowroomLocation
from app.models.showroom_daily_storage_summary import ShowroomDailyStorageSummary
from app.models.product import Product


class DashboardService:

    @staticmethod
    def get_summary(db: Session) -> dict:
        today = date.today()
        first_of_month = today.replace(day=1)

        total_stocks = db.query(func.coalesce(func.sum(ShowroomSampleStock.quantity), 0)).scalar()
        total_products = db.query(func.distinct(ShowroomSampleStock.product_id)).count()
        total_locations = db.query(ShowroomStorageLocation).filter(
            ShowroomStorageLocation.is_active == True
        ).count()

        movements_today = db.query(ShowroomMovement).filter(
            func.date(ShowroomMovement.date) == today
        ).count()

        incoming = db.query(ShowroomMovement).filter(
            ShowroomMovement.movement_type.in_(["SHOWROOM_IN", "HANDOVER", "RETURN"]),
            func.date(ShowroomMovement.date) == today,
        ).with_entities(func.coalesce(func.sum(ShowroomMovement.quantity), 0)).scalar()

        outgoing = db.query(ShowroomMovement).filter(
            ShowroomMovement.movement_type.in_(["SHOWROOM_OUT", "BORROW", "RELEASE"]),
            func.date(ShowroomMovement.date) == today,
        ).with_entities(func.coalesce(func.sum(ShowroomMovement.quantity), 0)).scalar()

        active_borrowings = db.query(ShowroomBorrowing).filter(
            ShowroomBorrowing.status == "BORROWED"
        ).count()

        overdue_borrowings = db.query(ShowroomBorrowing).filter(
            ShowroomBorrowing.status == "BORROWED",
            ShowroomBorrowing.expected_return_date < today,
        ).count()

        pending_guest = db.query(ShowroomGuestRelease).filter(
            ShowroomGuestRelease.status == "DRAFT"
        ).count()

        active_maintenance = db.query(ShowroomMaintenance).filter(
            ShowroomMaintenance.status.in_(["PENDING", "IN_PROGRESS"])
        ).count()

        pending_restock = db.query(ShowroomRestockRequest).filter(
            ShowroomRestockRequest.status == "PENDING"
        ).count()

        total_capacity = db.query(
            func.coalesce(func.sum(ShowroomStorageLocation.capacity_qty), 0)
        ).filter(ShowroomStorageLocation.is_active == True).scalar()

        used_capacity = db.query(
            func.coalesce(func.sum(ShowroomStorageLocation.used_capacity), 0)
        ).filter(ShowroomStorageLocation.is_active == True).scalar()

        capacity_pct = round(used_capacity / total_capacity * 100) if total_capacity > 0 else 0

        return {
            "total_items": total_stocks,
            "total_products": total_products,
            "total_locations": total_locations,
            "movements_today": movements_today,
            "incoming_today": incoming,
            "outgoing_today": outgoing,
            "active_borrowings": active_borrowings,
            "overdue_borrowings": overdue_borrowings,
            "pending_guest_releases": pending_guest,
            "active_maintenance": active_maintenance,
            "pending_restock": pending_restock,
            "capacity_used_pct": capacity_pct,
        }

    @staticmethod
    def get_recent_movements(db: Session, limit: int = 20) -> list:
        movements = (
            db.query(ShowroomMovement)
            .order_by(ShowroomMovement.date.desc())
            .limit(limit)
            .all()
        )
        result = []
        for m in movements:
            product = db.query(Product).filter(Product.id == m.product_id).first()
            from_loc = db.query(ShowroomLocation).filter(ShowroomLocation.id == m.from_location_id).first() if m.from_location_id else None
            to_loc = db.query(ShowroomLocation).filter(ShowroomLocation.id == m.to_location_id).first() if m.to_location_id else None
            from app.models.user import User
            user = db.query(User).filter(User.id == m.user_id).first()
            result.append({
                "id": m.id,
                "movement_type": m.movement_type,
                "product_name": product.display_name if product else "Unknown",
                "from_location": from_loc.name if from_loc else None,
                "to_location": to_loc.name if to_loc else None,
                "quantity": m.quantity,
                "sample_type": m.sample_type,
                "user_name": user.full_name if user else None,
                "date": str(m.date),
            })
        return result

    @staticmethod
    def get_heatmap_data(db: Session) -> list:
        stocks = db.query(ShowroomSampleStock).all()
        loc_map = {}
        for s in stocks:
            loc = db.query(ShowroomLocation).filter(ShowroomLocation.id == s.location_id).first()
            if not loc:
                continue
            key = s.location_id
            if key not in loc_map:
                loc_map[key] = {"location_id": key, "location_name": loc.name, "location_code": loc.code, "total": 0, "products": 0}
            loc_map[key]["total"] += s.quantity
            loc_map[key]["products"] += 1
        return list(loc_map.values())
