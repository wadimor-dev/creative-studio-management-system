# API Documentation — Modul Clinic

## Overview

Modul Clinic menangani manajemen klinik perusahaan: pasien, antrian, kunjungan, rekam medis, diagnosis, resep obat, sertifikat medis, dan audit trail.

**Base URL:** `/api/v1/clinic`

**Total endpoint:** 84

## Autentikasi

Semua endpoint mewajibkan JWT Bearer token di header `Authorization`. Token diperoleh dari endpoint `/api/v1/auth/login`.

---

## 1. Master Data (`/api/v1/clinic/master-data`)

### 1.1 Patients

| Method | Path | Deskripsi |
|--------|------|-----------|
| `GET` | `/master-data/patients` | List pasien (support `?q=`, `?limit=`, `?offset=`) |
| `GET` | `/master-data/patients/{patient_id}` | Detail pasien by UUID |
| `GET` | `/master-data/patients/by-employee/{employee_id}` | Cari pasien by employee_id (Integer) |
| `GET` | `/master-data/patients/by-mr/{mr_number}` | Cari pasien by nomor RM |
| `POST` | `/master-data/patients` | Create pasien baru |
| `PUT` | `/master-data/patients/{patient_id}` | Update data pasien |
| `DELETE` | `/master-data/patients/{patient_id}` | Hapus pasien |

**POST/PUT body:**
```json
{
  "employee_id": 1,
  "medical_record_number": "RM-001",
  "blood_type": "A" | "B" | "AB" | "O" | null,
  "rhesus": "POSITIVE" | "NEGATIVE" | null,
  "allergy_note": "string | null",
  "emergency_contact_name": "string | null",
  "emergency_contact_phone": "string | null"
}
```

### 1.2 Healthcare Professionals

| Method | Path | Deskripsi |
|--------|------|-----------|
| `GET` | `/master-data/healthcare-professionals` | List tenaga medis |
| `GET` | `/master-data/healthcare-professionals/{hp_id}` | Detail tenaga medis |
| `POST` | `/master-data/healthcare-professionals` | Create tenaga medis |
| `PUT` | `/master-data/healthcare-professionals/{hp_id}` | Update tenaga medis |
| `DELETE` | `/master-data/healthcare-professionals/{hp_id}` | Hapus tenaga medis |

**POST/PUT body:**
```json
{
  "employee_id": 1,
  "profession": "DOCTOR" | "NURSE" | "MIDWIFE" | "LAB_TECHNICIAN" | "PHARMACIST" | "DENTIST" | "OTHER",
  "specialization": "string | null",
  "license_number": "string | null",
  "status": "ACTIVE" | "INACTIVE" | "SUSPENDED"
}
```

### 1.3 ICD-10 Codes

| Method | Path | Deskripsi |
|--------|------|-----------|
| `GET` | `/master-data/icd10-codes` | List kode ICD-10 |
| `GET` | `/master-data/icd10-codes/{code_id}` | Detail kode ICD-10 |
| `POST` | `/master-data/icd10-codes` | Create kode ICD-10 baru |
| `PUT` | `/master-data/icd10-codes/{code_id}` | Update kode ICD-10 |
| `DELETE` | `/master-data/icd10-codes/{code_id}` | Hapus kode ICD-10 |

**POST/PUT body:**
```json
{
  "code": "A00.0",
  "name": "Cholera",
  "description": "string | null",
  "is_active": true
}
```

### 1.4 Medical Procedures

| Method | Path | Deskripsi |
|--------|------|-----------|
| `GET` | `/master-data/medical-procedures` | List prosedur medis |
| `GET` | `/master-data/medical-procedures/{proc_id}` | Detail prosedur |
| `POST` | `/master-data/medical-procedures` | Create prosedur baru |
| `PUT` | `/master-data/medical-procedures/{proc_id}` | Update prosedur |
| `DELETE` | `/master-data/medical-procedures/{proc_id}` | Hapus prosedur |

**POST/PUT body:**
```json
{
  "code": "PROC-001",
  "name": "EKG",
  "description": "string | null"
}
```

---

## 2. Registration (`/api/v1/clinic/registration`)

### 2.1 Queues

