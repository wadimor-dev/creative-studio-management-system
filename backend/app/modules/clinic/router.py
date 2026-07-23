from fastapi import APIRouter
from app.modules.clinic.routes import (
    master_data_router, registration_router, medical_router,
    pharmacy_router, certificates_router, audit_router,
)

router = APIRouter()

router.include_router(master_data_router, prefix="/master-data")
router.include_router(registration_router, prefix="/registration")
router.include_router(medical_router, prefix="/medical")
router.include_router(pharmacy_router, prefix="/pharmacy")
router.include_router(certificates_router, prefix="/certificates")
router.include_router(audit_router, prefix="/audit")
