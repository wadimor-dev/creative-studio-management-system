from sqlalchemy import Column, Integer, String, Date, DateTime
from datetime import datetime, timezone, timedelta
from app.database.base import Base


class ShowroomDailyStorageSummary(Base):
    __tablename__ = "showroom_daily_storage_summary"

    id = Column(Integer, primary_key=True, index=True)
    summary_date = Column(Date, nullable=False, index=True)
    total_items = Column(Integer, nullable=False, default=0)
    total_products = Column(Integer, nullable=False, default=0)
    total_locations = Column(Integer, nullable=False, default=0)
    total_movements = Column(Integer, nullable=False, default=0)
    incoming = Column(Integer, nullable=False, default=0)
    outgoing = Column(Integer, nullable=False, default=0)
    capacity_used_pct = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))

    __table_args__ = (
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},
    )
