"""Compatibility re-exports — prefer app.modules.showroom.schemas."""

from app.modules.showroom.schemas import (  # noqa: F401
    ShowroomDashboardStats,
    ShowroomMovementSummary,
    ShowroomStockStats,
    ShowroomStockMovement,
    TransferItem,
    TransferCreate,
    TransferUpdate,
    TransferResponse,
    TransferStats,
    StockInCreate,
    StockInUpdate,
    StockInResponse,
    StockInStats,
    StockOutCreate,
    StockOutUpdate,
    StockOutResponse,
    StockOutStats,
    ShowroomLocation,
)
