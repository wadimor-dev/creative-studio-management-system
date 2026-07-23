export const CLINIC_MODULE = 'clinic';

export const VISIT_STATUS = {
  CHECKIN: 'CHECKIN',
  SERVING: 'SERVING',
  FINISHED: 'FINISHED',
  CANCELLED: 'CANCELLED',
};

export const VISIT_STATUS_LABEL = {
  CHECKIN: 'Check In',
  SERVING: 'Diperiksa',
  FINISHED: 'Selesai',
  CANCELLED: 'Dibatalkan',
};

export const VISIT_STATUS_BADGE = {
  CHECKIN: 'bg-amber-100 text-amber-700',
  SERVING: 'bg-purple-100 text-purple-700',
  FINISHED: 'bg-green-100 text-green-700',
  CANCELLED: 'bg-red-100 text-red-700',
};

export const VISIT_TYPE = {
  REGULAR: 'REGULAR',
  EMERGENCY: 'EMERGENCY',
  FOLLOW_UP: 'FOLLOW_UP',
  REFERRAL: 'REFERRAL',
};

export const VISIT_TYPE_LABEL = {
  REGULAR: 'Biasa',
  EMERGENCY: 'Darurat',
  FOLLOW_UP: 'Kontrol',
  REFERRAL: 'Rujukan',
};

export const QUEUE_STATUS = {
  WAITING: 'WAITING',
  CALLING: 'CALLING',
  SERVING: 'SERVING',
  FINISHED: 'FINISHED',
  CANCELLED: 'CANCELLED',
};

export const QUEUE_STATUS_LABEL = {
  WAITING: 'Menunggu',
  CALLING: 'Dipanggil',
  SERVING: 'Dilayani',
  FINISHED: 'Selesai',
  CANCELLED: 'Dibatalkan',
};

export const QUEUE_STATUS_BADGE = {
  WAITING: 'bg-amber-100 text-amber-700',
  CALLING: 'bg-blue-100 text-blue-700',
  SERVING: 'bg-purple-100 text-purple-700',
  FINISHED: 'bg-green-100 text-green-700',
  CANCELLED: 'bg-red-100 text-red-700',
};

export const MR_STATUS = {
  ACTIVE: 'ACTIVE',
  FINALIZED: 'FINALIZED',
};

export const MR_STATUS_LABEL = {
  ACTIVE: 'Aktif',
  FINALIZED: 'Final',
};

export const DIAGNOSIS_TYPE = {
  PRIMARY: 'PRIMARY',
  SECONDARY: 'SECONDARY',
  DIFFERENTIAL: 'DIFFERENTIAL',
  FINAL: 'FINAL',
};

export const DIAGNOSIS_TYPE_LABEL = {
  PRIMARY: 'Utama',
  SECONDARY: 'Sekunder',
  DIFFERENTIAL: 'Diferensial',
  FINAL: 'Final',
};

export const RX_STATUS = {
  ACTIVE: 'ACTIVE',
  DISPENSED: 'DISPENSED',
  CANCELLED: 'CANCELLED',
};

export const RX_STATUS_LABEL = {
  ACTIVE: 'Aktif',
  DISPENSED: 'Diberikan',
  CANCELLED: 'Dibatalkan',
};

export const RX_STATUS_BADGE = {
  ACTIVE: 'bg-amber-100 text-amber-700',
  DISPENSED: 'bg-green-100 text-green-700',
  CANCELLED: 'bg-red-100 text-red-700',
};

export const CERT_TYPE = {
  SICK_LEAVE: 'SICK_LEAVE',
  MEDICAL_RECOMMENDATION: 'MEDICAL_RECOMMENDATION',
  GENERAL_CHECKUP: 'GENERAL_CHECKUP',
  VACCINATION: 'VACCINATION',
};

export const CERT_TYPE_LABEL = {
  SICK_LEAVE: 'Surat Sakit',
  MEDICAL_RECOMMENDATION: 'Rekomendasi Medis',
  GENERAL_CHECKUP: 'MCU',
  VACCINATION: 'Vaksinasi',
};

