// frontend/src/modules/clinic/api.js
import api from '../../api/axios'; // ⚠️ sesuaikan instance axios kamu
import { VISIT_STATUS } from './constants';

export const MOCK = true;
const delay = (ms = 300) => new Promise((r) => setTimeout(r, ms));

/* =========================================================================
 *  KONTRAK RESPONSE (acuan backend dev)
 *  Employee      : { id, employee_no, full_name, department, is_active }
 *  Medicine      : { id, code, name, unit, stock, min_stock }
 *  Visit         : { id, visit_no, employee_id, employee_name, queue_no,
 *                    complaint, status, medical_record_id, created_at }
 *  MedicalRecord : { id, visit_id, employee_id, subjective, objective,
 *                    assessment, plan, items:[{medicine_id,name,qty}], created_at }
 *
 *  ALUR registerVisit (6 langkah backend):
 *   1) Register Visit  → terima {employee_id, complaint}
 *   2) Validate Employee → karyawan harus ada & aktif
 *   3) Create Queue    → nomor antrian hari ini
 *   4) Create Visit    → status WAITING
 *   5) Generate Medical Record → rekam medis kosong tertaut visit
 *   6) Return Response → { visit, queue_no, medical_record_id }
 * ========================================================================= */

/* ---------- MOCK DATA ---------- */
let mockEmployees = [
  {
    id: 1,
    employee_no: 'EMP-001',
    full_name: 'Budi Santoso',
    department: 'Produksi',
    is_active: true,
  },
  {
    id: 2,
    employee_no: 'EMP-002',
    full_name: 'Siti Aminah',
    department: 'Finance',
    is_active: true,
  },
  {
    id: 3,
    employee_no: 'EMP-003',
    full_name: 'Andi Nugroho',
    department: 'Gudang',
    is_active: false,
  },
];

let mockMedicines = [
  {
    id: 1,
    code: 'OBT-001',
    name: 'Paracetamol 500mg',
    unit: 'tablet',
    stock: 120,
    min_stock: 20,
  },
  {
    id: 2,
    code: 'OBT-002',
    name: 'Amoxicillin 500mg',
    unit: 'kapsul',
    stock: 8,
    min_stock: 15,
  },
  {
    id: 3,
    code: 'OBT-003',
    name: 'Antasida',
    unit: 'tablet',
    stock: 60,
    min_stock: 20,
  },
];

let mockVisits = [];
let mockRecords = [];
let seq = { employee: 3, medicine: 3, visit: 0, record: 0 };

const todayQueueCount = () =>
  mockVisits.filter(
    (v) => new Date(v.created_at).toDateString() === new Date().toDateString(),
  ).length;

