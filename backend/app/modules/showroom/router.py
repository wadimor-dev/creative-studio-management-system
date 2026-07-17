"""Showroom API router — aggregates domain sub-routers."""

from fastapi import APIRouter

from app.modules.showroom.routes import (
    dashboard_router,
    stock_router,
    transfers_router,
    stock_in_router,
    stock_out_router,
    locations_router,
)

router = APIRouter()

router.include_router(dashboard_router)
router.include_router(stock_router)
router.include_router(transfers_router)
router.include_router(stock_in_router)
router.include_router(stock_out_router)
router.include_router(locations_router)
