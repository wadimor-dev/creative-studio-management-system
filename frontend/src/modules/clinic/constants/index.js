export const CLINIC_MODULE = 'clinic';

/* ---------- Visit (kunjungan) ---------- */
export const VISIT_STATUS = {
  WAITING: 'WAITING',
  IN_PROGRESS: 'IN_PROGRESS',
  COMPLETED: 'COMPLETED',
  CANCELLED: 'CANCELLED',
};

export const VISIT_STATUS_LABEL = {
  WAITING: 'Menunggu',
  IN_PROGRESS: 'Diperiksa',
  COMPLETED: 'Selesai',
  CANCELLED: 'Dibatalkan',
};

export const VISIT_STATUS_BADGE = {
  WAITING: 'bg-amber-100 text-amber-700',
  IN_PROGRESS: 'bg-purple-100 text-purple-700',
  COMPLETED: 'bg-green-100 text-green-700',
  CANCELLED: 'bg-red-100 text-red-700',
};

// state machine transisi status kunjungan
export const VISIT_TRANSITIONS = {
  WAITING: ['IN_PROGRESS', 'CANCELLED'],
  IN_PROGRESS: ['COMPLETED', 'CANCELLED'],
  COMPLETED: [],
  CANCELLED: [],
};

/* ---------- Umum ---------- */
export const GENDER = { MALE: 'MALE', FEMALE: 'FEMALE', OTHER: 'OTHER' };
export const GENDER_LABEL = {
  MALE: 'Laki-laki',
  FEMALE: 'Perempuan',
  OTHER: 'Lainnya',
};

// batas default stok obat menipis (kalau medicine.min_stock kosong)
export const LOW_STOCK_THRESHOLD = 10;

/* ---------- Query keys (TanStack Query) ---------- */
export const QK = {
  dashboard: ['clinic', 'dashboard'],
  employees: (params = {}) => ['clinic', 'employees', params],
  employee: (id) => ['clinic', 'employee', id],
  visits: (params = {}) => ['clinic', 'visits', params],
  visit: (id) => ['clinic', 'visit', id],
  queue: (params = {}) => ['clinic', 'queue', params],
  medicalRecords: (params = {}) => ['clinic', 'medical-records', params],
  medicalRecord: (id) => ['clinic', 'medical-record', id],
  medicines: (params = {}) => ['clinic', 'medicines', params],
  medicine: (id) => ['clinic', 'medicine', id],
};

/* ---------- Path route ---------- */
export const CLINIC_ROUTES = {
  dashboard: '/clinic/dashboard',
  visits: '/clinic/visits',
  queue: '/clinic/queue',
  medicalRecords: '/clinic/medical-records',
  medicines: '/clinic/medicines',
};
