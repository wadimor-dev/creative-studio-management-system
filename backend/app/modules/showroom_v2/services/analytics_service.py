from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.models.showroom_movement import ShowroomMovement
from app.models.showroom_sample_stock import ShowroomSampleStock
from app.models.showroom_borrowing import ShowroomBorrowing
from app.models.showroom_guest_release import ShowroomGuestRelease
from app.models.showroom_maintenance import ShowroomMaintenance
from app.models.showroom_location import ShowroomLocation
from app.models.product import Product


class AnalyticsService:

    @staticmethod
    def get_movement_trends(db: Session, days: int = 30) -> list:
        cutoff = datetime.now() - timedelta(days=days)
        movements = db.query(ShowroomMovement).filter(
            ShowroomMovement.date >= cutoff
        ).all()

        daily = {}
        for m in movements:
            day_str = m.date.strftime("%Y-%m-%d") if m.date else "unknown"
            if day_str not in daily:
                daily[day_str] = {"date": day_str, "incoming": 0, "outgoing": 0}
            mtype = m.movement_type
            if mtype in ("SHOWROOM_IN", "HANDOVER", "RETURN", "RESTOCK", "TRANSFER_IN"):
                daily[day_str]["incoming"] += m.quantity
            elif mtype in ("SHOWROOM_OUT", "BORROW", "RELEASE", "SCRAP", "TRANSFER_OUT"):
                daily[day_str]["outgoing"] += m.quantity

        return sorted(daily.values(), key=lambda x: x["date"])

    @staticmethod
    def get_top_products(db: Session, limit: int = 10) -> list:
        products = db.query(
            ShowroomSampleStock.product_id,
            func.sum(ShowroomSampleStock.quantity).label("total")
        ).group_by(ShowroomSampleStock.product_id).order_by(
            func.sum(ShowroomSampleStock.quantity).desc()
        ).limit(limit).all()

        result = []
        for p_id, total in products:
            product = db.query(Product).filter(Product.id == p_id).first()
            result.append({
                "product_id": p_id,
                "product_name": product.display_name if product else "Unknown",
                "total_quantity": total,
            })
        return result

    @staticmethod
    def get_location_utilization(db: Session) -> list:
        locations = db.query(ShowroomLocation).filter(ShowroomLocation.is_active == True).all()
        result = []
        for loc in locations:
            total = db.query(func.coalesce(func.sum(ShowroomSampleStock.quantity), 0)).filter(
                ShowroomSampleStock.location_id == loc.id
            ).scalar()
            result.append({
                "location_id": loc.id,
                "location_name": loc.name,
                "location_code": loc.code,
                "total_stock": total,
            })
        return sorted(result, key=lambda x: x["total_stock"], reverse=True)

    @staticmethod
    def get_borrowing_analytics(db: Session) -> dict:
        borrowings = db.query(ShowroomBorrowing).all()
        active = [b for b in borrowings if b.status == "BORROWED"]
        overdue = [b for b in active if b.expected_return_date and b.expected_return_date < datetime.now().date()]

        avg_days = 0
        returned = [b for b in borrowings if b.status == "RETURNED" and b.borrow_date and b.actual_return_date]
        if returned:
            total_days = sum((b.actual_return_date - b.borrow_date).days for b in returned)
            avg_days = round(total_days / len(returned), 1)

        return {
            "active_count": len(active),
            "overdue_count": len(overdue),
            "total_ever": len(borrowings),
            "avg_borrow_days": avg_days,
        }

    @staticmethod
    def get_guest_analytics(db: Session) -> dict:
        releases = db.query(ShowroomGuestRelease).all()
        return {
            "total": len(releases),
            "approved": len([r for r in releases if r.status == "APPROVED"]),
            "rejected": len([r for r in releases if r.status == "REJECTED"]),
            "pending": len([r for r in releases if r.status == "DRAFT"]),
        }
