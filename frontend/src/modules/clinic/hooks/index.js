import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'react-toastify'; // dipakai showroom juga; hapus kalau tak mau toast
import { clinicApi } from '../api';
import { QK } from '../constants';

/* ======================= DASHBOARD ======================= */
export const useClinicDashboard = () =>
  useQuery({ queryKey: QK.dashboard, queryFn: () => clinicApi.getDashboard() });

/* ======================= EMPLOYEES ======================= */
export const useEmployees = (params = {}) =>
  useQuery({
    queryKey: QK.employees(params),
    queryFn: () => clinicApi.getEmployees(params),
  });

export const useCreateEmployee = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload) => clinicApi.createEmployee(payload),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['clinic', 'employees'] });
      toast.success('Karyawan ditambahkan');
    },
    onError: (e) => toast.error(e.message),
  });
};

export const useImportEmployees = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (rows) => clinicApi.importEmployees(rows),
    onSuccess: (res) => {
      qc.invalidateQueries({ queryKey: ['clinic', 'employees'] });
      toast.success(`${res.imported} karyawan diimport`);
    },
    onError: (e) => toast.error(e.message),
  });
};

/* ======================= MEDICINES (OBAT) ======================= */
export const useMedicines = (params = {}) =>
  useQuery({
    queryKey: QK.medicines(params),
    queryFn: () => clinicApi.getMedicines(params),
  });

export const useCreateMedicine = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload) => clinicApi.createMedicine(payload),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['clinic', 'medicines'] });
      qc.invalidateQueries({ queryKey: QK.dashboard });
      toast.success('Obat ditambahkan');
    },
    onError: (e) => toast.error(e.message),
  });
};

export const useAdjustMedicineStock = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, delta }) => clinicApi.adjustMedicineStock(id, delta),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['clinic', 'medicines'] });
      qc.invalidateQueries({ queryKey: QK.dashboard });
      toast.success('Stok obat diperbarui');
    },
    onError: (e) => toast.error(e.message),
  });
};

/* ======================= VISITS & QUEUE ======================= */
export const useVisits = (params = {}) =>
  useQuery({
    queryKey: QK.visits(params),
    queryFn: () => clinicApi.getVisits(params),
  });

export const useQueue = () =>
  useQuery({
    queryKey: QK.queue(),
    queryFn: () => clinicApi.getQueue(),
    // refetchInterval: 15000,  // aktifkan kalau mau antrian auto-refresh tiap 15 dtk
  });

// Register Visit (alur 6 langkah). Return { visit, queue_no, medical_record_id }
export const useRegisterVisit = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload) => clinicApi.registerVisit(payload),
    onSuccess: (res) => {
      qc.invalidateQueries({ queryKey: ['clinic', 'visits'] });
      qc.invalidateQueries({ queryKey: ['clinic', 'queue'] });
      qc.invalidateQueries({ queryKey: QK.dashboard });
      toast.success(`Kunjungan terdaftar — antrian #${res.queue_no}`);
    },
    onError: (e) => toast.error(e.message),
  });
};

export const useUpdateVisitStatus = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, status }) => clinicApi.updateVisitStatus(id, status),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['clinic', 'visits'] });
      qc.invalidateQueries({ queryKey: ['clinic', 'queue'] });
      qc.invalidateQueries({ queryKey: QK.dashboard });
    },
    onError: (e) => toast.error(e.message),
  });
};

/* ======================= MEDICAL RECORDS ======================= */
export const useMedicalRecords = (params = {}) =>
  useQuery({
    queryKey: QK.medicalRecords(params),
    queryFn: () => clinicApi.getMedicalRecords(params),
  });

export const useMedicalRecord = (id) =>
  useQuery({
    queryKey: QK.medicalRecord(id),
    queryFn: () => clinicApi.getMedicalRecord(id),
    enabled: !!id,
  });

// Simpan rekam medis + POTONG STOK OBAT + visit → COMPLETED
export const useCompleteMedicalRecord = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ recordId, payload }) =>
      clinicApi.completeMedicalRecord(recordId, payload),
    onSuccess: () => {
      // stok obat berubah → wajib invalidate medicines + dashboard
      qc.invalidateQueries({ queryKey: ['clinic', 'medicines'] });
      qc.invalidateQueries({ queryKey: ['clinic', 'medical-records'] });
      qc.invalidateQueries({ queryKey: ['clinic', 'visits'] });
      qc.invalidateQueries({ queryKey: ['clinic', 'queue'] });
      qc.invalidateQueries({ queryKey: QK.dashboard });
      toast.success('Rekam medis tersimpan, stok obat diperbarui');
    },
    onError: (e) => toast.error(e.message),
  });
};
