from typing import Callable, Dict, Optional, Any
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.qr.models import ShowroomQREntity

_RESOLVERS: Dict[str, Callable] = {}


def register_resolver(entity_type: str, resolver: Callable):
    _RESOLVERS[entity_type] = resolver


def resolve_qr_token(db: Session, token: str) -> Optional[Dict[str, Any]]:
    qr = (
        db.query(ShowroomQREntity)
        .filter(ShowroomQREntity.token == token, ShowroomQREntity.is_active == True)
        .first()
    )
    if not qr:
        raise HTTPException(status_code=404, detail="QR code not found or inactive")

    resolver = _RESOLVERS.get(qr.entity_type)
    if not resolver:
        raise HTTPException(status_code=400, detail=f"No resolver for entity type: {qr.entity_type}")

    entity = resolver(db, qr.entity_type, qr.entity_id)
    if not entity:
        raise HTTPException(status_code=404, detail=f"Entity not found: {qr.entity_type}:{qr.entity_id}")

    return {
        "qr": {
            "id": qr.id,
            "token": qr.token,
            "entity_type": qr.entity_type,
            "entity_id": qr.entity_id,
            "label": qr.label,
        },
        "entity": entity,
    }


def _resolve_storage_location(db: Session, entity_type: str, entity_id: int) -> Optional[Dict]:
    from app.models.showroom_storage_location import ShowroomStorageLocation
    from app.models.showroom_location import ShowroomLocation
    loc = db.query(ShowroomStorageLocation).filter(ShowroomStorageLocation.id == entity_id).first()
    if not loc:
        return None
    showroom_loc = db.query(ShowroomLocation).filter(ShowroomLocation.id == loc.location_id).first() if loc.location_id else None
    return {
        "id": loc.id,
        "name": loc.name,
        "code": loc.code,
        "storage_type": loc.storage_type,
        "capacity_qty": loc.capacity_qty,
        "capacity_unit": loc.capacity_unit,
        "used_capacity": loc.used_capacity,
        "path": loc.path,
        "location_id": loc.location_id,
        "location_name": showroom_loc.name if showroom_loc else None,
    }


def _resolve_product(db: Session, entity_type: str, entity_id: int) -> Optional[Dict]:
    from app.models.product import Product
    p = db.query(Product).filter(Product.id == entity_id).first()
    if not p:
        return None
    return {
        "id": p.id,
        "display_name": p.display_name,
        "sku": getattr(p, "sku", None),
        "category": {"id": p.category.id, "name": p.category.name} if p.category else None,
        "motif": {"id": p.motif.id, "name": p.motif.name} if p.motif else None,
        "sub_motif": {"id": p.sub_motif.id, "name": p.sub_motif.name} if p.sub_motif else None,
        "variant": p.variant,
    }


def _resolve_showroom_location(db: Session, entity_type: str, entity_id: int) -> Optional[Dict]:
    from app.models.showroom_location import ShowroomLocation
    loc = db.query(ShowroomLocation).filter(ShowroomLocation.id == entity_id).first()
    if not loc:
        return None
    from app.models.showroom_sample_stock import ShowroomSampleStock
    from app.models.product import Product
    stocks = db.query(ShowroomSampleStock).filter(ShowroomSampleStock.location_id == loc.id).all()
    product_ids = list(set(s.product_id for s in stocks))
    product_count = len(product_ids)
    total_qty = sum(s.quantity for s in stocks)
    return {
        "id": loc.id,
        "name": loc.name,
        "code": loc.code,
        "type": loc.type,
        "description": loc.description,
        "product_count": product_count,
        "total_quantity": total_qty,
    }


register_resolver("storage", _resolve_storage_location)
register_resolver("product", _resolve_product)
register_resolver("location", _resolve_showroom_location)
