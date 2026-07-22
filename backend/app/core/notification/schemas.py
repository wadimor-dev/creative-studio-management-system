from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.core.notification.models import NotificationChannel, NotificationStatus


class NotificationCreate(BaseModel):
    user_id: int
    channel: NotificationChannel = NotificationChannel.IN_APP
    title: str
    body: Optional[str] = None
    reference_type: Optional[str] = None
    reference_id: Optional[int] = None


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    channel: NotificationChannel
    title: str
    body: Optional[str] = None
    status: NotificationStatus
    is_read: bool
    reference_type: Optional[str] = None
    reference_id: Optional[int] = None
    sent_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class NotificationBulkRead(BaseModel):
    ids: List[int]


class EmailNotificationRequest(BaseModel):
    to_email: EmailStr
    subject: str
    body: str
    html_body: Optional[str] = None
    cc: Optional[List[EmailStr]] = None
    bcc: Optional[List[EmailStr]] = None