| Method | Path | Deskripsi |
|--------|------|-----------|
| `GET` | `/registration/queues` | List antrian |
| `GET` | `/registration/queues/current` | Antrian yang sedang aktif hari ini |
| `GET` | `/registration/queues/waiting-count` | Jumlah antrian waiting |
| `GET` | `/registration/queues/{queue_id}` | Detail antrian |
| `POST` | `/registration/queues` | Create antrian baru |
| `PUT` | `/registration/queues/{queue_id}/status` | Update status antrian |

**POST body:**
```json
{
  "queue_number": "A001",
  "queue_date": "2026-07-22",
  "status": "WAITING"
}
```

### 2.2 Visits

| Method | Path | Deskripsi |
|--------|------|-----------|
| `GET` | `/registration/visits` | List kunjungan |
| `GET` | `/registration/visits/{visit_id}` | Detail kunjungan |
| `GET` | `/registration/visits/{visit_id}/detail` | Kunjungan + semua relasi (MR, SOAP, Vital, Diagnosis, Resep, Sertifikat) |
| `POST` | `/registration/visits` | Create kunjungan baru |
| `PUT` | `/registration/visits/{visit_id}` | Update kunjungan |
| `PUT` | `/registration/visits/{visit_id}/checkin` | Checkin → status CHECKIN |
| `PUT` | `/registration/visits/{visit_id}/start-serving` | Mulai periksa → SERVING |
| `PUT` | `/registration/visits/{visit_id}/finish` | Selesai → FINISHED |
| `PUT` | `/registration/visits/{visit_id}/cancel` | Batal → CANCELLED |

**POST body (create visit):**
```json
{
  "patient_profile_id": "uuid",
  "queue_id": "uuid | null",
  "healthcare_professional_id": "uuid | null",
  "visit_type": "REGULAR" | "EMERGENCY" | "FOLLOW_UP",
  "complaint": "string | null"
}
```

**Visit status machine:**
```
CHECKIN ──► SERVING ──► FINISHED
   │                     │
   └──► CANCELLED ◄──────┘
```

---

## 3. Medical (`/api/v1/clinic/medical`)

### 3.1 Medical Records

| Method | Path | Deskripsi |
|--------|------|-----------|
| `GET` | `/medical/medical-records` | List rekam medis |
| `GET` | `/medical/medical-records/{record_id}` | Detail rekam medis |
| `GET` | `/medical/medical-records/by-visit/{visit_id}` | RM per kunjungan |
| `POST` | `/medical/medical-records` | Create RM |
| `PUT` | `/medical/medical-records/{record_id}` | Update RM |
| `PUT` | `/medical/medical-records/{record_id}/finalize` | Final → readonly |

### 3.2 SOAP Notes

| Method | Path | Deskripsi |
|--------|------|-----------|
| `GET` | `/medical/soap-notes/{note_id}` | Detail SOAP |
| `GET` | `/medical/soap-notes/by-visit/{visit_id}` | SOAP per kunjungan |
| `POST` | `/medical/soap-notes` | Create SOAP |
| `PUT` | `/medical/soap-notes/{note_id}` | Update SOAP |
| `PUT` | `/medical/soap-notes/by-visit/{visit_id}` | Upsert SOAP by visit |

**SOAP fields:**
```json
{
  "visit_id": "uuid",
  "subjective": "Keluhan pasien",
  "objective": "Hasil pemeriksaan",
  "assessment": "Assessment dokter",
  "plan": "Rencana tindakan"
}
```

### 3.3 Vital Signs

| Method | Path | Deskripsi |
|--------|------|-----------|
| `GET` | `/medical/vital-signs/{vs_id}` | Detail vital sign |
| `GET` | `/medical/vital-signs/by-visit/{visit_id}` | Vital sign per kunjungan |
| `POST` | `/medical/vital-signs` | Create vital sign |
| `PUT` | `/medical/vital-signs/{vs_id}` | Update vital sign |
| `PUT` | `/medical/vital-signs/by-visit/{visit_id}` | Upsert vital sign by visit |

**Fields:**
```json
{
  "visit_id": "uuid",
  "systolic": 120, "diastolic": 80,
  "pulse": 72, "respiration": 20,
  "temperature": 36.5, "spo2": 98.0,
  "height": 170.0, "weight": 65.0
}
```

### 3.4 Diagnoses

