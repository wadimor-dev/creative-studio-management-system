import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.session import SessionLocal
from app.services.report_engine import report_engine
from app.services.dashboard_service import dashboard_service

def run_tests():
    db = SessionLocal()
    try:
        print("Testing dashboard service...")
        metrics = dashboard_service.get_dashboard(db, days=7)
        print("KPI:", metrics.get("kpi"))
        
        print("Testing report engine...")
        data = report_engine.get_report_data(db, report_type='daily')
        print("Summary:", data.get("summary"))
        print("Total Items:", data.get("total"))
        
        print("\nAll integration ran successfully!")
    except Exception as e:
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    run_tests()
