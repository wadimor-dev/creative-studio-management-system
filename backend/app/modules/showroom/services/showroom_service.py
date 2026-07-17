"""Showroom business logic — reuses Item inventory tables only."""

from __future__ import annotations

import re
from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session, joinedload

from app.exceptions.base import CSMSException
from app.models.inventory_transaction import InventoryTransaction, InventoryMovementType
from app.models.item_stock import ItemStock
from app.models.location import Location
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
)
from app.modules.showroom.services.helpers import (
    extract_meta,
    get_showroom_status,
    get_transaction_or_404,
    jakarta_now,
    jakarta_today,
    location_slug,
    parse_prefixed_id,
    resolve_item,
    resolve_location,
    set_meta,
    set_showroom_status,
)
from app.schemas.inventory import TransactionCreate
from app.services.inventory_service import inventory_service


class ShowroomService:
    # ------------------------------------------------------------------
    # Dashboard
    # ------------------------------------------------------------------

    def get_dashboard_stats(self, db: Session) -> ShowroomDashboardStats:
        today = jakarta_today()
        week_ago = today - timedelta(days=7)

        total_stock = db.query(func.sum(ItemStock.quantity)).scalar() or 0

        stock_in_today = (
            db.query(func.sum(InventoryTransaction.quantity))
            .filter(
                and_(
                    InventoryTransaction.type == InventoryMovementType.IN,
                    func.date(InventoryTransaction.date) == today,
                )
            )
            .scalar()
            or 0
        )

        stock_out_today = (
            db.query(func.sum(InventoryTransaction.quantity))
            .filter(
                and_(
                    InventoryTransaction.type == InventoryMovementType.OUT,
                    func.date(InventoryTransaction.date) == today,
                )
            )
            .scalar()
            or 0
        )

        pending_transfers = self._count_transfers_by_status(db, "pending")
        in_transit = self._count_transfers_by_status(db, "in_transit")

        stock_in_count = (
            db.query(InventoryTransaction)
            .filter(
                and_(
                    InventoryTransaction.type == InventoryMovementType.IN,
                    func.date(InventoryTransaction.date) == today,
                )
            )
            .count()
        )

        stock_out_count = (
            db.query(InventoryTransaction)
            .filter(
                and_(
                    InventoryTransaction.type == InventoryMovementType.OUT,
                    func.date(InventoryTransaction.date) == today,
                )
            )
            .count()
        )

        # Fallback heuristic for older transfers without status tags
        if pending_transfers == 0 and in_transit == 0:
            pending_transfers = (
                db.query(InventoryTransaction)
                .filter(
                    and_(
                        InventoryTransaction.type == InventoryMovementType.TRANSFER,
                        func.date(InventoryTransaction.date) >= today,
                    )
                )
                .count()
            )
            in_transit = (
                db.query(InventoryTransaction)
                .filter(
                    and_(
                        InventoryTransaction.type == InventoryMovementType.TRANSFER,
                        func.date(InventoryTransaction.date) >= week_ago,
                        func.date(InventoryTransaction.date) < today,
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
        transactions = (
            db.query(InventoryTransaction)
            .options(
                joinedload(InventoryTransaction.item),
                joinedload(InventoryTransaction.source_location),
                joinedload(InventoryTransaction.destination_location),
            )
            .order_by(InventoryTransaction.date.desc())
            .limit(limit)
            .all()
        )

        movements = []
        for tx in transactions:
            location = ""
            if tx.destination_location:
                location = tx.destination_location.name
            elif tx.source_location:
                location = tx.source_location.name

            movements.append(
                ShowroomMovementSummary(
                    id=f"MOV-{tx.id:04d}",
                    product=tx.item.name if tx.item else "Unknown",
                    type=tx.type.value,
                    quantity=tx.quantity,
                    location=location,
                    status=get_showroom_status(tx.notes, default="completed"),
                )
            )

        return movements

    # ------------------------------------------------------------------
    # Stock
    # ------------------------------------------------------------------

    def get_stock_stats(
        self, db: Session, location: Optional[str] = None
    ) -> ShowroomStockStats:
        today = jakarta_today()
        location_id = None
        if location and location != "all":
            location_id = resolve_location(db, location).id

        if location_id:
            total_stock = (
                db.query(func.sum(ItemStock.quantity))
                .filter(ItemStock.location_id == location_id)
                .scalar()
                or 0
            )
        else:
            total_stock = db.query(func.sum(ItemStock.quantity)).scalar() or 0

        stock_in_filter = [
            InventoryTransaction.type == InventoryMovementType.IN,
            func.date(InventoryTransaction.date) == today,
        ]
        stock_out_filter = [
            InventoryTransaction.type == InventoryMovementType.OUT,
            func.date(InventoryTransaction.date) == today,
        ]
        if location_id:
            stock_in_filter.append(InventoryTransaction.destination_location_id == location_id)
            stock_out_filter.append(InventoryTransaction.source_location_id == location_id)

        stock_in_today = (
            db.query(func.sum(InventoryTransaction.quantity)).filter(and_(*stock_in_filter)).scalar()
            or 0
        )
        stock_out_today = (
            db.query(func.sum(InventoryTransaction.quantity)).filter(and_(*stock_out_filter)).scalar()
            or 0
        )

        stock_in_count = db.query(InventoryTransaction).filter(and_(*stock_in_filter)).count()
        stock_out_count = db.query(InventoryTransaction).filter(and_(*stock_out_filter)).count()

        pending_transfers = self._count_transfers_by_status(db, "pending")
        in_transit = self._count_transfers_by_status(db, "in_transit")

        return ShowroomStockStats(
            totalStock=str(total_stock),
            stockInToday=f"+{stock_in_today}",
            stockOutToday=f"-{stock_out_today}",
            pendingTransfer=str(pending_transfers),
            stockInCount=f"{stock_in_count} transaksi",
            stockOutCount=f"{stock_out_count} transaksi",
            inTransit=f"{in_transit} dalam perjalanan",
        )

    def get_stock_movements(
        self, db: Session, location: Optional[str] = None
    ) -> List[ShowroomStockMovement]:
        query = db.query(InventoryTransaction).options(
            joinedload(InventoryTransaction.item),
            joinedload(InventoryTransaction.source_location),
            joinedload(InventoryTransaction.destination_location),
        )

        if location and location != "all":
            location_id = resolve_location(db, location).id
            query = query.filter(
                or_(
                    InventoryTransaction.source_location_id == location_id,
                    InventoryTransaction.destination_location_id == location_id,
                )
            )

        transactions = query.order_by(InventoryTransaction.date.desc()).limit(50).all()

        movements = []
        for tx in transactions:
            location_name = ""
            if tx.destination_location:
                location_name = tx.destination_location.name
            elif tx.source_location:
                location_name = tx.source_location.name

            movements.append(
                ShowroomStockMovement(
                    id=f"MOV-{tx.id:04d}",
                    product={
                        "sku": tx.item.sku if tx.item else "",
                        "name": tx.item.name if tx.item else "Unknown",
                    },
                    type=tx.type.value,
                    quantity=tx.quantity,
                    location=location_name,
                    date=tx.date.isoformat(),
                    status=get_showroom_status(tx.notes, default="completed"),
                    reference=tx.reference,
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
            db.query(InventoryTransaction)
            .filter(
                and_(
                    InventoryTransaction.type == InventoryMovementType.TRANSFER,
                    func.date(InventoryTransaction.date) == today,
                    InventoryTransaction.notes.like("%[showroom:completed]%"),
                )
            )
            .count()
        )

        # Include transfers without tag that happened today as completed
        if completed_today == 0:
            completed_today = (
                db.query(InventoryTransaction)
                .filter(
                    and_(
                        InventoryTransaction.type == InventoryMovementType.TRANSFER,
                        func.date(InventoryTransaction.date) == today,
                        or_(
                            InventoryTransaction.notes.is_(None),
                            ~InventoryTransaction.notes.like("%[showroom:%"),
                        ),
                    )
                )
                .count()
            )

        total_month = (
            db.query(InventoryTransaction)
            .filter(
                and_(
                    InventoryTransaction.type == InventoryMovementType.TRANSFER,
                    func.date(InventoryTransaction.date) >= month_start,
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
        query = (
            db.query(InventoryTransaction)
            .filter(InventoryTransaction.type == InventoryMovementType.TRANSFER)
            .options(
                joinedload(InventoryTransaction.item),
                joinedload(InventoryTransaction.source_location),
                joinedload(InventoryTransaction.destination_location),
            )
        )

        transactions = query.order_by(InventoryTransaction.date.desc()).limit(100).all()

        transfers = []
        for tx in transactions:
            tx_status = get_showroom_status(tx.notes, default="completed")
            if status and tx_status != status:
                continue

            estimated = extract_meta(tx.notes, "eta") or tx.date.date().isoformat()

            transfers.append(
                TransferResponse(
                    id=f"TRF-{tx.id:04d}",
                    fromLocation=tx.source_location.name if tx.source_location else "",
                    toLocation=tx.destination_location.name if tx.destination_location else "",
                    items=[
                        TransferItem(
                            product=tx.item.name if tx.item else "Unknown",
                            quantity=tx.quantity,
                        )
                    ],
                    totalQuantity=tx.quantity,
                    status=tx_status,
                    createdAt=tx.date.isoformat(),
                    estimatedArrival=estimated,
                )
            )

        return transfers

    def create_transfer(
        self, db: Session, user_id: int, transfer_in: TransferCreate
    ) -> TransferResponse:
        if not transfer_in.items:
            raise CSMSException("No items in transfer", status_code=400)

        source_loc = resolve_location(db, transfer_in.fromLocation)
        dest_loc = resolve_location(db, transfer_in.toLocation)

        if source_loc.id == dest_loc.id:
            raise CSMSException("Source and destination must be different", status_code=400)

        created_txs = []
        reference = f"TRF-{jakarta_now().strftime('%Y%m%d%H%M%S')}"
        base_notes = set_showroom_status(transfer_in.notes, "pending")
        base_notes = set_meta(base_notes, "eta", transfer_in.estimatedArrival)

        for idx, line in enumerate(transfer_in.items):
            item = resolve_item(db, line.product)
            tx_in = TransactionCreate(
                item_id=item.id,
                quantity=line.quantity,
                type=InventoryMovementType.TRANSFER,
                source_location_id=source_loc.id,
                destination_location_id=dest_loc.id,
                reference=reference if idx == 0 else f"{reference}-{idx + 1}",
                notes=base_notes,
            )
            # Commit only on the last item so all succeed or none
            commit = idx == len(transfer_in.items) - 1
            transaction = inventory_service.process_transaction(
                db, user_id, tx_in, commit=commit
            )
            created_txs.append(transaction)

        primary = created_txs[0]
        total_qty = sum(line.quantity for line in transfer_in.items)

        return TransferResponse(
            id=f"TRF-{primary.id:04d}",
            fromLocation=source_loc.name,
            toLocation=dest_loc.name,
            items=transfer_in.items,
            totalQuantity=total_qty,
            status="pending",
            createdAt=primary.date.isoformat(),
            estimatedArrival=transfer_in.estimatedArrival,
        )

    def update_transfer(
        self, db: Session, transfer_id: str, transfer_in: TransferUpdate
    ) -> TransferResponse:
        tx_id = parse_prefixed_id(transfer_id, expected_prefix="TRF")
        tx = get_transaction_or_404(db, tx_id)

        if tx.type != InventoryMovementType.TRANSFER:
            raise CSMSException("Not a transfer record", status_code=400)

        current_status = get_showroom_status(tx.notes, default="completed")
        if current_status == "cancelled":
            raise CSMSException("Cannot update a cancelled transfer", status_code=400)

        notes = tx.notes or ""
        if transfer_in.notes is not None:
            status = get_showroom_status(notes, default="pending")
            notes = set_showroom_status(transfer_in.notes, status)
            eta = extract_meta(tx.notes, "eta")
            if eta:
                notes = set_meta(notes, "eta", eta)

        if transfer_in.estimatedArrival is not None:
            notes = set_meta(notes, "eta", transfer_in.estimatedArrival)

        if transfer_in.status is not None:
            notes = set_showroom_status(notes, transfer_in.status)

        tx.notes = notes
        db.add(tx)
        db.commit()
        db.refresh(tx)

        return self._to_transfer_response(tx)

    def cancel_transfer(self, db: Session, user_id: int, transfer_id: str) -> TransferResponse:
        tx_id = parse_prefixed_id(transfer_id, expected_prefix="TRF")
        tx = get_transaction_or_404(db, tx_id)

        if tx.type != InventoryMovementType.TRANSFER:
            raise CSMSException("Not a transfer record", status_code=400)

        status = get_showroom_status(tx.notes, default="completed")
        if status == "cancelled":
            raise CSMSException("Transfer already cancelled", status_code=400)
        if status == "completed":
            raise CSMSException("Cannot cancel a completed transfer", status_code=400)

        # Reverse stock movement
        reverse = TransactionCreate(
            item_id=tx.item_id,
            quantity=tx.quantity,
            type=InventoryMovementType.TRANSFER,
            source_location_id=tx.destination_location_id,
            destination_location_id=tx.source_location_id,
            reference=f"CANCEL-{tx.reference or tx.id}",
            notes=set_showroom_status(f"Reversal of TRF-{tx.id:04d}", "completed"),
        )
        inventory_service.process_transaction(db, user_id, reverse, commit=False)

        tx.notes = set_showroom_status(tx.notes, "cancelled")
        db.add(tx)
        db.commit()
        db.refresh(tx)

        return self._to_transfer_response(tx)

    def confirm_transfer(self, db: Session, transfer_id: str) -> TransferResponse:
        tx_id = parse_prefixed_id(transfer_id, expected_prefix="TRF")
        tx = get_transaction_or_404(db, tx_id)

        if tx.type != InventoryMovementType.TRANSFER:
            raise CSMSException("Not a transfer record", status_code=400)

        status = get_showroom_status(tx.notes, default="completed")
        if status == "cancelled":
            raise CSMSException("Cannot confirm a cancelled transfer", status_code=400)

        tx.notes = set_showroom_status(tx.notes, "completed")
        db.add(tx)
        db.commit()
        db.refresh(tx)

        return self._to_transfer_response(tx)

    # ------------------------------------------------------------------
    # Stock In
    # ------------------------------------------------------------------

    def get_stock_in_stats(self, db: Session) -> StockInStats:
        today = jakarta_today()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)

        today_in = (
            db.query(func.sum(InventoryTransaction.quantity))
            .filter(
                and_(
                    InventoryTransaction.type == InventoryMovementType.IN,
                    func.date(InventoryTransaction.date) == today,
                )
            )
            .scalar()
            or 0
        )

        week_in = (
            db.query(func.sum(InventoryTransaction.quantity))
            .filter(
                and_(
                    InventoryTransaction.type == InventoryMovementType.IN,
                    func.date(InventoryTransaction.date) >= week_ago,
                )
            )
            .scalar()
            or 0
        )

        month_in = (
            db.query(func.sum(InventoryTransaction.quantity))
            .filter(
                and_(
                    InventoryTransaction.type == InventoryMovementType.IN,
                    func.date(InventoryTransaction.date) >= month_ago,
                )
            )
            .scalar()
            or 0
        )

        total_suppliers = (
            db.query(InventoryTransaction.notes)
            .filter(
                and_(
                    InventoryTransaction.type == InventoryMovementType.IN,
                    InventoryTransaction.notes.like("%[supplier:%"),
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
        transactions = (
            db.query(InventoryTransaction)
            .filter(InventoryTransaction.type == InventoryMovementType.IN)
            .options(
                joinedload(InventoryTransaction.item),
                joinedload(InventoryTransaction.destination_location),
                joinedload(InventoryTransaction.user),
            )
            .order_by(InventoryTransaction.date.desc())
            .limit(50)
            .all()
        )

        result = []
        for tx in transactions:
            supplier = extract_meta(tx.notes, "supplier") or (
                tx.user.username if tx.user else "Unknown"
            )
            result.append(
                StockInResponse(
                    id=f"IN-{tx.id:04d}",
                    product={
                        "sku": tx.item.sku if tx.item else "",
                        "name": tx.item.name if tx.item else "Unknown",
                    },
                    quantity=tx.quantity,
                    supplier=supplier,
                    location=tx.destination_location.name if tx.destination_location else "",
                    date=tx.date.isoformat(),
                    status=get_showroom_status(tx.notes, default="completed"),
                    reference=tx.reference,
                    notes=self._strip_meta_notes(tx.notes),
                )
            )
        return result

    def create_stock_in(
        self, db: Session, user_id: int, stock_in: StockInCreate
    ) -> StockInResponse:
        item = resolve_item(db, stock_in.product)
        location = resolve_location(db, stock_in.location)

        notes = set_showroom_status(stock_in.notes, "completed")
        notes = set_meta(notes, "supplier", stock_in.supplier)

        tx_in = TransactionCreate(
            item_id=item.id,
            quantity=stock_in.quantity,
            type=InventoryMovementType.IN,
            destination_location_id=location.id,
            reference=stock_in.reference,
            date=self._parse_date(stock_in.date),
            notes=notes,
        )

        transaction = inventory_service.process_transaction(db, user_id, tx_in)

        return StockInResponse(
            id=f"IN-{transaction.id:04d}",
            product={"sku": item.sku, "name": item.name},
            quantity=transaction.quantity,
            supplier=stock_in.supplier,
            location=location.name,
            date=transaction.date.isoformat(),
            status="completed",
            reference=transaction.reference,
            notes=stock_in.notes,
        )

    def update_stock_in(
        self, db: Session, stock_in_id: str, stock_in: StockInUpdate
    ) -> StockInResponse:
        tx_id = parse_prefixed_id(stock_in_id, expected_prefix="IN")
        tx = get_transaction_or_404(db, tx_id)

        if tx.type != InventoryMovementType.IN:
            raise CSMSException("Not a stock-in record", status_code=400)

        if stock_in.reference is not None:
            tx.reference = stock_in.reference

        notes = tx.notes or ""
        if stock_in.notes is not None:
            supplier = extract_meta(notes, "supplier")
            status = get_showroom_status(notes, default="completed")
            notes = set_showroom_status(stock_in.notes, status)
            if supplier:
                notes = set_meta(notes, "supplier", supplier)

        if stock_in.status is not None:
            notes = set_showroom_status(notes, stock_in.status)

        tx.notes = notes
        db.add(tx)
        db.commit()
        db.refresh(tx)

        return self._to_stock_in_response(tx)

    # ------------------------------------------------------------------
    # Stock Out
    # ------------------------------------------------------------------

    def get_stock_out_stats(self, db: Session) -> StockOutStats:
        today = jakarta_today()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)

        today_out = (
            db.query(func.sum(InventoryTransaction.quantity))
            .filter(
                and_(
                    InventoryTransaction.type == InventoryMovementType.OUT,
                    func.date(InventoryTransaction.date) == today,
                )
            )
            .scalar()
            or 0
        )

        week_out = (
            db.query(func.sum(InventoryTransaction.quantity))
            .filter(
                and_(
                    InventoryTransaction.type == InventoryMovementType.OUT,
                    func.date(InventoryTransaction.date) >= week_ago,
                )
            )
            .scalar()
            or 0
        )

        month_out = (
            db.query(func.sum(InventoryTransaction.quantity))
            .filter(
                and_(
                    InventoryTransaction.type == InventoryMovementType.OUT,
                    func.date(InventoryTransaction.date) >= month_ago,
                )
            )
            .scalar()
            or 0
        )

        total_customers = (
            db.query(InventoryTransaction.notes)
            .filter(
                and_(
                    InventoryTransaction.type == InventoryMovementType.OUT,
                    InventoryTransaction.notes.like("%[customer:%"),
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
        transactions = (
            db.query(InventoryTransaction)
            .filter(InventoryTransaction.type == InventoryMovementType.OUT)
            .options(
                joinedload(InventoryTransaction.item),
                joinedload(InventoryTransaction.source_location),
                joinedload(InventoryTransaction.user),
            )
            .order_by(InventoryTransaction.date.desc())
            .limit(50)
            .all()
        )

        result = []
        for tx in transactions:
            customer = extract_meta(tx.notes, "customer") or (
                tx.user.username if tx.user else "Unknown"
            )
            reason = extract_meta(tx.notes, "reason") or "Penjualan regular"
            result.append(
                StockOutResponse(
                    id=f"OUT-{tx.id:04d}",
                    product={
                        "sku": tx.item.sku if tx.item else "",
                        "name": tx.item.name if tx.item else "Unknown",
                    },
                    quantity=tx.quantity,
                    customer=customer,
                    location=tx.source_location.name if tx.source_location else "",
                    date=tx.date.isoformat(),
                    status=get_showroom_status(tx.notes, default="completed"),
                    reference=tx.reference,
                    reason=reason,
                    notes=self._strip_meta_notes(tx.notes),
                )
            )
        return result

    def create_stock_out(
        self, db: Session, user_id: int, stock_out: StockOutCreate
    ) -> StockOutResponse:
        item = resolve_item(db, stock_out.product)
        location = resolve_location(db, stock_out.location)

        notes = set_showroom_status(stock_out.notes, "completed")
        notes = set_meta(notes, "customer", stock_out.customer)
        notes = set_meta(notes, "reason", stock_out.reason)

        tx_in = TransactionCreate(
            item_id=item.id,
            quantity=stock_out.quantity,
            type=InventoryMovementType.OUT,
            source_location_id=location.id,
            reference=stock_out.reference,
            date=self._parse_date(stock_out.date),
            notes=notes,
        )

        transaction = inventory_service.process_transaction(db, user_id, tx_in)

        return StockOutResponse(
            id=f"OUT-{transaction.id:04d}",
            product={"sku": item.sku, "name": item.name},
            quantity=transaction.quantity,
            customer=stock_out.customer,
            location=location.name,
            date=transaction.date.isoformat(),
            status="completed",
            reference=transaction.reference,
            reason=stock_out.reason,
            notes=stock_out.notes,
        )

    def update_stock_out(
        self, db: Session, stock_out_id: str, stock_out: StockOutUpdate
    ) -> StockOutResponse:
        tx_id = parse_prefixed_id(stock_out_id, expected_prefix="OUT")
        tx = get_transaction_or_404(db, tx_id)

        if tx.type != InventoryMovementType.OUT:
            raise CSMSException("Not a stock-out record", status_code=400)

        if stock_out.reference is not None:
            tx.reference = stock_out.reference

        notes = tx.notes or ""
        customer = extract_meta(notes, "customer")
        reason = extract_meta(notes, "reason")
        status = get_showroom_status(notes, default="completed")

        if stock_out.notes is not None:
            notes = set_showroom_status(stock_out.notes, status)
            if customer:
                notes = set_meta(notes, "customer", customer)
            if reason:
                notes = set_meta(notes, "reason", reason)

        if stock_out.reason is not None:
            notes = set_meta(notes, "reason", stock_out.reason)

        if stock_out.status is not None:
            notes = set_showroom_status(notes, stock_out.status)

        tx.notes = notes
        db.add(tx)
        db.commit()
        db.refresh(tx)

        return self._to_stock_out_response(tx)

    # ------------------------------------------------------------------
    # Locations
    # ------------------------------------------------------------------

    def get_locations(self, db: Session) -> List[ShowroomLocation]:
        locations = db.query(Location).order_by(Location.name.asc()).all()
        return [
            ShowroomLocation(id=location_slug(loc.name), name=loc.name)
            for loc in locations
        ]

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _count_transfers_by_status(self, db: Session, status: str) -> int:
        return (
            db.query(InventoryTransaction)
            .filter(
                and_(
                    InventoryTransaction.type == InventoryMovementType.TRANSFER,
                    InventoryTransaction.notes.like(f"%[showroom:{status}]%"),
                )
            )
            .count()
        )

    def _parse_date(self, value: str):
        if not value:
            return jakarta_now()
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

    def _to_transfer_response(self, tx: InventoryTransaction) -> TransferResponse:
        return TransferResponse(
            id=f"TRF-{tx.id:04d}",
            fromLocation=tx.source_location.name if tx.source_location else "",
            toLocation=tx.destination_location.name if tx.destination_location else "",
            items=[
                TransferItem(
                    product=tx.item.name if tx.item else "Unknown",
                    quantity=tx.quantity,
                )
            ],
            totalQuantity=tx.quantity,
            status=get_showroom_status(tx.notes, default="completed"),
            createdAt=tx.date.isoformat(),
            estimatedArrival=extract_meta(tx.notes, "eta") or tx.date.date().isoformat(),
        )

    def _to_stock_in_response(self, tx: InventoryTransaction) -> StockInResponse:
        return StockInResponse(
            id=f"IN-{tx.id:04d}",
            product={
                "sku": tx.item.sku if tx.item else "",
                "name": tx.item.name if tx.item else "Unknown",
            },
            quantity=tx.quantity,
            supplier=extract_meta(tx.notes, "supplier")
            or (tx.user.username if tx.user else "Unknown"),
            location=tx.destination_location.name if tx.destination_location else "",
            date=tx.date.isoformat(),
            status=get_showroom_status(tx.notes, default="completed"),
            reference=tx.reference,
            notes=self._strip_meta_notes(tx.notes),
        )

    def _to_stock_out_response(self, tx: InventoryTransaction) -> StockOutResponse:
        return StockOutResponse(
            id=f"OUT-{tx.id:04d}",
            product={
                "sku": tx.item.sku if tx.item else "",
                "name": tx.item.name if tx.item else "Unknown",
            },
            quantity=tx.quantity,
            customer=extract_meta(tx.notes, "customer")
            or (tx.user.username if tx.user else "Unknown"),
            location=tx.source_location.name if tx.source_location else "",
            date=tx.date.isoformat(),
            status=get_showroom_status(tx.notes, default="completed"),
            reference=tx.reference,
            reason=extract_meta(tx.notes, "reason") or "Penjualan regular",
            notes=self._strip_meta_notes(tx.notes),
        )


showroom_service = ShowroomService()
