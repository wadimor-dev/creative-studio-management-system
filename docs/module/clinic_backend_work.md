# Clinic Backend Module — Architecture & Documentation

## Overview

The clinic module is a FastAPI sub-application (APIRouter) mounted at `/api/v1/clinic`. It manages the full clinical workflow:

1. **Master Data** — patient profiles, healthcare professionals, ICD-10 diagnosis codes, medical procedures
2. **Registration** — queue management, visit lifecycle (checkin → serving → finish/cancel)
3. **Medical** — medical records, SOAP notes, vital signs, diagnoses, visit procedures, attachments
4. **Pharmacy** — prescriptions, prescription items, medicine dispenses
5. **Certificates** — medical certificates (health, sick, fit-to-work)
6. **Audit** — activity logs

### Routing Hierarchy

```
main.py::app
└── /api/v1/clinic  (APIRouter, tag="clinic")
    ├── /master-data        ── master_data.py    (patients, HPs, ICD10, procedures)
    ├── /registration       ── registration.py   (queues, visits)
    ├── /medical            ── medical.py        (medical records, SOAP, vitals, diagnoses, procedures, attachments)
    ├── /pharmacy           ── pharmacy.py       (prescriptions, items, dispenses)
    ├── /certificates       ── certificates.py   (medical certificates)
    └── /audit              ── audit.py          (activity logs)
```

**Import chain:** `main.py → app/api/clinic.py → modules/clinic/router.py → routes/__init__.py → routes/{master_data,registration,...}.py` and `services/{...}.py`.

### Key Dependencies

| Dependency | Source | Used In |
|---|---|---|
| `db: Session = Depends(get_db)` | `core/database/session.py` | Every route |
| `current_user: User = Depends(get_current_user)` | `dependencies/auth.py` | All POST/PUT/DELETE (not GET) |

---

## Directory Inventory

The clinic module now lives at `backend/app/modules/hrd_ga/clinic/`. All paths below are relative to that directory unless noted.

**Sub-module placeholders** (empty, for future use): `patient/`, `medical_record/`, `examination/`, `medicine/`, `pharmacy/`, `doctor/`, `laboratory/`, `referral/`, `reports/`.

### Core Entry Points

| File | Role |
|---|---|
| `__init__.py` | Re-exports `router` from `router.py` |
| `router.py` | Aggregates the 6 sub-routers under prefixes |
| `app/api/clinic.py` | Thin shim so `main.py` imports like other routers |

### Models (`models/`) — 17 files + `__init__.py`

| File | Class(es) | Table | Key Columns |
|---|---|---|---|
| `patient_profile.py` | `PatientProfile` | `patient_profiles` | `employee_id` (FK→employees, unique), `medical_record_number` (unique), `blood_type`, `rhesus`, `allergy_note`, `emergency_contact_name/phone` |
| `healthcare_professional.py` | `HealthcareProfessional` | `healthcare_professionals` | `employee_id` (FK→employees, unique), `profession` (enum), `specialization`, `license_number`, `status` (enum) |
| `icd10_code.py` | `ICD10Code` | `icd10_codes` | `code` (unique), `name`, `description`, `is_active` |
| `medical_procedure.py` | `MedicalProcedure` | `medical_procedures` | `code` (unique), `name`, `description` |
| `queue.py` | `Queue` | `queues` | `queue_number`, `queue_date`, `status` (enum), `called_at`, `finished_at` |
| `visit.py` | `Visit` | `visits` | `visit_number` (unique), `patient_profile_id` (FK), `queue_id` (FK, unique), `healthcare_professional_id` (FK), `visit_type` (enum), `visit_date`, `complaint`, `visit_status` (enum) |
| `medical_record.py` | `MedicalRecord` | `medical_records` | `visit_id` (FK, unique), `record_number` (unique), `chief_complaint`, `present_illness`, `past_history`, `family_history`, `physical_exam`, `doctor_note`, `status` (enum) |
| `soap_note.py` | `SOAPNote` | `soap_notes` | `visit_id` (FK, unique), `subjective`, `objective`, `assessment`, `plan` |
| `vital_sign.py` | `VitalSign` | `vital_signs` | `visit_id` (FK, unique), `systolic`, `diastolic`, `pulse`, `respiration`, `temperature`, `spo2`, `height`, `weight`, `bmi` |
| `diagnosis.py` | `Diagnosis` | `diagnoses` | `visit_id` (FK), `icd10_id` (FK), `diagnosis_type` (enum), `diagnosis_note` |
| `visit_procedure.py` | `VisitProcedure` | `visit_procedures` | `visit_id` (FK), `procedure_id` (FK), `notes` |
| `medical_attachment.py` | `MedicalAttachment` | `medical_attachments` | `visit_id` (FK), `file_name`, `file_path`, `mime_type`, `uploaded_by` (FK→users) |
| `prescription.py` | `Prescription` | `prescriptions` | `visit_id` (FK, unique), `healthcare_professional_id` (FK), `prescription_date`, `status` (enum) |
| `prescription_item.py` | `PrescriptionItem` | `prescription_items` | `prescription_id` (FK), `medicine_id` (FK→items), `dosage`, `frequency`, `duration`, `quantity`, `instruction` |
| `medicine_dispense.py` | `MedicineDispense` | `medicine_dispenses` | `prescription_item_id` (FK, unique), `dispensed_by` (FK→users), `quantity`, `dispensed_at` |
| `medical_certificate.py` | `MedicalCertificate` | `medical_certificates` | `visit_id` (FK), `certificate_type` (enum), `start_date`, `end_date`, `diagnosis_summary`, `recommendation`, `issued_by` (FK→users) |
| `clinic_activity_log.py` | `ClinicActivityLog` | `clinic_activity_logs` | `user_id` (FK→users), `module`, `action`, `table_name`, `record_id`, `old_value` (JSON), `new_value` (JSON), `ip_address`, `device` |

