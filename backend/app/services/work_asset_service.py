from datetime import datetime, timezone, timedelta
from typing import List
from sqlalchemy.orm import Session
from app.constants.status import WorkAssetStatus
from app.models.work_asset import WorkAsset
from app.schemas.work_activity import WorkAssetPayload
from app.repositories.work_asset_repository import work_asset_repository
from app.services.inventory_service import inventory_service
from app.schemas.inventory import TransactionCreate
from app.models.inventory_transaction import InventoryMovementType

class WorkAssetService:
    def borrow_assets(
        self,
        db: Session,
        activity_id: int,
        user_id: int,
        assets: List[WorkAssetPayload],
        reference: str,
    ) -> List[WorkAsset]:
        borrowed_assets = []
        for asset in assets:
            tx_data = TransactionCreate(
                item_id=asset.item_id,
                type=InventoryMovementType.OUT,
                quantity=asset.quantity,
                source_location_id=asset.location_id,
                reference=reference,
                notes=f"Borrowed for work activity {activity_id}",
            )
            inventory_service.process_transaction(db, user_id, tx_data, commit=False)
            work_asset = work_asset_repository.create(
                db=db,
                work_activity_id=activity_id,
                item_id=asset.item_id,
                location_id=asset.location_id,
                quantity=asset.quantity,
                status=WorkAssetStatus.BORROWED,
                borrowed_at=datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None),
                commit=False,
            )
            borrowed_assets.append(work_asset)
        return borrowed_assets

    def return_assets(
        self,
        db: Session,
        activity_id: int,
        user_id: int,
        reference: str,
    ) -> List[WorkAsset]:
        borrowed_assets = work_asset_repository.find_borrowed_by_activity(db, activity_id)
        returned_assets = []
        for asset in borrowed_assets:
            tx_data = TransactionCreate(
                item_id=asset.item_id,
                type=InventoryMovementType.IN,
                quantity=asset.quantity,
                destination_location_id=asset.location_id,
                reference=reference,
                notes=f"Returned from work activity {activity_id}",
            )
            inventory_service.process_transaction(db, user_id, tx_data, commit=False)
            asset.status = WorkAssetStatus.RETURNED
            asset.returned_at = datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None)
            db.add(asset)
            returned_assets.append(asset)
        db.flush()
        return returned_assets

work_asset_service = WorkAssetService()
