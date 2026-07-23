from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_

from app.core.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.product import Product
from app.models.showroom_location import ShowroomLocation
from app.models.showroom_storage_location import ShowroomStorageLocation
from app.models.showroom_sample_stock import ShowroomSampleStock
from app.models.showroom_movement import ShowroomMovement
from app.models.showroom_movement_type import MovementType
from app.modules.hrd_ga.creative.showroom.schemas import SuccessResponse
from app.modules.hrd_ga.creative.showroom.services.base import (
    validate_quantity,
    get_or_create_stock,
    update_stock_with_optimistic_lock,
    log_activity,
    jakarta_now,
)

router = APIRouter()


@router.get("")
def list_showroom_products(
    location_id: int = Query(None),
    storage_location_id: int = Query(None),
    sample_type: str = Query(None),
    search: str = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = (
        db.query(ShowroomSampleStock)
        .options(
            joinedload(ShowroomSampleStock.product)
            .joinedload(Product.category),
            joinedload(ShowroomSampleStock.product)
            .joinedload(Product.motif),
            joinedload(ShowroomSampleStock.product)
            .joinedload(Product.sub_motif),
            joinedload(ShowroomSampleStock.location),
            joinedload(ShowroomSampleStock.storage_location),
        )
        .filter(ShowroomSampleStock.quantity > 0)
    )

    if location_id:
        query = query.filter(ShowroomSampleStock.location_id == location_id)
    if storage_location_id:
        query = query.filter(ShowroomSampleStock.storage_location_id == storage_location_id)
    if sample_type:
        query = query.filter(ShowroomSampleStock.sample_type == sample_type)
    if search:
        term = f"%{search.strip()}%"
        query = query.join(Product).filter(
            or_(Product.display_name.ilike(term), Product.sku.ilike(term))
        )

    total = query.count()
    query = query.order_by(ShowroomSampleStock.updated_at.desc())
    stocks = query.offset((page - 1) * per_page).limit(per_page).all()

    product_ids = set(s.product_id for s in stocks)
    stock_by_key = {}
    for s in stocks:
        stock_by_key[(s.product_id, s.location_id)] = s.id

    movements_map = {}
    if product_ids:
        all_movements = (
            db.query(ShowroomMovement)
            .options(
                joinedload(ShowroomMovement.from_location),
                joinedload(ShowroomMovement.to_location),
            )
            .filter(ShowroomMovement.product_id.in_(product_ids))
            .order_by(ShowroomMovement.created_at.desc())
            .all()
        )
        for m in all_movements:
            fid = m.to_location_id
            if fid:
                sid = stock_by_key.get((m.product_id, fid))
                if sid is not None and sid not in movements_map:
                    movements_map[sid] = m
            fid = m.from_location_id
            if fid:
                sid = stock_by_key.get((m.product_id, fid))
                if sid is not None and sid not in movements_map:
                    movements_map[sid] = m

    items = []
    for s in stocks:
        p = s.product
        mov = movements_map.get(s.id)
        item = {
            "id": s.id,
            "product_id": s.product_id,
            "product_name": p.display_name if p else None,
            "sku": p.sku if p else None,
            "variant": p.variant if p else None,
            "category": {"id": p.category.id, "name": p.category.name} if p and p.category else None,
            "motif": {"id": p.motif.id, "name": p.motif.name} if p and p.motif else None,
            "sub_motif": {"id": p.sub_motif.id, "name": p.sub_motif.name} if p and p.sub_motif else None,
            "location": {"id": s.location.id, "name": s.location.name, "code": s.location.code} if s.location else None,
            "storage_location": {"id": s.storage_location.id, "name": s.storage_location.name, "code": s.storage_location.code} if s.storage_location else None,
            "sample_type": s.sample_type,
            "quantity": s.quantity,
            "created_at": s.created_at.isoformat() if s.created_at else None,
            "updated_at": s.updated_at.isoformat() if s.updated_at else None,
            "movement": {
                "direction": "IN" if mov and mov.to_location_id == s.location_id else "OUT" if mov and mov.from_location_id == s.location_id else None,
                "type": mov.movement_type if mov else None,
                "from_location": {"id": mov.from_location.id, "name": mov.from_location.name, "code": mov.from_location.code} if mov and mov.from_location else None,
                "to_location": {"id": mov.to_location.id, "name": mov.to_location.name, "code": mov.to_location.code} if mov and mov.to_location else None,
                "date": mov.date.isoformat() if mov and mov.date else None,
            } if mov else None,
        }
        items.append(item)

    return SuccessResponse(data={
        "items": items,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": (total + per_page - 1) // per_page if total > 0 else 0,
    })


@router.post("/add")
def add_product_to_showroom(
    product_id: int = Query(...),
    location_id: int = Query(None),
    movement_type: str = Query("SHOWROOM_IN"),
    from_location_id: int = Query(None),
    to_location_id: int = Query(None),
    sample_type: str = Query("Display"),
    quantity: int = Query(1, ge=1),
    storage_location_id: int = Query(None),
    notes: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    validate_quantity(quantity)

    mt = db.query(MovementType).filter(MovementType.code == movement_type, MovementType.is_active.is_(True)).first()
    if not mt:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=f"Tipe pergerakan '{movement_type}' tidak valid")

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")

    if storage_location_id:
        storage = db.query(ShowroomStorageLocation).filter(
            ShowroomStorageLocation.id == storage_location_id,
            ShowroomStorageLocation.is_active.is_(True),
        ).first()
        if not storage:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Storage location tidak ditemukan")
        location_id = location_id or storage.location_id

    if not location_id:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="location_id atau storage_location_id diperlukan")

    location = db.query(ShowroomLocation).filter(ShowroomLocation.id == location_id).first()
    if not location:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Lokasi tidak ditemukan")

    src_loc = None
    if from_location_id:
        src_loc = db.query(ShowroomLocation).filter(ShowroomLocation.id == from_location_id).first()
        if not src_loc:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Lokasi asal tidak ditemukan")

    dst_loc = None
    if to_location_id:
        dst_loc = db.query(ShowroomLocation).filter(ShowroomLocation.id == to_location_id).first()
        if not dst_loc:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Lokasi tujuan tidak ditemukan")

    direction = mt.direction
    if direction == "IN":
        stock = get_or_create_stock(db, product_id, location_id, sample_type, storage_location_id)
        update_stock_with_optimistic_lock(db, stock.id, quantity)

        movement = ShowroomMovement(
            movement_type=movement_type,
            product_id=product_id,
            from_location_id=from_location_id,
            to_location_id=location_id,
            quantity=quantity,
            sample_type=sample_type,
            user_id=current_user.id,
            notes=notes or f"Manual add by {current_user.full_name}",
        )
        db.add(movement)
        db.commit()

        log_activity(
            db, "ADD_PRODUCT", "showroom_sample_stock", stock.id,
            user_id=current_user.id,
            detail=f"{movement_type} {quantity}x {product.display_name} ke {location.name} dari {src_loc.name if src_loc else '-'}",
        )

        return SuccessResponse(
            data={"stock_id": stock.id, "movement_id": movement.id, "quantity": stock.quantity, "movement_type": movement_type, "direction": direction},
            message=f"{movement_type} {quantity}x {product.display_name} berhasil",
        )

    else:
        existing = (
            db.query(ShowroomSampleStock)
            .filter(
                ShowroomSampleStock.product_id == product_id,
                ShowroomSampleStock.location_id == location_id,
                ShowroomSampleStock.sample_type == sample_type,
            )
            .first()
        )
        if not existing or existing.quantity < quantity:
            from fastapi import HTTPException
            raise HTTPException(
                status_code=400,
                detail=f"Stok tidak mencukupi (tersedia {existing.quantity if existing else 0})",
            )

        update_stock_with_optimistic_lock(db, existing.id, -quantity)
        stock_id = existing.id

        movement = ShowroomMovement(
            movement_type=movement_type,
            product_id=product_id,
            from_location_id=location_id,
            to_location_id=to_location_id,
            quantity=quantity,
            sample_type=sample_type,
            user_id=current_user.id,
            notes=notes or f"Manual remove by {current_user.full_name}",
        )
        db.add(movement)
        db.commit()

        log_activity(
            db, "REMOVE_PRODUCT", "showroom_sample_stock", stock_id,
            user_id=current_user.id,
            detail=f"{movement_type} {quantity}x {product.display_name} dari {location.name} ke {dst_loc.name if dst_loc else '-'}",
        )

        return SuccessResponse(
            data={"stock_id": stock_id, "movement_id": movement.id, "quantity": 0, "movement_type": movement_type, "direction": direction},
            message=f"{movement_type} {quantity}x {product.display_name} berhasil",
        )