**Common patterns across all models:**
- PK: `id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))`
- Timestamps: `created_at` / `updated_at` (DateTime, default utcnow, onupdate)
- Enums use Python `enum.Enum` subclasses stored as SAEnum
- Relationships use `back_populates` with `lazy="selectin"`
- User tracking via `created_by` / `updated_by` (FK→users.id)

### Enums (defined alongside models)

| Enum | Values | Used In |
|---|---|---|
| `BloodType` | `A, B, AB, O` | `patient_profiles` |
| `Rhesus` | `POSITIVE, NEGATIVE` | `patient_profiles` |
| `Profession` | `DOCTOR, NURSE, MIDWIFE, LAB_TECHNICIAN, PHARMACIST, DENTIST, OTHER` | `healthcare_professionals` |
| `ProfessionalStatus` | `ACTIVE, INACTIVE, SUSPENDED` | `healthcare_professionals` |
| `QueueStatus` | `WAITING, CALLING, SERVING, FINISHED, CANCELLED` | `queues` |
| `VisitStatus` | `CHECKIN, SERVING, FINISHED, CANCELLED` | `visits` |
| `VisitType` | `REGULAR, EMERGENCY, FOLLOW_UP` | `visits` |
| `MedicalRecordStatus` | `DRAFT, FINAL` | `medical_records` |
| `DiagnosisType` | `PRIMARY, SECONDARY` | `diagnoses` |
| `PrescriptionStatus` | `ACTIVE, DISPENSED, CANCELLED` | `prescriptions` |
| `CertificateType` | `HEALTH, SICK, FIT_TO_WORK` | `medical_certificates` |

### Schemas (`schemas/__init__.py` — single file, ~530 lines)

All Pydantic v2 schemas follow the `Base` / `Create` / `Update` / `Response` pattern with `model_config = ConfigDict(from_attributes=True)`.

**Composite schema:**
- `VisitDetailResponse` — extends `VisitResponse` with nested: `medical_record`, `soap_note`, `vital_sign`, `diagnoses[]`, `procedures[]`, `prescription` (with `items[]`), `certificates[]`, `attachments[]`

### Services (`services/`) — 17 files + `__init__.py`

Each service is a plain class instantiated as a module-level singleton in `services/__init__.py`:

