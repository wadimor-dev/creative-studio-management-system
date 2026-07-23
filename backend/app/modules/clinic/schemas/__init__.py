from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
from pydantic import BaseModel, ConfigDict


# ──────────────────────────────────────────────
# Shared Enums (mirrors models for Pydantic)
# ──────────────────────────────────────────────
from app.modules.clinic.models.patient_profile import BloodType, Rhesus
from app.modules.clinic.models.healthcare_professional import Profession, ProfessionalStatus
from app.modules.clinic.models.queue import QueueStatus
from app.modules.clinic.models.visit import VisitStatus, VisitType
from app.modules.clinic.models.medical_record import MedicalRecordStatus
from app.modules.clinic.models.diagnosis import DiagnosisType
from app.modules.clinic.models.prescription import PrescriptionStatus
from app.modules.clinic.models.medical_certificate import CertificateType


# ══════════════════════════════════════════════
# PATIENT
# ══════════════════════════════════════════════

class PatientProfileBase(BaseModel):
    employee_id: int
    medical_record_number: str
    blood_type: Optional[BloodType] = None
    rhesus: Optional[Rhesus] = None
    allergy_note: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None

class PatientProfileCreate(PatientProfileBase):
    pass

class PatientProfileUpdate(BaseModel):
    blood_type: Optional[BloodType] = None
    rhesus: Optional[Rhesus] = None
    allergy_note: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None

class PatientProfileResponse(PatientProfileBase):
    id: str
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    employee_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# ══════════════════════════════════════════════
# HEALTHCARE PROFESSIONAL
# ══════════════════════════════════════════════

class HealthcareProfessionalBase(BaseModel):
    employee_id: int
    profession: Profession
    specialization: Optional[str] = None
    license_number: Optional[str] = None
    status: ProfessionalStatus = ProfessionalStatus.ACTIVE

class HealthcareProfessionalCreate(HealthcareProfessionalBase):
    pass

class HealthcareProfessionalUpdate(BaseModel):
    profession: Optional[Profession] = None
    specialization: Optional[str] = None
    license_number: Optional[str] = None
    status: Optional[ProfessionalStatus] = None

class HealthcareProfessionalResponse(HealthcareProfessionalBase):
    id: str
    employee_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# ══════════════════════════════════════════════
# ICD-10 CODE
# ══════════════════════════════════════════════

class ICD10CodeBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    is_active: bool = True

class ICD10CodeCreate(ICD10CodeBase):
    pass

class ICD10CodeUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class ICD10CodeResponse(ICD10CodeBase):
    id: str

    model_config = ConfigDict(from_attributes=True)


# ══════════════════════════════════════════════
# MEDICAL PROCEDURE
# ══════════════════════════════════════════════

class MedicalProcedureBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None

class MedicalProcedureCreate(MedicalProcedureBase):
    pass

class MedicalProcedureUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None

class MedicalProcedureResponse(MedicalProcedureBase):
    id: str

    model_config = ConfigDict(from_attributes=True)


# ══════════════════════════════════════════════
# QUEUE
# ══════════════════════════════════════════════

class QueueBase(BaseModel):
    queue_number: str
    queue_date: date
    status: QueueStatus = QueueStatus.WAITING

class QueueCreate(QueueBase):
    pass

class QueueUpdate(BaseModel):
    status: Optional[QueueStatus] = None
    called_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None

class QueueResponse(QueueBase):
    id: str
    called_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ══════════════════════════════════════════════
# VISIT
# ══════════════════════════════════════════════

class VisitBase(BaseModel):
    patient_profile_id: str
    queue_id: Optional[str] = None
    healthcare_professional_id: Optional[str] = None
    visit_type: VisitType = VisitType.REGULAR
    complaint: Optional[str] = None

class VisitCreate(VisitBase):
    pass

class VisitUpdate(BaseModel):
    healthcare_professional_id: Optional[str] = None
    visit_type: Optional[VisitType] = None
    complaint: Optional[str] = None
    visit_status: Optional[VisitStatus] = None

class VisitResponse(BaseModel):
    id: str
    patient_profile_id: str
    queue_id: Optional[str] = None
    healthcare_professional_id: Optional[str] = None
    visit_type: VisitType = VisitType.REGULAR
    complaint: Optional[str] = None
    visit_number: str
    visit_date: datetime
    visit_status: VisitStatus
    created_at: datetime
    updated_at: datetime
    patient_name: Optional[str] = None
    doctor_name: Optional[str] = None
    queue_number: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# ══════════════════════════════════════════════
# MEDICAL RECORD
# ══════════════════════════════════════════════

class MedicalRecordBase(BaseModel):
    visit_id: str
    record_number: str
    chief_complaint: Optional[str] = None
    present_illness: Optional[str] = None
    past_history: Optional[str] = None
    family_history: Optional[str] = None
    physical_exam: Optional[str] = None
    doctor_note: Optional[str] = None

