import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database.session import SessionLocal
from app.models.user import User
from app.models.item import Item
from app.models.location import Location
from app.models.item_stock import ItemStock
from app.models.work_category import WorkCategory
from app.constants.work_activity import WorkEvidenceType
from app.schemas.work_activity import WorkActivityCreate, WorkAssetPayload
from app.services.work_activity_service import work_activity_service
from app.models.work_evidence import WorkEvidence
from datetime import datetime, timezone
from app.core.exceptions import CSMSException

def bypass_evidence(db, activity_id, user_id, type_):
    evidence = WorkEvidence(
        work_activity_id=activity_id,
        uploaded_by=user_id,
        type=type_,
        file_path="dummy.jpg",
        file_name="dummy.jpg",
        mime_type="image/jpeg",
        file_size=1024
    )
    db.add(evidence)
    db.commit()

def run_tests():
    db = SessionLocal()
    try:
        user = db.query(User).first()
        item = db.query(Item).first()
        location = db.query(Location).first()
        work_category = db.query(WorkCategory).first()
        
        if not (user and item and location and work_category):
            print("Missing seed data!")
            return
            
        stock = db.query(ItemStock).filter(ItemStock.item_id == item.id, ItemStock.location_id == location.id).first()
        if not stock:
            stock = ItemStock(item_id=item.id, location_id=location.id, quantity=10)
            db.add(stock)
            db.flush()
        else:
            stock.quantity = 10
            db.flush()
            
        db.commit()
        
        print(f"Setup done. Initial Stock: {stock.quantity}")

        print("\n--- POSITIVE TEST ---")
        act_in = WorkActivityCreate(category_id=work_category.id, activity_name="Test Borrow Camera")
        activity = work_activity_service.create_activity(db, act_in, user.id)
        bypass_evidence(db, activity.id, user.id, WorkEvidenceType.BEFORE)
        
        asset_payload = [WorkAssetPayload(item_id=item.id, location_id=location.id, quantity=1)]
        started = work_activity_service.start_activity(db, activity.id, user.id, assets=asset_payload)
        
        stock = db.query(ItemStock).filter(ItemStock.item_id == item.id, ItemStock.location_id == location.id).first()
        print(f"Stock after start: {stock.quantity} (expected 9)")
        assert stock.quantity == 9
        
        bypass_evidence(db, activity.id, user.id, WorkEvidenceType.AFTER)
        finished = work_activity_service.finish_activity(db, activity.id, user.id)
        
        stock = db.query(ItemStock).filter(ItemStock.item_id == item.id, ItemStock.location_id == location.id).first()
        print(f"Stock after finish: {stock.quantity} (expected 10)")
        assert stock.quantity == 10
        
        print("\n--- NEGATIVE TEST: BORROW MORE THAN STOCK ---")
        act_in2 = WorkActivityCreate(category_id=work_category.id, activity_name="Test Negative Borrow")
        activity2 = work_activity_service.create_activity(db, act_in2, user.id)
        bypass_evidence(db, activity2.id, user.id, WorkEvidenceType.BEFORE)
        
        try:
            asset_payload_over = [WorkAssetPayload(item_id=item.id, location_id=location.id, quantity=15)]
            work_activity_service.start_activity(db, activity2.id, user.id, assets=asset_payload_over)
            print("ERROR: Should have failed!")
        except CSMSException as e:
            print(f"SUCCESS (Expected failure): {e.detail}")
            
        print("\n--- NEGATIVE TEST: DUPLICATE ASSET IN PAYLOAD ---")
        try:
            asset_payload_dup = [
                WorkAssetPayload(item_id=item.id, location_id=location.id, quantity=1),
                WorkAssetPayload(item_id=item.id, location_id=location.id, quantity=1)
            ]
            work_activity_service.start_activity(db, activity2.id, user.id, assets=asset_payload_dup)
            print("ERROR: Should have failed!")
        except CSMSException as e:
            print(f"SUCCESS (Expected failure): {e.detail}")
            
        print("\nAll tests ran successfully.")
            
    finally:
        db.close()

if __name__ == "__main__":
    run_tests()