@router.delete("/{stock_id}")
def remove_product_from_showroom(
    stock_id: int,
    quantity: int = Query(None, ge=1),
    notes: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stock = (
        db.query(ShowroomSampleStock)
        .options(joinedload(ShowroomSampleStock.product))
        .filter(ShowroomSampleStock.id == stock_id)
        .first()
    )
    if not stock:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Stok tidak ditemukan")

    qty_to_remove = quantity if quantity else stock.quantity
    validate_quantity(qty_to_remove, stock.quantity)

    product_name = stock.product.display_name if stock.product else "Unknown"
    location_name = stock.location.name if stock.location else "Unknown"

    update_stock_with_optimistic_lock(db, stock.id, -qty_to_remove)

    movement = ShowroomMovement(
        movement_type="SHOWROOM_OUT",
        product_id=stock.product_id,
        from_location_id=stock.location_id,
        quantity=qty_to_remove,
        sample_type=stock.sample_type,
        user_id=current_user.id,
        notes=notes or f"Manual remove by {current_user.full_name}",
    )
    db.add(movement)
    db.commit()

    log_activity(
        db, "REMOVE_PRODUCT", "showroom_sample_stock", stock.id,
        user_id=current_user.id,
        detail=f"Removed {qty_to_remove}x {product_name} from {location_name}",
    )

    return SuccessResponse(
        message=f"{qty_to_remove}x {product_name} berhasil dihapus",
    )


@router.get("/report")
def get_showroom_report(
    period: str = Query("daily", pattern="^(daily|weekly|monthly)$"),
    start_date: str = Query(None),
    end_date: str = Query(None),
    location_id: int = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from datetime import datetime, timedelta, date

    today = jakarta_now().date()

    if start_date:
        sd = datetime.strptime(start_date, "%Y-%m-%d").date()
    else:
        if period == "daily":
            sd = today
        elif period == "weekly":
            sd = today - timedelta(days=today.weekday())
        else:
            sd = today.replace(day=1)

    if end_date:
        ed = datetime.strptime(end_date, "%Y-%m-%d").date()
    else:
        if period == "daily":
            ed = today
        elif period == "weekly":
            ed = sd + timedelta(days=6)
        else:
            import calendar
            _, last_day = calendar.monthrange(sd.year, sd.month)
            ed = sd.replace(day=last_day)

    ed_end = datetime.combine(ed, datetime.max.time())

    movements_query = db.query(ShowroomMovement).filter(
        ShowroomMovement.date >= sd,
        ShowroomMovement.date <= ed_end,
    )
    if location_id:
        movements_query = movements_query.filter(
            or_(ShowroomMovement.from_location_id == location_id, ShowroomMovement.to_location_id == location_id)
        )

    movements = movements_query.order_by(ShowroomMovement.date.desc()).all()
    movement_list = []
    for m in movements:
        p = db.query(Product).filter(Product.id == m.product_id).first()
        mt_dir = db.query(MovementType.direction).filter(MovementType.code == m.movement_type).scalar()
        direction = mt_dir or "IN"
        movement_list.append({
            "id": m.id,
            "movement_type": m.movement_type,
            "direction": direction,
            "product_name": p.display_name if p else None,
            "product_sku": p.sku if p else None,
            "quantity": m.quantity,
            "sample_type": m.sample_type,
            "from_location": m.from_location.name if m.from_location else None,
            "to_location": m.to_location.name if m.to_location else None,
            "date": m.date.isoformat() if m.date else None,
            "notes": m.notes,
        })

    stock_query = db.query(ShowroomSampleStock).filter(ShowroomSampleStock.quantity > 0)
    if location_id:
        stock_query = stock_query.filter(ShowroomSampleStock.location_id == location_id)

    total_items = stock_query.count()
    total_quantity = sum(s.quantity for s in stock_query.all())

    all_dirs = {r.code: r.direction for r in db.query(MovementType.code, MovementType.direction).all()}
    in_count = sum(1 for m in movements if all_dirs.get(m.movement_type, "IN") == "IN")
    out_count = sum(1 for m in movements if all_dirs.get(m.movement_type, "IN") == "OUT")
    in_qty = sum(m.quantity for m in movements if all_dirs.get(m.movement_type, "IN") == "IN")
    out_qty = sum(m.quantity for m in movements if all_dirs.get(m.movement_type, "IN") == "OUT")

    return SuccessResponse(data={
        "period": {"start": sd.isoformat(), "end": ed.isoformat(), "label": period},
        "summary": {
            "total_items": total_items,
            "total_quantity": total_quantity,
            "in_count": in_count,
            "out_count": out_count,
            "in_qty": in_qty,
            "out_qty": out_qty,
        },
        "movements": movement_list,
    })



