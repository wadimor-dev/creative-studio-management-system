from app.modules.clinic.services.patient_profile_service import PatientProfileService
from app.modules.clinic.services.healthcare_professional_service import HealthcareProfessionalService
from app.modules.clinic.services.icd10_code_service import ICD10CodeService
from app.modules.clinic.services.medical_procedure_service import MedicalProcedureService
from app.modules.clinic.services.queue_service import QueueService
from app.modules.clinic.services.visit_service import VisitService
from app.modules.clinic.services.medical_record_service import MedicalRecordService
from app.modules.clinic.services.soap_note_service import SOAPNoteService
from app.modules.clinic.services.vital_sign_service import VitalSignService
from app.modules.clinic.services.diagnosis_service import DiagnosisService
from app.modules.clinic.services.visit_procedure_service import VisitProcedureService
from app.modules.clinic.services.medical_attachment_service import MedicalAttachmentService
from app.modules.clinic.services.prescription_service import PrescriptionService
from app.modules.clinic.services.prescription_item_service import PrescriptionItemService
from app.modules.clinic.services.medicine_dispense_service import MedicineDispenseService
from app.modules.clinic.services.medical_certificate_service import MedicalCertificateService
from app.modules.clinic.services.clinic_activity_log_service import ClinicActivityLogService

patient_profile_service = PatientProfileService()
healthcare_professional_service = HealthcareProfessionalService()
icd10_code_service = ICD10CodeService()
medical_procedure_service = MedicalProcedureService()
queue_service = QueueService()
visit_service = VisitService()
medical_record_service = MedicalRecordService()
soap_note_service = SOAPNoteService()
vital_sign_service = VitalSignService()
diagnosis_service = DiagnosisService()
visit_procedure_service = VisitProcedureService()
medical_attachment_service = MedicalAttachmentService()
prescription_service = PrescriptionService()
prescription_item_service = PrescriptionItemService()
medicine_dispense_service = MedicineDispenseService()
medical_certificate_service = MedicalCertificateService()
clinic_activity_log_service = ClinicActivityLogService()

__all__ = [
    "patient_profile_service",
    "healthcare_professional_service",
    "icd10_code_service",
    "medical_procedure_service",
    "queue_service",
    "visit_service",
    "medical_record_service",
    "soap_note_service",
    "vital_sign_service",
    "diagnosis_service",
    "visit_procedure_service",
    "medical_attachment_service",
    "prescription_service",
    "prescription_item_service",
    "medicine_dispense_service",
    "medical_certificate_service",
    "clinic_activity_log_service",
]