export const BLOOD_TYPE = { A: 'A', B: 'B', AB: 'AB', O: 'O' };
export const RHESUS = { POSITIVE: 'POSITIVE', NEGATIVE: 'NEGATIVE' };
export const RHESUS_LABEL = { POSITIVE: '+', NEGATIVE: '-' };

export const PROFESSION = {
  DOCTOR: 'DOCTOR',
  NURSE: 'NURSE',
  MIDWIFE: 'MIDWIFE',
  PHARMACIST: 'PHARMACIST',
  LAB_TECHNICIAN: 'LAB_TECHNICIAN',
  DENTIST: 'DENTIST',
  OTHER: 'OTHER',
};

export const PROFESSION_LABEL = {
  DOCTOR: 'Dokter',
  NURSE: 'Perawat',
  MIDWIFE: 'Bidan',
  PHARMACIST: 'Apoteker',
  LAB_TECHNICIAN: 'Teknisi Lab',
  DENTIST: 'Dokter Gigi',
  OTHER: 'Lainnya',
};

export const GENDER = { MALE: 'MALE', FEMALE: 'FEMALE', OTHER: 'OTHER' };
export const GENDER_LABEL = {
  MALE: 'Laki-laki',
  FEMALE: 'Perempuan',
  OTHER: 'Lainnya',
};

export const LOW_STOCK_THRESHOLD = 10;

export const QK = {
  dashboard: ['clinic', 'dashboard'],
  patientProfiles: (p) => ['clinic', 'patient-profiles', p],
  patientProfile: (id) => ['clinic', 'patient-profile', id],
  hcProfessionals: (p) => ['clinic', 'hc-professionals', p],
  hcProfessional: (id) => ['clinic', 'hc-professional', id],
  icd10: (p) => ['clinic', 'icd10', p],
  icd10Code: (id) => ['clinic', 'icd10-code', id],
  procedures: (p) => ['clinic', 'procedures', p],
  procedure: (id) => ['clinic', 'procedure', id],
  queues: (p) => ['clinic', 'queues', p],
  queue: (id) => ['clinic', 'queue', id],
  visits: (p) => ['clinic', 'visits', p],
  visit: (id) => ['clinic', 'visit', id],
  visitDetail: (id) => ['clinic', 'visit-detail', id],
  medicalRecords: (p) => ['clinic', 'medical-records', p],
  medicalRecord: (id) => ['clinic', 'medical-record', id],
  medicalRecordByVisit: (vid) => ['clinic', 'medical-record-visit', vid],
  soapNote: (id) => ['clinic', 'soap-note', id],
  soapNoteByVisit: (vid) => ['clinic', 'soap-note-visit', vid],
  vitalSign: (id) => ['clinic', 'vital-sign', id],
  vitalSignByVisit: (vid) => ['clinic', 'vital-sign-visit', vid],
  diagnosesByVisit: (vid) => ['clinic', 'diagnoses-visit', vid],
  visitProceduresByVisit: (vid) => ['clinic', 'visit-procs-visit', vid],
  attachmentsByVisit: (vid) => ['clinic', 'attachments-visit', vid],
  prescriptions: (p) => ['clinic', 'prescriptions', p],
  prescription: (id) => ['clinic', 'prescription', id],
  prescriptionByVisit: (vid) => ['clinic', 'prescription-visit', vid],
  rxItems: (rid) => ['clinic', 'rx-items', rid],
  certificates: (p) => ['clinic', 'certificates', p],
  certificate: (id) => ['clinic', 'certificate', id],
  certificateByVisit: (vid) => ['clinic', 'certificate-visit', vid],
  activityLogs: (p) => ['clinic', 'activity-logs', p],
};

export const CLINIC_ROUTES = {
  dashboard: '/clinic/dashboard',
  visits: '/clinic/visits',
  visitDetail: (id) => `/clinic/visits/${id}`,
  queue: '/clinic/queue',
  medicalRecords: '/clinic/medical-records',
  medicines: '/clinic/medicines',
  patients: '/clinic/patients',
  hcProfessionals: '/clinic/healthcare-professionals',
  icd10: '/clinic/icd10',
  procedures: '/clinic/medical-procedures',
  prescriptions: '/clinic/prescriptions',
  certificates: '/clinic/certificates',
  activityLogs: '/clinic/activity-logs',
};
