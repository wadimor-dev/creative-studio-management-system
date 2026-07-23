from app.modules.clinic.routes.master_data import router as master_data_router
from app.modules.clinic.routes.registration import router as registration_router
from app.modules.clinic.routes.medical import router as medical_router
from app.modules.clinic.routes.pharmacy import router as pharmacy_router
from app.modules.clinic.routes.certificates import router as certificates_router
from app.modules.clinic.routes.audit import router as audit_router

__all__ = ["master_data_router", "registration_router", "medical_router", "pharmacy_router", "certificates_router", "audit_router"]
