from datetime import datetime, timezone, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException


def jakarta_now():
    return datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None)


def jakarta_today():
    return jakarta_now().date()


def get_or_404(db: Session, model, record_id: int, label: str = "Record"):
    record = db.query(model).filter(model.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail=f"{label} with id {record_id} not found")
    return record


def validate_quantity(qty: int, max_qty: int = None):
    if qty <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")
    if max_qty and qty > max_qty:
        raise HTTPException(status_code=400, detail=f"Quantity {qty} exceeds available {max_qty}")


def acquire_stock_lock(db: Session, stock_id: int):
    from sqlalchemy import text
    from app.models.showroom_sample_stock import ShowroomSampleStock

    stock = (
        db.query(ShowroomSampleStock)
        .with_for_update(nowait=False)
        .filter(ShowroomSampleStock.id == stock_id)
        .first()
    )
    return stock


def get_or_create_stock(
    db: Session,
    product_id: int,
    location_id: int,
    sample_type: str = None,
    storage_location_id: int = None,
):
    from app.models.showroom_sample_stock import ShowroomSampleStock

    stock = (
        db.query(ShowroomSampleStock)
        .filter(
            ShowroomSampleStock.product_id == product_id,
            ShowroomSampleStock.location_id == location_id,
            ShowroomSampleStock.sample_type == sample_type,
        )
        .first()
    )
    if not stock:
        stock = ShowroomSampleStock(
            product_id=product_id,
            location_id=location_id,
            sample_type=sample_type,
            storage_location_id=storage_location_id,
            quantity=0,
            version=1,
        )
        db.add(stock)
        db.flush()
    return stock


def update_stock_with_optimistic_lock(
    db: Session,
    stock_id: int,
    quantity_delta: int,
):
    from app.models.showroom_sample_stock import ShowroomSampleStock

    stock = acquire_stock_lock(db, stock_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock record not found")

    expected_version = stock.version
    new_qty = stock.quantity + quantity_delta

    if new_qty < 0:
        raise HTTPException(
            status_code=409,
            detail=f"Insufficient stock (have {stock.quantity}, need {abs(quantity_delta)})",
        )

    updated = (
        db.query(ShowroomSampleStock)
        .filter(
            ShowroomSampleStock.id == stock_id,
            ShowroomSampleStock.version == expected_version,
        )
        .update(
            {
                "quantity": new_qty,
                "version": expected_version + 1,
            }
        )
    )

    if updated == 0:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Optimistic lock conflict: stock was modified by another transaction. Please retry.",
        )

    if new_qty == 0:
        db.query(ShowroomSampleStock).filter(ShowroomSampleStock.id == stock_id).delete()
        db.flush()
        return None

    db.flush()
    stock = db.query(ShowroomSampleStock).filter(ShowroomSampleStock.id == stock_id).first()
    return stock
