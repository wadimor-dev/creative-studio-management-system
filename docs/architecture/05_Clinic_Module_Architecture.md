# Clinic Module Architecture

## Daftar Isi

- [1. Filosofi Arsitektur](#1-filosofi-arsitektur)
- [2. Backend Architecture](#2-backend-architecture)
  - [2.1 Entity Relationship Diagram](#21-entity-relationship-diagram)
  - [2.2 Enums](#22-enums)
  - [2.3 Struktur Direktori](#23-struktur-direktori)
  - [2.4 Models & Relationships](#24-models--relationships)
  - [2.5 Service Layer](#25-service-layer)
  - [2.6 Route Layer](#26-route-layer)
  - [2.7 Schema Layer](#27-schema-layer)
  - [2.8 Migration Strategy](#28-migration-strategy)
  - [2.9 Seed Data](#29-seed-data)
- [3. Frontend Architecture](#3-frontend-architecture)
  - [3.1 Struktur Direktori](#31-struktur-direktori)
  - [3.2 Data Flow](#32-data-flow)
  - [3.3 Route Configuration](#33-route-configuration)
  - [3.4 Layout & Navigation](#34-layout--navigation)
  - [3.5 Komponen](#35-komponen)
- [4. Alur Bisnis](#4-alur-bisnis)
  - [4.1 Alur Registrasi Kunjungan](#41-alur-registrasi-kunjungan)
  - [4.2 Alur Pemeriksaan Medis](#42-alur-pemeriksaan-medis)
  - [4.3 Alur Farmasi](#43-alur-farmasi)
- [5. Integrasi dengan Modul Lain](#5-integrasi-dengan-modul-lain)
- [6. Security & Authorization](#6-security--authorization)

---

## 1. Filosofi Arsitektur

Modul Clinic dirancang sebagai **modular domain-driven module** yang berdiri sendiri di dalam folder `backend/app/modules/clinic/`. Prinsip utama:

1. **Separation of Concerns** — Setiap entitas memiliki model, service, schema, dan route sendiri.
2. **UUID sebagai Primary Key** — Semua tabel clinic menggunakan UUID string (36 karakter) untuk menghindari konflik id numerik di lingkungan terdistribusi. Pengecualian: FK ke `employees.id` dan `items.id` tetap `Integer` karena merupakan milik modul HR dan Inventory.
3. **Soft Delete tidak digunakan** — Data klinik bersifat audit trail; penghapusan fisik tidak dilakukan. Status dibatalkan/dihentikan via kolom status enum.
4. **Lazy Loading + Selectin** — Relasi menggunakan `lazy="selectin"` untuk mencegah N+1 query pada daftar visit.
5. **Cascade Delete-Orphan** — Relasi parent-child (Visit → Diagnosis, Visit → Prescription, dll) menggunakan `cascade="all, delete-orphan"` agar data orphan tidak tertinggal.

---

## 2. Backend Architecture

### 2.1 Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        patient_profiles                              │
│  PK id (UUID), employee_id (FK→employees), mr_number, blood_type,   │
│  rhesus, allergy_note, emergency_contact_name/phone, created_at,    │
│  updated_at, created_by, updated_by                                  │
└──────────────────────────┬──────────────────────────────────────────┘
                           │ 1:N
┌──────────────────────────▼──────────────────────────────────────────┐
│                            queues                                    │
│  PK id (UUID), queue_number (string), queue_date, status,           │
│  called_at, finished_at                                              │
└──────────────────────────┬──────────────────────────────────────────┘
                           │ 1:1
┌──────────────────────────▼──────────────────────────────────────────┐
│                            visits                                    │
│  PK id (UUID), visit_number (unique), patient_profile_id (FK),      │
│  queue_id (FK→queues, unique), hc_professional_id (FK),             │
│  visit_type (enum), complaint, visit_status (enum), visit_date,      │
│  created_at, updated_at                                              │
└───────┬──────────┬──────────┬──────────┬──────┬──────┬──────┬───────┘
        │          │          │          │      │      │      │
     1:1 │      1:1 │      1:1 │      1:N │  1:N │  1:1 │  1:N │  1:N
  ┌──────▼──┐ ┌────▼───┐ ┌────▼───┐ ┌───▼────┐ ┌─▼────┐ ┌▼────┐ ┌─▼──────┐
  │medical  │ │soap    │ │vital   │ │diagnoses│ │visit │ │presc│ │med.    │
  │records  │ │notes   │ │signs   │ │(N rows) │ │proc. │ │rip. │ │cert.   │
  │(1 per   │ │(1 per  │ │(1 per  │ │icd10_id│ │(N    │ │(1   │ │(N      │
  │ visit)  │ │ visit) │ │ visit) │ │FK→icd10│ │rows) │ │per  │ │rows)   │
  └─────────┘ └────────┘ └────────┘ └─────────┘ └──────┘ │visit│ └────────┘
                                                          │     │
                                                     ┌────▼─────▼──────┐
                                                     │prescription_    │
                                                     │items (N rows)   │
                                                     │medicine_id      │
                                                     │(FK→items.id)    │
                                                     └─────────────────┘

┌──────────────────┐  ┌──────────────────┐  ┌─────────────────────────┐
│  healthcare_     │  │   icd10_codes    │  │   medical_procedures    │
│  professionals   │  │  (master data)   │  │   (master data)         │
│  employee_id FK  │  │  code, name,     │  │  code, name, desc       │
│  profession enum │  │  desc, is_active │  │                         │
└──────────────────┘  └──────────────────┘  └─────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                      clinic_activity_logs                            │
│  PK id (UUID), user_id, module, action, table_name, record_id,      │
│  old_value (JSON), new_value (JSON), ip_address, device, created_at │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 Enums

| Enum | Values | Digunakan di |
|------|--------|-------------|
| `BloodType` | A, B, AB, O | PatientProfile |
| `Rhesus` | POSITIVE, NEGATIVE | PatientProfile |
| `Profession` | DOCTOR, NURSE, MIDWIFE, LAB_TECHNICIAN, PHARMACIST, DENTIST, OTHER | HealthcareProfessional |
| `ProfessionalStatus` | ACTIVE, INACTIVE, SUSPENDED | HealthcareProfessional |
| `QueueStatus` | WAITING, CALLING, SERVING, FINISHED, CANCELLED | Queue |
| `VisitStatus` | CHECKIN, SERVING, FINISHED, CANCELLED | Visit |
| `VisitType` | REGULAR, EMERGENCY, FOLLOW_UP | Visit |
| `MedicalRecordStatus` | DRAFT, FINAL | MedicalRecord |
| `DiagnosisType` | PRIMARY, SECONDARY | Diagnosis |
| `PrescriptionStatus` | ACTIVE, DISPENSED, CANCELLED | Prescription |
| `CertificateType` | HEALTH, SICK, FIT_TO_WORK | MedicalCertificate |

### 2.3 Struktur Direktori

```
backend/app/modules/clinic/
├── __init__.py                  # Re-export router
├── router.py                    # Aggregator: gabung 6 sub-router
├── models/                      # SQLAlchemy ORM models
│   ├── __init__.py
│   ├── patient_profile.py
│   ├── queue.py
│   ├── visit.py
│   ├── medical_record.py
│   ├── soap_note.py
│   ├── vital_sign.py
│   ├── diagnosis.py
│   ├── icd10_code.py
│   ├── medical_procedure.py
│   ├── visit_procedure.py
│   ├── medical_attachment.py
│   ├── healthcare_professional.py
│   ├── prescription.py
│   ├── prescription_item.py
│   ├── medicine_dispense.py
│   ├── medical_certificate.py
│   └── clinic_activity_log.py
├── schemas/
│   └── __init__.py              # 60+ Pydantic schemas dalam 1 file
├── services/                    # Business logic layer
│   ├── __init__.py
│   ├── patient_profile_service.py
│   ├── queue_service.py
│   ├── visit_service.py
│   ├── medical_record_service.py
│   ├── soap_note_service.py
│   ├── vital_sign_service.py
│   ├── diagnosis_service.py
│   ├── icd10_code_service.py
│   ├── medical_procedure_service.py
│   ├── visit_procedure_service.py
│   ├── medical_attachment_service.py
│   ├── healthcare_professional_service.py
│   ├── prescription_service.py
│   ├── prescription_item_service.py
│   ├── medicine_dispense_service.py
│   ├── medical_certificate_service.py
│   └── clinic_activity_log_service.py
├── routes/                      # FastAPI routers
│   ├── __init__.py              # Re-export 6 routers
│   ├── master_data.py           # Patients, HCProf, ICD10, Procedures
│   ├── registration.py          # Queues, Visits, status transitions
│   ├── medical.py               # MedicalRecords, SOAP, Vitals, Diagnoses, etc.
│   ├── pharmacy.py              # Prescriptions, Items, Dispenses
│   ├── certificates.py          # MedicalCertificates
│   └── audit.py                 # ActivityLogs
└── dependencies.py              # (belum ada — dependency inject dari modul global)
```

### 2.4 Models & Relationships

**17 models** total, semua menggunakan UUID string sebagai primary key.

| Model | Table | Parent (FK) | Children |
|-------|-------|-------------|----------|
| `PatientProfile` | `patient_profiles` | `employee_id` → `employees.id` | `visits[]` |
| `Queue` | `queues` | — | `visit` (1:1) |
| `Visit` | `visits` | `patient_profile_id` → `patient_profiles.id`, `queue_id` → `queues.id`, `healthcare_professional_id` → `healthcare_professionals.id` | `medical_record`, `soap_note`, `vital_sign`, `diagnoses[]`, `visit_procedures[]`, `prescription`, `certificates[]`, `attachments[]` |
| `MedicalRecord` | `medical_records` | `visit_id` → `visits.id` (unique) | — |
| `SOAPNote` | `soap_notes` | `visit_id` → `visits.id` (unique) | — |
| `VitalSign` | `vital_signs` | `visit_id` → `visits.id` (unique) | — |
| `Diagnosis` | `diagnoses` | `visit_id` → `visits.id`, `icd10_id` → `icd10_codes.id` | — |
| `VisitProcedure` | `visit_procedures` | `visit_id` → `visits.id`, `procedure_id` → `medical_procedures.id` | — |
| `MedicalAttachment` | `medical_attachments` | `visit_id` → `visits.id` | — |
| `Prescription` | `prescriptions` | `visit_id` → `visits.id` (unique) | `items[]` |
| `PrescriptionItem` | `prescription_items` | `prescription_id` → `prescriptions.id`, `medicine_id` → `items.id` (inventory) | — |
| `MedicineDispense` | `medicine_dispenses` | `prescription_item_id` → `prescription_items.id` | — |
| `HealthcareProfessional` | `healthcare_professionals` | `employee_id` → `employees.id` (unique) | `visits[]` |
| `ICD10Code` | `icd10_codes` | — | `diagnoses[]` |
| `MedicalProcedure` | `medical_procedures` | — | `visit_procedures[]` |
| `MedicalCertificate` | `medical_certificates` | `visit_id` → `visits.id` | — |
| `ClinicActivityLog` | `clinic_activity_logs` | — | — |

**Key design notes:**
- `patient_profiles.employee_id` (Integer) — FK ke tabel `employees` dari modul HR. Satu pasien = satu karyawan.
- `prescription_items.medicine_id` (Integer) — FK ke tabel `items` dari modul Inventory. Obat dikelola sebagai item inventory.
- Semua relasi 1:1 (MedicalRecord, SOAPNote, VitalSign, Prescription ke Visit) menggunakan `uselist=False` di SQLAlchemy.
- Polymorphic cascade: semua child Visit (diagnoses, procedures, certificates, attachments) menggunakan `cascade="all, delete-orphan"`.

### 2.5 Service Layer

Setiap service mengikuti pola yang konsisten:

```python
# Contoh pola: patient_profile_service.py
from app.core.database import get_db_session
from app.modules.clinic.models.patient_profile import PatientProfile
from app.modules.clinic.schemas import PatientProfileCreate, PatientProfileUpdate

class PatientProfileService:
    def __init__(self):
        self.db = next(get_db_session())

    def list(self, params: dict) -> list[PatientProfile]:
        query = self.db.query(PatientProfile)
        # filter + pagination
        return query.all()

    def get(self, id: str) -> PatientProfile | None:
        return self.db.query(PatientProfile).filter(PatientProfile.id == id).first()

    def create(self, data: PatientProfileCreate) -> PatientProfile:
        profile = PatientProfile(**data.model_dump())
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
        return profile
```

Total 17 service classes, masing-masing menangani satu entitas. Service dipanggil langsung dari route handler. Tidak ada repository layer terpisah — service langsung menggunakan SQLAlchemy session.

### 2.6 Route Layer

6 router files yang diagregasi di `router.py`:

```python
# router.py — agregasi semua sub-router
router.include_router(master_data_router, prefix="/master-data")      # 22 endpoints
router.include_router(registration_router, prefix="/registration")     # 15 endpoints
router.include_router(medical_router, prefix="/medical")              # 28 endpoints
router.include_router(pharmacy_router, prefix="/pharmacy")             # 12 endpoints
router.include_router(certificates_router, prefix="/certificates")    # 5 endpoints
router.include_router(audit_router, prefix="/audit")                  # 2 endpoints
```

Router utama di-register di `app/main.py` dengan prefix `/api/v1/clinic`.

**Total endpoint: 84**

#### master_data.py (prefix `/master-data`)
| Endpoint | Method | Deskripsi |
|----------|--------|-----------|
| `/patients` | GET/POST | List & create pasien |
| `/patients/{id}` | GET/PUT/DELETE | Get/update/delete pasien |
| `/patients/by-employee/{employee_id}` | GET | Cari pasien via employee_id |
| `/patients/by-mr/{mr_number}` | GET | Cari pasien via nomor RM |
| `/healthcare-professionals` | GET/POST | List & create tenaga medis |
| `/healthcare-professionals/{id}` | GET/PUT/DELETE | Get/update/delete tenaga medis |
| `/icd10-codes` | GET/POST | List & create kode ICD-10 |
| `/icd10-codes/{id}` | GET/PUT/DELETE | Get/update/delete ICD-10 |
| `/medical-procedures` | GET/POST | List & create prosedur |
| `/medical-procedures/{id}` | GET/PUT/DELETE | Get/update/delete prosedur |

#### registration.py (prefix `/registration`)
| Endpoint | Method | Deskripsi |
|----------|--------|-----------|
| `/queues` | GET/POST | List & create antrian |
| `/queues/current` | GET | Antrian yang sedang aktif |
| `/queues/waiting-count` | GET | Jumlah waiting |
| `/queues/{id}` | GET | Detail antrian |
| `/queues/{id}/status` | PUT | Update status antrian |
| `/visits` | GET/POST | List & create kunjungan |
| `/visits/{id}` | GET/PUT | Get/update kunjungan |
| `/visits/{id}/detail` | GET | Kunjungan lengkap + semua relasi |
| `/visits/{id}/checkin` | PUT | Checkin → CHECKIN |
| `/visits/{id}/start-serving` | PUT | Mulai periksa → SERVING |
| `/visits/{id}/finish` | PUT | Selesai → FINISHED |
| `/visits/{id}/cancel` | PUT | Batal → CANCELLED |

#### medical.py (prefix `/medical`)
| Endpoint | Method | Deskripsi |
|----------|--------|-----------|
| `/medical-records` | GET/POST | List & create RM |
| `/medical-records/{id}` | GET/PUT | Get/update RM |
| `/medical-records/{id}/finalize` | PUT | Finalkan RM |
| `/medical-records/by-visit/{visit_id}` | GET | RM per kunjungan |
| `/soap-notes/{id}` | GET | Detail SOAP |
| `/soap-notes/by-visit/{visit_id}` | GET/PUT | SOAP per kunjungan |
| `/soap-notes` | POST | Create SOAP |
| `/vital-signs/{id}` | GET | Detail vital sign |
| `/vital-signs/by-visit/{visit_id}` | GET/PUT | Vital sign per kunjungan |
| `/vital-signs` | POST | Create vital sign |
| `/diagnoses/by-visit/{visit_id}` | GET | Diagnosa per kunjungan |
| `/diagnoses` | POST | Create diagnosa |
| `/diagnoses/{id}` | PUT/DELETE | Update/delete diagnosa |
| `/visit-procedures/by-visit/{visit_id}` | GET | Tindakan per kunjungan |
| `/visit-procedures` | POST | Create tindakan |
| `/visit-procedures/{id}` | PUT/DELETE | Update/delete tindakan |
| `/medical-attachments/by-visit/{visit_id}` | GET | Lampiran per kunjungan |
| `/medical-attachments` | POST | Upload lampiran |
| `/medical-attachments/{id}` | PUT/DELETE | Update/delete lampiran |

#### pharmacy.py (prefix `/pharmacy`)
| Endpoint | Method | Deskripsi |
|----------|--------|-----------|
| `/prescriptions/{id}` | GET | Detail resep |
| `/prescriptions/by-visit/{visit_id}` | GET | Resep per kunjungan |
| `/prescriptions` | POST | Create resep |
| `/prescriptions/{id}` | PUT | Update resep |
| `/prescriptions/{id}/dispense` | PUT | Dispense obat |
| `/prescriptions/{id}/cancel` | PUT | Cancel resep |
| `/prescription-items/by-prescription/{rx_id}` | GET | Item per resep |
| `/prescription-items` | POST | Tambah item |
| `/prescription-items/{id}` | PUT/DELETE | Update/delete item |
| `/medicine-dispenses/{id}` | GET | Detail dispense |
| `/medicine-dispenses` | POST | Create dispense |

#### certificates.py (prefix `/certificates`)
| Endpoint | Method | Deskripsi |
|----------|--------|-----------|
| `/medical-certificates/{id}` | GET | Detail sertifikat |
| `/medical-certificates/by-visit/{visit_id}` | GET | Sertifikat per kunjungan |
| `/medical-certificates` | POST | Create sertifikat |
| `/medical-certificates/{id}` | PUT/DELETE | Update/delete sertifikat |

#### audit.py (prefix `/audit`)
| Endpoint | Method | Deskripsi |
|----------|--------|-----------|
| `/activity-logs` | GET | List log aktivitas |
| `/activity-logs` | POST | Create log aktivitas |

### 2.7 Schema Layer

Semua Pydantic schema didefinisikan dalam satu file `schemas/__init__.py` untuk menghindari circular import. Pola penamaan:

- `{Entity}Base` — field bersama untuk create & response
- `{Entity}Create(Base)` — validasi input saat create
- `{Entity}Update(BaseModel)` — semua field opsional untuk partial update
- `{Entity}Response(Base)` — field tambahan: `id`, `created_at`, computed fields

**Schema khusus:**
```python
class VisitDetailResponse(VisitResponse):
    medical_record: Optional[MedicalRecordResponse] = None
    soap_note: Optional[SOAPNoteResponse] = None
    vital_sign: Optional[VitalSignResponse] = None
    diagnoses: List[DiagnosisResponse] = []
    procedures: List[VisitProcedureResponse] = []
    prescription: Optional[PrescriptionResponse] = None
    certificates: List[MedicalCertificateResponse] = []
    attachments: List[MedicalAttachmentResponse] = []
```

`VisitDetailResponse` mengagregasi semua data yang berhubungan dengan satu kunjungan dalam satu response, digunakan oleh endpoint `GET /visits/{id}/detail`.

### 2.8 Migration Strategy

Satu migration file: `001a0b0c0d0e` yang:
- Bergantung pada `4f2500b21ba9` (revisi terakhir sebelum clinic)
- Membuat 17 tabel dengan seluruh FK, index, dan constraint enum
- Menggunakan engine MySQL dengan charset `utf8mb4`

Cara upgrade:
```bash
cd backend
alembic upgrade head
```

### 2.9 Seed Data

Script: `scripts/clinic/seed_icd10.py`

Mengisi data awal:
- **28 kode ICD-10** — penyakit umum (A00–J45)
- **20 prosedur medis** — tindakan umum (EKG, injeksi, jahit luka, dll)

Jalankan:
```bash
cd backend
python -m scripts.clinic.seed_icd10
```

---

## 3. Frontend Architecture

### 3.1 Struktur Direktori

```
frontend/src/modules/clinic/
├── index.js                          # Re-export komponen utama
├── routes.jsx                        # Route definitions
├── api.js                            # API client (~60 methods)
├── constants/
│   └── index.js                      # Enums, labels, query keys, route paths
├── helpers/
│   └── index.js                      # Formatting, status helpers
├── hooks/
│   └── index.js                      # ~40 React Query hooks
├── components/
│   ├── index.jsx                     # Re-export komponen
│   └── StatusBadge.jsx               # Generic status badge
├── pages/
│   ├── Dashboard.jsx                 # Ringkasan klinik
│   ├── Queue.jsx                     # Manajemen antrian
│   ├── Visits.jsx                    # Daftar & registrasi kunjungan
│   ├── VisitDetail.jsx               # Detail kunjungan lengkap
│   ├── MedicalRecords.jsx            # SOAP + Vitals + Diagnoses
│   ├── Medicines.jsx                 # Stok obat (dari inventory)
│   ├── Patients.jsx                  # CRUD pasien
│   ├── HealthcareProfessionals.jsx   # CRUD tenaga medis
│   ├── ICD10Codes.jsx                # CRUD ICD-10
│   └── MedicalProcedures.jsx         # CRUD prosedur
├── layout/
│   └── ClinicLayout.jsx              # Sidebar + nav
└── utils/
```

### 3.2 Data Flow

```
┌──────────────┐     ┌──────────────────┐     ┌──────────────────┐
│   Pages      │────▶│  React Query     │────▶│   clinicApi      │
│  (JSX View)  │     │  (hooks/index)   │     │   (api.js)       │
└──────────────┘     └──────────────────┘     └──────────────────┘
                                                      │
                                                      ▼
                                               ┌──────────────────┐
                                               │  Axios Instance   │
                                               │  (src/api/axios)  │
                                               └──────────────────┘
                                                      │
                                                      ▼
                                               ┌──────────────────┐
                                               │   FastAPI Routes  │
                                               │  /api/v1/clinic/* │
                                               └──────────────────┘
```

**Pattern React Query yang digunakan:**
- `useQuery` untuk GET requests dengan query key `['clinic', entity, params]`
- `useMutation` untuk POST/PUT/DELETE dengan `onSuccess` callback yang melakukan `invalidateQueries`
- Setiap mutation menampilkan toast notification via `react-toastify`

**Contoh hook:**
```javascript
// GET — list pasien
export const usePatientProfiles = (params) =>
  useQuery({
    queryKey: ['clinic', 'patient-profiles', params],
    queryFn: () => clinicApi.getPatientProfiles(params),
  });

// MUTATION — create patient profile + invalidate cache + toast
export const useCreatePatientProfile = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (p) => clinicApi.createPatientProfile(p),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['clinic', 'patient-profiles'] });
      toast.success('Pasien ditambahkan');
    },
    onError: (e) => toast.error(e?.response?.data?.detail || e.message),
  });
};
```

### 3.3 Route Configuration

Routes didefinisikan di `frontend/src/routes/index.jsx`:

```jsx
<Route element={<ProtectedRoute permission='CLINIC' />}>
  <Route element={<ClinicLayout />}>
    <Route path='/clinic/*' element={<ClinicRoutes />} />
  </Route>
</Route>
```

Routes spesifik di `modules/clinic/routes.jsx`:
| Path | Page | Deskripsi |
|------|------|-----------|
| `/clinic/dashboard` | Dashboard | Ringkasan hari ini |
| `/clinic/visits` | Visits | Daftar + registrasi kunjungan |
| `/clinic/visits/:id` | VisitDetail | Detail kunjungan lengkap |
| `/clinic/queue` | Queue | Manajemen antrian |
| `/clinic/medical-records` | MedicalRecords | SOAP, vital, diagnosis |
| `/clinic/medicines` | Medicines | Stok obat |
| `/clinic/patients` | Patients | CRUD pasien |
| `/clinic/healthcare-professionals` | HealthcareProfessionals | CRUD tenaga medis |
| `/clinic/icd10` | ICD10Codes | CRUD kode ICD-10 |
| `/clinic/medical-procedures` | MedicalProcedures | CRUD prosedur |

### 3.4 Layout & Navigation

`ClinicLayout.jsx` menyediakan sidebar navigasi dengan 9 menu item:

1. **Dashboard** — `LayoutDashboard`
2. **Antrian** — `Clock`
3. **Kunjungan** — `ClipboardList`
4. **Rekam Medis** — `FileText`
5. **Pasien** — `Users`
6. **Tenaga Medis** — `UserCog`
7. **Obat & Stok** — `Pill`
8. **ICD-10** — `BookOpen`
9. **Prosedur** — `Activity`

Sidebar menggunakan komponen `NavLink` dari React Router dengan highlight otomatis berdasarkan path aktif. Mobile toggle menggunakan state `sidebarOpen` dengan overlay.

### 3.5 Komponen

Saat ini hanya ada satu komponen bersama:

**`StatusBadge`** — Badge serbaguna untuk menampilkan status:
```jsx
<StatusBadge label={visitStatusLabel(v.visit_status)} className={visitStatusBadge(v.visit_status)} />
```

Tidak ada komponen kompleks lainnya karena setiap page menggunakan pendekatan **inline CRUD** — form create/edit langsung di dalam page, bukan di modal/dialog terpisah. Pola ini dipilih untuk kesederhanaan dan kecepatan development.

---

## 4. Alur Bisnis

### 4.1 Alur Registrasi Kunjungan

```
Frontend                              Backend
────────                               ───────
1. Pilih pasien (search/select)
2. Pilih visit type
3. Isi complaint
4. Klik "Daftar Kunjungan"
      │
      ▼
5. POST /registration/queues ──────▶  Create Queue (status WAITING)
      │                                queue_number: auto-generated
      │                                queue_date: today
      │
      ◀─────── queue_id ──────────────
      │
 6. POST /registration/visits ───────▶  Create Visit
      │  {patient_profile_id,          visit_number: auto-generated
      │   queue_id, visit_type,        visit_status: CHECKIN
      │   complaint}
      │
      ◀─────── visit response ─────────
      │
7. Tampilkan konfirmasi
   (queue number, visit number)
```

### 4.2 Alur Pemeriksaan Medis

```
Frontend                              Backend
────────                               ───────
1. Queue page: Klik "Panggil"
      │
      ▼
2. PUT /visits/{id}/start-serving ──▶  Visit → SERVING
                                        Queue → CALLING/SERVING
      │
3. Medical Records page:
   - Pilih pasien dari list SERVING
   - Isi Vital Sign → PUT /vital-signs/by-visit/{visit_id}
   - Isi SOAP → PUT /soap-notes/by-visit/{visit_id}
   - Tambah Diagnosis → POST /diagnoses
   - Tambah Tindakan → POST /visit-procedures
   - Buat Resep → POST /prescriptions
      │
4. Klinik farmasi:
   - Dispense → PUT /prescriptions/{id}/dispense
   - POST /medicine-dispenses
      │
5. PUT /visits/{id}/finish ─────────▶  Visit → FINISHED
                                        Queue → FINISHED
```

### 4.3 Alur Farmasi

```
1. Setelah visit SERVING, dokter membuat resep:
   POST /pharmacy/prescriptions
     { visit_id, healthcare_professional_id }
     ▶ Resep status: ACTIVE

2. Tambah item obat:
   POST /pharmacy/prescription-items
     { prescription_id, medicine_id, dosage, frequency, quantity }
     ▶ medicine_id: FK ke items.id (inventory)

3. Farmasi melakukan dispense:
   PUT /pharmacy/prescriptions/{id}/dispense
     ▶ Resep status: DISPENSED

4. Catat dispense detail:
   POST /pharmacy/medicine-dispenses
     { prescription_item_id, quantity }
     ▶ Mencatat siapa yang mendispense & waktu
```

---

## 5. Integrasi dengan Modul Lain

| Modul | Tabel/Entity | Relasi |
|-------|-------------|--------|
| **HR / Employee** | `employees` | `patient_profiles.employee_id`, `healthcare_professionals.employee_id` |
| **Inventory** | `items` | `prescription_items.medicine_id` |
| **Auth** | `users` | `patient_profiles.created_by`, `clinic_activity_logs.user_id`, `medical_certificates.issued_by` |

**Catatan:** Clinic module **membaca** data dari HR dan Inventory tetapi **tidak menulis**. Semua data employee/items dikelola oleh modul masing-masing.

### 5.1 Architectural Guidelines (Enterprise ERP)

#### 1. Employee adalah Core Entity
Employee adalah entitas inti yang dikelola oleh **HR Module**, terpisah dari **User** (auth). Clinic mereferensi `employees.id` via `patient_profiles.employee_id` dan `healthcare_professionals.employee_id`. Tidak ada duplikasi data karyawan di Clinic.

#### 2. Clinic Tidak Boleh Memiliki Data Employee
Clinic **read-only** terhadap data employee. Semua operasi write (create/update/delete employee) dilakukan oleh HR Module. Clinic hanya menyimpan data tambahan yang spesifik untuk keperluan medis (MR number, golongan darah, riwayat alergi, kontak darurat) di tabel `patient_profiles`.

#### 3. `patients` → `patient_profiles`
Tabel direname dari `patients` menjadi `patient_profiles` karena "patient" di konteks perusahaan bukanlah master entity — core entity adalah Employee. Model `Patient` diganti menjadi `PatientProfile`. URL endpoint `/patients` tetap dipertahankan untuk backward compatibility di V1; internal routing merujuk ke `PatientProfileService`.

#### 4. HR → Clinic Integration Strategy
| V | Strategy | Keterangan |
|---|----------|------------|
| V1 | **Excel Import** | Bootstrap data employee ke clinic via file Excel. Cocok untuk go-live cepat. |
| V2 | **API Integration** | Clinic memanggil HR API untuk lookup/sync data employee secara real-time. |
| V3 | **Domain Events** | Event-driven integration via message broker (RabbitMQ/Kafka). HR publish event `employee.created/updated/deactivated`; Clinic consume untuk sync otomatis. |

#### 5. Inventory Owns Medicine Stock
Obat adalah item inventory yang dikelola oleh **Inventory Module**. Clinic hanya menulis resep dengan `prescription_items.medicine_id` → `items.id`. Stock opname, pricing, dan procurement sepenuhnya milik Inventory. Tidak ada tabel stok obat di Clinic.

#### 6. BPJS sebagai Modul Terpisah
BPJS (badan penyelenggara jaminan sosial) tidak boleh di-embed di dalam Clinic Module. BPJS akan menjadi **module terpisah** (`bpjs`) dengan tabel dan logika sendiri:
- `bpjs_participants` — data kepesertaan BPJS
- `bpjs_claims` — klaim BPJS per kunjungan
- `bpjs_referrals` — rujukan BPJS
- Integrasi dengan Clinic via `visit_id` (UUID) sebagai foreign key

---

## 6. Security & Authorization

- Semua endpoint clinic berada di balik `ProtectedRoute` dengan permission `CLINIC` di frontend.
- Backend menggunakan dependency `get_current_active_user` dari `app.dependencies` untuk memvalidasi token JWT.
- Permission checking (PBAC) diterapkan per-route action. Endpoint sensitif seperti finalize medical record dan dispense prescription memerlukan permission khusus.
- Audit trail dicatat via `ClinicActivityLog` untuk setiap operasi create/update/delete pada data klinik.
