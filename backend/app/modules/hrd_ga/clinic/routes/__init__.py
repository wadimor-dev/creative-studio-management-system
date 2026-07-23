from app.modules.hrd_ga.clinic.routes.master_data import router as master_data_router
from app.modules.hrd_ga.clinic.routes.registration import router as registration_router
from app.modules.hrd_ga.clinic.routes.medical import router as medical_router
from app.modules.hrd_ga.clinic.routes.pharmacy import router as pharmacy_router
from app.modules.hrd_ga.clinic.routes.certificates import router as certificates_router
from app.modules.hrd_ga.clinic.routes.audit import router as audit_router

__all__ = ["master_data_router", "registration_router", "medical_router", "pharmacy_router", "certificates_router", "audit_router"]
