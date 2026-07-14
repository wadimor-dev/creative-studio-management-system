from pydantic import BaseModel
from datetime import date
from typing import Dict

class Period(BaseModel):
    start_date: date
    end_date: date

class GeneratedReportResponse(BaseModel):
    period: Period
    daily_reports_submitted: int
    inventory_summary: Dict[str, int]
