"""Shared helpers for showroom services (product / placement domain)."""

from __future__ import annotations

import re
from datetime import datetime, timezone, timedelta
from typing import Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.core.exceptions import CSMSException
from app.models.product import Product
from app.models.product_movement import ProductMovement, ProductMovementReason
from app.models.product_placement import ProductPlacement

STATUS_TAG_RE = re.compile(r"\[showroom:(\w+)\]")
ID_PREFIX_RE = re.compile(r"^(?:TRF|IN|OUT|MOV)-(\d+)$", re.IGNORECASE)

# Frontend stock-out reason values → ProductMovementReason
STOCK_OUT_REASON_MAP = {
    "penjualan-regular": ProductMovementReason.OTHER,
    "pesanan-khusus": ProductMovementReason.OTHER,
    "transfer": ProductMovementReason.OTHER,
    "rusak": ProductMovementReason.DAMAGED,
    "hilang": ProductMovementReason.MISSING,
    "sample": ProductMovementReason.SALES_SAMPLE,
    "lainnya": ProductMovementReason.OTHER,
    "gift": ProductMovementReason.GIFT,
    "sales_sample": ProductMovementReason.SALES_SAMPLE,
    "sales-sample": ProductMovementReason.SALES_SAMPLE,
    "damaged": ProductMovementReason.DAMAGED,
    "missing": ProductMovementReason.MISSING,
    "photo_shoot": ProductMovementReason.PHOTO_SHOOT,
    "tv_studio": ProductMovementReason.TV_STUDIO,
}


def jakarta_now() -> datetime:
    return datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None)


def jakarta_today():
    return jakarta_now().date()


def placement_slug(placement: ProductPlacement) -> str:
    """Stable UI id: prefer code, else slugified name."""
    if placement.code:
        return placement.code.lower().replace(" ", "-")
    return placement.name.lower().replace(" ", "-")


def location_slug(name: str) -> str:
    return name.lower().replace(" ", "-")


def resolve_placement(db: Session, location_key: str) -> ProductPlacement:
    """Resolve product placement by code, name, slug, or numeric id."""
    if not location_key:
        raise CSMSException("Location is required", status_code=400)

    query = db.query(ProductPlacement).options(joinedload(ProductPlacement.placement_type))

    placement = query.filter(
        or_(
            ProductPlacement.code == location_key,
            ProductPlacement.name == location_key,
        )
    ).first()
    if placement:
        return placement

    if location_key.isdigit():
        placement = query.filter(ProductPlacement.id == int(location_key)).first()
        if placement:
            return placement

    key = location_key.lower().strip()
    for placement in query.filter(ProductPlacement.is_active.is_(True)).all():
        if placement_slug(placement) == key:
            return placement
        if location_slug(placement.name) == key:
            return placement
        if placement.code and placement.code.lower() == key:
            return placement

    raise CSMSException(f"Location not found: {location_key}", status_code=404)


def resolve_product(db: Session, product_key: str) -> Product:
    """Resolve finished-goods product by SKU or display_name."""
    if not product_key:
        raise CSMSException("Product is required", status_code=400)

    product = (
        db.query(Product)
        .filter(or_(Product.sku == product_key, Product.display_name == product_key))
        .first()
    )
    if product:
        return product

    key = product_key.lower().strip()
    product = (
        db.query(Product)
        .filter(or_(Product.sku.ilike(key), Product.display_name.ilike(key)))
        .first()
    )
    if product:
        return product

    raise CSMSException(f"Product not found: {product_key}", status_code=404)


def map_stock_out_reason(reason: Optional[str]) -> ProductMovementReason:
    if not reason:
        return ProductMovementReason.OTHER

    normalized = reason.strip().lower().replace(" ", "-")
    if normalized in STOCK_OUT_REASON_MAP:
        return STOCK_OUT_REASON_MAP[normalized]

    # Allow raw enum values from API clients
    try:
        return ProductMovementReason(reason.strip().upper())
    except ValueError:
        return ProductMovementReason.OTHER


def parse_prefixed_id(raw_id: str, expected_prefix: Optional[str] = None) -> int:
    """Parse TRF-0001 / IN-0001 / OUT-0001 / MOV-0001 into integer id."""
    if raw_id.isdigit():
        return int(raw_id)

    match = ID_PREFIX_RE.match(raw_id.strip())
    if not match:
        raise CSMSException(f"Invalid id format: {raw_id}", status_code=400)

    if expected_prefix:
        prefix = raw_id.split("-", 1)[0].upper()
        if prefix != expected_prefix.upper():
            raise CSMSException(
                f"Expected id prefix {expected_prefix}, got {prefix}",
                status_code=400,
            )

    return int(match.group(1))


def get_showroom_status(notes: Optional[str], default: str = "completed") -> str:
    if notes:
        match = STATUS_TAG_RE.search(notes)
        if match:
            return match.group(1)
    return default


def set_showroom_status(notes: Optional[str], status: str) -> str:
    base = STATUS_TAG_RE.sub("", notes or "").strip()
    tag = f"[showroom:{status}]"
    combined = f"{tag} {base}".strip() if base else tag
    return combined[:500]


def extract_meta(notes: Optional[str], key: str) -> Optional[str]:
    if not notes:
        return None
    match = re.search(rf"\[{re.escape(key)}:([^\]]+)\]", notes)
    return match.group(1).strip() if match else None


def set_meta(notes: Optional[str], key: str, value: str) -> str:
    pattern = re.compile(rf"\[{re.escape(key)}:[^\]]*\]")
    base = pattern.sub("", notes or "").strip()
    tag = f"[{key}:{value}]"
    combined = f"{tag} {base}".strip() if base else tag
    return combined[:500]


def get_movement_or_404(db: Session, movement_id: int) -> ProductMovement:
    movement = (
        db.query(ProductMovement)
        .options(
            joinedload(ProductMovement.product),
            joinedload(ProductMovement.source_placement),
            joinedload(ProductMovement.destination_placement),
            joinedload(ProductMovement.user),
        )
        .filter(ProductMovement.id == movement_id)
        .first()
    )
    if not movement:
        raise CSMSException("Record not found", status_code=404)
    return movement


def truncate_notes(notes: Optional[str], max_len: int = 500) -> Optional[str]:
    if notes is None:
        return None
    return notes[:max_len]
