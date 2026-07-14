from datetime import datetime, timezone, timedelta, date
import calendar

def utc_now() -> datetime:
    return datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None)

def local_now() -> datetime:
    return datetime.now()

def today() -> date:
    return date.today()

def start_of_day(dt: datetime = None) -> datetime:
    if not dt:
        dt = local_now()
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)

def end_of_day(dt: datetime = None) -> datetime:
    if not dt:
        dt = local_now()
    return dt.replace(hour=23, minute=59, second=59, microsecond=999999)

def start_of_month(year: int, month: int) -> date:
    return date(year, month, 1)

def end_of_month(year: int, month: int) -> date:
    _, last_day = calendar.monthrange(year, month)
    return date(year, month, last_day)

def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    return dt.strftime(format_str)

def parse_datetime(dt_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    return datetime.strptime(dt_str, format_str)
