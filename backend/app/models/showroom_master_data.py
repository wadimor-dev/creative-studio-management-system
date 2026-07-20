from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from app.database.base import Base


class ShowroomMasterData(Base):
    __tablename__ = "showroom_master_data"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    value = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    sort_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None), onupdate=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))