| Service | Key Methods | Notes |
|---|---|---|
| `PatientProfileService` | CRUD + `get_by_employee_id`, `get_by_medical_record_number` | Employee name joined via employee relationship |
| `HealthcareProfessionalService` | CRUD + `get_by_employee_id` | Filters by profession, status |
| `ICD10CodeService` | CRUD + `get_by_code`, `bulk_create` | Search by code/name, active-only filter |
| `MedicalProcedureService` | CRUD + `bulk_create` | Search by code/name |
| `QueueService` | CRUD + `get_current_queue`, `get_waiting_count`, `update_status` | Queue number formatting (alpha prefix + 3-digit numeric) |
| `VisitService` | CRUD + `get_detail`, `get_by_patient_profile`, `checkin`, `start_serving`, `finish`, `cancel` | Status methods sync queue status + timestamps |
| `MedicalRecordService` | CRUD + `get_by_visit_id`, `finalize` | `finalize` sets status to FINAL |
| `SOAPNoteService` | CRUD + `get_by_visit_id`, `upsert` | Upsert creates or updates by visit_id |
| `VitalSignService` | CRUD + `get_by_visit_id`, `upsert` | BMI auto-calculated from height/weight |
| `DiagnosisService` | CRUD + `get_by_visit` | Links to ICD-10 code |
| `VisitProcedureService` | CRUD + `get_by_visit` | Links to medical procedure |
| `MedicalAttachmentService` | CRUD + `get_by_visit` | File metadata only (files stored externally) |
| `PrescriptionService` | CRUD + `get_by_visit_id`, `dispense`, `cancel` | Dispense sets status + triggers dispense records |
| `PrescriptionItemService` | CRUD + `get_by_prescription` | Links to items inventory table |
| `MedicineDispenseService` | CRUD + `get_by_prescription_item` | One-to-one with prescription_item |
| `MedicalCertificateService` | CRUD + `get_by_visit` | Certificate types for different purposes |
| `ClinicActivityLogService` | `get_all`, `log` | Stores JSON diff, IP, device info |

**Error handling pattern:** Services raise `CSMSException(message, status_code)` from `app.core.exceptions`.

### Routes (`routes/`) — 6 files + `__init__.py`

#### `master_data.py` — Prefix `/master-data`

| Method | Path | Function | Tag |
|---|---|---|---|
| GET | `/patients` | `list_patients` | clinic-patients |
| GET | `/patients/{patient_id}` | `get_patient` | clinic-patients |
| GET | `/patients/by-employee/{employee_id}` | `get_patient_by_employee` | clinic-patients |
| GET | `/patients/by-mr/{mr_number}` | `get_patient_by_mr` | clinic-patients |
| POST | `/patients` | `create_patient` | clinic-patients |
| PUT | `/patients/{patient_id}` | `update_patient` | clinic-patients |
| DELETE | `/patients/{patient_id}` | `delete_patient` | clinic-patients |
| GET | `/healthcare-professionals` | `list_hp` | clinic-hp |
| GET | `/healthcare-professionals/{hp_id}` | `get_hp` | clinic-hp |
| POST | `/healthcare-professionals` | `create_hp` | clinic-hp |
| PUT | `/healthcare-professionals/{hp_id}` | `update_hp` | clinic-hp |
| DELETE | `/healthcare-professionals/{hp_id}` | `delete_hp` | clinic-hp |
| GET | `/icd10-codes` | `list_icd10` | clinic-icd10 |
| GET | `/icd10-codes/{code_id}` | `get_icd10` | clinic-icd10 |
| POST | `/icd10-codes` | `create_icd10` | clinic-icd10 |
| PUT | `/icd10-codes/{code_id}` | `update_icd10` | clinic-icd10 |
| DELETE | `/icd10-codes/{code_id}` | `delete_icd10` | clinic-icd10 |
| GET | `/medical-procedures` | `list_procedures` | clinic-procedures |
| GET | `/medical-procedures/{proc_id}` | `get_procedure` | clinic-procedures |
| POST | `/medical-procedures` | `create_procedure` | clinic-procedures |
| PUT | `/medical-procedures/{proc_id}` | `update_procedure` | clinic-procedures |
| DELETE | `/medical-procedures/{proc_id}` | `delete_procedure` | clinic-procedures |

#### `registration.py` — Prefix `/registration`