| Method | Path | Deskripsi |
|--------|------|-----------|
| `GET` | `/medical/diagnoses/by-visit/{visit_id}` | List diagnosis per kunjungan |
| `POST` | `/medical/diagnoses` | Tambah diagnosis |
| `PUT` | `/medical/diagnoses/{diagnosis_id}` | Update diagnosis |
| `DELETE` | `/medical/diagnoses/{diagnosis_id}` | Hapus diagnosis |

### 3.5 Visit Procedures

| Method | Path | Deskripsi |
|--------|------|-----------|
| `GET` | `/medical/visit-procedures/by-visit/{visit_id}` | List tindakan per kunjungan |
| `POST` | `/medical/visit-procedures` | Tambah tindakan |
| `PUT` | `/medical/visit-procedures/{vp_id}` | Update tindakan |
| `DELETE` | `/medical/visit-procedures/{vp_id}` | Hapus tindakan |

### 3.6 Medical Attachments

| Method | Path | Deskripsi |
|--------|------|-----------|
| `GET` | `/medical/medical-attachments/by-visit/{visit_id}` | List lampiran per kunjungan |
| `POST` | `/medical/medical-attachments` | Upload lampiran |
| `PUT` | `/medical/medical-attachments/{att_id}` | Update lampiran |
| `DELETE` | `/medical/medical-attachments/{att_id}` | Hapus lampiran |

---

## 4. Pharmacy (`/api/v1/clinic/pharmacy`)

### 4.1 Prescriptions

| Method | Path | Deskripsi |
|--------|------|-----------|
| `GET` | `/pharmacy/prescriptions/{rx_id}` | Detail resep (termasuk items) |
| `GET` | `/pharmacy/prescriptions/by-visit/{visit_id}` | Resep per kunjungan |
| `POST` | `/pharmacy/prescriptions` | Create resep |
| `PUT` | `/pharmacy/prescriptions/{rx_id}` | Update resep |
| `PUT` | `/pharmacy/prescriptions/{rx_id}/dispense` | Dispense → DISPENSED |
| `PUT` | `/pharmacy/prescriptions/{rx_id}/cancel` | Cancel → CANCELLED |

### 4.2 Prescription Items

| Method | Path | Deskripsi |
|--------|------|-----------|
| `GET` | `/pharmacy/prescription-items/by-prescription/{rx_id}` | List item resep |
| `POST` | `/pharmacy/prescription-items` | Tambah item |
| `PUT` | `/pharmacy/prescription-items/{item_id}` | Update item |
| `DELETE` | `/pharmacy/prescription-items/{item_id}` | Hapus item |

### 4.3 Medicine Dispenses

| Method | Path | Deskripsi |
|--------|------|-----------|
| `GET` | `/pharmacy/medicine-dispenses/{dispense_id}` | Detail dispense |
| `POST` | `/pharmacy/medicine-dispenses` | Create dispense |

---

## 5. Certificates (`/api/v1/clinic/certificates`)

### 5.1 Medical Certificates

| Method | Path | Deskripsi |
|--------|------|-----------|
| `GET` | `/certificates/medical-certificates/{cert_id}` | Detail sertifikat |
| `GET` | `/certificates/medical-certificates/by-visit/{visit_id}` | Sertifikat per kunjungan |
| `POST` | `/certificates/medical-certificates` | Create sertifikat |
| `PUT` | `/certificates/medical-certificates/{cert_id}` | Update sertifikat |
| `DELETE` | `/certificates/medical-certificates/{cert_id}` | Hapus sertifikat |

**Fields:**
```json
{
  "visit_id": "uuid",
  "certificate_type": "HEALTH" | "SICK" | "FIT_TO_WORK",
  "start_date": "2026-07-22",
  "end_date": "2026-07-24 | null",
  "diagnosis_summary": "string | null",
  "recommendation": "string | null"
}
```

---

## 6. Audit (`/api/v1/clinic/audit`)

| Method | Path | Deskripsi |
|--------|------|-----------|
| `GET` | `/audit/activity-logs` | List log aktivitas |
| `POST` | `/audit/activity-logs` | Create log |

---

## Response Format

Semua response mengembalikan JSON. List endpoint mengembalikan array langsung atau object dengan pagination:

```json
// Single object
{ "id": "uuid", "field": "value", ... }

// List
[
  { "id": "uuid", ... },
  { "id": "uuid", ... }
]
```

Error response:
```json
{
  "detail": "Error message string"
}
```