class MedicalRecordCreate(MedicalRecordBase):
    pass

class MedicalRecordUpdate(BaseModel):
    chief_complaint: Optional[str] = None
    present_illness: Optional[str] = None
    past_history: Optional[str] = None
    family_history: Optional[str] = None
    physical_exam: Optional[str] = None
    doctor_note: Optional[str] = None
    status: Optional[MedicalRecordStatus] = None

class MedicalRecordResponse(MedicalRecordBase):
    id: str
    status: MedicalRecordStatus

    model_config = ConfigDict(from_attributes=True)


# ══════════════════════════════════════════════
# SOAP NOTE
# ══════════════════════════════════════════════

class SOAPNoteBase(BaseModel):
    visit_id: str
    subjective: Optional[str] = None
    objective: Optional[str] = None
    assessment: Optional[str] = None
    plan: Optional[str] = None

class SOAPNoteCreate(SOAPNoteBase):
    pass

class SOAPNoteUpdate(BaseModel):
    subjective: Optional[str] = None
    objective: Optional[str] = None
    assessment: Optional[str] = None
    plan: Optional[str] = None

class SOAPNoteResponse(SOAPNoteBase):
    id: str

    model_config = ConfigDict(from_attributes=True)


# ══════════════════════════════════════════════
# VITAL SIGN
# ══════════════════════════════════════════════

class VitalSignBase(BaseModel):
    visit_id: str
    systolic: Optional[int] = None
    diastolic: Optional[int] = None
    pulse: Optional[int] = None
    respiration: Optional[int] = None
    temperature: Optional[Decimal] = None
    spo2: Optional[Decimal] = None
    height: Optional[Decimal] = None
    weight: Optional[Decimal] = None

class VitalSignCreate(VitalSignBase):
    pass

class VitalSignUpdate(BaseModel):
    systolic: Optional[int] = None
    diastolic: Optional[int] = None
    pulse: Optional[int] = None
    respiration: Optional[int] = None
    temperature: Optional[Decimal] = None
    spo2: Optional[Decimal] = None
    height: Optional[Decimal] = None
    weight: Optional[Decimal] = None

class VitalSignResponse(VitalSignBase):
    id: str
    bmi: Optional[Decimal] = None

    model_config = ConfigDict(from_attributes=True)


# ══════════════════════════════════════════════
# DIAGNOSIS
# ══════════════════════════════════════════════

class DiagnosisBase(BaseModel):
    visit_id: str
    icd10_id: str
    diagnosis_type: DiagnosisType
    diagnosis_note: Optional[str] = None

class DiagnosisCreate(DiagnosisBase):
    pass

class DiagnosisUpdate(BaseModel):
    diagnosis_type: Optional[DiagnosisType] = None
    diagnosis_note: Optional[str] = None

class DiagnosisResponse(DiagnosisBase):
    id: str
    icd10_code: Optional[str] = None
    icd10_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# ══════════════════════════════════════════════
# VISIT PROCEDURE
# ══════════════════════════════════════════════

class VisitProcedureBase(BaseModel):
    visit_id: str
    procedure_id: str
    notes: Optional[str] = None

class VisitProcedureCreate(VisitProcedureBase):
    pass

class VisitProcedureUpdate(BaseModel):
    notes: Optional[str] = None

class VisitProcedureResponse(VisitProcedureBase):
    id: str
    procedure_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# ══════════════════════════════════════════════
# MEDICAL ATTACHMENT
# ══════════════════════════════════════════════

class MedicalAttachmentBase(BaseModel):
    visit_id: str
    file_name: str
    file_path: str
    mime_type: Optional[str] = None

class MedicalAttachmentCreate(MedicalAttachmentBase):
    pass

class MedicalAttachmentUpdate(BaseModel):
    file_name: Optional[str] = None
    mime_type: Optional[str] = None

class MedicalAttachmentResponse(MedicalAttachmentBase):
    id: str
    uploaded_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


# ══════════════════════════════════════════════
# PRESCRIPTION ITEM
# ══════════════════════════════════════════════

class PrescriptionItemBase(BaseModel):
    prescription_id: str
    medicine_id: int
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    duration: Optional[str] = None
    quantity: int
    instruction: Optional[str] = None

class PrescriptionItemCreate(PrescriptionItemBase):
    pass

class PrescriptionItemUpdate(BaseModel):
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    duration: Optional[str] = None
    quantity: Optional[int] = None
    instruction: Optional[str] = None

class PrescriptionItemResponse(PrescriptionItemBase):
    id: str
    medicine_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# ══════════════════════════════════════════════
# PRESCRIPTION
# ══════════════════════════════════════════════

class PrescriptionBase(BaseModel):
    visit_id: str
    healthcare_professional_id: Optional[str] = None

class PrescriptionCreate(PrescriptionBase):
    pass