| Method | Path | Function | Tag |
|---|---|---|---|
| GET | `/queues` | `list_queues` | clinic-queues |
| GET | `/queues/current` | `get_current_queue` | clinic-queues |
| GET | `/queues/waiting-count` | `get_waiting_count` | clinic-queues |
| GET | `/queues/{queue_id}` | `get_queue` | clinic-queues |
| POST | `/queues` | `create_queue` | clinic-queues |
| PUT | `/queues/{queue_id}/status` | `update_queue_status` | clinic-queues |
| GET | `/visits` | `list_visits` | clinic-visits |
| GET | `/visits/{visit_id}` | `get_visit` | clinic-visits |
| GET | `/visits/{visit_id}/detail` | `get_visit_detail` | clinic-visits |
| POST | `/visits` | `create_visit` | clinic-visits |
| PUT | `/visits/{visit_id}` | `update_visit` | clinic-visits |
| PUT | `/visits/{visit_id}/checkin` | `checkin_visit` | clinic-visits |
| PUT | `/visits/{visit_id}/start-serving` | `start_serving` | clinic-visits |
| PUT | `/visits/{visit_id}/finish` | `finish_visit` | clinic-visits |
| PUT | `/visits/{visit_id}/cancel` | `cancel_visit` | clinic-visits |

#### `medical.py` — Prefix `/medical`

| Method | Path | Function | Tag |
|---|---|---|---|
| GET | `/medical-records` | `list_medical_records` | clinic-medical-records |
| GET | `/medical-records/{record_id}` | `get_medical_record` | clinic-medical-records |
| GET | `/medical-records/by-visit/{visit_id}` | `get_medical_record_by_visit` | clinic-medical-records |
| POST | `/medical-records` | `create_medical_record` | clinic-medical-records |
| PUT | `/medical-records/{record_id}` | `update_medical_record` | clinic-medical-records |
| PUT | `/medical-records/{record_id}/finalize` | `finalize_medical_record` | clinic-medical-records |
| GET | `/soap-notes/{note_id}` | `get_soap_note` | clinic-soap |
| GET | `/soap-notes/by-visit/{visit_id}` | `get_soap_by_visit` | clinic-soap |
| POST | `/soap-notes` | `create_soap_note` | clinic-soap |
| PUT | `/soap-notes/{note_id}` | `update_soap_note` | clinic-soap |
| PUT | `/soap-notes/by-visit/{visit_id}` | `upsert_soap_note` | clinic-soap |
| GET | `/vital-signs/{vs_id}` | `get_vital_sign` | clinic-vitals |
| GET | `/vital-signs/by-visit/{visit_id}` | `get_vitals_by_visit` | clinic-vitals |
| POST | `/vital-signs` | `create_vital_sign` | clinic-vitals |
| PUT | `/vital-signs/{vs_id}` | `update_vital_sign` | clinic-vitals |
| PUT | `/vital-signs/by-visit/{visit_id}` | `upsert_vital_sign` | clinic-vitals |
| GET | `/diagnoses/by-visit/{visit_id}` | `get_diagnoses_by_visit` | clinic-diagnoses |
| POST | `/diagnoses` | `create_diagnosis` | clinic-diagnoses |
| PUT | `/diagnoses/{diagnosis_id}` | `update_diagnosis` | clinic-diagnoses |
| DELETE | `/diagnoses/{diagnosis_id}` | `delete_diagnosis` | clinic-diagnoses |
| GET | `/visit-procedures/by-visit/{visit_id}` | `get_procedures_by_visit` | clinic-visit-procedures |
| POST | `/visit-procedures` | `create_visit_procedure` | clinic-visit-procedures |
| PUT | `/visit-procedures/{vp_id}` | `update_visit_procedure` | clinic-visit-procedures |
| DELETE | `/visit-procedures/{vp_id}` | `delete_visit_procedure` | clinic-visit-procedures |
| GET | `/medical-attachments/by-visit/{visit_id}` | `get_attachments_by_visit` | clinic-attachments |
| POST | `/medical-attachments` | `create_attachment` | clinic-attachments |
| PUT | `/medical-attachments/{att_id}` | `update_attachment` | clinic-attachments |
| DELETE | `/medical-attachments/{att_id}` | `delete_attachment` | clinic-attachments |

#### `pharmacy.py` — Prefix `/pharmacy`

