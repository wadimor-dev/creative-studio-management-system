from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List, Dict
from fastapi import HTTPException
import json

from app.models.showroom_storage_location import ShowroomStorageLocation
from app.models.showroom_sample_stock import ShowroomSampleStock
from app.modules.showroom_v2.services.base import jakarta_now, get_or_404, log_activity


class StorageService:

    @staticmethod
    def _rebuild_path(db: Session, location_id: int) -> str:
        parts = []
        current_id = location_id
        visited = set()
        while current_id:
            if current_id in visited:
                raise HTTPException(status_code=500, detail="Circular reference detected in storage locations")
            visited.add(current_id)
            loc = db.query(ShowroomStorageLocation).filter(ShowroomStorageLocation.id == current_id).first()
            if not loc:
                break
            parts.append(loc.code)
            current_id = loc.parent_id
        return "/".join(reversed(parts))

    @staticmethod
    def _rebuild_all_paths(db: Session, location_id: int):
        children = db.query(ShowroomStorageLocation).filter(
            ShowroomStorageLocation.parent_id == location_id
        ).all()
        for child in children:
            child.path = StorageService._rebuild_path(db, child.id)
            db.flush()
            StorageService._rebuild_all_paths(db, child.id)

    @staticmethod
    def _recalculate_capacity(db: Session, storage_location_id: int) -> int:
        total = (
            db.query(func.coalesce(func.sum(ShowroomSampleStock.quantity), 0))
            .filter(ShowroomSampleStock.storage_location_id == storage_location_id)
            .scalar()
        )
        loc = db.query(ShowroomStorageLocation).filter(
            ShowroomStorageLocation.id == storage_location_id
        ).first()
        if loc:
            loc.used_capacity = total
            db.flush()
        return total

    @staticmethod
    def _validate_depth(db: Session, parent_id: int = None) -> None:
        if not parent_id:
            return
        parent = get_or_404(db, ShowroomStorageLocation, parent_id, "Parent storage location")
        if parent.parent_id:
            raise HTTPException(
                status_code=400,
                detail="Maximum storage depth exceeded (max 2 levels: root → child → leaf)",
            )

    @staticmethod
    def _to_dict(loc: ShowroomStorageLocation, db: Session) -> dict:
        return {
            "id": loc.id,
            "name": loc.name,
            "code": loc.code,
            "parent_id": loc.parent_id,
            "location_id": loc.location_id,
            "storage_type": loc.storage_type,
            "capacity_qty": loc.capacity_qty,
            "capacity_unit": loc.capacity_unit,
            "capacity_note": loc.capacity_note,
            "used_capacity": loc.used_capacity,
            "path": loc.path,
            "description": loc.description,
            "is_active": loc.is_active,
            "version": loc.version,
            "created_at": str(loc.created_at) if loc.created_at else None,
            "updated_at": str(loc.updated_at) if loc.updated_at else None,
        }

    @staticmethod
    def get_all(db: Session, location_id: int = None, parent_id: int = None) -> List[Dict]:
        query = db.query(ShowroomStorageLocation).filter(ShowroomStorageLocation.is_active == True)
        if location_id:
            query = query.filter(ShowroomStorageLocation.location_id == location_id)
        if parent_id is not None:
            query = query.filter(ShowroomStorageLocation.parent_id == parent_id)
        locs = query.order_by(ShowroomStorageLocation.path).all()
        return [StorageService._to_dict(l, db) for l in locs]

    @staticmethod
    def get_tree(db: Session, location_id: int = None) -> List[Dict]:
        query = db.query(ShowroomStorageLocation).filter(ShowroomStorageLocation.is_active == True)
        if location_id:
            query = query.filter(ShowroomStorageLocation.location_id == location_id)
        all_locs = query.order_by(ShowroomStorageLocation.path).all()
        loc_map = {l.id: {**StorageService._to_dict(l, db), "children": []} for l in all_locs}
        roots = []
        for l in all_locs:
            node = loc_map[l.id]
            if l.parent_id and l.parent_id in loc_map:
                loc_map[l.parent_id]["children"].append(node)
            else:
                roots.append(node)
        return roots

    @staticmethod
    def get_by_id(db: Session, storage_id: int) -> Dict:
        loc = get_or_404(db, ShowroomStorageLocation, storage_id, "Storage location")
        return StorageService._to_dict(loc, db)

    @staticmethod
    def create(db: Session, data: dict, user_id: int) -> Dict:
        StorageService._validate_depth(db, data.get("parent_id"))

        existing = db.query(ShowroomStorageLocation).filter(
            ShowroomStorageLocation.code == data["code"]
        ).first()
        if existing:
            raise HTTPException(status_code=409, detail=f"Storage location code '{data['code']}' already exists")

        loc = ShowroomStorageLocation(
            name=data["name"],
            code=data["code"],
            parent_id=data.get("parent_id"),
            location_id=data["location_id"],
            storage_type=data.get("storage_type", "shelf"),
            capacity_qty=data.get("capacity_qty"),
            capacity_unit=data.get("capacity_unit", "PCS"),
            capacity_note=data.get("capacity_note"),
            description=data.get("description"),
            used_capacity=0,
            version=1,
        )
        db.add(loc)
        db.flush()

        loc.path = StorageService._rebuild_path(db, loc.id)
        db.flush()

        log_activity(
            db, action="STORAGE_CREATE", entity_type="storage_location",
            entity_id=loc.id, user_id=user_id,
            new_value=json.dumps(StorageService._to_dict(loc, db), default=str),
        )

        db.commit()
        return StorageService._to_dict(loc, db)

    @staticmethod
    def update(db: Session, storage_id: int, data: dict, user_id: int) -> Dict:
        loc = get_or_404(db, ShowroomStorageLocation, storage_id, "Storage location")

        if "parent_id" in data:
            if data["parent_id"] == storage_id:
                raise HTTPException(status_code=400, detail="Cannot set self as parent")
            StorageService._validate_depth(db, data["parent_id"])

        if "code" in data and data["code"] != loc.code:
            existing = db.query(ShowroomStorageLocation).filter(
                ShowroomStorageLocation.code == data["code"],
                ShowroomStorageLocation.id != storage_id,
            ).first()
            if existing:
                raise HTTPException(status_code=409, detail=f"Code '{data['code']}' already exists")

        old_val = StorageService._to_dict(loc, db)

        for field in ["name", "code", "parent_id", "location_id", "storage_type",
                       "capacity_qty", "capacity_unit", "capacity_note", "description", "is_active"]:
            if field in data:
                setattr(loc, field, data[field])

        loc.version += 1

        if "parent_id" in data or "code" in data:
            loc.path = StorageService._rebuild_path(db, loc.id)
            StorageService._rebuild_all_paths(db, loc.id)

        db.flush()

        log_activity(
            db, action="STORAGE_UPDATE", entity_type="storage_location",
            entity_id=loc.id, user_id=user_id,
            old_value=json.dumps(old_val, default=str),
            new_value=json.dumps(StorageService._to_dict(loc, db), default=str),
        )

        db.commit()
        return StorageService._to_dict(loc, db)

    @staticmethod
    def delete(db: Session, storage_id: int, user_id: int):
        loc = get_or_404(db, ShowroomStorageLocation, storage_id, "Storage location")

        children = db.query(ShowroomStorageLocation).filter(
            ShowroomStorageLocation.parent_id == storage_id
        ).count()
        if children > 0:
            raise HTTPException(status_code=400, detail="Cannot delete storage location with children")

        stocks = db.query(ShowroomSampleStock).filter(
            ShowroomSampleStock.storage_location_id == storage_id
        ).count()
        if stocks > 0:
            raise HTTPException(status_code=400, detail="Cannot delete storage location with stock")

        loc.is_active = False
        loc.version += 1
        db.flush()

        log_activity(
            db, action="STORAGE_DELETE", entity_type="storage_location",
            entity_id=loc.id, user_id=user_id,
            old_value=json.dumps(StorageService._to_dict(loc, db), default=str),
        )

        db.commit()
        return {"message": "Storage location deactivated", "id": storage_id}
