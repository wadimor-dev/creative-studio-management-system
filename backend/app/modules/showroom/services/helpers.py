"""Shared helpers for showroom services."""

from __future__ import annotations

import re
from datetime import datetime, timezone, timedelta
from typing import Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.exceptions.base import CSMSException
from app.models.inventory_transaction import InventoryTransaction
from app.models.item import Item
from app.models.location import Location

STATUS_TAG_RE = re.compile(r"\[showroom:(\w+)\]")
ID_PREFIX_RE = re.compile(r"^(?:TRF|IN|OUT|MOV)-(\d+)$", re.IGNORECASE)


def jakarta_now() -> datetime:
    return datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None)


def jakarta_today():
    return jakarta_now().date()


def location_slug(name: str) -> str:
    return name.lower().replace(" ", "-")


def resolve_location(db: Session, location_key: str) -> Location:
    """Resolve location by name, slug, or numeric id."""
    if not location_key:
        raise CSMSException("Location is required", status_code=400)

    location = db.query(Location).filter(Location.name == location_key).first()
    if location:
        return location

    if location_key.isdigit():
        location = db.query(Location).filter(Location.id == int(location_key)).first()
        if location:
            return location

    key = location_key.lower().strip()
    for loc in db.query(Location).all():
        if location_slug(loc.name) == key:
            return loc

    raise CSMSException(f"Location not found: {location_key}", status_code=404)


def resolve_item(db: Session, product_key: str) -> Item:
    """Resolve item by SKU or name (exact, then case-insensitive)."""
    if not product_key:
        raise CSMSException("Product is required", status_code=400)

    item = (
        db.query(Item)
        .filter(or_(Item.sku == product_key, Item.name == product_key))
        .first()
    )
    if item:
        return item

    key = product_key.lower().strip()
    item = (
        db.query(Item)
        .filter(or_(Item.sku.ilike(key), Item.name.ilike(key)))
        .first()
    )
    if item:
        return item

    raise CSMSException(f"Item not found: {product_key}", status_code=404)


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
    return f"{tag} {base}".strip() if base else tag


def extract_meta(notes: Optional[str], key: str) -> Optional[str]:
    """Extract [key:value] meta from notes."""
    if not notes:
        return None
    match = re.search(rf"\[{re.escape(key)}:([^\]]+)\]", notes)
    return match.group(1).strip() if match else None


def set_meta(notes: Optional[str], key: str, value: str) -> str:
    pattern = re.compile(rf"\[{re.escape(key)}:[^\]]*\]")
    base = pattern.sub("", notes or "").strip()
    tag = f"[{key}:{value}]"
    return f"{tag} {base}".strip() if base else tag


def get_transaction_or_404(db: Session, transaction_id: int) -> InventoryTransaction:
    tx = db.query(InventoryTransaction).filter(InventoryTransaction.id == transaction_id).first()
    if not tx:
        raise CSMSException("Record not found", status_code=404)
    return tx
