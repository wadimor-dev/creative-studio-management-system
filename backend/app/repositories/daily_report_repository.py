from app.repositories.base_repository import BaseRepository
from app.models.daily_report import DailyReport
from app.schemas.daily_report import DailyReportCreate, DailyReportUpdate

class DailyReportRepository(BaseRepository[DailyReport, DailyReportCreate, DailyReportUpdate]):
    def __init__(self):
        super().__init__(DailyReport)

daily_report_repo = DailyReportRepository()
