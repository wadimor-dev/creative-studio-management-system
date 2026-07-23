import uuid
import enum
from datetime import datetime, date
from sqlalchemy import Column, String, Date, DateTime, Enum as SAEnum
from sqlalchemy.orm import relationship
from app.core.database.base import Base


class QueueStatus(str, enum.Enum):
    WAITING = "WAITING"
    CALLING = "CALLING"
    SERVING = "SERVING"
    FINISHED = "FINISHED"
    CANCELLED = "CANCELLED"


class Queue(Base):
    __tablename__ = "queues"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    queue_number = Column(String(20), nullable=False)
    queue_date = Column(Date, default=date.today, nullable=False, index=True)
    status = Column(SAEnum(QueueStatus, name="queue_status_enum", create_constraint=True, validate_strings=True), default=QueueStatus.WAITING, nullable=False)
    called_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)

    visit = relationship("Visit", back_populates="queue", uselist=False)
