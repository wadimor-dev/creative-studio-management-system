// frontend/src/modules/clinic/helpers/index.js
import {
  VISIT_TRANSITIONS,
  VISIT_STATUS_BADGE,
  VISIT_STATUS_LABEL,
  LOW_STOCK_THRESHOLD,
} from '../constants';

/* ---------- Formatters ---------- */
export const formatDate = (v) =>
  !v
    ? '-'
    : new Date(v).toLocaleDateString('id-ID', {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
      });

export const formatDateTime = (v) =>
  !v
    ? '-'
    : new Date(v).toLocaleString('id-ID', {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });

export const formatTime = (v) =>
  !v
    ? '-'
    : new Date(v).toLocaleTimeString('id-ID', {
        hour: '2-digit',
        minute: '2-digit',
      });

export const calcAge = (birthDate) => {
  if (!birthDate) return null;
  const b = new Date(birthDate);
  const now = new Date();
  let age = now.getFullYear() - b.getFullYear();
  const m = now.getMonth() - b.getMonth();
  if (m < 0 || (m === 0 && now.getDate() < b.getDate())) age--;
  return age;
};

export const isToday = (v) => {
  if (!v) return false;
  const d = new Date(v);
  const n = new Date();
  return d.toDateString() === n.toDateString();
};

/* ---------- Status kunjungan ---------- */
export const visitStatusLabel = (s) => VISIT_STATUS_LABEL[s] || s;
export const visitStatusBadge = (s) =>
  VISIT_STATUS_BADGE[s] || 'bg-gray-100 text-gray-600';
export const nextStatuses = (current) => VISIT_TRANSITIONS[current] || [];
export const canTransition = (current, target) =>
  nextStatuses(current).includes(target);

/* ---------- Obat ---------- */
export const isLowStock = (med) =>
  (med?.stock ?? 0) <= (med?.min_stock ?? LOW_STOCK_THRESHOLD);

/* ---------- Validasi form ---------- */
export const validateRegisterVisit = ({ employee_id, complaint }) => {
  const errors = [];
  if (!employee_id) errors.push('Karyawan wajib dipilih');
  if (!complaint || !complaint.trim()) errors.push('Keluhan wajib diisi');
  return errors;
};

export const validateEmployee = ({ employee_no, full_name }) => {
  const errors = [];
  if (!employee_no || !employee_no.trim())
    errors.push('NIK/No. karyawan wajib diisi');
  if (!full_name || !full_name.trim()) errors.push('Nama wajib diisi');
  return errors;
};

// item = [{ medicine_id, qty }]; medicines = daftar master obat
export const validateMedicalRecord = ({ items = [] }, medicines = []) => {
  const errors = [];
  items.forEach((it) => {
    const med = medicines.find((m) => m.id === Number(it.medicine_id));
    if (!med) {
      errors.push(`Obat id ${it.medicine_id} tidak ditemukan`);
      return;
    }
    if (it.qty <= 0) errors.push(`Jumlah "${med.name}" harus > 0`);
    if (it.qty > med.stock)
      errors.push(`Stok "${med.name}" tidak cukup (sisa ${med.stock})`);
  });
  return errors;
};

export const groupBy = (arr, keyFn) =>
  (arr || []).reduce((acc, item) => {
    const k = keyFn(item);
    (acc[k] = acc[k] || []).push(item);
    return acc;
  }, {});
