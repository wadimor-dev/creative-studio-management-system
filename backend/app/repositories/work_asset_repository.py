from typing import List
from sqlalchemy.orm import Session
from app.models.work_asset import WorkAsset

class WorkAssetRepository:
    def create(
        self,
        db: Session,
        work_activity_id: int,
        item_id: int,
        location_id: int,
        quantity: int,
        status: str,
        borrowed_at,
        returned_at=None,
        commit: bool = True,
    ) -> WorkAsset:
        db_obj = WorkAsset(
            work_activity_id=work_activity_id,
            item_id=item_id,
            location_id=location_id,
            quantity=quantity,
            status=status,
            borrowed_at=borrowed_at,
            returned_at=returned_at,
        )
        db.add(db_obj)
        if commit:
            db.commit()
            db.refresh(db_obj)
        else:
            db.flush()
        return db_obj

    def find_borrowed_by_activity(self, db: Session, activity_id: int) -> List[WorkAsset]:
        return db.query(WorkAsset).filter(
            WorkAsset.work_activity_id == activity_id,
            WorkAsset.status == "BORROWED"
        ).all()

    def find_by_activity(self, db: Session, activity_id: int) -> List[WorkAsset]:
        return db.query(WorkAsset).filter(
            WorkAsset.work_activity_id == activity_id
        ).all()

work_asset_repository = WorkAssetRepository()
