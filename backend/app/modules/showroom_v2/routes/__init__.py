from fastapi import APIRouter
from app.modules.showroom_v2.routes import dashboard, dashboard_v2, sample, borrowing, guest, stock_control, reporting, master_data, public, storage, qr_scan

router = APIRouter()

router.include_router(dashboard_v2.router, prefix="/dashboard", tags=["Showroom Dashboard V2"])
router.include_router(dashboard.router, prefix="/dashboard/legacy", tags=["Showroom Dashboard Legacy"])
router.include_router(sample.router, prefix="/samples", tags=["Showroom Samples"])
router.include_router(borrowing.router, prefix="/borrowings", tags=["Showroom Borrowings"])
router.include_router(guest.router, prefix="/guests", tags=["Showroom Guests"])
router.include_router(stock_control.router, prefix="/stock-control", tags=["Showroom Stock Control"])
router.include_router(reporting.router, prefix="/reports", tags=["Showroom Reports"])
router.include_router(master_data.router, prefix="/master-data", tags=["Showroom Master Data"])
router.include_router(public.router, prefix="/public", tags=["Showroom Public"])
router.include_router(storage.router, prefix="/storage", tags=["Showroom Storage"])
router.include_router(qr_scan.router, prefix="/qr", tags=["Showroom QR Scan"])
