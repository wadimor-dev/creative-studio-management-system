from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.core.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.modules.hrd_ga.creative.showroom.schemas import GuestReleaseCreate, SuccessResponse
from app.modules.hrd_ga.creative.showroom.services.guest_service import GuestService

router = APIRouter()


class RejectRelease(BaseModel):
    reason: Optional[str] = None


class ReturnFromGuest(BaseModel):
    location_id: int
    notes: Optional[str] = None


@router.get("/")
def get_releases(
    status: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    releases = GuestService.get_all(db, status)
    return SuccessResponse(data=releases)


@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stats = GuestService.get_stats(db)
    return SuccessResponse(data=stats)


@router.get("/{release_id}")
def get_release(
    release_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    release = GuestService.get_by_id(db, release_id)
    return SuccessResponse(data=release)


@router.post("/")
def create_release(
    data: GuestReleaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    release = GuestService.create_release(db, data, current_user.id)
    return SuccessResponse(data=release, message="Guest release created (Draft)")


@router.post("/{release_id}/approve")
def approve_release(
    release_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    release = GuestService.approve_release(db, release_id, current_user.id)
    return SuccessResponse(data=release, message="Guest release approved and stock reduced")


@router.post("/{release_id}/reject")
def reject_release(
    release_id: int,
    data: RejectRelease,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    release = GuestService.reject_release(db, release_id, current_user.id, data.reason)
    return SuccessResponse(data=release, message="Guest release rejected")


@router.post("/{release_id}/return")
def return_from_guest(
    release_id: int,
    data: ReturnFromGuest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = GuestService.return_from_guest(db, release_id, data.location_id, current_user.id, data.notes)
    return SuccessResponse(data=result, message="Sample returned from guest")
