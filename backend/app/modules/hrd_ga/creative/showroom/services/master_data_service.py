from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.showroom_master_data import ShowroomMasterData
from app.modules.hrd_ga.creative.showroom.schemas import MasterDataCreate, MasterDataUpdate
from app.modules.hrd_ga.creative.showroom.services.base import get_or_404


class MasterDataService:

    VALID_TYPES = [
        "location_type",
        "purpose",
        "sample_type",
        "maintenance_type",
        "borrow_reason",
        "release_reason",
    ]

    @staticmethod
    def _to_dict(m: ShowroomMasterData) -> dict:
        return {
            "id": m.id,
            "type": m.type,
            "name": m.name,
            "value": m.value,
            "description": m.description,
            "is_active": m.is_active,
            "sort_order": m.sort_order,
        }

    @staticmethod
    def get_all(db: Session, item_type: str = None, active_only: bool = False):
        query = db.query(ShowroomMasterData)
        if item_type:
            query = query.filter(ShowroomMasterData.type == item_type)
        if active_only:
            query = query.filter(ShowroomMasterData.is_active == True)
        query = query.order_by(ShowroomMasterData.type, ShowroomMasterData.sort_order, ShowroomMasterData.name)
        items = query.all()
        return [MasterDataService._to_dict(i) for i in items]

    @staticmethod
    def get_by_id(db: Session, item_id: int):
        item = get_or_404(db, ShowroomMasterData, item_id, "Master Data")
        return MasterDataService._to_dict(item)

    @staticmethod
    def create(db: Session, data: MasterDataCreate):
        if data.type not in MasterDataService.VALID_TYPES:
            raise HTTPException(status_code=400, detail=f"Invalid type. Valid: {MasterDataService.VALID_TYPES}")

        existing = db.query(ShowroomMasterData).filter(
            ShowroomMasterData.type == data.type,
            ShowroomMasterData.value == data.value,
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail=f"Value '{data.value}' already exists for type '{data.type}'")

        item = ShowroomMasterData(
            type=data.type,
            name=data.name,
            value=data.value,
            description=data.description,
            sort_order=data.sort_order or 0,
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        return MasterDataService._to_dict(item)

    @staticmethod
    def update(db: Session, item_id: int, data: MasterDataUpdate):
        item = get_or_404(db, ShowroomMasterData, item_id, "Master Data")
        if data.name is not None:
            item.name = data.name
        if data.value is not None:
            existing = db.query(ShowroomMasterData).filter(
                ShowroomMasterData.type == item.type,
                ShowroomMasterData.value == data.value,
                ShowroomMasterData.id != item_id,
            ).first()
            if existing:
                raise HTTPException(status_code=400, detail=f"Value '{data.value}' already exists")
            item.value = data.value
        if data.description is not None:
            item.description = data.description
        if data.is_active is not None:
            item.is_active = data.is_active
        if data.sort_order is not None:
            item.sort_order = data.sort_order
        db.commit()
        return MasterDataService._to_dict(item)

    @staticmethod
    def delete(db: Session, item_id: int):
        item = get_or_404(db, ShowroomMasterData, item_id, "Master Data")
        db.delete(item)
        db.commit()
        return {"deleted": True}

    @staticmethod
    def seed_defaults(db: Session):
        defaults = [
            ("sample_type", "Display", "display", "Untuk tampilan/etagere", 1),
            ("sample_type", "Photography", "photography", "Untuk kebutuhan foto/shooting", 2),
            ("sample_type", "Premium", "premium", "Sample kualitas premium untuk VIP", 3),
            ("sample_type", "Archive", "archive", "Sample arsip/tidak aktif", 4),
            ("maintenance_type", "Cleaning", "CLEANING", "Pembersihan sample", 1),
            ("maintenance_type", "Repair", "REPAIR", "Perbaikan sample", 2),
            ("maintenance_type", "Laundry", "LAUNDRY", "Pencucian sample", 3),
            ("maintenance_type", "Retired", "RETIRED", "Sample sudah tidak layak", 4),
            ("maintenance_type", "Other", "OTHER", "Maintenance lainnya", 5),
            ("purpose", "Display", "display", "Untuk etagere display", 1),
            ("purpose", "Photography", "photography", "Untuk kebutuhan foto", 2),
            ("purpose", "Shooting", "shooting", "Untuk kebutuhan video/shooting", 3),
            ("purpose", "Exhibition", "exhibition", "Untuk pameran/pamer", 4),
            ("purpose", "Client Meeting", "client_meeting", "Untuk pertemuan klien", 5),
            ("purpose", "Quality Check", "quality_check", "Pengecekan kualitas", 6),
            ("borrow_reason", "Internal Display", "internal_display", "Pinjam untuk display internal", 1),
            ("borrow_reason", "Photography", "photography", "Pinjam untuk foto", 2),
            ("borrow_reason", "Client Preview", "client_preview", "Pinjam untuk preview klien", 3),
            ("borrow_reason", "Maintenance", "maintenance", "Pinjam untuk perawatan", 4),
            ("release_reason", "Client Sampling", "client_sampling", "Rilis untuk sampling klien", 1),
            ("release_reason", "Exhibition", "exhibition", "Rilis untuk pameran", 2),
            ("release_reason", "Marketing", "marketing", "Rilis untuk kebutuhan marketing", 3),
            ("release_reason", "VIP Display", "vip_display", "Rilis untuk VIP display", 4),
            ("location_type", "Internal", "internal", "Lokasi dalam showroom", 1),
            ("location_type", "External", "external", "Lokasi luar showroom", 2),
        ]

        seeded = 0
        for dtype, name, value, desc, order in defaults:
            existing = db.query(ShowroomMasterData).filter(
                ShowroomMasterData.type == dtype,
                ShowroomMasterData.value == value,
            ).first()
            if not existing:
                item = ShowroomMasterData(
                    type=dtype, name=name, value=value,
                    description=desc, sort_order=order,
                )
                db.add(item)
                seeded += 1
        db.commit()
        return {"seeded": seeded, "total_defaults": len(defaults)}
