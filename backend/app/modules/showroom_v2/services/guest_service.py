from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.showroom_guest_release import ShowroomGuestRelease
from app.models.showroom_movement import ShowroomMovement, ShowroomMovementType
from app.models.showroom_sample_stock import ShowroomSampleStock
from app.models.product import Product
from app.models.showroom_location import ShowroomLocation
from app.models.user import User
from app.modules.showroom_v2.schemas import GuestReleaseCreate, GuestReleaseResponse
from app.modules.showroom_v2.services.base import jakarta_now, get_or_404


class GuestService:

    @staticmethod
    def _to_dict(g: ShowroomGuestRelease, db: Session) -> dict:
        product = db.query(Product).filter(Product.id == g.product_id).first()
        location = db.query(ShowroomLocation).filter(ShowroomLocation.id == g.location_id).first() if g.location_id else None
        user = db.query(User).filter(User.id == g.user_id).first()
        approver = db.query(User).filter(User.id == g.approved_by).first() if g.approved_by else None
        rejector = db.query(User).filter(User.id == g.rejected_by).first() if g.rejected_by else None
        movement_dict = None
        if g.movement_id:
            m = db.query(ShowroomMovement).filter(ShowroomMovement.id == g.movement_id).first()
            if m:
                movement_dict = {"id": m.id, "movement_type": m.movement_type.value if hasattr(m.movement_type, 'value') else m.movement_type, "date": str(m.date)}
        return {
            "id": g.id,
            "product": {"id": product.id, "name": product.display_name} if product else None,
            "location": {"id": location.id, "name": location.name, "code": location.code} if location else None,
            "quantity": g.quantity,
            "sample_type": g.sample_type,
            "guest_name": g.guest_name,
            "guest_company": g.guest_company,
            "purpose": g.purpose,
            "release_date": str(g.release_date),
            "status": g.status,
            "user": {"id": user.id, "name": user.full_name} if user else None,
            "approved_by": {"id": approver.id, "name": approver.full_name} if approver else None,
            "approved_at": str(g.approved_at) if g.approved_at else None,
            "rejected_by": {"id": rejector.id, "name": rejector.full_name} if rejector else None,
            "rejected_at": str(g.rejected_at) if g.rejected_at else None,
            "movement": movement_dict,
            "notes": g.notes,
            "created_at": str(g.created_at) if g.created_at else None,
        }

    @staticmethod
    def get_all(db: Session, status: str = None):
        query = db.query(ShowroomGuestRelease).order_by(ShowroomGuestRelease.created_at.desc())
        if status:
            query = query.filter(ShowroomGuestRelease.status == status.upper())
        releases = query.all()
        return [GuestService._to_dict(r, db) for r in releases]

    @staticmethod
    def get_by_id(db: Session, release_id: int):
        r = get_or_404(db, ShowroomGuestRelease, release_id, "Guest Release")
        return GuestService._to_dict(r, db)

    @staticmethod
    def create_release(db: Session, data: GuestReleaseCreate, user_id: int):
        from datetime import datetime as dt
        get_or_404(db, Product, data.product_id, "Product")
        get_or_404(db, ShowroomLocation, data.location_id, "Location")

        release = ShowroomGuestRelease(
            product_id=data.product_id,
            location_id=data.location_id,
            quantity=data.quantity,
            sample_type=data.sample_type,
            guest_name=data.guest_name,
            guest_company=data.guest_company,
            purpose=data.purpose,
            release_date=dt.strptime(data.release_date, "%Y-%m-%d").date(),
            status="DRAFT",
            user_id=user_id,
            notes=data.notes,
        )
        db.add(release)
        db.commit()
        db.refresh(release)
        return GuestService._to_dict(release, db)

    @staticmethod
    def approve_release(db: Session, release_id: int, user_id: int):
        from app.modules.showroom_v2.services.sample_service import SampleService
        release = get_or_404(db, ShowroomGuestRelease, release_id, "Guest Release")
        if release.status != "DRAFT":
            raise HTTPException(status_code=400, detail=f"Cannot approve release with status {release.status}")

        existing = db.query(ShowroomSampleStock).filter(
            ShowroomSampleStock.product_id == release.product_id,
            ShowroomSampleStock.location_id == release.location_id,
            ShowroomSampleStock.sample_type == release.sample_type,
        ).first()
        if not existing or existing.quantity < release.quantity:
            avail = existing.quantity if existing else 0
            raise HTTPException(status_code=400, detail=f"Insufficient stock (available: {avail})")

        movement = SampleService._create_movement(
            db=db,
            movement_type=ShowroomMovementType.RELEASE,
            product_id=release.product_id,
            quantity=release.quantity,
            user_id=user_id,
            from_location_id=release.location_id,
            sample_type=release.sample_type,
            purpose=f"Release to {release.guest_name}" + (f" ({release.guest_company})" if release.guest_company else ""),
            notes=release.notes,
            reference_type="guest_release",
            reference_id=release.id,
        )
        SampleService._update_stock(db, release.product_id, release.location_id, -release.quantity, release.sample_type)

        release.status = "APPROVED"
        release.approved_by = user_id
        release.approved_at = jakarta_now()
        release.movement_id = movement.id
        db.commit()
        db.refresh(release)
        return GuestService._to_dict(release, db)

    @staticmethod
    def reject_release(db: Session, release_id: int, user_id: int, reason: str = None):
        release = get_or_404(db, ShowroomGuestRelease, release_id, "Guest Release")
        if release.status != "DRAFT":
            raise HTTPException(status_code=400, detail=f"Cannot reject release with status {release.status}")

        release.status = "REJECTED"
        release.rejected_by = user_id
        release.rejected_at = jakarta_now()
        if reason:
            release.notes = f"[Rejected] {reason}" + (f"\n{release.notes}" if release.notes else "")
        db.commit()
        db.refresh(release)
        return GuestService._to_dict(release, db)

    @staticmethod
    def return_from_guest(db: Session, release_id: int, location_id: int, user_id: int, notes: str = None):
        from app.modules.showroom_v2.services.sample_service import SampleService
        release = get_or_404(db, ShowroomGuestRelease, release_id, "Guest Release")
        if release.status != "APPROVED":
            raise HTTPException(status_code=400, detail=f"Cannot return release with status {release.status}")

        movement = SampleService._create_movement(
            db=db,
            movement_type=ShowroomMovementType.RETURN,
            product_id=release.product_id,
            quantity=release.quantity,
            user_id=user_id,
            to_location_id=location_id,
            sample_type=release.sample_type,
            purpose=f"Return from {release.guest_name}",
            notes=notes,
            reference_type="guest_release",
            reference_id=release.id,
        )
        SampleService._update_stock(db, release.product_id, location_id, release.quantity, release.sample_type)

        release.status = "RETURNED"
        db.commit()
        return {"status": "returned", "movement_id": movement.id}

    @staticmethod
    def get_stats(db: Session):
        from datetime import date as dt_date
        today = dt_date.today()
        draft = db.query(ShowroomGuestRelease).filter(ShowroomGuestRelease.status == "DRAFT").count()
        released_this_month = db.query(ShowroomGuestRelease).filter(
            ShowroomGuestRelease.status == "APPROVED",
            ShowroomGuestRelease.release_date >= today.replace(day=1),
        ).count()
        total_guests = db.query(ShowroomGuestRelease).filter(
            ShowroomGuestRelease.status == "APPROVED"
        ).count()
        return {
            "pending_approval": draft,
            "released_this_month": released_this_month,
            "total_guests": total_guests,
        }
