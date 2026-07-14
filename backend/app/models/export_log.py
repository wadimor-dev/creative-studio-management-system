from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta

from app.database.base import Base

class ExportLog(Base):
    __tablename__ = "export_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(String(50), nullable=False) # e.g. "weekly", "monthly", "daily"
    format = Column(String(10), nullable=False) # e.g. "PDF", "EXCEL"
    created_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None), nullable=False)

    user = relationship("User")
