from app.core.database.session import SessionLocal
from app.models.work_activity import WorkActivity
from app.constants.work_activity import WorkActivityStatus
from sqlalchemy import func
from datetime import datetime, timedelta, timezone

def check_db():
    db = SessionLocal()
    try:
        now = datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None)
        start_date = now - timedelta(days=6)
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        
        volume_data = db.query(
            func.date(WorkActivity.end_time).label('date'),
            func.count(WorkActivity.id).label('count')
        ).filter(
            WorkActivity.status == WorkActivityStatus.COMPLETED,
            WorkActivity.end_time >= start_date
        ).group_by(func.date(WorkActivity.end_time)).all()
        
        if volume_data:
            print(f"Type of row.date: {type(volume_data[0].date)}")
            print(f"Value of row.date: {volume_data[0].date}")
            try:
                print("strftime output:", volume_data[0].date.strftime("%Y-%m-%d"))
            except Exception as e:
                print("Error with strftime:", e)
        
    finally:
        db.close()

if __name__ == "__main__":
    check_db()
