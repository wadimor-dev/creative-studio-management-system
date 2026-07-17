from app.modules.showroom.routes.dashboard import router as dashboard_router
from app.modules.showroom.routes.stock import router as stock_router
from app.modules.showroom.routes.transfers import router as transfers_router
from app.modules.showroom.routes.stock_in import router as stock_in_router
from app.modules.showroom.routes.stock_out import router as stock_out_router
from app.modules.showroom.routes.locations import router as locations_router

__all__ = [
    "dashboard_router",
    "stock_router",
    "transfers_router",
    "stock_in_router",
    "stock_out_router",
    "locations_router",
]
