"""Showroom business logic — finished goods only (Product / Placement / Movement)."""

from __future__ import annotations

import re
from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session, joinedload

from app.exceptions.base import CSMSException
from app.models.product import Product
from app.models.product_movement import (
    ProductMovement,
    ProductMovementReason,
    ProductMovementType,
)
from app.models.product_placement import ProductPlacement
from app.models.product_stock import ProductPlacementStock
from app.modules.showroom.schemas import (
    ShowroomDashboardStats,
    ShowroomMovementSummary,
    ShowroomStockStats,
    ShowroomStockMovement,
    TransferCreate,
    TransferUpdate,
    TransferResponse,
    TransferStats,
    TransferItem,
    StockInCreate,
    StockInUpdate,
    StockInResponse,
    StockInStats,
    StockOutCreate,
    StockOutUpdate,
    StockOutResponse,
    StockOutStats,
    ShowroomLocation,
    ShowroomProductOption,
)
from app.modules.showroom.services.helpers import (
    extract_meta,
    get_movement_or_404,
    get_showroom_status,
    jakarta_now,
    jakarta_today,
    map_stock_out_reason,
    parse_prefixed_id,
    placement_slug,
    resolve_placement,
    resolve_product,
    set_meta,
    set_showroom_status,
    truncate_notes,
)
from app.services.movement_engine import MovementEngine


