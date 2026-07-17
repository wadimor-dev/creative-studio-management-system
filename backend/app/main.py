from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from app.core.config import settings
from app.core.lifespan import lifespan
from app.config.cors import setup_cors
from app.config.logging import setup_logging
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.logging import LoggingMiddleware
from app.exceptions.base import CSMSException
from fastapi.exceptions import RequestValidationError
from app.exceptions.validation import custom_exception_handler, validation_exception_handler
from app.api.health import router as health_router
from app.api.users import router as users_router
from app.api.auth import router as auth_router
from app.api.inventory import router as inventory_router
from app.api.dashboard import router as dashboard_router
from app.api.reports import router as reports_router
from app.api.export import router as export_router
from app.api.categories import router as categories_router
from app.api.product_master import router as product_master_router
from app.api.products import router as products_router
from app.api.product_movements import router as product_movements_router
from app.api.product_stocks import router as product_stocks_router
from app.api.locations import router as locations_router
from app.api.work_activities import router as work_activities_router

# Setup logging
setup_logging()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Middlewares (order matters: last added = first executed = outermost)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestIDMiddleware)

# Setup CORS (must be last/outermost middleware)
setup_cors(app)

# Exception Handlers
app.add_exception_handler(CSMSException, custom_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Routers
app.include_router(health_router, prefix=settings.API_V1_STR)
app.include_router(auth_router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(users_router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(inventory_router, prefix=f"{settings.API_V1_STR}/inventory", tags=["inventory"])
app.include_router(dashboard_router, prefix=f"{settings.API_V1_STR}/dashboard", tags=["dashboard"])
app.include_router(reports_router, prefix=f"{settings.API_V1_STR}/reports", tags=["reports"])
app.include_router(export_router, prefix=f"{settings.API_V1_STR}/export", tags=["export"])
app.include_router(categories_router, prefix=f"{settings.API_V1_STR}/categories", tags=["categories"])
app.include_router(product_master_router, prefix=f"{settings.API_V1_STR}/product-master", tags=["product-master"])
app.include_router(products_router, prefix=f"{settings.API_V1_STR}/products", tags=["products"])
app.include_router(product_movements_router, prefix=f"{settings.API_V1_STR}/product-movements", tags=["product-movements"])
app.include_router(product_stocks_router, prefix=f"{settings.API_V1_STR}/product-stocks", tags=["product-stocks"])
app.include_router(locations_router, prefix=f"{settings.API_V1_STR}/locations", tags=["locations"])
app.include_router(work_activities_router, prefix=f"{settings.API_V1_STR}/work-activities", tags=["work-activities"])

from app.api.product_placements import router as product_placements_router
from app.api.product_scanner import router as product_scanner_router
from app.api.product_opname import router as product_opname_router

app.include_router(product_placements_router, prefix=f"{settings.API_V1_STR}/product-placements", tags=["product-placements"])
app.include_router(product_scanner_router, prefix=f"{settings.API_V1_STR}/product-scanner", tags=["product-scanner"])
app.include_router(product_opname_router, prefix=f"{settings.API_V1_STR}/product-opname", tags=["product-opname"])

from app.api.logs import router as logs_router
app.include_router(logs_router, prefix=f"{settings.API_V1_STR}/logs", tags=["logs"])

from app.api.system import router as system_router
app.include_router(system_router, prefix=f"{settings.API_V1_STR}/system", tags=["system"])

from app.api.showroom import router as showroom_router
app.include_router(showroom_router, prefix=f"{settings.API_V1_STR}/showroom", tags=["showroom"])

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.APP_NAME}"}
