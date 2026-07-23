from datetime import date, datetime
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.exceptions import CSMSException
from app.modules.hrd_ga.clinic.models.queue import Queue, QueueStatus
from app.modules.hrd_ga.clinic.models.visit import Visit
from app.modules.hrd_ga.clinic.schemas import QueueCreate, QueueUpdate, QueueResponse


class QueueService:

    def get_all(self, db: Session, skip: int = 0, limit: int = 100,
                queue_date: Optional[date] = None,
                status: Optional[QueueStatus] = None) -> List[QueueResponse]:
        query = db.query(Queue)
        query_date = queue_date or date.today()
        query = query.filter(Queue.queue_date == query_date)
        if status:
            query = query.filter(Queue.status == status)
        items = query.order_by(Queue.queue_number).offset(skip).limit(limit).all()
        return [QueueResponse.model_validate(q) for q in items]

    def get_by_id(self, db: Session, queue_id: str) -> QueueResponse:
        queue = db.query(Queue).filter(Queue.id == queue_id).first()
        if not queue:
            raise CSMSException("Queue not found", status_code=404)
        return QueueResponse.model_validate(queue)

    def get_current_queue(self, db: Session, queue_date: Optional[date] = None) -> Optional[QueueResponse]:
        query_date = queue_date or date.today()
        queue = db.query(Queue).filter(
            Queue.queue_date == query_date,
            Queue.status.in_([QueueStatus.CALLING, QueueStatus.SERVING])
        ).order_by(Queue.queue_number).first()
        if not queue:
            return None
        return QueueResponse.model_validate(queue)

    def create(self, db: Session, data: QueueCreate) -> QueueResponse:
        today = data.queue_date
        max_num = db.query(func.max(Queue.queue_number)).filter(
            Queue.queue_date == today
        ).scalar()
        prefix = "A"
        next_num = 1
        if max_num:
            num_part = max_num.lstrip("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            prefix = max_num[:len(max_num) - len(num_part)] or prefix
            if num_part.isdigit():
                next_num = int(num_part) + 1
        data.queue_number = f"{prefix}{str(next_num).zfill(3)}"
        queue = Queue(**data.model_dump())
        db.add(queue)
        db.commit()
        db.refresh(queue)
        return QueueResponse.model_validate(queue)

    def update_status(self, db: Session, queue_id: str, new_status: QueueStatus) -> QueueResponse:
        queue = db.query(Queue).filter(Queue.id == queue_id).first()
        if not queue:
            raise CSMSException("Queue not found", status_code=404)

        now = datetime.utcnow()
        if new_status == QueueStatus.CALLING:
            queue.called_at = now
        elif new_status == QueueStatus.FINISHED:
            queue.finished_at = now
        elif new_status == QueueStatus.CANCELLED:
            queue.finished_at = now

        queue.status = new_status
        db.commit()
        db.refresh(queue)
        return QueueResponse.model_validate(queue)

    def get_waiting_count(self, db: Session, queue_date: Optional[date] = None) -> int:
        query_date = queue_date or date.today()
        return db.query(Queue).filter(
            Queue.queue_date == query_date,
            Queue.status == QueueStatus.WAITING
        ).count()


queue_service = QueueService()
