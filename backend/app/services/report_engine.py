from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta, timezone
from collections import defaultdict
import calendar

from app.models.user import User
from app.core.organization.employee.models import Employee
from app.models.work_activity import WorkActivity
from app.models.work_category import WorkCategory
from app.models.work_asset import WorkAsset
from app.constants.work_activity import WorkActivityStatus
from app.models.work_evidence import WorkEvidence

class ReportEngine:
    def _apply_filters(self, query, filters: dict):
        if filters.get('start_date'):
            query = query.filter(WorkActivity.end_time >= filters['start_date'])
        if filters.get('end_date'):
            query = query.filter(WorkActivity.end_time <= filters['end_date'])
        if filters.get('user_id'):
            query = query.filter(WorkActivity.user_id == filters['user_id'])
        if filters.get('category_id'):
            query = query.filter(WorkActivity.category_id == filters['category_id'])
        if filters.get('status'):
            query = query.filter(WorkActivity.status == filters['status'])
        return query

    def get_aggregate_summary(self, db: Session, filters: dict = None) -> dict:
        filters = filters or {}
        
        # Base query for all activities matching the basic filters (ignoring status)
        base_query = db.query(WorkActivity)
        
        # Apply filters except status to get general stats
        f_no_status = {k: v for k, v in filters.items() if k != 'status'}
        general_query = self._apply_filters(base_query, f_no_status)
        all_activities = general_query.all()
        
        total_activity = len(all_activities)
        completed = sum(1 for a in all_activities if a.status == WorkActivityStatus.COMPLETED)
        working = sum(1 for a in all_activities if a.status == WorkActivityStatus.WORKING)
        cancelled = sum(1 for a in all_activities if a.status == WorkActivityStatus.CANCELLED)
        
        total_seconds = 0
        assets_used = set()
        total_evidence = 0
        
        # Apply specific filters (including status) for calculating seconds and assets
        query = self._apply_filters(base_query, filters)
        filtered_activities = query.all()
        
        for act in filtered_activities:
            act_seconds = act.worked_seconds
            if act.status == WorkActivityStatus.WORKING and act.current_session_started_at:
                now_wib = datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None)
                act_seconds += (now_wib - act.current_session_started_at).total_seconds()
            
            total_seconds += act_seconds
            
            for asset in act.assets:
                assets_used.add(asset.item_id)
                
            total_evidence += len(act.evidences)
                
        def format_duration(seconds):
            h = int(seconds // 3600)
            m = int((seconds % 3600) // 60)
            if h > 0:
                return f"{h} Jam {m} Menit"
            return f"{m} Menit"

        return {
            "total_activity": total_activity,
            "completed": completed,
            "working": working,
            "cancelled": cancelled,
            "total_duration_seconds": int(total_seconds),
            "total_duration_human": format_duration(total_seconds),
            "total_assets": len(assets_used),
            "total_evidence": total_evidence
        }
        
    def get_working_activities_duration(self, db: Session, now: datetime) -> str:
        working_activities = db.query(WorkActivity).filter(
            WorkActivity.status == WorkActivityStatus.WORKING
        ).all()
        
        total_seconds = 0
        for act in working_activities:
            act_seconds = act.worked_seconds
            if act.current_session_started_at:
                st = act.current_session_started_at.replace(tzinfo=None)
                safe_now = now.replace(tzinfo=None)
                act_seconds += (safe_now - st).total_seconds()
            total_seconds += act_seconds
                
        def format_duration(seconds):
            h = int(seconds // 3600)
            m = int((seconds % 3600) // 60)
            if h > 0:
                return f"{h} Jam {m} Menit"
            return f"{m} Menit"
            
        return format_duration(total_seconds)

    def get_report_data(self, db: Session, report_type: str, skip: int = 0, limit: int = 20, **filters) -> dict:
        from sqlalchemy.orm import joinedload, selectinload
        from app.models.user import User
        from app.models.work_category import WorkCategory
        
        now = datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None)
        start_date = None
        end_date = None
        
        if report_type == 'daily':
            date_param = filters.get('date')
            if date_param:
                dt = datetime.strptime(date_param, '%Y-%m-%d')
                start_date = dt.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)
                end_date = dt.replace(hour=23, minute=59, second=59, microsecond=999999, tzinfo=timezone.utc)
            else:
                start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
                end_date = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        elif report_type == 'weekly':
            start_date = now - timedelta(days=now.weekday())
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + timedelta(days=6, hours=23, minutes=59, seconds=59)
        elif report_type == 'monthly':
            month = filters.get('month', now.month)
            year = filters.get('year', now.year)
            start_date = datetime(year=int(year), month=int(month), day=1, tzinfo=timezone.utc)
            last_day = calendar.monthrange(int(year), int(month))[1]
            end_date = datetime(year=int(year), month=int(month), day=last_day, hour=23, minute=59, second=59, tzinfo=timezone.utc)

        f = {
            'start_date': start_date,
            'end_date': end_date
        }
        
        for k in ['user_id', 'category_id', 'status', 'division']:
            if filters.get(k):
                f[k] = filters[k]
                
        query = db.query(WorkActivity).options(
            joinedload(WorkActivity.user).joinedload(User.role),
            joinedload(WorkActivity.user).joinedload(User.employee).joinedload(Employee.division),
            joinedload(WorkActivity.category),
            selectinload(WorkActivity.assets).joinedload(WorkAsset.item),
            selectinload(WorkActivity.assets).joinedload(WorkAsset.location),
            selectinload(WorkActivity.evidences)
        )
        query = self._apply_filters(query, f)
        
        activities = query.order_by(WorkActivity.end_time.is_(None), WorkActivity.end_time.desc(), WorkActivity.start_time.desc()).offset(skip).limit(limit).all()
        
        formatted_activities = []
        for act in activities:
            dur_seconds = act.worked_seconds
            if act.status == WorkActivityStatus.WORKING and act.current_session_started_at:
                now_wib = datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None)
                dur_seconds += (now_wib - act.current_session_started_at).total_seconds()
            
            h = int(dur_seconds // 3600)
            m = int((dur_seconds % 3600) // 60)
            dur_human = f"{h} Jam {m} Menit" if h > 0 else f"{m} Menit"
                
            assets = []
            for a in act.assets:
                assets.append({
                    "id": a.id,
                    "item": a.item.name if a.item else "-",
                    "location": a.location.name if getattr(a, 'location', None) else "-",
                    "qty": a.quantity
                })
            
            evs = {"before": None, "progress": [], "after": None}
            for ev in act.evidences:
                ev_data = {
                    "id": ev.id,
                    "type": ev.type.value,
                    "storage_path": ev.file_path,
                    "thumbnail": ev.file_path, # Placeholder for thumbnail logic later
                    "uploaded_at": ev.uploaded_at.isoformat() if ev.uploaded_at else None
                }
                if ev.type.value == "BEFORE":
                    evs["before"] = ev_data
                elif ev.type.value == "AFTER":
                    evs["after"] = ev_data
                else:
                    evs["progress"].append(ev_data)
                
            formatted_activities.append({
                "id": act.id,
                "date": act.end_time.isoformat() if act.end_time else (act.start_time.isoformat() if act.start_time else None),
                "employee": act.user.full_name or act.user.username if act.user else "Unknown",
                "division": act.user.employee.division.name if act.user and act.user.employee and act.user.employee.division else "Unassigned",
                "category": act.category.name if act.category else "Uncategorized",
                "activity": act.activity_name,
                "duration_seconds": int(dur_seconds),
                "duration_human": dur_human,
                "assets": assets,
                "evidence_count": len(act.evidences),
                "evidences": evs,
                "status": act.status.value,
                "start_time": act.start_time.isoformat() if act.start_time else None,
                "end_time": act.end_time.isoformat() if act.end_time else None,
                "notes": act.notes or ""
            })
            
        summary = self.get_aggregate_summary(db, f)
        
        current_user_name = "System" # Will be overridden by Export Manager or API later
        
        return {
            "metadata": {
                "schema_version": "1.0",
                "generated_at": datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None).isoformat(),
                "generated_by": current_user_name,
                "report_type": report_type.capitalize(),
                "period": f"{start_date.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')}" if start_date and end_date else "All Time",
                "company": "Wadimor",
                "generated_from": "Creative Division",
                "application_version": "1.0.0"
            },
            "summary": summary,
            "activities": formatted_activities
        }

report_engine = ReportEngine()