/* ---------- API ---------- */
export const clinicApi = {
  /* ===== Employees ===== */
  async getEmployees(params = {}) {
    if (MOCK) {
      await delay();
      const q = (params.q || '').toLowerCase();
      return mockEmployees.filter(
        (e) =>
          !q ||
          e.full_name.toLowerCase().includes(q) ||
          e.employee_no.toLowerCase().includes(q),
      );
    }
    const { data } = await api.get('/clinic/employees', { params });
    return data;
  },
  async createEmployee(payload) {
    if (MOCK) {
      await delay();
      const id = ++seq.employee;
      const created = { id, is_active: true, ...payload };
      mockEmployees = [created, ...mockEmployees];
      return created;
    }
    const { data } = await api.post('/clinic/employees', payload);
    return data;
  },
  // import massal (dari CSV/Excel) — payload: array of { employee_no, full_name, department }
  async importEmployees(list = []) {
    if (MOCK) {
      await delay();
      const created = list.map((row) => ({
        id: ++seq.employee,
        is_active: true,
        ...row,
      }));
      mockEmployees = [...created, ...mockEmployees];
      return { imported: created.length, employees: created };
    }
    const { data } = await api.post('/clinic/employees/import', { rows: list });
    return data;
  },

  /* ===== Medicines (master obat + stok) ===== */
  async getMedicines(params = {}) {
    if (MOCK) {
      await delay();
      return mockMedicines;
    }
    const { data } = await api.get('/clinic/medicines', { params });
    return data;
  },
  async createMedicine(payload) {
    if (MOCK) {
      await delay();
      const id = ++seq.medicine;
      const created = { id, stock: 0, min_stock: 10, ...payload };
      mockMedicines = [created, ...mockMedicines];
      return created;
    }
    const { data } = await api.post('/clinic/medicines', payload);
    return data;
  },
  // tambah/kurangi stok manual (restock). delta boleh negatif
  async adjustMedicineStock(id, delta) {
    if (MOCK) {
      await delay();
      mockMedicines = mockMedicines.map((m) =>
        m.id === Number(id) ? { ...m, stock: Math.max(0, m.stock + delta) } : m,
      );
      return mockMedicines.find((m) => m.id === Number(id));
    }
    const { data } = await api.patch(`/clinic/medicines/${id}/adjust`, {
      delta,
    });
    return data;
  },

  /* ===== Visit flow (Register Visit) ===== */
  async registerVisit({ employee_id, complaint }) {
    if (MOCK) {
      await delay();
      // (2) Validate Employee
      const emp = mockEmployees.find((e) => e.id === Number(employee_id));
      if (!emp) throw new Error('Karyawan tidak ditemukan');
      if (!emp.is_active)
        throw new Error('Karyawan non-aktif, tidak bisa mendaftar');

      // (3) Create Queue
      const queue_no = todayQueueCount() + 1;
      // (4) Create Visit
      const visitId = ++seq.visit;
      // (5) Generate Medical Record (kosong)
      const recordId = ++seq.record;
      const record = {
        id: recordId,
        visit_id: visitId,
        employee_id: emp.id,
        subjective: '',
        objective: '',
        assessment: '',
        plan: '',
        items: [],
        created_at: new Date().toISOString(),
      };
      mockRecords = [record, ...mockRecords];

      const visit = {
        id: visitId,
        visit_no: `VIS-${String(visitId).padStart(5, '0')}`,
        employee_id: emp.id,
        employee_name: emp.full_name,
        queue_no,
        complaint,
        status: VISIT_STATUS.WAITING,
        medical_record_id: recordId,
        created_at: new Date().toISOString(),
      };
      mockVisits = [visit, ...mockVisits];

      // (6) Return Response
      return { visit, queue_no, medical_record_id: recordId };
    }
    const { data } = await api.post('/clinic/visits/register', {
      employee_id,
      complaint,
    });
    return data;
  },

  async getVisits(params = {}) {
    if (MOCK) {
      await delay();
      return mockVisits.filter(
        (v) => !params.status || v.status === params.status,
      );
    }
    const { data } = await api.get('/clinic/visits', { params });
    return data;
  },

  // antrian hari ini: WAITING / IN_PROGRESS, urut nomor antrian
  async getQueue() {
    if (MOCK) {
      await delay();
      return mockVisits
        .filter(
          (v) =>
            new Date(v.created_at).toDateString() === new Date().toDateString(),
        )
        .filter(
          (v) =>
            v.status === VISIT_STATUS.WAITING ||
            v.status === VISIT_STATUS.IN_PROGRESS,
        )
        .sort((a, b) => a.queue_no - b.queue_no);
    }
    const { data } = await api.get('/clinic/visits/queue');
    return data;
  },

  async updateVisitStatus(id, status) {
    if (MOCK) {
      await delay();
      mockVisits = mockVisits.map((v) =>
        v.id === Number(id) ? { ...v, status } : v,
      );
      return mockVisits.find((v) => v.id === Number(id));
    }
    const { data } = await api.patch(`/clinic/visits/${id}/status`, { status });
    return data;
  },

  /* ===== Medical Record + pengurangan stok obat ===== */
  async getMedicalRecord(id) {
    if (MOCK) {
      await delay();
      return mockRecords.find((r) => r.id === Number(id));
    }
    const { data } = await api.get(`/clinic/medical-records/${id}`);
    return data;
  },
  async getMedicalRecords(params = {}) {
    if (MOCK) {
      await delay();
      return mockRecords;
    }
    const { data } = await api.get('/clinic/medical-records', { params });
    return data;
  },

  // simpan rekam medis + KURANGI STOK OBAT + tandai visit COMPLETED
  // payload: { subjective, objective, assessment, plan, items:[{medicine_id, qty}] }
  async completeMedicalRecord(recordId, payload) {
    if (MOCK) {
      await delay();
      const record = mockRecords.find((r) => r.id === Number(recordId));
      if (!record) throw new Error('Rekam medis tidak ditemukan');

      // validasi & kurangi stok
      const items = (payload.items || []).map((it) => {
        const med = mockMedicines.find((m) => m.id === Number(it.medicine_id));
        if (!med) throw new Error(`Obat id ${it.medicine_id} tidak ditemukan`);
        if (it.qty > med.stock)
          throw new Error(`Stok "${med.name}" tidak cukup (sisa ${med.stock})`);
        return { medicine_id: med.id, name: med.name, qty: it.qty };
      });
      // eksekusi pengurangan stok
      items.forEach((it) => {
        mockMedicines = mockMedicines.map((m) =>
          m.id === it.medicine_id ? { ...m, stock: m.stock - it.qty } : m,
        );
      });

      const updated = { ...record, ...payload, items };
      mockRecords = mockRecords.map((r) => (r.id === record.id ? updated : r));
      // visit → COMPLETED
      mockVisits = mockVisits.map((v) =>
        v.id === record.visit_id ? { ...v, status: VISIT_STATUS.COMPLETED } : v,
      );
      return updated;
    }
    const { data } = await api.post(
      `/clinic/medical-records/${recordId}/complete`,
      payload,
    );
    return data;
  },

  /* ===== Dashboard ===== */
  async getDashboard() {
    if (MOCK) {
      await delay();
      const today = mockVisits.filter(
        (v) =>
          new Date(v.created_at).toDateString() === new Date().toDateString(),
      );
      const byStatus = today.reduce((acc, v) => {
        acc[v.status] = (acc[v.status] || 0) + 1;
        return acc;
      }, {});
      return {
        totals: {
          employeesActive: mockEmployees.filter((e) => e.is_active).length,
          visitsToday: today.length,
          waitingCount: byStatus[VISIT_STATUS.WAITING] || 0,
        },
        visitsByStatus: byStatus,
        todayQueue: today
          .filter(
            (v) =>
              v.status === VISIT_STATUS.WAITING ||
              v.status === VISIT_STATUS.IN_PROGRESS,
          )
          .sort((a, b) => a.queue_no - b.queue_no),
        lowStockMedicines: mockMedicines.filter(
          (m) => m.stock <= (m.min_stock ?? 10),
        ),
      };
    }
    const { data } = await api.get('/clinic/dashboard');
    return data;
  },
};
