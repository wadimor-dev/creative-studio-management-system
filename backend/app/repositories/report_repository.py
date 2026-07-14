from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.daily_report import DailyReport
from datetime import date

class ReportRepository:
    def count_reports_in_period(self, db: Session, start_date: date, end_date: date) -> int:
        return db.query(DailyReport).filter(
            func.date(DailyReport.report_date) >= start_date,
            func.date(DailyReport.report_date) <= end_date
        ).count()

report_repo = ReportRepository()
