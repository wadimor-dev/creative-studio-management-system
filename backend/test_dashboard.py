import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database.session import SessionLocal
from app.services.dashboard_service import dashboard_service

def run_tests():
    db = SessionLocal()
    try:
        print("Testing dashboard service...")
        metrics = dashboard_service.get_dashboard(db, days=7)
        print("KPI:", metrics.get("kpi"))
        print("Studio Status:", metrics.get("studio_status"))
        print("Summary:", metrics.get("summary"))
        print("Recent Activity (count):", len(metrics.get("recent_activity", [])))
        print("Current Activity (count):", len(metrics.get("current_activity", [])))
        
        # charts
        charts = metrics.get("charts", {})
        print("Volume Chart days:", len(charts.get("volume", [])))
        print("Category Chart categories:", len(charts.get("category", [])))
        
        print("\nAll dashboard aggregation ran successfully!")
    except Exception as e:
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    run_tests()