class PrescriptionUpdate(BaseModel):
    status: Optional[PrescriptionStatus] = None

class PrescriptionResponse(PrescriptionBase):
    id: str
    prescription_date: datetime
    status: PrescriptionStatus
    doctor_name: Optional[str] = None
    items: List[PrescriptionItemResponse] = []

    model_config = ConfigDict(from_attributes=True)


# ══════════════════════════════════════════════
# MEDICINE DISPENSE
# ══════════════════════════════════════════════

class MedicineDispenseBase(BaseModel):
    prescription_item_id: str
    quantity: int

class MedicineDispenseCreate(MedicineDispenseBase):
    pass

class MedicineDispenseResponse(MedicineDispenseBase):
    id: str
    dispensed_by: Optional[int] = None
    dispensed_at: datetime
    dispenser_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# ══════════════════════════════════════════════
# MEDICAL CERTIFICATE
# ══════════════════════════════════════════════

class MedicalCertificateBase(BaseModel):
    visit_id: str
    certificate_type: CertificateType
    start_date: date
    end_date: Optional[date] = None
    diagnosis_summary: Optional[str] = None
    recommendation: Optional[str] = None

class MedicalCertificateCreate(MedicalCertificateBase):
    pass

class MedicalCertificateUpdate(BaseModel):
    certificate_type: Optional[CertificateType] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    diagnosis_summary: Optional[str] = None
    recommendation: Optional[str] = None

class MedicalCertificateResponse(MedicalCertificateBase):
    id: str
    issued_by: Optional[int] = None
    issuer_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# ══════════════════════════════════════════════
# CLINIC ACTIVITY LOG
# ══════════════════════════════════════════════

class ClinicActivityLogBase(BaseModel):
    user_id: Optional[int] = None
    module: str
    action: str
    table_name: Optional[str] = None
    record_id: Optional[str] = None

class ClinicActivityLogCreate(ClinicActivityLogBase):
    old_value: Optional[dict] = None
    new_value: Optional[dict] = None
    ip_address: Optional[str] = None
    device: Optional[str] = None

class ClinicActivityLogResponse(ClinicActivityLogBase):
    id: str
    old_value: Optional[dict] = None
    new_value: Optional[dict] = None
    ip_address: Optional[str] = None
    device: Optional[str] = None
    created_at: datetime
    username: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# ══════════════════════════════════════════════
# Combined Request/Response for Visit Detail
# ══════════════════════════════════════════════

class VisitDetailResponse(VisitResponse):
    medical_record: Optional[MedicalRecordResponse] = None
    soap_note: Optional[SOAPNoteResponse] = None
    vital_sign: Optional[VitalSignResponse] = None
    diagnoses: List[DiagnosisResponse] = []
    procedures: List[VisitProcedureResponse] = []
    prescription: Optional[PrescriptionResponse] = None
    certificates: List[MedicalCertificateResponse] = []
    attachments: List[MedicalAttachmentResponse] = []

    model_config = ConfigDict(from_attributes=True)


__all__ = [
    "BloodType", "Rhesus", "Profession", "ProfessionalStatus",
    "QueueStatus", "VisitStatus", "VisitType", "MedicalRecordStatus",
    "DiagnosisType", "PrescriptionStatus", "CertificateType",
    "PatientProfileCreate", "PatientProfileUpdate", "PatientProfileResponse",
    "HealthcareProfessionalCreate", "HealthcareProfessionalUpdate", "HealthcareProfessionalResponse",
    "ICD10CodeCreate", "ICD10CodeUpdate", "ICD10CodeResponse",
    "MedicalProcedureCreate", "MedicalProcedureUpdate", "MedicalProcedureResponse",
    "QueueCreate", "QueueUpdate", "QueueResponse",
    "VisitCreate", "VisitUpdate", "VisitResponse",
    "MedicalRecordCreate", "MedicalRecordUpdate", "MedicalRecordResponse",
    "SOAPNoteCreate", "SOAPNoteUpdate", "SOAPNoteResponse",
    "VitalSignCreate", "VitalSignUpdate", "VitalSignResponse",
    "DiagnosisCreate", "DiagnosisUpdate", "DiagnosisResponse",
    "VisitProcedureCreate", "VisitProcedureUpdate", "VisitProcedureResponse",
    "MedicalAttachmentCreate", "MedicalAttachmentUpdate", "MedicalAttachmentResponse",
    "PrescriptionCreate", "PrescriptionUpdate", "PrescriptionResponse",
    "PrescriptionItemCreate", "PrescriptionItemUpdate", "PrescriptionItemResponse",
    "MedicineDispenseCreate", "MedicineDispenseResponse",
    "MedicalCertificateCreate", "MedicalCertificateUpdate", "MedicalCertificateResponse",
    "ClinicActivityLogCreate", "ClinicActivityLogResponse",
    "VisitDetailResponse",
]
