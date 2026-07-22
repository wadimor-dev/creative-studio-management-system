import json
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.showroom_sample_stock import ShowroomSampleStock
from app.models.showroom_movement import ShowroomMovement
from app.models.showroom_storage_location import ShowroomStorageLocation
from app.models.showroom_location import ShowroomLocation
from app.models.product import Product
from app.core.database.helpers import (
    jakarta_now, get_or_404, get_or_create_stock,
    update_stock_with_optimistic_lock, validate_quantity,
)


def _log_activity(db, action, entity_type, entity_id, user_id=None, request_id=None, detail=None):
    from app.models.showroom_activity_log import ShowroomActivityLog
    import uuid

    log = ShowroomActivityLog(
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        actor_id=user_id,
        actor_type="USER",
        request_id=request_id or str(uuid.uuid4()),
        detail=detail,
        created_at=jakarta_now(),
    )
    db.add(log)
    return log


class QRScanService:

    @staticmethod
    def process_storage_scan(
        db: Session,
        qr_data: dict,
        action: str,
        product_id: int = None,
        quantity: int = None,
        sample_type: str = None,
        items: list = None,
        user_id: int = None,
        request_id: str = None,
    ) -> dict:
        entity = qr_data.get("entity", {})
        qr_info = qr_data.get("qr", {})
        entity_type = qr_info.get("entity_type", "storage")
        entity_id = entity.get("id")

        if not entity_id:
            raise HTTPException(status_code=400, detail="Invalid QR: no entity")

        if entity_type == "location":
            loc = get_or_404(db, ShowroomLocation, entity_id, "Location")
            location_id = loc.id
            storage_id = None
        else:
            storage = get_or_404(db, ShowroomStorageLocation, entity_id, "Storage location")
            storage_id = storage.id
            location_id = storage.location_id

        if action == "CHECK_INVENTORY":
            return QRScanService._handle_check_inventory(db, entity_type, storage_id, location_id, storage, loc)

        if action in ("STOCK_IN", "STOCK_OUT"):
            return QRScanService._handle_stock_mutation(
                db, action, entity_type, entity_id, storage_id, location_id,
                product_id, quantity, sample_type, user_id, request_id,
            )

        if action == "STOCK_OPNAME":
            return QRScanService._handle_stock_opname(
                db, storage_id, location_id, items, user_id, sample_type,
            )

        raise HTTPException(status_code=400, detail=f"Unknown action: {action}")

    @staticmethod
    def _handle_check_inventory(db, entity_type, storage_id, location_id, storage, loc):
        from app.models.product import Product
        query = db.query(ShowroomSampleStock)
        if storage_id:
            query = query.filter(ShowroomSampleStock.storage_location_id == storage_id)
        else:
            query = query.filter(ShowroomSampleStock.location_id == location_id)
        stocks = query.all()
        items = []
        for s in stocks:
            product = db.query(Product).filter(Product.id == s.product_id).first()
            items.append({
                "product_id": s.product_id,
                "product_name": product.display_name if product else "Unknown",
                "sku": product.sku if product else None,
                "sample_type": s.sample_type,
                "quantity": s.quantity,
                "category": {"id": product.category.id, "name": product.category.name} if product and product.category else None,
                "motif": {"id": product.motif.id, "name": product.motif.name} if product and product.motif else None,
                "sub_motif": {"id": product.sub_motif.id, "name": product.sub_motif.name} if product and product.sub_motif else None,
                "variant": product.variant if product else None,
            })
        result = {
            "action": "CHECK_INVENTORY",
            "entity_type": entity_type,
            "items": items,
            "total_items": sum(i["quantity"] for i in items),
        }
        if storage_id:
            result["storage"] = {
                "id": storage.id, "name": storage.name, "code": storage.code,
                "storage_type": storage.storage_type,
                "capacity_qty": storage.capacity_qty,
                "used_capacity": storage.used_capacity,
            }
        else:
            result["location"] = {
                "id": loc.id, "name": loc.name, "code": loc.code,
            }
        return result

    @staticmethod
    def _handle_stock_mutation(db, action, entity_type, entity_id, storage_id, location_id,
                                product_id, quantity, sample_type, user_id, request_id):
        if not product_id or not quantity:
            raise HTTPException(status_code=400, detail="product_id and quantity required")

        validate_quantity(quantity)
        get_or_404(db, Product, product_id, "Product")

        delta = quantity if action == "STOCK_IN" else -quantity

        stock = get_or_create_stock(
            db,
            product_id=product_id,
            location_id=location_id,
            sample_type=sample_type,
            storage_location_id=storage_id,
        )

        updated_stock = update_stock_with_optimistic_lock(db, stock.id, delta)

        movement = ShowroomMovement(
            movement_type="SHOWROOM_IN" if action == "STOCK_IN" else "SHOWROOM_OUT",
            product_id=product_id,
            to_location_id=location_id if action == "STOCK_IN" else None,
            from_location_id=location_id if action == "STOCK_OUT" else None,
            quantity=quantity,
            sample_type=sample_type,
            user_id=user_id,
            date=jakarta_now(),
            notes=f"QR scan {action}",
        )
        db.add(movement)
        db.flush()

        if storage_id:
            from app.core.storage.service import StorageService
            StorageService._recalculate_capacity(db, storage_id)

        _log_activity(
            db, action=f"QR_{action}", entity_type=entity_type,
            entity_id=entity_id, user_id=user_id, request_id=request_id,
            detail=json.dumps({
                "product_id": product_id, "quantity": quantity,
                "sample_type": sample_type, "entity_type": entity_type, "entity_id": entity_id,
            }),
        )

        db.commit()

        result = {
            "action": action, "entity_type": entity_type,
            "product_id": product_id, "quantity": quantity,
            "movement_id": movement.id,
            "new_stock": updated_stock.quantity if updated_stock else 0,
        }
        if storage_id:
            result["storage_id"] = storage_id
        result["location_id"] = location_id
        return result

    @staticmethod
    def _handle_stock_opname(db, storage_id, location_id, items, user_id, sample_type):
        if not items:
            raise HTTPException(status_code=400, detail="items required for STOCK_OPNAME")
        adjustments = []
        for item in items:
            pid = item.get("product_id")
            actual_qty = item.get("actual_quantity", 0)
            st = item.get("sample_type")
            if not pid:
                continue
            stock_query = db.query(ShowroomSampleStock).filter(ShowroomSampleStock.product_id == pid)
            if storage_id:
                stock_query = stock_query.filter(ShowroomSampleStock.storage_location_id == storage_id)
            else:
                stock_query = stock_query.filter(ShowroomSampleStock.location_id == location_id)
            stock = stock_query.first()
            current_qty = stock.quantity if stock else 0
            delta = actual_qty - current_qty
            if delta == 0:
                adjustments.append({"product_id": pid, "variance": 0})
                continue
            stock_obj = get_or_create_stock(db, product_id=pid, location_id=location_id, sample_type=st, storage_location_id=storage_id)
            updated_stock = update_stock_with_optimistic_lock(db, stock_obj.id, delta)
            movement = ShowroomMovement(
                movement_type="ADJUSTMENT",
                product_id=pid,
                quantity=abs(delta),
                to_location_id=location_id if delta > 0 else None,
                from_location_id=location_id if delta < 0 else None,
                sample_type=st,
                user_id=user_id,
                date=jakarta_now(),
                notes=f"QR scan STOCK_OPNAME adjustment",
            )
            db.add(movement)
            adjustments.append({"product_id": pid, "variance": delta, "new_quantity": updated_stock.quantity if updated_stock else actual_qty})
        db.commit()
        return {"action": "STOCK_OPNAME", "adjustments": adjustments}

    @staticmethod
    def process_product_scan(
        db: Session,
        qr_data: dict,
        action: str,
        storage_location_id: int = None,
        quantity: int = None,
        user_id: int = None,
        request_id: str = None,
    ) -> dict:
        entity = qr_data.get("entity", {})
        product_id = entity.get("id")

        if not product_id:
            raise HTTPException(status_code=400, detail="Invalid QR: no product")

        if action == "CHECK_STOCK":
            stocks = (
                db.query(ShowroomSampleStock)
                .filter(ShowroomSampleStock.product_id == product_id)
                .all()
            )
            product = db.query(Product).filter(Product.id == product_id).first()
            items = []
            for s in stocks:
                loc = db.query(ShowroomLocation).filter(ShowroomLocation.id == s.location_id).first()
                storage = db.query(ShowroomStorageLocation).filter(ShowroomStorageLocation.id == s.storage_location_id).first() if s.storage_location_id else None
                items.append({
                    "location_id": s.location_id,
                    "location_name": loc.name if loc else "Unknown",
                    "storage_id": s.storage_location_id,
                    "storage_name": storage.name if storage else None,
                    "storage_code": storage.code if storage else None,
                    "sample_type": s.sample_type,
                    "quantity": s.quantity,
                })
            return {
                "action": "CHECK_STOCK",
                "product_id": product_id,
                "product_name": product.display_name if product else None,
                "sku": product.sku if product else None,
                "category": {"id": product.category.id, "name": product.category.name} if product and product.category else None,
                "motif": {"id": product.motif.id, "name": product.motif.name} if product and product.motif else None,
                "sub_motif": {"id": product.sub_motif.id, "name": product.sub_motif.name} if product and product.sub_motif else None,
                "items": items,
                "total_quantity": sum(i["quantity"] for i in items),
            }

        raise HTTPException(status_code=400, detail=f"Unsupported product scan action: {action}")