class ShowroomService:
    # ------------------------------------------------------------------
    # Dashboard
    # ------------------------------------------------------------------

    def get_dashboard_stats(self, db: Session) -> ShowroomDashboardStats:
        today = jakarta_today()
        week_ago = today - timedelta(days=7)

        total_stock = db.query(func.sum(ProductPlacementStock.quantity)).scalar() or 0

        stock_in_today = (
            db.query(func.sum(ProductMovement.quantity))
            .filter(
                and_(
                    ProductMovement.type == ProductMovementType.IN,
                    func.date(ProductMovement.date) == today,
                )
            )
            .scalar()
            or 0
        )

        stock_out_today = (
            db.query(func.sum(ProductMovement.quantity))
            .filter(
                and_(
                    ProductMovement.type == ProductMovementType.OUT,
                    func.date(ProductMovement.date) == today,
                )
            )
            .scalar()
            or 0
        )

        pending_transfers = self._count_transfers_by_status(db, "pending")
        in_transit = self._count_transfers_by_status(db, "in_transit")

        stock_in_count = (
            db.query(ProductMovement)
            .filter(
                and_(
                    ProductMovement.type == ProductMovementType.IN,
                    func.date(ProductMovement.date) == today,
                )
            )
            .count()
        )

        stock_out_count = (
            db.query(ProductMovement)
            .filter(
                and_(
                    ProductMovement.type == ProductMovementType.OUT,
                    func.date(ProductMovement.date) == today,
                )
            )
            .count()
        )

        if pending_transfers == 0 and in_transit == 0:
            pending_transfers = (
                db.query(ProductMovement)
                .filter(
                    and_(
                        ProductMovement.type == ProductMovementType.TRANSFER,
                        ProductMovement.reason == ProductMovementReason.SHOWROOM_TRANSFER,
                        func.date(ProductMovement.date) >= today,
                    )
                )
                .count()
            )
            in_transit = (
                db.query(ProductMovement)
                .filter(
                    and_(
                        ProductMovement.type == ProductMovementType.TRANSFER,
                        ProductMovement.reason == ProductMovementReason.SHOWROOM_TRANSFER,
                        func.date(ProductMovement.date) >= week_ago,
                        func.date(ProductMovement.date) < today,
                    )
                )
                .count()
            )

        return ShowroomDashboardStats(
            totalStock=str(total_stock),
            stockInToday=f"+{stock_in_today}",
            stockOutToday=f"-{stock_out_today}",
            pendingTransfer=str(pending_transfers),
            stockInCount=f"{stock_in_count} transaksi",
            stockOutCount=f"{stock_out_count} transaksi",
            inTransit=f"{in_transit} dalam perjalanan",
        )

    def get_recent_movements(self, db: Session, limit: int = 5) -> List[ShowroomMovementSummary]:
        movements_q = (
            db.query(ProductMovement)
            .options(
                joinedload(ProductMovement.product),
                joinedload(ProductMovement.source_placement),
                joinedload(ProductMovement.destination_placement),
            )
            .order_by(ProductMovement.date.desc())
            .limit(limit)
            .all()
        )

        result = []
        for mv in movements_q:
            location = ""
            if mv.destination_placement:
                location = mv.destination_placement.name
            elif mv.source_placement:
                location = mv.source_placement.name

            result.append(
                ShowroomMovementSummary(
                    id=f"MOV-{mv.id:04d}",
                    product=mv.product.display_name if mv.product else "Unknown",
                    type=mv.type.value,
                    quantity=mv.quantity,
                    location=location,
                    status=get_showroom_status(mv.notes, default="completed"),
                )
            )
        return result

    # ------------------------------------------------------------------
    # Stock
    # ------------------------------------------------------------------

    def get_stock_stats(
        self, db: Session, location: Optional[str] = None
    ) -> ShowroomStockStats:
        today = jakarta_today()
        placement_id = None
        if location and location != "all":
            placement_id = resolve_placement(db, location).id

        if placement_id:
            total_stock = (
                db.query(func.sum(ProductPlacementStock.quantity))
                .filter(ProductPlacementStock.placement_id == placement_id)
                .scalar()
                or 0
            )
        else:
            total_stock = db.query(func.sum(ProductPlacementStock.quantity)).scalar() or 0

        stock_in_filter = [
            ProductMovement.type == ProductMovementType.IN,
            func.date(ProductMovement.date) == today,
        ]
        stock_out_filter = [
            ProductMovement.type == ProductMovementType.OUT,
            func.date(ProductMovement.date) == today,
        ]
        if placement_id:
            stock_in_filter.append(ProductMovement.destination_placement_id == placement_id)
            stock_out_filter.append(ProductMovement.source_placement_id == placement_id)

        stock_in_today = (
            db.query(func.sum(ProductMovement.quantity)).filter(and_(*stock_in_filter)).scalar()
            or 0
        )
        stock_out_today = (
            db.query(func.sum(ProductMovement.quantity)).filter(and_(*stock_out_filter)).scalar()
            or 0
        )

        stock_in_count = db.query(ProductMovement).filter(and_(*stock_in_filter)).count()
        stock_out_count = db.query(ProductMovement).filter(and_(*stock_out_filter)).count()

        return ShowroomStockStats(
            totalStock=str(total_stock),
            stockInToday=f"+{stock_in_today}",
            stockOutToday=f"-{stock_out_today}",
            pendingTransfer=str(self._count_transfers_by_status(db, "pending")),
            stockInCount=f"{stock_in_count} transaksi",
            stockOutCount=f"{stock_out_count} transaksi",
            inTransit=f"{self._count_transfers_by_status(db, 'in_transit')} dalam perjalanan",
        )

    def get_stock_movements(
        self, db: Session, location: Optional[str] = None
    ) -> List[ShowroomStockMovement]:
        query = db.query(ProductMovement).options(
            joinedload(ProductMovement.product),
            joinedload(ProductMovement.source_placement),
            joinedload(ProductMovement.destination_placement),
        )

        if location and location != "all":
            placement_id = resolve_placement(db, location).id
            query = query.filter(
                or_(
                    ProductMovement.source_placement_id == placement_id,
                    ProductMovement.destination_placement_id == placement_id,
                )
            )

        rows = query.order_by(ProductMovement.date.desc()).limit(50).all()

        movements = []
        for mv in rows:
            location_name = ""
            if mv.destination_placement:
                location_name = mv.destination_placement.name
            elif mv.source_placement:
                location_name = mv.source_placement.name

            movements.append(
                ShowroomStockMovement(
                    id=f"MOV-{mv.id:04d}",
                    product={
                        "sku": mv.product.sku if mv.product else "",
                        "name": mv.product.display_name if mv.product else "Unknown",
                    },
                    type=mv.type.value,
                    quantity=mv.quantity,
                    location=location_name,
                    date=mv.date.isoformat(),
                    status=get_showroom_status(mv.notes, default="completed"),
                    reference=mv.reference,
                )
            )
        return movements

    # ------------------------------------------------------------------
    # Transfers
    # ------------------------------------------------------------------

    def get_transfer_stats(self, db: Session) -> TransferStats:
        today = jakarta_today()
        month_start = today.replace(day=1)

        pending = self._count_transfers_by_status(db, "pending")
        in_transit = self._count_transfers_by_status(db, "in_transit")

        completed_today = (
            db.query(ProductMovement)
            .filter(
                and_(
                    ProductMovement.type == ProductMovementType.TRANSFER,
                    ProductMovement.reason == ProductMovementReason.SHOWROOM_TRANSFER,
                    func.date(ProductMovement.date) == today,
                    ProductMovement.notes.like("%[showroom:completed]%"),
                )
            )
            .count()
        )

        if completed_today == 0:
            completed_today = (
                db.query(ProductMovement)
                .filter(
                    and_(
                        ProductMovement.type == ProductMovementType.TRANSFER,
                        ProductMovement.reason == ProductMovementReason.SHOWROOM_TRANSFER,
                        func.date(ProductMovement.date) == today,
                        or_(
                            ProductMovement.notes.is_(None),
                            ~ProductMovement.notes.like("%[showroom:%"),
                        ),
                    )
                )
                .count()
            )

        total_month = (
            db.query(ProductMovement)
            .filter(
                and_(
                    ProductMovement.type == ProductMovementType.TRANSFER,
                    ProductMovement.reason == ProductMovementReason.SHOWROOM_TRANSFER,
                    func.date(ProductMovement.date) >= month_start,
                )
            )
            .count()
        )

        return TransferStats(
            pendingTransfer=str(pending),
            inTransit=str(in_transit),
            completedToday=str(completed_today),
            totalThisMonth=str(total_month),
        )

    def get_transfers(self, db: Session, status: Optional[str] = None) -> List[TransferResponse]:
        rows = (
            db.query(ProductMovement)
            .filter(
                ProductMovement.type == ProductMovementType.TRANSFER,
                ProductMovement.reason == ProductMovementReason.SHOWROOM_TRANSFER,
            )
            .options(
                joinedload(ProductMovement.product),
                joinedload(ProductMovement.source_placement),
                joinedload(ProductMovement.destination_placement),
            )
            .order_by(ProductMovement.date.desc())
            .limit(100)
            .all()
        )

        transfers = []
        for mv in rows:
            tx_status = get_showroom_status(mv.notes, default="completed")
            if status and tx_status != status:
                continue

            estimated = extract_meta(mv.notes, "eta") or mv.date.date().isoformat()
            transfers.append(
                TransferResponse(
                    id=f"TRF-{mv.id:04d}",
                    fromLocation=mv.source_placement.name if mv.source_placement else "",
                    toLocation=mv.destination_placement.name if mv.destination_placement else "",
                    items=[
                        TransferItem(
                            product=mv.product.display_name if mv.product else "Unknown",
                            quantity=mv.quantity,
                        )
                    ],
                    totalQuantity=mv.quantity,
                    status=tx_status,
                    createdAt=mv.date.isoformat(),
                    estimatedArrival=estimated,
                )
            )
        return transfers

    def create_transfer(
        self, db: Session, user_id: int, transfer_in: TransferCreate
    ) -> TransferResponse:
        if not transfer_in.items:
            raise CSMSException("No items in transfer", status_code=400)

        source = resolve_placement(db, transfer_in.fromLocation)
        dest = resolve_placement(db, transfer_in.toLocation)

        if source.id == dest.id:
            raise CSMSException("Source and destination must be different", status_code=400)

        engine = MovementEngine(db)
        reference = f"TRF-{jakarta_now().strftime('%Y%m%d%H%M%S')}"
        base_notes = set_showroom_status(transfer_in.notes, "pending")
        base_notes = set_meta(base_notes, "eta", transfer_in.estimatedArrival)

        created = []
        try:
            for idx, line in enumerate(transfer_in.items):
                product = resolve_product(db, line.product)
                is_last = idx == len(transfer_in.items) - 1
                movement = engine.execute_movement(
                    product_id=product.id,
                    type=ProductMovementType.TRANSFER,
                    reason=ProductMovementReason.SHOWROOM_TRANSFER,
                    quantity=line.quantity,
                    user_id=user_id,
                    source_placement_id=source.id,
                    destination_placement_id=dest.id,
                    reference=reference if idx == 0 else f"{reference}-{idx + 1}",
                    reference_type="showroom_transfer",
                    notes=truncate_notes(base_notes),
                    commit=is_last,
                )
                created.append(movement)
        except Exception:
            db.rollback()
            raise

        primary = created[0]
        return TransferResponse(
            id=f"TRF-{primary.id:04d}",
            fromLocation=source.name,
            toLocation=dest.name,
            items=transfer_in.items,
            totalQuantity=sum(line.quantity for line in transfer_in.items),
            status="pending",
            createdAt=primary.date.isoformat(),
            estimatedArrival=transfer_in.estimatedArrival,
        )

    def update_transfer(
        self, db: Session, transfer_id: str, transfer_in: TransferUpdate
    ) -> TransferResponse:
        mv_id = parse_prefixed_id(transfer_id, expected_prefix="TRF")
        mv = get_movement_or_404(db, mv_id)
        self._assert_showroom_transfer(mv)

        current_status = get_showroom_status(mv.notes, default="completed")
        if current_status == "cancelled":
            raise CSMSException("Cannot update a cancelled transfer", status_code=400)

        notes = mv.notes or ""
        if transfer_in.notes is not None:
            status = get_showroom_status(notes, default="pending")
            notes = set_showroom_status(transfer_in.notes, status)
            eta = extract_meta(mv.notes, "eta")
            if eta:
                notes = set_meta(notes, "eta", eta)

        if transfer_in.estimatedArrival is not None:
            notes = set_meta(notes, "eta", transfer_in.estimatedArrival)

        if transfer_in.status is not None:
            notes = set_showroom_status(notes, transfer_in.status)

        mv.notes = truncate_notes(notes)
        db.add(mv)
        db.commit()
        db.refresh(mv)
        return self._to_transfer_response(mv)

    def cancel_transfer(self, db: Session, user_id: int, transfer_id: str) -> TransferResponse:
        mv_id = parse_prefixed_id(transfer_id, expected_prefix="TRF")
        mv = get_movement_or_404(db, mv_id)
        self._assert_showroom_transfer(mv)

        status = get_showroom_status(mv.notes, default="completed")
        if status == "cancelled":
            raise CSMSException("Transfer already cancelled", status_code=400)
        if status == "completed":
            raise CSMSException("Cannot cancel a completed transfer", status_code=400)

        engine = MovementEngine(db)
        engine.execute_movement(
            product_id=mv.product_id,
            type=ProductMovementType.TRANSFER,
            reason=ProductMovementReason.SHOWROOM_TRANSFER,
            quantity=mv.quantity,
            user_id=user_id,
            source_placement_id=mv.destination_placement_id,
            destination_placement_id=mv.source_placement_id,
            reference=f"CANCEL-{mv.reference or mv.id}",
            reference_type="showroom_transfer_cancel",
            notes=set_showroom_status(f"Reversal of TRF-{mv.id:04d}", "completed"),
            commit=False,
        )

        mv.notes = set_showroom_status(mv.notes, "cancelled")
        db.add(mv)
        db.commit()
        db.refresh(mv)
        return self._to_transfer_response(mv)

    def confirm_transfer(self, db: Session, transfer_id: str) -> TransferResponse:
        mv_id = parse_prefixed_id(transfer_id, expected_prefix="TRF")
        mv = get_movement_or_404(db, mv_id)
        self._assert_showroom_transfer(mv)

        status = get_showroom_status(mv.notes, default="completed")
        if status == "cancelled":
            raise CSMSException("Cannot confirm a cancelled transfer", status_code=400)

        mv.notes = set_showroom_status(mv.notes, "completed")
        db.add(mv)
        db.commit()
        db.refresh(mv)
        return self._to_transfer_response(mv)

    # ------------------------------------------------------------------
    # Stock In
    # ------------------------------------------------------------------

    def get_stock_in_stats(self, db: Session) -> StockInStats:
        today = jakarta_today()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)

        today_in = (
            db.query(func.sum(ProductMovement.quantity))
            .filter(
                and_(
                    ProductMovement.type == ProductMovementType.IN,
                    func.date(ProductMovement.date) == today,
                )
            )
            .scalar()
            or 0
        )
        week_in = (
            db.query(func.sum(ProductMovement.quantity))
            .filter(
                and_(
                    ProductMovement.type == ProductMovementType.IN,
                    func.date(ProductMovement.date) >= week_ago,
                )
            )
            .scalar()
            or 0
        )
        month_in = (
            db.query(func.sum(ProductMovement.quantity))
            .filter(
                and_(
                    ProductMovement.type == ProductMovementType.IN,
                    func.date(ProductMovement.date) >= month_ago,
                )
            )
            .scalar()
            or 0
        )
        total_suppliers = (
            db.query(ProductMovement.notes)
            .filter(
                and_(
                    ProductMovement.type == ProductMovementType.IN,
                    ProductMovement.notes.like("%[supplier:%"),
                )
            )
            .distinct()
            .count()
        )

        return StockInStats(
            todayIn=str(today_in),
            thisWeek=str(week_in),
            thisMonth=str(month_in),
            totalSuppliers=str(total_suppliers),
        )

    def get_stock_in(self, db: Session) -> List[StockInResponse]:
        rows = (
            db.query(ProductMovement)
            .filter(ProductMovement.type == ProductMovementType.IN)
            .options(
                joinedload(ProductMovement.product),
                joinedload(ProductMovement.destination_placement),
                joinedload(ProductMovement.user),
            )
            .order_by(ProductMovement.date.desc())
            .limit(50)
            .all()
        )

        result = []
        for mv in rows:
            supplier = extract_meta(mv.notes, "supplier") or (
                mv.user.username if mv.user else "Unknown"
            )
            result.append(
                StockInResponse(
                    id=f"IN-{mv.id:04d}",
                    product={
                        "sku": mv.product.sku if mv.product else "",
                        "name": mv.product.display_name if mv.product else "Unknown",
                    },
                    quantity=mv.quantity,
                    supplier=supplier,
                    location=mv.destination_placement.name if mv.destination_placement else "",
                    date=mv.date.isoformat(),
                    status=get_showroom_status(mv.notes, default="completed"),
                    reference=mv.reference,
                    notes=self._strip_meta_notes(mv.notes),
                )
            )
        return result

    def create_stock_in(
        self, db: Session, user_id: int, stock_in: StockInCreate
    ) -> StockInResponse:
        product = resolve_product(db, stock_in.product)
        placement = resolve_placement(db, stock_in.location)

        notes = set_showroom_status(stock_in.notes, "completed")
        notes = set_meta(notes, "supplier", stock_in.supplier)

        engine = MovementEngine(db)
        movement = engine.execute_movement(
            product_id=product.id,
            type=ProductMovementType.IN,
            reason=ProductMovementReason.RECEIVE_FROM_FACTORY,
            quantity=stock_in.quantity,
            user_id=user_id,
            destination_placement_id=placement.id,
            reference=stock_in.reference,
            reference_type="showroom_stock_in",
            notes=truncate_notes(notes),
        )

        parsed_date = self._parse_date(stock_in.date)
        if parsed_date:
            movement.date = parsed_date
            db.add(movement)
            db.commit()
            db.refresh(movement)

        return StockInResponse(
            id=f"IN-{movement.id:04d}",
            product={"sku": product.sku, "name": product.display_name},
            quantity=movement.quantity,
            supplier=stock_in.supplier,
            location=placement.name,
            date=movement.date.isoformat(),
            status="completed",
            reference=movement.reference,
            notes=stock_in.notes,
        )

    def update_stock_in(
        self, db: Session, stock_in_id: str, stock_in: StockInUpdate
    ) -> StockInResponse:
        mv_id = parse_prefixed_id(stock_in_id, expected_prefix="IN")
        mv = get_movement_or_404(db, mv_id)

        if mv.type != ProductMovementType.IN:
            raise CSMSException("Not a stock-in record", status_code=400)

        if stock_in.reference is not None:
            mv.reference = stock_in.reference

        notes = mv.notes or ""
        if stock_in.notes is not None:
            supplier = extract_meta(notes, "supplier")
            status = get_showroom_status(notes, default="completed")
            notes = set_showroom_status(stock_in.notes, status)
            if supplier:
                notes = set_meta(notes, "supplier", supplier)

        if stock_in.status is not None:
            notes = set_showroom_status(notes, stock_in.status)

        mv.notes = truncate_notes(notes)
        db.add(mv)
        db.commit()
        db.refresh(mv)
        return self._to_stock_in_response(mv)

    # ------------------------------------------------------------------
    # Stock Out
    # ------------------------------------------------------------------

    def get_stock_out_stats(self, db: Session) -> StockOutStats:
        today = jakarta_today()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)

        today_out = (
            db.query(func.sum(ProductMovement.quantity))
            .filter(
                and_(
                    ProductMovement.type == ProductMovementType.OUT,
                    func.date(ProductMovement.date) == today,
                )
            )
            .scalar()
            or 0
        )
        week_out = (
            db.query(func.sum(ProductMovement.quantity))
            .filter(
                and_(
                    ProductMovement.type == ProductMovementType.OUT,
                    func.date(ProductMovement.date) >= week_ago,
                )
            )
            .scalar()
            or 0
        )
        month_out = (
            db.query(func.sum(ProductMovement.quantity))
            .filter(
                and_(
                    ProductMovement.type == ProductMovementType.OUT,
                    func.date(ProductMovement.date) >= month_ago,
                )
            )
            .scalar()
            or 0
        )
        total_customers = (
            db.query(ProductMovement.notes)
            .filter(
                and_(
                    ProductMovement.type == ProductMovementType.OUT,
                    ProductMovement.notes.like("%[customer:%"),
                )
            )
            .distinct()
            .count()
        )

        return StockOutStats(
            todayOut=str(today_out),
            thisWeek=str(week_out),
            thisMonth=str(month_out),
            totalCustomers=str(total_customers),
        )

    def get_stock_out(self, db: Session) -> List[StockOutResponse]:
        rows = (
            db.query(ProductMovement)
            .filter(ProductMovement.type == ProductMovementType.OUT)
            .options(
                joinedload(ProductMovement.product),
                joinedload(ProductMovement.source_placement),
                joinedload(ProductMovement.user),
            )
            .order_by(ProductMovement.date.desc())
            .limit(50)
            .all()
        )

        result = []
        for mv in rows:
            customer = extract_meta(mv.notes, "customer") or (
                mv.user.username if mv.user else "Unknown"
            )
            reason = extract_meta(mv.notes, "reason") or mv.reason.value
            result.append(
                StockOutResponse(
                    id=f"OUT-{mv.id:04d}",
                    product={
                        "sku": mv.product.sku if mv.product else "",
                        "name": mv.product.display_name if mv.product else "Unknown",
                    },
                    quantity=mv.quantity,
                    customer=customer,
                    location=mv.source_placement.name if mv.source_placement else "",
                    date=mv.date.isoformat(),
                    status=get_showroom_status(mv.notes, default="completed"),
                    reference=mv.reference,
                    reason=reason,
                    notes=self._strip_meta_notes(mv.notes),
                )
            )
        return result

    def create_stock_out(
        self, db: Session, user_id: int, stock_out: StockOutCreate
    ) -> StockOutResponse:
        product = resolve_product(db, stock_out.product)
        placement = resolve_placement(db, stock_out.location)
        reason = map_stock_out_reason(stock_out.reason)

        notes = set_showroom_status(stock_out.notes, "completed")
        notes = set_meta(notes, "customer", stock_out.customer)
        notes = set_meta(notes, "reason", stock_out.reason)

        engine = MovementEngine(db)
        movement = engine.execute_movement(
            product_id=product.id,
            type=ProductMovementType.OUT,
            reason=reason,
            quantity=stock_out.quantity,
            user_id=user_id,
            source_placement_id=placement.id,
            reference=stock_out.reference,
            reference_type="showroom_stock_out",
            notes=truncate_notes(notes),
        )

        parsed_date = self._parse_date(stock_out.date)
        if parsed_date:
            movement.date = parsed_date
            db.add(movement)
            db.commit()
            db.refresh(movement)

        return StockOutResponse(
            id=f"OUT-{movement.id:04d}",
            product={"sku": product.sku, "name": product.display_name},
            quantity=movement.quantity,
            customer=stock_out.customer,
            location=placement.name,
            date=movement.date.isoformat(),
            status="completed",
            reference=movement.reference,
            reason=stock_out.reason,
            notes=stock_out.notes,
        )

    def update_stock_out(
        self, db: Session, stock_out_id: str, stock_out: StockOutUpdate
    ) -> StockOutResponse:
        mv_id = parse_prefixed_id(stock_out_id, expected_prefix="OUT")
        mv = get_movement_or_404(db, mv_id)

        if mv.type != ProductMovementType.OUT:
            raise CSMSException("Not a stock-out record", status_code=400)

        if stock_out.reference is not None:
            mv.reference = stock_out.reference

        notes = mv.notes or ""
        customer = extract_meta(notes, "customer")
        reason_meta = extract_meta(notes, "reason")
        status = get_showroom_status(notes, default="completed")

        if stock_out.notes is not None:
            notes = set_showroom_status(stock_out.notes, status)
            if customer:
                notes = set_meta(notes, "customer", customer)
            if reason_meta:
                notes = set_meta(notes, "reason", reason_meta)

        if stock_out.reason is not None:
            notes = set_meta(notes, "reason", stock_out.reason)
            mv.reason = map_stock_out_reason(stock_out.reason)

        if stock_out.status is not None:
            notes = set_showroom_status(notes, stock_out.status)

        mv.notes = truncate_notes(notes)
        db.add(mv)
        db.commit()
        db.refresh(mv)
        return self._to_stock_out_response(mv)

    # ------------------------------------------------------------------
    # Locations (= product placements)
    # ------------------------------------------------------------------

    def get_locations(self, db: Session) -> List[ShowroomLocation]:
        placements = (
            db.query(ProductPlacement)
            .options(joinedload(ProductPlacement.placement_type))
            .filter(ProductPlacement.is_active.is_(True))
            .order_by(ProductPlacement.name.asc())
            .all()
        )
        return [
            ShowroomLocation(id=placement_slug(p), name=p.name)
            for p in placements
        ]

    # ------------------------------------------------------------------
    # Products + Scanner resolve
    # ------------------------------------------------------------------

    def get_products(
        self, db: Session, search: Optional[str] = None, limit: int = 200
    ) -> List[ShowroomProductOption]:
        query = db.query(Product).order_by(Product.display_name.asc())
        if search:
            term = f"%{search.strip()}%"
            query = query.filter(
                or_(Product.sku.ilike(term), Product.display_name.ilike(term))
            )
        products = query.limit(limit).all()
        return [
            ShowroomProductOption(
                id=p.id,
                sku=p.sku,
                name=p.display_name,
            )
            for p in products
        ]

    def resolve_scan(self, db: Session, code: str) -> dict:
        """Resolve scanned barcode/code to placement or product (showroom-scoped API)."""
        if not code or not code.strip():
            raise CSMSException("Scan code is required", status_code=400)

        raw = code.strip()

        # 1) Placement by exact code
        placement = (
            db.query(ProductPlacement)
            .filter(ProductPlacement.code == raw, ProductPlacement.is_active.is_(True))
            .first()
        )

        # 2) Placement by slug / name via helper
        if not placement:
            try:
                placement = resolve_placement(db, raw)
                if not placement.is_active:
                    placement = None
            except CSMSException:
                placement = None

        if placement:
            stocks = (
                db.query(ProductPlacementStock)
                .options(joinedload(ProductPlacementStock.product))
                .filter(
                    ProductPlacementStock.placement_id == placement.id,
                    ProductPlacementStock.quantity > 0,
                )
                .all()
            )
            return {
                "type": "placement",
                "id": placement.id,
                "code": placement.code,
                "slug": placement_slug(placement),
                "name": placement.name,
                "level": placement.level,
                "stocks": [
                    {
                        "product_id": s.product_id,
                        "product_name": s.product.display_name if s.product else "",
                        "sku": s.product.sku if s.product else "",
                        "quantity": s.quantity,
                        "reserved_quantity": s.reserved_quantity or 0,
                    }
                    for s in stocks
                ],
            }

        # 3) Product by SKU / display name
        try:
            product = resolve_product(db, raw)
        except CSMSException:
            raise CSMSException(
                f"Code '{raw}' not recognized as a valid placement or product.",
                status_code=404,
            )

        return {
            "type": "product",
            "id": product.id,
            "sku": product.sku,
            "display_name": product.display_name,
            "name": product.display_name,
        }

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _count_transfers_by_status(self, db: Session, status: str) -> int:
        return (
            db.query(ProductMovement)
            .filter(
                and_(
                    ProductMovement.type == ProductMovementType.TRANSFER,
                    ProductMovement.reason == ProductMovementReason.SHOWROOM_TRANSFER,
                    ProductMovement.notes.like(f"%[showroom:{status}]%"),
                )
            )
            .count()
        )

    def _assert_showroom_transfer(self, mv: ProductMovement) -> None:
        if mv.type != ProductMovementType.TRANSFER:
            raise CSMSException("Not a transfer record", status_code=400)
        if mv.reason != ProductMovementReason.SHOWROOM_TRANSFER:
            raise CSMSException("Not a showroom transfer record", status_code=400)

    def _parse_date(self, value: Optional[str]):
        if not value:
            return None
        try:
            parsed = datetime.fromisoformat(value)
            if parsed.tzinfo:
                return parsed.replace(tzinfo=None)
            return parsed
        except ValueError:
            raise CSMSException(f"Invalid date: {value}", status_code=400)

    def _strip_meta_notes(self, notes: Optional[str]) -> Optional[str]:
        if not notes:
            return None
        cleaned = re.sub(r"\[[^\]]+\]", "", notes).strip()
        return cleaned or None

    def _to_transfer_response(self, mv: ProductMovement) -> TransferResponse:
        return TransferResponse(
            id=f"TRF-{mv.id:04d}",
            fromLocation=mv.source_placement.name if mv.source_placement else "",
            toLocation=mv.destination_placement.name if mv.destination_placement else "",
            items=[
                TransferItem(
                    product=mv.product.display_name if mv.product else "Unknown",
                    quantity=mv.quantity,
                )
            ],
            totalQuantity=mv.quantity,
            status=get_showroom_status(mv.notes, default="completed"),
            createdAt=mv.date.isoformat(),
            estimatedArrival=extract_meta(mv.notes, "eta") or mv.date.date().isoformat(),
        )

    def _to_stock_in_response(self, mv: ProductMovement) -> StockInResponse:
        return StockInResponse(
            id=f"IN-{mv.id:04d}",
            product={
                "sku": mv.product.sku if mv.product else "",
                "name": mv.product.display_name if mv.product else "Unknown",
            },
            quantity=mv.quantity,
            supplier=extract_meta(mv.notes, "supplier")
            or (mv.user.username if mv.user else "Unknown"),
            location=mv.destination_placement.name if mv.destination_placement else "",
            date=mv.date.isoformat(),
            status=get_showroom_status(mv.notes, default="completed"),
            reference=mv.reference,
            notes=self._strip_meta_notes(mv.notes),
        )

    def _to_stock_out_response(self, mv: ProductMovement) -> StockOutResponse:
        return StockOutResponse(
            id=f"OUT-{mv.id:04d}",
            product={
                "sku": mv.product.sku if mv.product else "",
                "name": mv.product.display_name if mv.product else "Unknown",
            },
            quantity=mv.quantity,
            customer=extract_meta(mv.notes, "customer")
            or (mv.user.username if mv.user else "Unknown"),
            location=mv.source_placement.name if mv.source_placement else "",
            date=mv.date.isoformat(),
            status=get_showroom_status(mv.notes, default="completed"),
            reference=mv.reference,
            reason=extract_meta(mv.notes, "reason") or mv.reason.value,
            notes=self._strip_meta_notes(mv.notes),
        )


showroom_service = ShowroomService()
