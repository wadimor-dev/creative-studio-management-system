from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta
import calendar
from app.models.inventory_transaction import InventoryTransaction
from app.models.daily_report import DailyReport
from app.constants.inventory import TransactionType

class ReportGeneratorService:
    def generate_summary(self, db: Session, start_date: date, end_date: date):
        daily_reports_count = db.query(DailyReport).filter(
            func.date(DailyReport.report_date) >= start_date,
            func.date(DailyReport.report_date) <= end_date
        ).count()
        
        tx_query = db.query(
            InventoryTransaction.transaction_type,
            func.sum(InventoryTransaction.quantity).label("total_quantity")
        ).filter(
            func.date(InventoryTransaction.created_at) >= start_date,
            func.date(InventoryTransaction.created_at) <= end_date
        ).group_by(InventoryTransaction.transaction_type).all()
        
        tx_summary = {
            TransactionType.STOCK_IN: 0,
            TransactionType.STOCK_OUT: 0,
            TransactionType.RETURN: 0
        }
        
        for tx_type, total in tx_query:
            if tx_type in tx_summary:
                tx_summary[tx_type] = int(total) if total else 0
                
        return {
            "period": {
                "start_date": start_date,
                "end_date": end_date
            },
            "daily_reports_submitted": daily_reports_count,
            "inventory_summary": tx_summary
        }
        
    def generate_weekly(self, db: Session, reference_date: date = None):
        if not reference_date:
            reference_date = date.today()
        # Monday is 0, Sunday is 6
        start_date = reference_date - timedelta(days=reference_date.weekday())
        end_date = start_date + timedelta(days=6)
        
        return self.generate_summary(db, start_date, end_date)
        
    def generate_monthly(self, db: Session, year: int, month: int):
        start_date = date(year, month, 1)
        _, last_day = calendar.monthrange(year, month)
        end_date = date(year, month, last_day)
        
        return self.generate_summary(db, start_date, end_date)

report_generator_service = ReportGeneratorService()
