from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta, timezone
from collections import defaultdict
import calendar

from app.models.user import User
from app.models.work_activity import WorkActivity
from app.models.work_category import WorkCategory
from app.models.item import Item
from app.models.work_asset import WorkAsset
from app.constants.work_activity import WorkActivityStatus
from app.services.report_engine import report_engine

class DashboardService:
    def get_dashboard(self, db: Session, days: int = 7) -> dict:
        now = datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Use ReportEngine for aggregated metrics
        # Today's completed tasks filter
        today_filters = {'start_date': today_start}
        today_summary = report_engine.get_aggregate_summary(db, filters=today_filters)
        
        # All time or this month summary for EOM
        this_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        month_filters = {'start_date': this_month_start}
        
        # We still need working count and assets out (which are current snapshots)
        working_count = db.query(func.count(WorkActivity.id)).filter(
            WorkActivity.status == WorkActivityStatus.WORKING
        ).scalar() or 0
        
        assets_out = db.query(func.count(WorkAsset.id)).filter(
            WorkAsset.status == 'BORROWED'
        ).scalar() or 0
        
        studio_status = {
            "working": working_count,
            "assets_out": assets_out,
            "completed": today_summary["completed"]
        }
        
        # KPI uses today's summary from ReportEngine
        working_hours = report_engine.get_working_activities_duration(db, now)
        total_secs = today_summary.get("total_duration_seconds", 0)
        completed = today_summary.get("completed", 0)
        avg_duration = "0 Menit"
        if completed > 0:
            avg_secs = total_secs / completed
            h = int(avg_secs // 3600)
            m = int((avg_secs % 3600) // 60)
            avg_duration = f"{h} Jam {m} Menit" if h > 0 else f"{m} Menit"
            
        kpi = {
            "active_workers": working_count,
            "completed_tasks_today": completed,
            "assets_out": assets_out,
            "current_working_hours": working_hours,
            "average_completion_time": avg_duration
        }
        
        # Charts (keep logic here or move to engine, but we can reuse the queries since they are specific to dashboard visualization format)
        charts = self.get_charts(db, now, days)
        
        return {
            "studio_status": studio_status,
            "kpi": kpi,
            "current_activity": self.get_current_activity(db),
            "charts": charts,
            "recent_activity": self.get_recent_activity(db),
            "summary": self.get_summary(db, this_month_start)
        }

    def get_current_activity(self, db: Session) -> list:
        activities = db.query(WorkActivity).filter(
            WorkActivity.status == WorkActivityStatus.WORKING
        ).order_by(WorkActivity.start_time.desc()).limit(50).all()
        
        result = []
        for act in activities:
            result.append({
                "id": act.id,
                "user": act.user.full_name or act.user.username if act.user else "Unknown",
                "activity": act.activity_name,
                "category": act.category.name if act.category else "Uncategorized",
                "start_time": act.start_time.isoformat() if act.start_time else None,
                "status": act.status.value
            })
        return result

    def get_charts(self, db: Session, now: datetime, days: int) -> dict:
        start_date = now - timedelta(days=days-1)
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # 1. Volume Aktivitas
        volume_data = db.query(
            func.date(WorkActivity.end_time).label('date'),
            func.count(WorkActivity.id).label('count')
        ).filter(
            WorkActivity.status == WorkActivityStatus.COMPLETED,
            WorkActivity.end_time >= start_date
        ).group_by(func.date(WorkActivity.end_time)).all()
        
        vol_dict = {row.date.strftime("%Y-%m-%d"): row.count for row in volume_data}
        
        volume_chart = []
        for i in range(days):
            d = start_date + timedelta(days=i)
            d_str = d.strftime("%Y-%m-%d")
            # For UI, maybe day name
            day_name = calendar.day_abbr[d.weekday()]
            volume_chart.append({
                "date": d_str,
                "name": day_name,
                "completed": vol_dict.get(d_str, 0)
            })
            
        # 2. Kategori Aktivitas (Pie Chart)
        cat_data = db.query(
            WorkCategory.name,
            func.count(WorkActivity.id).label('count')
        ).join(WorkActivity, WorkActivity.category_id == WorkCategory.id).filter(
            WorkActivity.status == WorkActivityStatus.COMPLETED,
            WorkActivity.end_time >= start_date
        ).group_by(WorkCategory.id).all()
        
        total_cat = sum(row.count for row in cat_data)
        category_chart = []
        for row in cat_data:
            pct = (row.count / total_cat * 100) if total_cat > 0 else 0
            category_chart.append({
                "name": row.name,
                "value": row.count,
                "percentage": round(pct, 1)
            })
            
        return {
            "volume": volume_chart,
            "category": category_chart
        }

    def get_recent_activity(self, db: Session) -> list:
        activities = db.query(WorkActivity).order_by(
            WorkActivity.end_time.is_(None), WorkActivity.end_time.desc(), WorkActivity.start_time.desc()
        ).limit(20).all()
        
        result = []
        for act in activities:
            result.append({
                "id": act.id,
                "user": act.user.full_name or act.user.username if act.user else "Unknown",
                "activity": act.activity_name,
                "category": act.category.name if act.category else "Uncategorized",
                "started": act.start_time.isoformat() if act.start_time else None,
                "finished": act.end_time.isoformat() if act.end_time else None,
                "status": act.status.value
            })
        return result

    def get_summary(self, db: Session, this_month_start: datetime) -> dict:
        eom = db.query(
            User.full_name, User.username,
            func.count(WorkActivity.id).label('count')
        ).join(WorkActivity, WorkActivity.user_id == User.id).filter(
            WorkActivity.status == WorkActivityStatus.COMPLETED,
            WorkActivity.end_time >= this_month_start
        ).group_by(User.id).order_by(func.count(WorkActivity.id).desc()).first()
        
        mua = db.query(
            Item.name,
            func.count(WorkAsset.id).label('count')
        ).join(WorkAsset).filter(
            WorkAsset.created_at >= this_month_start
        ).group_by(Item.id).order_by(func.count(WorkAsset.id).desc()).first()
        
        mpc = db.query(
            WorkCategory.name,
            func.count(WorkActivity.id).label('count')
        ).join(WorkActivity, WorkActivity.category_id == WorkCategory.id).filter(
            WorkActivity.status == WorkActivityStatus.COMPLETED,
            WorkActivity.end_time >= this_month_start
        ).group_by(WorkCategory.id).order_by(func.count(WorkActivity.id).desc()).first()
        
        return {
            "employee_of_month": {
                "name": (eom.full_name or eom.username) if eom else "None",
                "value": f"{eom.count if eom else 0} activities"
            },
            "most_used_asset": {
                "name": mua.name if mua else "None",
                "value": f"{mua.count if mua else 0} times borrowed"
            },
            "most_productive_category": {
                "name": mpc.name if mpc else "None",
                "value": f"{mpc.count if mpc else 0} activities"
            }
        }

dashboard_service = DashboardService()
