from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.core.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.showroom_movement_type import MovementType
from app.modules.showroom_v2.schemas import SuccessResponse

router = APIRouter()


class MovementTypeCreate(BaseModel):
    code: str
    name: str
    direction: str
    is_active: bool = True
    notes: Optional[str] = None


class MovementTypeUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    direction: Optional[str] = None
    is_active: Optional[bool] = None
    notes: Optional[str] = None


@router.get("/")
def get_movement_types(
    active_only: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = db.query(MovementType)
    if active_only:
        q = q.filter(MovementType.is_active.is_(True))
    items = q.order_by(MovementType.code).all()
    return SuccessResponse(data=[{
        "id": t.id,
        "code": t.code,
        "name": t.name,
        "direction": t.direction,
        "is_active": t.is_active,
        "notes": t.notes,
    } for t in items])


@router.get("/{item_id}")
def get_movement_type(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    t = db.query(MovementType).filter(MovementType.id == item_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Movement type not found")
    return SuccessResponse(data={
        "id": t.id, "code": t.code, "name": t.name,
        "direction": t.direction, "is_active": t.is_active, "notes": t.notes,
    })


@router.post("/")
def create_movement_type(
    data: MovementTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = db.query(MovementType).filter(MovementType.code == data.code).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Code '{data.code}' already exists")
    if data.direction not in ("IN", "OUT"):
        raise HTTPException(status_code=400, detail="Direction must be IN or OUT")
    t = MovementType(code=data.code, name=data.name, direction=data.direction, is_active=data.is_active, notes=data.notes)
    db.add(t)
    db.commit()
    db.refresh(t)
    return SuccessResponse(data={
        "id": t.id, "code": t.code, "name": t.name,
        "direction": t.direction, "is_active": t.is_active, "notes": t.notes,
    }, message="Movement type created")


@router.put("/{item_id}")
def update_movement_type(
    item_id: int,
    data: MovementTypeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    t = db.query(MovementType).filter(MovementType.id == item_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Movement type not found")
    if data.code is not None:
        dup = db.query(MovementType).filter(MovementType.code == data.code, MovementType.id != item_id).first()
        if dup:
            raise HTTPException(status_code=400, detail=f"Code '{data.code}' already exists")
        t.code = data.code
    if data.name is not None:
        t.name = data.name
    if data.direction is not None:
        if data.direction not in ("IN", "OUT"):
            raise HTTPException(status_code=400, detail="Direction must be IN or OUT")
        t.direction = data.direction
    if data.is_active is not None:
        t.is_active = data.is_active
    if data.notes is not None:
        t.notes = data.notes
    db.commit()
    db.refresh(t)
    return SuccessResponse(data={
        "id": t.id, "code": t.code, "name": t.name,
        "direction": t.direction, "is_active": t.is_active, "notes": t.notes,
    }, message="Movement type updated")


@router.delete("/{item_id}")
def delete_movement_type(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    t = db.query(MovementType).filter(MovementType.id == item_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Movement type not found")
    db.delete(t)
    db.commit()
    return SuccessResponse(message="Movement type deleted")