| Method | Path | Function | Tag |
|---|---|---|---|
| GET | `/prescriptions/{rx_id}` | `get_prescription` | clinic-prescriptions |
| GET | `/prescriptions/by-visit/{visit_id}` | `get_prescription_by_visit` | clinic-prescriptions |
| POST | `/prescriptions` | `create_prescription` | clinic-prescriptions |
| PUT | `/prescriptions/{rx_id}` | `update_prescription` | clinic-prescriptions |
| PUT | `/prescriptions/{rx_id}/dispense` | `dispense_prescription` | clinic-prescriptions |
| PUT | `/prescriptions/{rx_id}/cancel` | `cancel_prescription` | clinic-prescriptions |
| GET | `/prescription-items/by-prescription/{rx_id}` | `get_items_by_prescription` | clinic-prescription-items |
| POST | `/prescription-items` | `create_prescription_item` | clinic-prescription-items |
| PUT | `/prescription-items/{item_id}` | `update_prescription_item` | clinic-prescription-items |
| DELETE | `/prescription-items/{item_id}` | `delete_prescription_item` | clinic-prescription-items |
| GET | `/medicine-dispenses/{dispense_id}` | `get_dispense` | clinic-dispenses |
| POST | `/medicine-dispenses` | `create_dispense` | clinic-dispenses |

#### `certificates.py` — Prefix `/certificates`

| Method | Path | Function | Tag |
|---|---|---|---|
| GET | `/medical-certificates/{cert_id}` | `get_certificate` | clinic-certificates |
| GET | `/medical-certificates/by-visit/{visit_id}` | `get_certificates_by_visit` | clinic-certificates |
| POST | `/medical-certificates` | `create_certificate` | clinic-certificates |
| PUT | `/medical-certificates/{cert_id}` | `update_certificate` | clinic-certificates |
| DELETE | `/medical-certificates/{cert_id}` | `delete_certificate` | clinic-certificates |

#### `audit.py` — Prefix `/audit`

| Method | Path | Function | Tag |
|---|---|---|---|
| GET | `/activity-logs` | `list_activity_logs` | clinic-audit |
| POST | `/activity-logs` | `create_activity_log` | clinic-audit |

---

## Data Flow / Request Lifecycle

```
Client (HTTP)
  │
  ▼
main.py → FastAPI app (ASGI)
  │
  ├── CORS middleware (core/security/cors.py)
  ├── Request ID middleware
  ├── Logging middleware
  │
  ▼
router: /api/v1/clinic/{sub-prefix}/{resource}
  │
  ├── Depends(get_db) → SQLAlchemy Session
  ├── [if POST/PUT/DELETE] Depends(get_current_user) → User model
  │
  ▼
Route handler (routes/{domain}.py)
  │
  ├── Validates request → Pydantic schema (Create/Update)
  ├── Calls service method
  │
  ▼
Service (services/{resource}_service.py)
  │
  ├── Business logic, error handling (CSMSException)
  ├── ORM queries via db: Session
  │
  ▼
Model → SQLAlchemy ORM → MySQL
  │
  ▼
Response: create_success_response(data) → JSON
```

---

## Migration History (Clinic-specific)

| Revision ID | Description | Parent |
|---|---|---|
| `001a0b0c0d0e` | Create all 17 clinic tables (idempotent) | `4f2500b21ba9` (employee schema) |
| `4f70ca5e63bc` | Rename `patients`→`patient_profiles`, `visits.patient_id`→`patient_profile_id`, fix rhesus enum values (`+`/`-` → `POSITIVE`/`NEGATIVE`) | `001a0b0c0d0e` |

---

## Visit Lifecycle (Status Transitions)

```
Queue created (WAITING)
  │
  ▼
Visit created + queue linked (CHECKIN)
  │
  ▼ (via PUT /visits/{id}/checkin)
Queue → CALLING
Visit → CHECKIN (unchanged; queue called)
  │
  ▼ (via PUT /visits/{id}/start-serving)
Queue → SERVING, called_at = now
Visit → SERVING
  │
  ├── ▼ (via PUT /visits/{id}/finish)
  │   Queue → FINISHED, finished_at = now
  │   Visit → FINISHED
  │
  └── ▼ (via PUT /visits/{id}/cancel)
      Queue → CANCELLED
      Visit → CANCELLED
```

---

## Seed Script

`scripts/seed_clinic.py` populates:

- Company → Branch → Divisions → Departments → Positions → JobLevels
- Users → Employees
- Items (20 medicines)
- ICD10Codes (27 codes) + MedicalProcedures (12 procedures)
- PatientProfiles (8 profiles linked to employees)
- HealthcareProfessionals (6 professionals: 3 doctors, nurse, midwife, pharmacist)
- 8 Queues + 8 Visits with full clinical data (medical records, SOAP, vital signs, diagnoses, procedures, prescriptions with items, dispenses, certificates)
