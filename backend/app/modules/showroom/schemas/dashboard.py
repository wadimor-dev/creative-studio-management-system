from pydantic import BaseModel


class ShowroomDashboardStats(BaseModel):
    totalStock: str
    stockInToday: str
    stockOutToday: str
    pendingTransfer: str
    stockInCount: str
    stockOutCount: str
    inTransit: str


class ShowroomMovementSummary(BaseModel):
    id: str
    product: str
    type: str
    quantity: int
    location: str
    status: str
