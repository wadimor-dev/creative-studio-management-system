from fastapi import APIRouter
from app.modules.hrd_ga.creative.showroom.routes import router as routes_router

router = APIRouter()

router.include_router(routes_router)
