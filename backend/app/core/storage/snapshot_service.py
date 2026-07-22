from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from app.models.showroom_sample_stock import ShowroomSampleStock
from app.models.showroom_storage_snapshot import ShowroomStorageSnapshot
from app.models.showroom_daily_storage_summary import ShowroomDailyStorageSummary
from app.models.showroom_storage_location import ShowroomStorageLocation
from app.models.showroom_movement import ShowroomMovement
from app.core.database.helpers import jakarta_now


class SnapshotService:

    @staticmethod
    def create_snapshot(db: Session, snapshot_type: str = "MANUAL") -> dict:
        stocks = db.query(ShowroomSampleStock).filter(
            ShowroomSampleStock.storage_location_id.isnot(None)
        ).all()

        count = 0
        for s in stocks:
            snap = ShowroomStorageSnapshot(
                storage_location_id=s.storage_location_id,
                product_id=s.product_id,
                sample_type=s.sample_type,
                quantity=s.quantity,
                snapshot_type=snapshot_type,
            )
            db.add(snap)
            count += 1

        db.flush()
        db.commit()
        return {"snapshots_created": count, "type": snapshot_type}

    @staticmethod
    def rebuild_daily_summary(db: Session, target_date: str = None) -> dict:
        if target_date:
            summary_date = datetime.strptime(target_date, "%Y-%m-%d").date()
        else:
            summary_date = jakarta_now().date()

        total_items = db.query(func.coalesce(func.sum(ShowroomSampleStock.quantity), 0)).scalar()
        total_products = db.query(func.distinct(ShowroomSampleStock.product_id)).count()
        total_locations = db.query(ShowroomStorageLocation).filter(
            ShowroomStorageLocation.is_active == True
        ).count()

        movements = db.query(ShowroomMovement).filter(
            func.date(ShowroomMovement.date) == summary_date
        ).all()

        total_movements = len(movements)
        incoming = sum(m.quantity for m in movements if m.movement_type in ("SHOWROOM_IN", "HANDOVER", "RETURN", "RESTOCK"))
        outgoing = sum(m.quantity for m in movements if m.movement_type in ("SHOWROOM_OUT", "BORROW", "RELEASE", "SCRAP"))

        total_capacity = db.query(
            func.coalesce(func.sum(ShowroomStorageLocation.capacity_qty), 0)
        ).filter(ShowroomStorageLocation.is_active == True).scalar()
        used_capacity = db.query(
            func.coalesce(func.sum(ShowroomStorageLocation.used_capacity), 0)
        ).filter(ShowroomStorageLocation.is_active == True).scalar()
        capacity_pct = round(used_capacity / total_capacity * 100) if total_capacity > 0 else 0

        existing = db.query(ShowroomDailyStorageSummary).filter(
            ShowroomDailyStorageSummary.summary_date == summary_date
        ).first()

        if existing:
            existing.total_items = total_items
            existing.total_products = total_products
            existing.total_locations = total_locations
            existing.total_movements = total_movements
            existing.incoming = incoming
            existing.outgoing = outgoing
            existing.capacity_used_pct = capacity_pct
        else:
            summary = ShowroomDailyStorageSummary(
                summary_date=summary_date,
                total_items=total_items,
                total_products=total_products,
                total_locations=total_locations,
                total_movements=total_movements,
                incoming=incoming,
                outgoing=outgoing,
                capacity_used_pct=capacity_pct,
            )
            db.add(summary)

        db.flush()
        db.commit()
        return {
            "date": str(summary_date),
            "total_items": total_items,
            "total_products": total_products,
            "incoming": incoming,
            "outgoing": outgoing,
            "capacity_pct": capacity_pct,
        }

    @staticmethod
    def get_summary_history(db: Session, days: int = 30) -> list:
        from datetime import timedelta
        cutoff = jakarta_now().date() - timedelta(days=days)
        summaries = db.query(ShowroomDailyStorageSummary).filter(
            ShowroomDailyStorageSummary.summary_date >= cutoff
        ).order_by(ShowroomDailyStorageSummary.summary_date).all()
        return [
            {
                "date": str(s.summary_date),
                "total_items": s.total_items,
                "incoming": s.incoming,
                "outgoing": s.outgoing,
                "capacity_pct": s.capacity_used_pct,
            }
            for s in summaries
        ]
